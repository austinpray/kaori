from .Command import Command

from config import KIZUNA_WEB_URL
from kizuna.models.User import User
from kizuna.utils import build_url, slack_link
from kizuna.models import ReactionImageTag
from random import choice


class ReactCommand(Command):
    def __init__(self, Session) -> None:
        help_text = 'kizuna react - view available reaction images and tags\n' \
                    'kizuna react add - upload some reaction images\n' \
                    'kizuna react <tag> - Send a reaction related to the tag'
        self.Session = Session
        super().__init__(name='react',
                         pattern='react(?:ion)?(?: (.*))?$',
                         help_text=help_text,
                         is_at=True)

    def respond(self, slack_client, message, matches):
        send = self.send_ephemeral_factory(slack_client, message['channel'], message['user'])
        send_public = self.send_factory(slack_client, message['channel'])

        session = self.Session()
        user = User.get_by_slack_id(session, message['user'])
        query = matches[0]
        if query:
            query = query.strip()

        if not user:
            return send("I don't have your users in the db. Prolly run 'kizuna refresh users' and if that still "
                        "doesn't fix it: Austin fucked up somewhere :^(")

        def authenticated_path(path):
            return build_url(KIZUNA_WEB_URL, path, {'auth': user.get_token()})

        react_homepage_url = authenticated_path('/react')
        react_add_image_url = authenticated_path('/react/images/new')

        if not query:
            # kizuna react$
            return send(react_homepage_url)

        if query == 'add':
            # kizuna react add
            return send(react_add_image_url)

        # kizuna react <tag>
        def add_images_nag():
            add_images = slack_link('(Add Images)', react_add_image_url)
            view_images = slack_link('(View Images)', react_homepage_url)
            send("You can add some images with that tag though! {} {}".format(add_images, view_images))

        tag = session.query(ReactionImageTag).filter(ReactionImageTag.name == query).first()
        if tag:
            if len(tag.images) > 0:
                return send_public(choice(tag.images).url)

            send_public('I don\'t have any images with the tag "{}" :^('.format(query))
            return add_images_nag()

        send_public('I don\'t have that "{}" as a tag :^('.format(query))
        return add_images_nag()
