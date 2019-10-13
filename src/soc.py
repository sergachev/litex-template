from migen.genlib.io import CRG, Signal
from litex.soc.integration.soc_core import SoCCore
from litex.soc.cores import dna, xadc, icap, spi_flash, gpio


class BaseSoC(SoCCore):
    csr_map = {
        "dna": 11,
        "xadc": 12,
        "icap": 13,
        "gpio_led": 14,
        "flash": 15,
        "gpio_flash_cs": 16,
    }
    csr_map.update(SoCCore.csr_map)

    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(1e9/platform.default_clk_period)
        SoCCore.__init__(self, platform,
                         cpu_type='vexriscv',
                         clk_freq=sys_clk_freq,
                         integrated_rom_size=24*1024,
                         integrated_main_ram_size=12*1024,
                         csr_data_width=32,
                         **kwargs)
        self.submodules.crg = CRG(platform.request(platform.default_clk_name))
        self.submodules.dna = dna.DNA()
        self.submodules.xadc = xadc.XADC()
        self.submodules.icap = icap.ICAP()
        self.submodules.gpio_led = gpio.GPIOOut(platform.request("user_led"))
        spi_pads = platform.request("spiflash")
        spi_pads.cs_n = Signal()
        self.submodules.flash = spi_flash.S7SPIFlash(pads=spi_pads,
                                                     sys_clk_freq=sys_clk_freq)
        self.submodules.gpio_flash_cs = gpio.GPIOOut(platform.request("spi_cs_n"))
