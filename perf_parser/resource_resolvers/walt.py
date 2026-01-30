from perf_parser.models import ResourceContext, ResolvedPair
from perf_parser.utils.cpu import (
    get_cpu_index_for_cluster,
    get_next_available_frequency_for_cluster,
)
from typing import Iterable


def resolve_walt_path(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    value = get_next_available_frequency_for_cluster(ctx.target_info, ctx.cluster, ctx.raw_value)
    return [
        (
            ctx.node.replace(
                'policy0', f'policy{get_cpu_index_for_cluster(ctx.target_info, ctx.cluster)}'
            ),
            str(value),
        )
    ]
