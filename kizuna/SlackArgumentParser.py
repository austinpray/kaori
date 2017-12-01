from argparse import ArgumentParser


class SlackArgumentParserException(Exception):
    pass


class SlackArgumentParser(ArgumentParser):
    def error(self, message):
        raise SlackArgumentParserException(message)
