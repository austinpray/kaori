from kizuna.AtGraphEdge import AtGraphEdge
from kizuna.User import User
from kizuna.Command import Command
import pygraphviz as pgv


class AtGraphCommand(Command):
    def __init__(self, db_session) -> None:
        help_text = "{bot} at graph - show the graph of @'s\n"
        self.db_session = db_session

        super().__init__('at-graph', "(?:show )?at graph(?: show)?$", help_text, True)

    def respond(self, slack_client, message, matches):
        session = self.db_session()

        edges = session.query(AtGraphEdge).all()

        if not edges or len(edges) < 1:
            return

        G = pgv.AGraph(directed=True)
        for edge in edges:
            G.add_edge(edge.head_user.name, edge.tail_user.name, label=edge.weight, weight=edge.weight)

        image_path = '/tmp/graph.png'
        G.layout(prog='dot')
        G.draw(image_path)
        slack_client.api_call('files.upload',
                              as_user=True,
                              channels=message['channel'],
                              filename='graph.png',
                              file=open(image_path, 'rb'))

        return None
