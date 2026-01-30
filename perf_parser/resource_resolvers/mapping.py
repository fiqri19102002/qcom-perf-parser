from perf_parser.models import ResourceKey, ResourceResolver
from perf_parser.resource_resolvers import core_ctl, msm_perf
from typing import Dict

resource_resolvers: Dict[ResourceKey, ResourceResolver] = {
    # (major, minor): handler
    (0x2, 0x0): msm_perf.resolve_msm_perf,
    (0x2, 0x1): msm_perf.resolve_msm_perf,
    (0x3, 0x20): lambda x: [], # unsupported - sched_per_task_boost
    (0x4, 0x0): core_ctl.resolve_lock_min_cores,
}