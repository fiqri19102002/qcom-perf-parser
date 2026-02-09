import subprocess
from typing import OrderedDict

from powerhint_json.models import DefaultGetter, Node


def create_node_min(name: str, path: str, values: set[str]) -> Node:
    return create_node_msm_perf(
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


def create_node_max(name: str, path: str, values: set[str]) -> Node:
    return create_node_msm_perf(
        name,
        path,
        values,
        lambda path, values: (
            '0:9999999 1:9999999 2:9999999 3:9999999 4:9999999 5:9999999 6:9999999 7:9999999'
        ),
    )


def create_node_msm_perf(
    name: str, path: str, values: set[str], default_getter: DefaultGetter
) -> Node:
    default_value = default_getter(path, values)

    # avoid duplication of the default value
    if default_value in values:
        values.remove(default_value)

    sorted_values = sorted(
        values, key=lambda s: [[int(x) for x in cpu_value.split(':')] for cpu_value in s.split()]
    )
    return OrderedDict(
        [
            ('Name', name),
            ('Path', path),
            ('Values', [default_value] + sorted_values),
        ]
    )
