import os
from copy import deepcopy
from random import choice
from typing import List, Dict
from rich.table import Table
from io import StringIO

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from kaori.skills import DB
from ..core import stupid, baby, clown, horny, cursed, feral, EVA, CRIT, SPEED, Card
from ...models.Card import Card as CardModel


def collect_cards(module) -> Dict[str, Card]:
    card_variables: List[Card] = [
        getattr(module, var_name) for var_name in
        dir(module) if isinstance(getattr(module, var_name), Card)
    ]
    return {card.slug: card for card in card_variables}


def find_card(module, search: str) -> Card:
    with db().session_scope() as session:
        card = CardModel.search_for_one(session, search)
        if card:
            return card.engine

    available_cards = collect_cards(module)

    if search.lower() == 'random':
        return deepcopy(choice(list(available_cards.values())))

    search_slug = Card.sluggify_name(search)
    if search_slug in available_cards:
        return deepcopy(available_cards[search_slug])

    for slug, card in available_cards.items():
        if slug.startswith(search_slug):
            return deepcopy(card)

    raise ValueError(f'cannot find a card for {search}')


def db_session() -> Session:
    make_session = db_sessionmaker()
    session = make_session()
    return session


def db_sessionmaker():
    db_engine = create_engine(os.getenv('GSIM_DATABASE_URL') or os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)
    return make_session


def db() -> DB:
    return DB(make_session=db_sessionmaker())


def card_table(card: Card, title_style="bold underline yellow") -> Table:
    table = Table(title=card.title, show_header=False, title_style=title_style)
    table.add_column("Natures", justify="right")
    table.add_column("Stats", justify="right")

    nature_table = Table(header_style="bold magenta")
    nature_table.add_column("Nature")
    nature_table.add_column("Value", justify="right")

    stat_table = Table(header_style="bold dodger_blue2")
    stat_table.add_column("Stat")
    stat_table.add_column("Value", justify="right")

    nature_styles = {
        stupid: 'bright_red',
        baby: 'bright_green',
        clown: 'bright_yellow',
        horny: 'bright_blue',
        cursed: 'bright_magenta',
        feral: 'bright_cyan'
    }

    def style_row(nature, r):
        return f"[{nature_styles[nature]}] {str(r)}"

    for k, v in card.nature_values.items():
        target_stat = card.combat_strat.natures[k].boosts
        stat = card._stat(target_stat)
        if target_stat in {EVA, CRIT}:
            stat = f"{round(stat * 100)}%"
        if target_stat == SPEED:
            stat = f"{round(stat, 3)}"

        nature_table.add_row(style_row(k, k), style_row(k, v))
        stat_table.add_row(style_row(k, card.combat_strat.natures[k].boosts), style_row(k, stat))

    table.add_row(nature_table, stat_table)
    return table


def card_markdown(card):
    out = StringIO()

    def p(x=None):
        return print(x, file=out) if x else print(file=out)

    p(f"#### {card.title}")
    p()
    p("Nature | Value | Stat | Value ")
    p("------ | --- | ---- | --- ")
    for k, v in card.nature_values.items():
        target_stat = card.combat_strat.natures[k].boosts
        stat = card._stat(target_stat)
        if target_stat in {EVA, CRIT}:
            stat = f"{round(stat * 100)}%"

        p(' | '.join([
            f"**{k}**",
            str(v),
            f"**{card.combat_strat.natures[k].boosts}**",
            str(stat),
        ]))
    p()

    return out.getvalue()
