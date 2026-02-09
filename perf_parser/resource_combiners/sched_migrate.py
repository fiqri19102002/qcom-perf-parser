import subprocess
from typing import List

from perf_parser.utils.constants import SCHED_MIGRATE_VALUE_UNSET


def combine_sched_migrate(values: List[str], path: str) -> str:
    set_values = subprocess.check_output(
        [
            'adb',
            'shell',
            'su',
            '-c',
            'cat',
            path,
        ],
        text=True,
    ).split()

    for s in values:
        for i, value in enumerate(s.split()):
            if value != SCHED_MIGRATE_VALUE_UNSET:
                set_values[i] = value

    return ' '.join(set_values[: len(values[0].split())])
