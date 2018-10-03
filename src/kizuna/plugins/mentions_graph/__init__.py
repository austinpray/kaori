import re
from subprocess import CalledProcessError
from threading import Thread
from time import sleep

from graphviz import Digraph
from palettable import tableau
from slacktools.arguments import SlackArgumentParserException, SlackArgumentParser

from kizuna.adapters.slack import SlackAdapter, SlackMessage, SlackCommand
from kizuna.plugins.users import User
from kizuna.skills.db import DB
from kizuna.support.strings import WAIT_A_SEC, JAP_DOT
from .models import MentionGraphEdge

parser = SlackArgumentParser(prog='kizuna mentions', description='Generate a mentions graph', add_help=False)
available_layouts = ['dot', 'neato', 'fdp', 'twopi', 'circo']

markdown_available_layouts = list(map(lambda s: f'`{s}`', available_layouts))
parser.add_argument('--layout',
                    '-l',
                    dest='layout',
                    default='dot',
                    help='Defaults to `dot`. Can be any of ' + ', '.join(markdown_available_layouts))

parser.add_argument('--raster',
                    '-r',
                    dest='raster',
                    action='store_true',
                    help='Set to render a png instead of a pdf')

parser.add_help_argument()


class MentionGraphCommand(SlackCommand):

    @staticmethod
    def handle(message: SlackMessage, bot: SlackAdapter, db: DB):

        if not bot.addressed_by(message):
            return

        matches = bot.understands(message, with_pattern=re.compile('mentions(?: (.*))?', re.I))

        if not matches:
            return

        user_args = matches.group(1).split() if matches. else []

        try:
            args = parser.parse_args(user_args)
        except SlackArgumentParserException as err:
            return bot.reply(message, str(err))

        user_layout = args.layout
        output_format = 'png' if args.raster else 'pdf'

        if user_layout not in available_layouts:
            layout_error_message = ("Oops! --user_layout needs to be one of '{}'. "
                                    "You gave me '{}'").format(', '.join(available_layouts), user_layout)
            return bot.reply(message, layout_error_message)

        if args.help:
            return bot.respond(message, parser.get_help())

        with db.session_scope() as session:
            edges = session.query(MentionGraphEdge).order_by(MentionGraphEdge.weight.asc()).all()
            users = session.query(User).order_by(User.name.asc()).all()

            if not edges or len(edges) < 1:
                bot.reply(message, "Uhh...Could not find any edges in the db. Something is probably wrong.")
                return

            loading_message = bot.reply(message, WAIT_A_SEC + JAP_DOT)

            loaded = False

            def continiously_update_loading_message():
                cycle_count = 0
                dot_count = 1
                while not loaded and cycle_count < 20:
                    sleep(1)
                    if loaded:
                        break
                    dot_count = dot_count + 1 if dot_count < 3 else 1
                    new_text = WAIT_A_SEC + (dot_count * JAP_DOT)
                    slack_client.api_call("chat.update",
                                          ts=loading_message['ts'],
                                          channel=channel,
                                          text=new_text,
                                          as_user=True)
                    cycle_count += 1

            thread = Thread(target=continiously_update_loading_message)

            if loading_message['ok']:
                thread.start()

            graph = Digraph(comment='Mentions', format=output_format)
            color_index = 0
            user_color_map = {}
            colors = tableau.get_map('Tableau_20').hex_colors

            for user in users:
                color = colors[color_index]
                color_index = color_index + 1 if color_index < (len(colors) - 1) else 0
                user_color_map[user.name] = color
                graph.node(user.name, color=color)

            max_weight = edges[len(edges) - 1].weight
            min_weight = edges[0].weight

            max_penwidth = 5
            min_penwidth = 0.10

            max_fontsize = 20
            min_fontsize = 7

            def scale_penwidth_by(value):
                return self.linear_scale(max_weight, min_weight, max_penwidth, min_penwidth, value)

            def scale_fontsize_by(value):
                return self.linear_scale(max_weight, min_weight, max_fontsize, min_fontsize, value)

            for edge in edges:
                graph.edge(edge.head_user.name,
                           edge.tail_user.name,
                           penwidth=str(scale_penwidth_by(edge.weight)),
                           label=str(edge.weight),
                           weight=str(edge.weight),
                           fontsize=str(scale_fontsize_by(edge.weight)),
                           fontcolor=str(user_color_map[edge.head_user.name]),
                           color=user_color_map[edge.head_user.name])

            def dot():
                graph.engine = 'dot'

            def neato():
                graph.engine = 'neato'

            def fdp():
                graph.engine = 'fdp'

            def twopi():
                graph.engine = 'twopi'

            def circo():
                graph.engine = 'circo'

            def layout_graph(layout):
                return {
                    "dot": dot,
                    "neato": neato,
                    "fdp": fdp,
                    "twopi": twopi,
                    "circo": circo
                }.get(layout, dot)

            try:
                layout_graph(user_layout)()

                slack_client.api_call('files.upload',
                                      as_user=True,
                                      channels=message['channel'],
                                      filename=f'graph.{output_format}',
                                      file=graph.pipe())
            except CalledProcessError as err:
                send_message('Encountered a problem while rendering the graph :monkas:')
                raise err
            except TypeError as err:
                send_message('Encountered a problem while trying to write the graph to the file system :monkas:')
                raise err
            finally:
                loaded = True
                thread.join()
                slack_client.api_call("chat.delete",
                                      ts=loading_message['ts'],
                                      channel=channel,
                                      as_user=True)
