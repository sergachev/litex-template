from litex.build.xilinx import XilinxPlatform
from litex.build.xilinx.common import xilinx_special_overrides
from litex.soc.cores.icap import ICAP
from migen.fhdl.module import Module
from migen.fhdl.structure import ClockDomain
from litex.build.generic_platform import Pins


_io = [
    ("clk", 0, Pins(1)),
    ("rst", 0, Pins(1)),
    ('trigger', 0, Pins(1)),
]

REG_CMD = 0b00100
CMD_IPROG = 0b01111


class SoC(Module):
    def __init__(self, platform):
        icap = self.submodules.icap = ICAP()
        self.clock_domains.cd_sys = ClockDomain('sys')
        self.comb += [
            self.cd_sys.clk.eq(platform.request('clk')),
            self.cd_sys.rst.eq(platform.request('rst')),
            icap.send.re.eq(platform.request('trigger'))
        ]
        icap.addr.storage.reset = REG_CMD
        icap.data.storage.reset = CMD_IPROG


def export():
    platform = XilinxPlatform(device='', io=_io)
    soc = SoC(platform)
    fragment = soc.get_fragment()
    platform.finalize(fragment)
    v_output = platform.get_verilog(fragment, name="icap", special_overrides=xilinx_special_overrides)
    v_output.write("icap.v")


if __name__ == '__main__':
    export()
