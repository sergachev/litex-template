import argparse
import os

from litex.soc.integration.soc_core import soc_core_args, soc_core_argdict
from litex.soc.integration.builder import builder_args, builder_argdict, Builder
from litex.build.sim.config import SimConfig

import platform1
import sim_platform2
from soc import BaseSoC


def main():
    parser = argparse.ArgumentParser(description="LiteX SoC")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument("--build_gateware", action='store_true')
    parser.add_argument("--yosys", action="store_true")
    parser.add_argument("--sim", action="store_true")
    parser.add_argument("--opt-level", default="O3", help="compilation optimization level")
    parser.add_argument("--threads", default=1, help="number of threads")
    args = parser.parse_args()
    builder_kwargs = builder_argdict(args)
    platform = sim_platform2.Platform() if args.sim else platform1.Platform()
    cls = BaseSoC
    soc = cls(platform, sim=args.sim, **soc_core_argdict(args))
    builder = Builder(soc, **builder_kwargs)
    builder.add_software_package("firmware", src_dir=os.path.join(os.getcwd(), 'src', 'firmware'))
    if args.sim:
        sim_config = SimConfig(default_clk="sys_clk")
        sim_config.add_module("serial2console", "serial")
        builder.build(run=False, threads=args.threads, sim_config=sim_config, opt_level=args.opt_level)
        builder.build(build=False, threads=args.threads, sim_config=sim_config, opt_level=args.opt_level)
    else:
        builder.build(run=args.build_gateware, synth_mode="yosys" if args.yosys else "vivado")


if __name__ == "__main__":
    main()
