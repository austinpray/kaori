def test_card_text():
    from ..test.cards.meme_cards import matt_morgan, ubu, kim_jong_un_lil_sis

    assert matt_morgan.title == 'Matt Morgan (S-tier cursed baby)'
    assert ubu.title == 'ubu (C-tier feral and cursed)'
    assert kim_jong_un_lil_sis.title == "Kim Jong Un's Little Sister (S-tier horny baby)"
