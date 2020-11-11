from .card import Card


def test_card_text():
    from ..test.cards.meme_cards import matt_morgan, ubu, kim_jong_un_lil_sis

    assert matt_morgan.title == 'Matt Morgan (S-tier cursed baby)'
    assert ubu.title == 'ubu (C-tier feral and cursed)'
    assert kim_jong_un_lil_sis.title == "Kim Jong Un's Little Sister (S-tier horny baby)"


def test_card_generate():
    card = Card.generate('ubu2', 'F', ['horny', 'clown'])
    assert card.title == 'ubu2 (F-tier horny clown)'

    assert sum([
        card.stupid,
        card.baby,
        card.clown,
        card.horny,
        card.cursed,
        card.feral,
    ]) == 10


def test_card_hp():
    from ..test.cards.hp_cards import high_hp
    from ..test.cards.meme_cards import sachiko

    assert high_hp.max_hp == 100
    assert sachiko.max_hp == 83
