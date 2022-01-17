import argparse
from migen import *
from migen.genlib.misc import WaitTimer
from litex.soc.integration.builder import builder_args, builder_argdict, Builder
from litex.build.sim.config import SimConfig
from litex.soc.integration.soc_core import SoCMini
from litex.soc.interconnect import ahb
from litex.build.sim import SimPlatform
from litex.build.generic_platform import Pins
from litex.soc.cores.cpu.gowin_emcu.core import AHBFlash


_io = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
]


class Platform(SimPlatform):
    default_clk_name = "sys_clk"
    default_clk_period = 1000  # ~ 1MHz

    def __init__(self):
        SimPlatform.__init__(self, "SIM", _io)

    def do_finalize(self, fragment, *args, **kwargs):
        pass


class SimSoC(SoCMini):
    def __init__(self, platform, sys_clk_freq):
        super().__init__(platform, sys_clk_freq)
        self.comb += platform.trace.eq(1)

        bus = ahb.Interface()
        self.submodules += AHBFlash(bus)

        platform.add_sources('build', "prim_sim.v")

        wt = self.submodules.wt = WaitTimer(8)

        loop_counter = Signal(10)
        self.sync += If(loop_counter == 100, Finish())

        fsm = self.submodules.fsm = FSM()
        fsm.act('INIT',
                NextValue(bus.sel, 1),
                NextValue(bus.trans, ahb.TransferType.NONSEQUENTIAL),
                NextValue(bus.addr, 0b1111111100001111001101),
                NextValue(loop_counter, loop_counter + 1),
                NextState('WAIT0')
                )
        fsm.act('WAIT0', NextState('WAIT'))
        fsm.act('WAIT',
                NextValue(bus.trans, ahb.TransferType.IDLE),
                If(bus.readyout,
                   NextState('DONE')))
        fsm.act('DONE',
                wt.wait.eq(1),
                If(wt.done, NextState('INIT')))


def main():
    parser = argparse.ArgumentParser()
    builder_args(parser)
    args = parser.parse_args()
    builder_kwargs = builder_argdict(args)
    platform = Platform()
    soc = SimSoC(platform, 1e9 / platform.default_clk_period)
    builder = Builder(soc, **builder_kwargs)
    sim_config = SimConfig(default_clk=platform.default_clk_name)
    builder.build(sim_config=sim_config, opt_level='O3', trace=True, trace_fst=False)


if __name__ == "__main__":
    main()
