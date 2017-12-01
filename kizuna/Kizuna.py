from kizuna.strings import HAI_DOMO, KIZUNA


class Kizuna:
    def __init__(self, bot_id, slack_client) -> None:
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
        self.registered_commands = []

    def is_at(self, text):
        return text.startswith(self.respond_tokens)

    def register_command(self, command):
        self.registered_commands.append(command)

    def handle_message(self, message):
        if 'user' in message and message['user'] == self.bot_id:
            return

        if 'text' in message and message['text']:
            message['text'] = message['text'].strip()
        else:
            return

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
