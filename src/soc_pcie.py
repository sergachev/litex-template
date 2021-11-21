import os
from migen.genlib.misc import WaitTimer
from litex.build.generic_platform import tools
from litex.soc.interconnect.csr import *
from litex.soc.integration.soc_core import SoCMini
from litex.soc.cores.clock import S7MMCM
from litex.soc.integration.export import get_csr_header, get_soc_header, get_mem_header
from litepcie.phy.s7pciephy import S7PCIEPHY
from litepcie.core import LitePCIeEndpoint, LitePCIeMSI
from litepcie.frontend.dma import LitePCIeDMA
from litepcie.frontend.wishbone import LitePCIeWishboneBridge


class _CRG(Module, AutoCSR):
    def __init__(self, platform, sys_clk_freq):
        self.rst = CSR()
        self.clock_domains.cd_sys = ClockDomain()

        # Delay software reset by 10us to ensure write has been acked on PCIe.
        rst_delay = WaitTimer(int(10e-6*sys_clk_freq))
        self.submodules += rst_delay
        self.sync += If(self.rst.re, rst_delay.wait.eq(1))

        self.submodules.pll = pll = S7MMCM(speedgrade=platform.speed_grade)
        self.comb += pll.reset.eq(rst_delay.done)
        pll.register_clkin(platform.request(platform.default_clk_name), 1e9 / platform.default_clk_period)
        pll.create_clkout(self.cd_sys, sys_clk_freq)


class PCIeDMASoC(SoCMini):
    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(100e6)
        SoCMini.__init__(self, platform, sys_clk_freq,
                         csr_data_width=32,
                         ident="LitePCIe example design",
                         ident_version=True,
                         with_uart=True,
                         uart_name="bridge")
        self.submodules.crg = _CRG(platform, sys_clk_freq)
        self.add_csr("crg")
        self.submodules.pcie_phy = S7PCIEPHY(platform, platform.request("pcie_x1"))
        self.pcie_phy.add_timing_constraints(platform)
        # platform.add_false_path_constraints(self.crg.cd_sys.clk, self.pcie_phy.cd_pcie.clk)
        self.add_csr("pcie_phy")
        self.submodules.pcie_endpoint = LitePCIeEndpoint(self.pcie_phy)

        self.submodules.pcie_bridge = LitePCIeWishboneBridge(self.pcie_endpoint,
                                                             base_address=self.mem_map["csr"])
        self.add_wb_master(self.pcie_bridge.wishbone)

        self.submodules.pcie_dma0 = LitePCIeDMA(self.pcie_phy, self.pcie_endpoint,
                                                with_loopback=True)
        self.add_csr("pcie_dma0")
        self.submodules.pcie_dma1 = LitePCIeDMA(self.pcie_phy, self.pcie_endpoint,
                                                with_loopback=True)
        self.add_csr("pcie_dma1")
        self.add_constant("DMA_CHANNELS", 2)

        self.submodules.pcie_msi = LitePCIeMSI()
        self.add_csr("pcie_msi")
        self.comb += self.pcie_msi.source.connect(self.pcie_phy.msi)
        self.interrupts = {
            "PCIE_DMA0_WRITER":    self.pcie_dma0.writer.irq,
            "PCIE_DMA0_READER":    self.pcie_dma0.reader.irq,
            "PCIE_DMA1_WRITER":    self.pcie_dma1.writer.irq,
            "PCIE_DMA1_READER":    self.pcie_dma1.reader.irq,
        }
        for i, (k, v) in enumerate(sorted(self.interrupts.items())):
            self.comb += self.pcie_msi.irqs[i].eq(v)
            self.add_constant(k + "_INTERRUPT", i)

    def generate_software_headers(self, output_dir):
        csr_header = get_csr_header(self.csr_regions, self.constants, with_access_functions=False)
        tools.write_to_file(os.path.join(output_dir, "csr.h"), csr_header)
        soc_header = get_soc_header(self.constants, with_access_functions=False)
        tools.write_to_file(os.path.join(output_dir, "soc.h"), soc_header)
        mem_header = get_mem_header(self.mem_regions)
        tools.write_to_file(os.path.join(output_dir, "mem.h"), mem_header)


default_subtarget = PCIeDMASoC
