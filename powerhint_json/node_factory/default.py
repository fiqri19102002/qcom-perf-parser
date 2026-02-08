from powerhint_json.models import Node, DefaultGetter
import subprocess


def create_node(name: str, path: str, values: set[str]) -> Node:
    return create_node_default(
        name,
        path,
        values,
        lambda path, values: subprocess.check_output(
            [
                'adb',
                'shell',
                'cat',
                path,
            ],
            text=True,
        ).strip(),
    )


def create_node_default(
    name: str, path: str, values: set[str], default_getter: DefaultGetter
) -> Node:
    default_value = default_getter(path, values)

    # avoid duplication of the default value
    if default_value in values:
        values.remove(default_value)

    return {
        'Name': name,
        'Path': path,
        'Values': [default_value] + list(values),
        'DefaultIndex': 0,
        'ResetOnInit': True,
    }
