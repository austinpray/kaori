from argparse import ArgumentParser
from io import StringIO


class SlackArgumentParserException(Exception):
    pass


class SlackArgumentParser(ArgumentParser):
    """
    If, for some silly reason, you want your bot to accept
    argparse.ArgumentParser style arguments you can use this.
    """

    def error(self, message):
        """
        We override this method because ArgumentParser's error() method prints
        stuff to stdout and then calls exit(1)

        :raise: SlackArgumentParserException
        """

        raise SlackArgumentParserException(message)

    def get_help(self):
        help_text_capture = StringIO()
        self.print_help(file=help_text_capture)
        help_text = help_text_capture.getvalue()
        help_text = help_text.replace('usage: ', '')
        return help_text

    def add_help_argument(self):
        self.add_argument('-h',
                          '--help',
                          action='store_true',
                          dest='help',
                          help='show this help message')
