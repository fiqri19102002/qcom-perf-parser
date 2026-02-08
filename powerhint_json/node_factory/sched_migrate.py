from powerhint_json.models import Node
from powerhint_json.node_factory.default import create_node_default
import subprocess


def _get_default_value(path: str, values: set[str]) -> str:
    read_value = subprocess.check_output(
        [
            'adb',
            'shell',
            'cat',
            path,
        ],
        text=True,
    ).strip()

    # make sure to align the length of the default value with the values we set
    # which is determined with knowledge about the cpu clusters. The node sometimes
    # reports 3 values but you can only write the first two...
    value = next(iter(values))
    if not value:
        print(f'no value set for {path}')
        sys.exit()
    return ' '.join(read_value.split()[: len(value.split())])


def create_node(name: str, path: str, values: set[str]) -> Node:
    return create_node_default(name, path, values, _get_default_value)
