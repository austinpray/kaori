from escpos.printer import Usb
from escpos.exceptions import Error as PrinterError
import click
import json
from pprint import pprint
import requests


def send_to_printer(message):
    p = Usb(0x0416, 0x5011, 0, profile="POS-5890")
    p.text(message)
    p.cut('PART')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('text', nargs=-1)
def send(text):
    output_string = ' '.join(str(s) for s in text)
    click.echo('printing:')
    click.echo(output_string)
    send_to_printer(f'{output_string}\n')


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
        message_id = m['id']
        return requests.put(f'{messages_url}/{message_id}',
                            headers=headers,
                            data=json.dumps({'printed': printed}))

    output = []
    for message in messages:
        update_req = mark_message_printed(message, printed=True)
        user_name = message['user_name']
        text = message['text']
        if update_req.status_code == 200:
            output.append(f'{user_name}: {text}')

    output_string = '\n'.join(output)
    if do_print:
        try:
            return send_to_printer(f'{output_string}\n')
        except PrinterError:
            click.echo(f'printer error: {PrinterError}')
            for message in messages:
                mark_message_printed(message, printed=False)

    click.echo(output_string)


if __name__ == '__main__':
    cli()
