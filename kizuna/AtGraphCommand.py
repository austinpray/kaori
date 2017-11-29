from kizuna.AtGraphEdge import AtGraphEdge
from kizuna.User import User
from kizuna.Command import Command
import pygraphviz as pgv


class AtGraphCommand(Command):
    def __init__(self, db_session) -> None:
        help_text = "{bot} mentions <layout=dot> - show the mention graph. Available formats are" \
                    "dot, neato, fdp, sfdp, twopi, circo, raw\n "
        self.db_session = db_session

        pattern = "mentions(?: (dot|neato|fdp|sfdp|twopi|circo|raw))?$"
        super().__init__('mention-graph', pattern, help_text, True)

    def respond(self, slack_client, message, matches):
        session = self.db_session()

        edges = session.query(AtGraphEdge).all()
        layout = 'dot' if not matches[0] else matches[0]

        if not edges or len(edges) < 1:
            return

        G = pgv.AGraph(directed=True)
        for edge in edges:
            G.add_edge(edge.head_user.name, edge.tail_user.name, label=edge.weight, weight=edge.weight)

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
