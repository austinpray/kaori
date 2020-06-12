from kaori.adapters.slack import SlackMessage
from kaori.plugins.gacha import UpdateCardCommand
from kaori.support.di import build_di_args
from kaori.worker import k


def test_di():
    fake_slack = SlackMessage({'event': {}})
    components = {fake_slack} | k.get_base_components()
    to_di = build_di_args(components, UpdateCardCommand.handle)
    assert fake_slack in to_di.values()
    assert to_di['file_uploader'].__class__.__name__ in ['LocalFileUploader']
