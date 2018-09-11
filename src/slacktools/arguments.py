from argparse import ArgumentParser


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
