import subprocess
from typing import OrderedDict

from powerhint_json.models import DefaultGetter, Node


def create_node(name: str, path: str, values: set[str]) -> Node:
    return create_node_default(
        name,
        path,
        values,
        lambda path, values: subprocess.check_output(
            [
                'adb',
                'shell',
                'su',
                '-c',
                'cat',
                path,
            ],
            text=True,
        ).strip(),
    )


def value_key(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def create_node_default(
    name: str, path: str, values: set[str], default_getter: DefaultGetter
) -> Node:
    default_value = default_getter(path, values)

    # avoid duplication of the default value
    if default_value in values:
        values.remove(default_value)
    sorted_values = sorted(values, key=value_key)

    return OrderedDict(
        [
            ('Name', name),
            ('Path', path),
            ('Values', [default_value] + sorted_values),
            ('DefaultIndex', 0),
            ('ResetOnInit', True),
        ]
    )
