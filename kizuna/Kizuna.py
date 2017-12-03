from kizuna.strings import \
    JAP_DOT, LQUO, RQUO, YOSHI, HAI_DOMO, KIZUNA, VERSION_TRANSITION_TEMPLATE, VERSION_UPDATE_TEMPLATE, VERSION_UP

from os import path
import json
from pprint import pprint

from kizuna.models.Meta import Meta


class Kizuna:
    def __init__(self, bot_id, slack_client, main_channel='#banter') -> None:
        self.bot_id = bot_id
        self.sc = slack_client
        self.respond_tokens = (
            'kizuna',
            'Kizuna',
            '@kizuna',
            '@Kizuna',
            '<@{}>'.format(bot_id),
            KIZUNA
        )
        self.main_channel = main_channel
        self.registered_commands = []

    def is_at(self, text):
        return text.startswith(self.respond_tokens)

    def register_command(self, command):
        self.registered_commands.append(command)

    @staticmethod
    def read_dev_info(dev_info_path):
        if not path.isfile(dev_info_path):
            print('startup: no dev file at "{}"'.format(dev_info_path))
            return {}

        dev_info = json.load(open(dev_info_path))
        print('startup: dev info loaded from "{}"'.format(dev_info_path))
        pprint(dev_info)
        return dev_info

    def handle_startup(self, dev_info, db_session):
        def send(text,
                 title=None,
                 footer=None,
                 footer_icon=None):
            attachment = {
                'title': title,
                'color': 'good',
                'text': text,
                'footer': footer,
                'footer_icon': footer_icon
            }
            return self.sc.api_call("chat.postMessage",
                                    channel=self.main_channel,
                                    attachments=[attachment],
                                    as_user=True)

        new_revision = dev_info.get('revision')
        if not new_revision:
            return

        current_revision = db_session.query(Meta).filter(Meta.key == 'current_revision').first()
        previous_revision = db_session.query(Meta).filter(Meta.key == 'previous_revision').first()

        if not current_revision:
            current_revision = Meta(key='current_revision', value=new_revision)
            db_session.add(current_revision)
            db_session.commit()
            out = YOSHI + JAP_DOT
            revision_link = self.slack_link(current_revision.value[:7],
                                            self.get_revision_github_url(current_revision.value))
            out += VERSION_UPDATE_TEMPLATE.replace('{{VERSION}}', LQUO + revision_link + RQUO)
            return send(out, title=VERSION_UP)

        if new_revision == current_revision.value:
            return

        if not previous_revision:
            previous_revision = Meta(key='previous_revision', value=current_revision.value)
            db_session.add(previous_revision)

        previous_revision.value = current_revision.value
        current_revision.value = new_revision
        db_session.commit()

        out = YOSHI + JAP_DOT
        out += VERSION_TRANSITION_TEMPLATE
        previous_revision_link = self.slack_link(previous_revision.value[:7],
                                                 self.get_revision_github_url(previous_revision.value))
        current_revision_link = self.slack_link(current_revision.value[:7],
                                                self.get_revision_github_url(current_revision.value))
        out = out \
            .replace('{{FROM_VERSION}}', LQUO + previous_revision_link + RQUO) \
            .replace('{{TO_VERSION}}', LQUO + current_revision_link + RQUO)
        compare_link = self.slack_link('Compare Changes on GitHub',
                                       self.get_revision_range_github_url(previous_revision.value,
                                                                          current_revision.value))
        return send(out, title=VERSION_UP, footer=compare_link)

    @staticmethod
    def slack_link(text, url):
        return '<{}|{}>'.format(url, text)

    @staticmethod
    def get_revision_github_url(revision):
        return 'https://github.com/austinpray/kizuna/commit/{}'.format(revision)

    @staticmethod
    def get_revision_range_github_url(old_revision, new_revision):
        return 'https://github.com/austinpray/kizuna/compare/{}...{}'.format(old_revision, new_revision)

    def handle_message(self, message):
        if 'user' in message and message['user'] == self.bot_id:
            return

        if 'text' not in message or not message['text']:
            return

        message['text'] = message['text'].strip()
        text = message['text']
        channel = message['channel']
        if self.is_at(text):
            parts = text.split(' ', 1)
            if len(parts) < 2:
                return

            at, command_text = parts
            message['text'] = command_text

            if command_text.lower() in ['-h', '--help', 'help']:
                help_header = HAI_DOMO
                help_text_list = list(map(lambda c: c.help(self.respond_tokens[0]), self.registered_commands))

                separator = '\n' + ':sparkles:' * 5 + '\n'

                help_commands = help_header + '\n\n' + separator.join(help_text_list[:-1]) + help_text_list[-1]
                return self.sc.api_call("chat.postMessage",
                                        channel=channel,
                                        text=help_commands,
                                        as_user=True)

            registered_at_commands = filter(lambda c: c.is_at, self.registered_commands)
            for command in registered_at_commands:
                command.maybe_respond(self.sc, message)
            return

        registered_general_commands = filter(lambda c: not c.is_at, self.registered_commands)

        for command in registered_general_commands:
            command.maybe_respond(self.sc, message)
