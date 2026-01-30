from perf_parser.models import ResourceKey, ResourceResolver
from perf_parser.resource_resolvers import cluster, core_ctl, msm_perf, walt
from typing import Dict

resource_resolvers: Dict[ResourceKey, ResourceResolver] = {
    (0x2, 0x0): msm_perf.resolve_msm_perf,  # msm_perf - min freq
    (0x2, 0x1): msm_perf.resolve_msm_perf,  # msm_perf - max freq
    (0x2, 0x2): walt.resolve_walt_path,
    (0x2, 0x3): walt.resolve_walt_path,
    (0x3, 0x20): lambda x: [],  # unsupported - sched_per_task_boost
    (0x4, 0x0): core_ctl.resolve_lock_min_cores,  # core_ctl - lock_min_cores
    (0x5, 0x11): cluster.resolve_cpu_cluster,  # walt - predictive load
}
