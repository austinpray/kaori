import pytest
from slacktools.arguments import SlackArgumentParser, SlackArgumentParserException

def test_arguments():
    """haha what a useless test"""
    with pytest.raises(SlackArgumentParserException):
        p = SlackArgumentParser()
        p.error('ayy')
