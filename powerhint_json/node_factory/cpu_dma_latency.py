import subprocess
from typing import OrderedDict

from powerhint_json.models import Node


def create_node(name: str, path: str, values: set[str]) -> Node:
    default_value = subprocess.check_output(
        [
            'adb',
            'shell',
            'su',
            '-c',
            'od -An -td4 -N4',
            path,
        ],
        text=True,
    ).strip()

    # avoid duplication of the default value
    if default_value in values:
        values.remove(default_value)
    sorted_values = sorted(values)

    return OrderedDict(
        [
            ('Name', name),
            ('Path', path),
            ('Values', [default_value] + sorted_values),
            ('HoldFd', True),
        ]
    )
