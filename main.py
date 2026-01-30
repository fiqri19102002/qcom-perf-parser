from perf_parser.parsers import boostsconfig, resourceconfigs, targetinfo
from perf_parser.models import (
    Boost,
    BoostKey,
    PowerHint,
    ResolvedPair,
    ResourceConfig,
    ResourceContext,
    ResourceEntry,
    ResourceKey,
    TargetInfo,
)
from powerhint_json.generator import generate_powerhint_json
from perf_parser.resource_resolvers.mapping import resource_resolvers
from perf_parser.resource_combiners.mapping import resource_combiners
import sys
import os
import argparse
from typing import DefaultDict, List, Tuple, Optional
from collections import defaultdict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QCOM perf config parser')
    parser.add_argument('dump_path', help='Path to dump')
    parser.add_argument(
        '-pbc', '--perfboostsconfig', help='Path to perfboostsconfig.xml', required=False
    )
    parser.add_argument('-ph', '--powerhint', help='Path to powerhint.xml', required=False)
    parser.add_argument(
        '-crc', '--commonresourceconfigs', help='Path to commonresourceconfigs.xml', required=False
    )
    parser.add_argument(
        '-trc', '--targetresourceconfigs', help='Path to targetresourceconfigs.xml', required=False
    )
    parser.add_argument('-ti', '--targetconfig', help='Path to targetconfig.xml', required=False)
    parser.add_argument(
        '-t', '--target', help='target platform, for example: volcano', required=True
    )

    argument = parser.parse_args()

    perfboostsconfig_path = argument.perfboostsconfig or os.path.join(
        argument.dump_path, 'vendor/etc/perf/perfboostsconfig.xml'
    )
    powerhint_path = argument.powerhint or os.path.join(
        argument.dump_path, 'vendor/etc/powerhint.xml'
    )
    commonresourceconfigs_path = argument.commonresourceconfigs or os.path.join(
        argument.dump_path, 'vendor/etc/perf/commonresourceconfigs.xml'
    )
    targetresourceconfigs_path = argument.targetresourceconfigs or os.path.join(
        argument.dump_path, 'vendor/etc/perf/targetresourceconfigs.xml'
    )
    targetconfig_path = argument.targetconfig or os.path.join(
        argument.dump_path, 'vendor/etc/perf/targetconfig.xml'
    )

    # perfboostsconfig.xml and powerhints.xml include all boosts with the resources and values to be set
    perfboosts = boostsconfig.parse_boost_xml(perfboostsconfig_path)
    powerhints = boostsconfig.parse_boost_xml(powerhint_path)

    # commonresourceconfigs.xml and targetresourceconfigs.xml map the resource major/minor to paths
    resource_config: ResourceConfig = resourceconfigs.parse_base_config(commonresourceconfigs_path)
    resourceconfigs.apply_overrides(resource_config, targetresourceconfigs_path)

    # targetinfo.xml contains information about the clusters
    targetconfigs = targetinfo.parse_target_info_xml(targetconfig_path)
    target_info: Optional[TargetInfo] = next(
        (t for t in targetconfigs if t.name == argument.target),
        None,
    )
    if target_info is None:
        print(f'unable to find target info for {argument.target}')
        sys.exit()

    powerhint_map: List[Tuple[BoostKey, str]] = [
        ((0x00001206, None, None), 'SUSTAINED_PERFORMANCE'),
        ((0x00001080, 1, 120), 'INTERACTION'),
        ((0x00001081, 10, None), 'LAUNCH'),
        ((0x00001330, None, None), 'CAMERA_STREAMING_LOW'),
        ((0x00001331, None, None), 'CAMERA_STREAMING_MID'),
        ((0x00001332, None, None), 'CAMERA_STREAMING_HIGH'),
        ((0x00001337, None, None), 'CAMERA_LAUNCH'),
    ]

    generated_powerhints: List[PowerHint] = []
    for bk, powerhint_name in powerhint_map:
        boost_id, boost_type, boost_fps = bk
        boost: Optional[Boost] = next(
            (
                b
                for b in perfboosts + powerhints
                if b.id == boost_id
                and argument.target in b.target
                and (boost_type is None or b.type == boost_type)
                and (boost_fps is None or boost_fps in b.fps)
            ),
            None,
        )
        if not boost:
            print(
                f'Requested boost for {powerhint_name} not found! id: {boost_id}, type: {boost_type}, fps: {boost_fps}'
            )
            continue

        grouped_by_path: DefaultDict[Tuple[str, ResourceKey], List[str]] = defaultdict(list)
        for opcode, raw_value in boost.resources:
            major = (opcode & 0x1FC00000) >> 22
            minor = (opcode & 0x000FC000) >> 14
            cluster = (opcode & 0x00000F00) >> 8

            resource_key: ResourceKey = (major, minor)
            if resource_key not in resource_config:
                print(f'resource 0x{hex(opcode)} is not defined!')
                continue
            resource: ResourceEntry = resource_config[resource_key]

            if not resource.supported:
                continue

            if not resource.node:
                print(f'missing node for {resource}')
                continue

            ctx = ResourceContext(
                boost=boost,
                node=resource.node,
                raw_value=raw_value,
                cluster=cluster,
                target_info=target_info,
            )

            resolver = resource_resolvers.get(
                resource_key, lambda ctx: [(ctx.node, str(ctx.raw_value))]
            )
            for path, value in resolver(ctx):
                grouped_by_path[(path, resource_key)].append(value)

        actions: List[ResolvedPair] = []
        for (path, resource_key), values in grouped_by_path.items():
            combiner = resource_combiners.get(
                resource_key, lambda values, path: 'FIXME'.join(values)
            )
            value = combiner(values, path)
            print(f'{path}: {value}')
            actions.append((path, value))

        generated_powerhints.append(
            PowerHint(name=powerhint_name, duration=boost.timeout, actions=actions)
        )

    generate_powerhint_json(generated_powerhints, 'powerhint.json')
