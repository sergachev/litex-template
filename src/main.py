import argparse
import os

from litex.soc.integration.common import get_mem_data
from litex.soc.integration.soc_core import soc_core_args, soc_core_argdict
from litex.soc.integration.builder import builder_args, builder_argdict, Builder
from litex.soc.cores.cpu import VexRiscv
from litex.build.sim.config import SimConfig

import platform1
from soc import BaseSoC


def main():
    platform = platform1.Platform()
    soc_cls = BaseSoC
    cpu = VexRiscv

    parser = argparse.ArgumentParser(description="LiteX SoC")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument('--run_sim', action='store_true')
    parser.add_argument("--opt-level", default="O3", help="compilation optimization level")
    parser.add_argument("--threads", default=1, help="number of threads")
    args = parser.parse_args()
    builder_kwargs = builder_argdict(args)
    soc_kwargs = soc_core_argdict(args)
    output_dir = builder_kwargs['output_dir'] = f"soc_{soc_cls.__name__.lower()}_{platform.name}"
    fw_file = os.path.join(output_dir, "software", "firmware", "firmware.bin")
    if args.run_sim:
        soc_kwargs['integrated_main_ram_init'] = get_mem_data(fw_file, cpu.endianness)
    soc = BaseSoC(platform, cpu=cpu, output_dir=builder_kwargs['output_dir'], **soc_kwargs)
    builder = Builder(soc, **builder_kwargs)
    builder.add_software_package("firmware", src_dir=os.path.join(os.getcwd(), 'src', 'firmware'))
    if args.run_sim:
        sim_config = SimConfig(default_clk="sys_clk")
        sim_config.add_module("serial2console", "serial")
        builder.build(run=False, threads=args.threads, sim_config=sim_config, opt_level=args.opt_level)
        builder.build(build=False, threads=args.threads, sim_config=sim_config, opt_level=args.opt_level)
    else:
        builder.build(build=False, run=False)


if __name__ == "__main__":
    main()
