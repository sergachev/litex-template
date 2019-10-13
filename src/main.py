import argparse
import os

from litex.soc.integration.soc_core import soc_core_args, soc_core_argdict
from litex.soc.integration.builder import builder_args, builder_argdict, Builder

from platform1 import Platform
from soc import BaseSoC


def main():
    parser = argparse.ArgumentParser(description="LiteX SoC")
    builder_args(parser)
    soc_core_args(parser)
    parser.add_argument("--build_gateware", action='store_true')
    parser.add_argument("--yosys", action="store_true")
    args = parser.parse_args()

    platform = Platform()
    cls = BaseSoC
    soc = cls(platform, **soc_core_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder.add_software_package("firmware", src_dir=os.path.join(os.getcwd(), 'src', 'firmware'))
    builder.build(run=args.build_gateware, synth_mode="yosys" if args.yosys else "vivado")


if __name__ == "__main__":
    main()
