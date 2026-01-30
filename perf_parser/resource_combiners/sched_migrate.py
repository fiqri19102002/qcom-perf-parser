from perf_parser.models import ResourceContext
from perf_parser.utils.constants import SCHED_MIGRATE_VALUE_UNSET
from typing import Iterable
import subprocess


def combine_sched_migrate(values: Iterable[str], path: str) -> str:
    first: str = SCHED_MIGRATE_VALUE_UNSET
    second: str = SCHED_MIGRATE_VALUE_UNSET
    for value in values:
        a, b = value.split()
        if a is not SCHED_MIGRATE_VALUE_UNSET:
            first = a
        if b is not SCHED_MIGRATE_VALUE_UNSET:
            second = b

    def_first, def_second = subprocess.check_output(
        [
            'adb',
            'shell',
            'cat',
            path,
        ],
        text=True,
    ).split()[:2]

    if first is SCHED_MIGRATE_VALUE_UNSET:
        first = def_first
    if second is SCHED_MIGRATE_VALUE_UNSET:
        second = def_second

    return f'{first} {second}'
