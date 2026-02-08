from powerhint_json.models import Node
from powerhint_json.node_factory.default import create_node_default
import subprocess


def create_node(name: str, path: str, values: set[str]) -> Node:
    default_value = subprocess.check_output(
        [
            'adb',
            'shell',
            'od -An -td4 -N4',
            path,
        ],
        text=True,
    ).strip()

    # avoid duplication of the default value
    if default_value in values:
        values.remove(default_value)

    return {
        'Name': name,
        'Path': path,
        'Values': [default_value] + list(values),
        'HoldFd': True,
    }
