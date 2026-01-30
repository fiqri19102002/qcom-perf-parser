from perf_parser.models import ResourceContext, ResolvedPair
from perf_parser.utils.cpu import get_cpu_index_for_cluster
from typing import Iterable


def resolve_cpu_cluster(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    return [
        (
            ctx.node.replace(
                'cpu0', f'cpu{get_cpu_index_for_cluster(ctx.target_info, ctx.cluster)}'
            ),
            str(ctx.raw_value),
        )
    ]
