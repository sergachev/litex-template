import argparse
import os

from litex.soc.integration.common import get_mem_data
from litex.soc.integration.soc_core import soc_core_args, soc_core_argdict
from litex.soc.integration.builder import builder_args, builder_argdict, Builder
from litex.soc.cores.cpu.vexriscv.core import VexRiscv
from litex.build.sim.config import SimConfig

import platform_xilinx
import platform_sim
from soc_base import BaseSoC
from soc_pcie import PCIeDMASoC


def main():
    soc_cls = BaseSoC
    cpu = VexRiscv

    parser = argparse.ArgumentParser(description="LiteX SoC")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument("--build_gateware", action='store_true')
    parser.add_argument("--yosys", action="store_true")
    parser.add_argument("--sim", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    builder_kwargs = builder_argdict(args)
    soc_kwargs = soc_core_argdict(args)
    platform = platform_sim.Platform() if args.sim else platform_xilinx.Platform()
    output_dir = builder_kwargs['output_dir'] = 'build'
    fw_file = os.path.join(output_dir, "software", "firmware", "firmware.bin")
    soc_kwargs['integrated_rom_size'] = 32 * 1024
    soc_kwargs["integrated_main_ram_size"] = 16 * 1024
    try:
        soc_kwargs['integrated_main_ram_init'] = get_mem_data(fw_file, cpu.endianness)
    except OSError:
        pass
    soc = soc_cls(platform, cpu=cpu, sim=args.sim, output_dir=output_dir, **soc_kwargs)
    builder = Builder(soc, **builder_kwargs)
    builder.add_software_package("firmware", src_dir=os.path.join(os.getcwd(), 'src', 'firmware'))
    if args.sim:
        sim_config = SimConfig(default_clk="sys_clk")
        sim_config.add_module("serial2console", "serial")
        builder.build(run=False, sim_config=sim_config, opt_level='O3')
        if args.run:
            builder.build(build=False, sim_config=sim_config)
    else:
        builder.build(run=args.build_gateware, synth_mode="yosys" if args.yosys else "vivado")


if __name__ == "__main__":
    main()
