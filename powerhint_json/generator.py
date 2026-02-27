import json
from collections import defaultdict
from typing import Dict, List, OrderedDict

from perf_parser.models import PowerHint, ResolvedPair
from powerhint_json.models import Action, Node, NodeFactory
from powerhint_json.node_factory.default import create_node
from powerhint_json.node_factory.mapping import node_factories


def _generate_name(path: str) -> str:
    path = (
        path.replace('-', ' ')
        .replace('_', ' ')
        .replace('.', ' ')
        .replace(',', ' ')
        .replace('/', ' ')
    )
    path_list = path.split()
    return path_list[0] + ''.join(i.capitalize() for i in path_list[1:])


def generate_powerhint_json(powerhints: List[PowerHint], path: str) -> None:
    ph_json: OrderedDict[str, List[Node] | List[Action]] = OrderedDict()
    node_to_actions: Dict[str, List[ResolvedPair]] = defaultdict(list)

    ph_nodes: List[Node] = []
    ph_actions: List[Action] = []
    for powerhint in powerhints:
        for action in powerhint.actions:
            node_path, value = action
            node_to_actions[node_path].append(action)

            node_name = _generate_name(node_path)
            ph_actions.append(
                OrderedDict(
                    [
                        ('PowerHint', powerhint.name),
                        ('Node', node_name),
                        ('Value', value),
                        (
                            'Duration',
                            powerhint.duration,
                        ),
                    ]
                )
            )

    for node_path, actions in node_to_actions.items():
        node_name = _generate_name(node_path)
        values = {action[1] for action in actions}

        factory: NodeFactory = node_factories.get(node_path, create_node)
        ph_nodes.append(factory(node_name, node_path, values))

    ph_json['Nodes'] = ph_nodes
    ph_json['Actions'] = ph_actions

    with open(path, 'w') as f:
        json.dump(ph_json, f, indent=4)

    return
