from kizuna.AtGraphEdge import AtGraphEdge
from kizuna.User import User
from kizuna.Command import Command
import pygraphviz as pgv
from palettable import tableau


class AtGraphCommand(Command):
    def __init__(self, db_session) -> None:
        help_text = "{bot} mentions <layout=dot> - show the mention graph. Available formats are" \
                    "dot, neato, fdp, sfdp, twopi, circo, raw\n "
        self.db_session = db_session

        pattern = "mentions(?: (dot|neato|fdp|sfdp|twopi|circo|raw))?$"
        super().__init__('mention-graph', pattern, help_text, True)

    def respond(self, slack_client, message, matches):
        session = self.db_session()

        edges = session.query(AtGraphEdge).order_by(AtGraphEdge.weight.asc()).all()
        users = session.query(User).order_by(User.name.asc()).all()
        layout = 'dot' if not matches[0] else matches[0]

        if not edges or len(edges) < 1:
            return

        G = pgv.AGraph(directed=True)
        color_index = 0
        user_color_map = {}
        colors = tableau.get_map('Tableau_20').hex_colors

        for user in users:
            color = colors[color_index]
            color_index = color_index + 1 if color_index < (len(colors) - 1) else 0
            user_color_map[user.name] = color
            G.add_node(user.name, color=color)

        max_penwidth = 5
        min_penwidth = 0.10

        max_weight = edges[len(edges) - 1].weight
        min_weight = edges[0].weight

        for edge in edges:
            old_range = (max_weight - min_weight)
            new_range = (max_penwidth - min_penwidth)
            penwidth = (((edge.weight - min_weight) * new_range) / old_range) + min_penwidth
            G.add_edge(edge.head_user.name,
                       edge.tail_user.name,
                       penwidth=penwidth,
                       label=edge.weight,
                       weight=edge.weight,
                       fontcolor=user_color_map[edge.head_user.name],
                       color=user_color_map[edge.head_user.name])

        if layout == 'raw':
            return slack_client.api_call('files.upload',
                                         as_user=True,
                                         channels=message['channel'],
                                         filename='graph.dot',
                                         file=G.string())

        image_path = '/tmp/graph.png'

        def dot():
            G.layout(prog='dot')

        def neato():
            G.graph_attr.update(overlap='scale')
            G.graph_attr.update(splines=True)
            G.graph_attr.update(sep=1)
            G.layout(prog='neato')

        def fdp():
            G.layout(prog='fdp')

        def sfdp():
            G.layout(prog='sfdp')

        def twopi():
            G.layout(prog='twopi')

        def circo():
            G.layout(prog='circo')

        def layout_graph(layout):
            return {
                "dot": dot,
                "neato": neato,
                "fdp": fdp,
                "sfdp": sfdp,
                "twopi": twopi,
                "circo": circo
            }.get(layout, dot)

        layout_graph(layout)()

        G.draw(image_path)
        slack_client.api_call('files.upload',
                              as_user=True,
                              channels=message['channel'],
                              filename='graph.png',
                              file=open(image_path, 'rb'))

        return None
