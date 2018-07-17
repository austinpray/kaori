from kizuna.models.AtGraphEdge import AtGraphEdge
from kizuna.models.User import User
from kizuna.commands.Command import Command
from palettable import tableau

from subprocess import CalledProcessError

from graphviz import Digraph

from kizuna.strings import WAIT_A_SEC, JAP_DOT

from threading import Thread
from time import sleep

from kizuna.SlackArgumentParser import SlackArgumentParser, SlackArgumentParserException


class AtGraphCommand(Command):
    def __init__(self, db_session) -> None:
        self.db_session = db_session

        self.available_layouts = ['dot', 'neato', 'fdp', 'twopi', 'circo']

        parser = SlackArgumentParser(prog='kizuna mentions', description='Generate a mentions graph', add_help=False)
        self.add_help_command(parser)

        markdown_available_layouts = list(map(lambda s: '`{}`'.format(s), self.available_layouts))
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

        self.set_help_text(parser)
        self.parser = parser

        pattern = "mentions(?: (.*))?$"
        super().__init__('mention-graph', pattern, self.help_text, True)

    @staticmethod
    def linear_scale(old_max, old_min, new_max, new_min, value):
        old_range = (old_max - old_min)
        if old_range == 0:
            return value
        new_range = (new_max - new_min)
        return (((value - old_min) * new_range) / old_range) + new_min

    def respond(self, slack_client, message, matches):
        channel = message['channel']
        send = self.send_factory(slack_client, message['channel'])

        user_args = matches[0].split(' ') if matches[0] else []
        try:
            args = self.parser.parse_args(user_args)
        except SlackArgumentParserException as err:
            return send(str(err))

        user_layout = args.layout
        output_format = 'png' if args.raster else 'pdf'

        def send_message(text):
            return slack_client.api_call("chat.postMessage",
                                         channel=channel,
                                         text=text,
                                         as_user=True)

        if user_layout not in self.available_layouts:
            layout_error_message = ("Oops! --user_layout needs to be one of '{}'. "
                                    "You gave me '{}'").format(', '.join(self.available_layouts), user_layout)
            return send_message(layout_error_message)

        if args.help:
            return send_message(self.help_text)

        session = self.db_session()

        edges = session.query(AtGraphEdge).order_by(AtGraphEdge.weight.asc()).all()
        users = session.query(User).order_by(User.name.asc()).all()

        if not edges or len(edges) < 1:
            send_message("Uhh...Could not find any edges in the db. Something is probably wrong.")
            return

        loading_message = slack_client.api_call("chat.postMessage",
                                                channel=channel,
                                                text=WAIT_A_SEC + JAP_DOT,
                                                as_user=True)

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

        # if user_layout == 'raw':
        #     return slack_client.api_call('files.upload',
        #                                  as_user=True,
        #                                  channels=message['channel'],
        #                                  filename='graph.dot',
        #                                  file=graph.do)

        def dot():
            graph.engine = 'dot'

        def neato():
            # G.graph_attr.update(overlap='scale')
            # G.graph_attr.update(splines=True)
            # G.graph_attr.update(sep=1)
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

        return None
