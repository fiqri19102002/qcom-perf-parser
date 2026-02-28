import subprocess
from typing import Iterable

from perf_parser.models import ResolvedPair, ResourceContext


def resolve_clk_scale(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    fstab_suffix = subprocess.check_output(
        [
            'adb',
            'shell',
            'getprop ro.boot.fstab_suffix',
        ],
        text=True,
    ).strip()

    return [
        (
            '/sys/class/scsi_host/host0/../../../clkscale_enable'
            if fstab_suffix == 'default'
            else '/sys/class/mmc_host/mmc0/clk_scaling/enable',
            str(ctx.raw_value),
        )
    ]
