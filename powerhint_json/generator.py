from perf_parser.models import PowerHint, ResolvedPair
from powerhint_json.node_factory.default import create_node
from powerhint_json.node_factory.mapping import node_factories
from typing import Dict, List, OrderedDict
from collections import defaultdict
from dataclasses import dataclass
import json
import subprocess


def _generate_name(path: str) -> str:
    path = (
        path.replace('-', ' ')
        .replace('_', ' ')
        .replace('.', ' ')
        .replace(',', ' ')
        .replace('/', ' ')
    )
    path = path.split()
    return path[0] + ''.join(i.capitalize() for i in path[1:])


def generate_powerhint_json(powerhints: List[PowerHint], path: str) -> None:
    ph_json: OrderedDict[str, List[OrderedDict[str, int | str | List[str]]]] = OrderedDict()
    node_to_actions: Dict[str, List[ResolvedPair]] = defaultdict(list)

    ph_json['Nodes'] = []
    nodes: List[Node] = ph_json['Nodes']
    ph_json['Actions'] = []
    actions: List[Action] = ph_json['Actions']
    for powerhint in powerhints:
        for action in powerhint.actions:
            node_path, value = action
            node_to_actions[node_path].append(action)

            node_name = _generate_name(node_path)
            actions.append(
                {
                    'PowerHint': powerhint.name,
                    'Node': node_name,
                    'Value': value,
                    'Duration': powerhint.duration,
                }
            )

    for node_path, actions in node_to_actions.items():
        node_name = _generate_name(node_path)
        values = {action[1] for action in actions}

        factory: NodeFactory = node_factories.get(node_path, create_node)
        nodes.append(factory(node_name, node_path, values))

    with open(path, 'w') as f:
        json.dump(ph_json, f, indent=4)

    return
