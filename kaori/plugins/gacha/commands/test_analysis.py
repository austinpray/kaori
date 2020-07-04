from .analysis import generate_report_charts
import os

def test_report():
    from ..engine.test.cards import sachiko, matt_morgan, ubu, xss, balanced_S, low_dmg

    data = [sachiko, matt_morgan, ubu, ubu, xss, balanced_S, low_dmg]

    report = generate_report_charts(data)

    for f in report.values():
        f.seek(0, os.SEEK_END)

    assert report['rarity'].tell() > 0
    assert report['natures'].tell() > 0



