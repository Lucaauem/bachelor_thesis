from py2neo import Graph, Node, Relationship
import json

class GraphDBService:
    _graph: Graph

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._graph = Graph(uri, auth=(user, password))

    def insert_model(self, model: list[dict]) -> None:
        self._graph.run('MATCH (n) DETACH DELETE n') # Clear old model
        
        for obj in model:
            self._insert_object(obj)

        for obj in model:
            self._create_relation(obj, model)

    def _insert_object(self, obj: dict) -> None:
        obj_type = obj['object_type']
        properties = {
            'id': obj['uuid'],
            'data': json.dumps(obj)
        }

        node = Node(obj_type, **properties)
        self._graph.merge(node, obj_type, 'id')

    def _create_relation(self, obj, model) -> None:
        for key in obj['references']:
            for target in obj['references'][key]:
                from_node = self._graph.nodes.match(obj['object_type'], id=obj['uuid']).first()
                to_node = self._graph.nodes.match(GraphDBService._get_label(target, model), id=target).first()

                if not from_node:
                    print(f"[WARN] Source node with id {obj['uuid']} not found")
                    return
                if not to_node:
                    print(f"[WARN] Target node with id {target} not found")
                    return

                rel = Relationship(from_node, key, to_node)
                self._graph.merge(rel)


    @staticmethod
    def _get_label(uuid: str, model: list[dict]) -> str | None:
        for obj in model:
            if obj['uuid'] == uuid:
                return obj['object_type']
            
        return None