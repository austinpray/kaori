from escpos.printer import Usb, Dummy
from escpos.exceptions import Error as PrinterError
from usb.core import USBError
import arrow
from types import SimpleNamespace

import click
import json
import requests

class FaxMessage(object):

    def __init__(self, user_name, created_at, text) -> None:
        self.user_name = user_name
        self.created_at = created_at
        self.text = text

    def __repr__(self) -> str:
        return f'<FaxMessage ' \
               f'user_name="{self.user_name}" ' \
               f'created_at="{self.get_human_timestamp()}" ' \
               f'text="{self.text}">'

    def get_human_timestamp(self):
        timestamp = arrow.get(self.created_at).to('local')
        return timestamp.format('YYYY-MM-DD HH:mm:ss ZZ')

    @staticmethod
    def from_dict(target_dict):
        return FaxMessage(target_dict['user_name'],
                          target_dict['created_at'],
                          target_dict['text'])



def get_printer():
    return Usb(0x0416, 0x5011, 0, profile="POS-5890")

def send_text_to_printer(text):
    p = get_printer()
    p.text(text)
    p.cut()

def format_printer_message(printer, message: FaxMessage):
    printer.set(bold=True)
    printer.textln(message.user_name)
    printer.set(font='b')
    printer.textln(message.get_human_timestamp())
    printer.set()
    printer.textln(message.text)

@click.group()
def cli():
    pass


@cli.command()
@click.argument('text', nargs=-1)
def send_text(text):
    output_string = ' '.join(str(s) for s in text)
    click.echo('printing:')
    click.echo(output_string)
    send_text_to_printer(f'{output_string}\n')

@cli.command()
@click.argument('json_message')
def send_message(json_message):
    m = FaxMessage.from_dict(json.loads(json_message))
    p = get_printer()
    format_printer_message(p, m)
    p.cut()

@cli.command()
@click.argument('path')
def send_image(path):
    p = get_printer()
    p.image(path, impl='bitImageColumn')
    p.cut()

dev_api_base = 'http://localhost:8001'
prod_api_base = 'https://api.kizuna.guap.io'


@cli.command()
@click.option('--auth', required=True)
@click.option('--dev/--no-dev', default=False)
@click.option('--print/--no-print', 'do_print', default=True)
def fetch(auth, dev, do_print):
    api_base = dev_api_base if dev else prod_api_base
    messages_url = f'{api_base}/fax_messages'

    headers = {'Authorization': f'Bearer {auth}'}
    api_req = requests.get(messages_url, headers=headers)

    if api_req.status_code != 200:
        return click.echo(f'something went wrong (status {api_req.status_code}): {api_req.text}')

    api_res = api_req.json()
    messages = api_res['messages']

    if not messages or len(messages) < 1:
        return click.echo('no messages')

    def mark_message_printed(m, printed=True):
        if not do_print:
            res = SimpleNamespace()
            res.status_code = 200
            return res

        message_id = m['id']
        return requests.put(f'{messages_url}/{message_id}',
                            headers=headers,
                            data=json.dumps({'printed': printed}))

    output = []
    for message_dict in messages:
        update_req = mark_message_printed(message_dict, printed=True)
        message = FaxMessage.from_dict(message_dict)
        if update_req.status_code == 200:
            output.append(message)

    if do_print:
        try:
            if len(output) < 1:
                return

            printer = get_printer()
            for message in output:
                format_printer_message(printer, message)
                printer.ln()
            printer.cut()
            return
        except (PrinterError, USBError) as e:
            click.echo(f'printer error: {e}')
            for message_dict in messages:
                mark_message_printed(message_dict, printed=False)

    click.echo('\n'.join([str(m) for m in output]))


if __name__ == '__main__':
    cli()
