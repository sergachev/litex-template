# from migen.genlib.io import CRG
# from litex.soc.integration.soc_core import SoCCore
# from litex.soc.cores import gpio, uart


# class BaseSoC(SoCCore):
#     csr_map = {
#         "gpio_led": 14,
#     }
#     csr_map.update(SoCCore.csr_map)
#
#     def __init__(self, platform, sim: bool, **kwargs):
#         sys_clk_freq = int(1e9/platform.default_clk_period)
#         SoCCore.__init__(self, platform,
#                          cpu_type='vexriscv',
#                          clk_freq=sys_clk_freq,
#                          integrated_rom_size=24*1024,
#                          integrated_main_ram_size=12*1024,
#                          csr_data_width=32,
#                          with_uart=not sim,
#                          **kwargs)
#         self.submodules.crg = CRG(platform.request(platform.default_clk_name))
#         self.submodules.gpio_led = gpio.GPIOOut(platform.request("user_led"))
#
#         if sim:
#             self.submodules.uart_phy = uart.RS232PHYModel(platform.request("serial"))
#             self.submodules.uart = uart.UART(self.uart_phy)
#             self.add_csr("uart")
#             self.add_interrupt("uart")

from litex.soc.interconnect.csr import *

from litex.soc.integration.soc_core import SoCMini

from litepcie.phy.s7pciephy import S7PCIEPHY
from litepcie.core import LitePCIeEndpoint, LitePCIeMSI
from litepcie.frontend.dma import LitePCIeDMA
from litepcie.frontend.wishbone import LitePCIeWishboneBridge


class _CRG(Module, AutoCSR):
    def __init__(self, platform):
        self.clock_domains.cd_sys = ClockDomain("sys")
        self.comb += self.cd_sys.clk.eq(ClockSignal("pcie"))


class PCIeDMASoC(SoCMini):
    # default_platform = "kc705"
    mem_map = {"csr": 0x00000000}

    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(125e6)
        SoCMini.__init__(self, platform, sys_clk_freq, csr_data_width=32,
                         ident="LitePCIe example design", ident_version=True, **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform)

        # PCIe PHY ---------------------------------------------------------------------------------
        self.submodules.pcie_phy = S7PCIEPHY(platform, platform.request("pcie_x1"))
        self.add_csr("pcie_phy")

        # PCIe Endpoint ----------------------------------------------------------------------------
        self.submodules.pcie_endpoint = LitePCIeEndpoint(self.pcie_phy)

        # PCIe Wishbone bridge ---------------------------------------------------------------------
        self.submodules.pcie_bridge = LitePCIeWishboneBridge(self.pcie_endpoint, lambda a: 1)
        self.add_wb_master(self.pcie_bridge.wishbone)

        # PCIe DMA ---------------------------------------------------------------------------------
        self.submodules.pcie_dma = LitePCIeDMA(self.pcie_phy, self.pcie_endpoint, with_loopback=True)
        self.add_csr("pcie_dma")

        # PCIe MSI ---------------------------------------------------------------------------------
        self.submodules.pcie_msi = LitePCIeMSI()
        self.add_csr("pcie_msi")
        self.comb += self.pcie_msi.source.connect(self.pcie_phy.msi)
        self.interrupts = {
            "PCIE_DMA_WRITER":    self.pcie_dma.writer.irq,
            "PCIE_DMA_READER":    self.pcie_dma.reader.irq
        }
        for i, (k, v) in enumerate(sorted(self.interrupts.items())):
            self.comb += self.pcie_msi.irqs[i].eq(v)
            self.add_constant(k + "_INTERRUPT", i)


default_subtarget = PCIeDMASoC
