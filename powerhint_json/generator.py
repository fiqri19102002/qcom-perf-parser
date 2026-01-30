from perf_parser.models import PowerHint, ResolvedPair
from typing import Dict, List, OrderedDict
from dataclasses import dataclass
import json
import subprocess

Node = OrderedDict[str, str | List[str]]
Action = OrderedDict[str, str | int]


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
    nodes_lookup: Dict[str, OrderedDict[str, str | List[str]]] = {}

    ph_json['Nodes'] = []
    nodes: List[Node] = ph_json['Nodes']
    ph_json['Actions'] = []
    actions: List[Action] = ph_json['Actions']
    for powerhint in powerhints:
        for action in powerhint.actions:
            node_path, value = action
            node_name = _generate_name(node_path)
            if node_path not in nodes_lookup:
                if node_path == "/dev/cpu_dma_latency":
                    current_value = subprocess.check_output(
                        [
                            'adb',
                            'shell',
                            'od -An -td4 -N4',
                            node_path,
                        ],
                        text=True,
                    ).strip()
                    node: Node = {
                        'Name': node_name,
                        'Path': node_path,
                        'Values': [current_value, value],
                        'HoldFd': True,
                    }

                else:
                    current_value = subprocess.check_output(
                        [
                            'adb',
                            'shell',
                            'cat',
                            node_path,
                        ],
                        text=True,
                    ).strip()
                    if node_path == "/proc/sys/walt/sched_upmigrate" or node_path == "/proc/sys/walt/sched_downmigrate":
                        first, second, _ = current_value.split("\t")
                        current_value = f"{first} {second}"
                    node: Node = {
                        'Name': node_name,
                        'Path': node_path,
                        'Values': [current_value, value] if current_value != value else [value],
                        'ResetOnInit': True,
                    }
                nodes.append(node)
                nodes_lookup[node_path] = node
            else:
                if value not in nodes_lookup[node_path]['Values']:
                    nodes_lookup[node_path]['Values'].append(value)

            actions.append(
                {
                    'PowerHint': powerhint.name,
                    'Node': node_name,
                    'Value': value,
                    'Duration': powerhint.duration,
                }
            )

    with open(path, 'w') as f:
        json.dump(ph_json, f, indent=4)

    return
