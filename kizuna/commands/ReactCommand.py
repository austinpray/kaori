from .Command import Command


class ReactCommand(Command):
    def __init__(self) -> None:
        help_text = 'kizuna react - view available reaction images and tags\n'\
                    'kizuna react <tag> - Send a reaction related to the tag'
        super().__init__(name='react',
                         pattern='react(?: (.*))?$',
                         help_text=help_text,
                         is_at=True)
