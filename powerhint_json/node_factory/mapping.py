from powerhint_json.models import NodeFactory
from powerhint_json.node_factory import cpu_dma_latency, msm_perf, sched_migrate
from typing import Dict

node_factories: Dict[str, NodeFactory] = {
    # path: node factory
    '/dev/cpu_dma_latency': cpu_dma_latency.create_node,
    '/proc/sys/walt/sched_upmigrate': sched_migrate.create_node,
    '/proc/sys/walt/sched_downmigrate': sched_migrate.create_node,
    '/sys/kernel/msm_performance/parameters/cpu_min_freq': msm_perf.create_node_min,
    '/sys/kernel/msm_performance/parameters/cpu_max_freq': msm_perf.create_node_max,
}
