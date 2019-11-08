from migen.genlib.io import CRG
from litex.soc.integration.soc_core import SoCCore
from litex.soc.cores import gpio, uart
from litex.soc.cores.spi import SPIMaster


class BaseSoC(SoCCore):
    csr_map = {
        "gpio_led": 14,
        'spi_master': 15,
    }
    csr_map.update(SoCCore.csr_map)

    def __init__(self, platform, cpu, **kwargs):
        sys_clk_freq = int(1e9 / platform.default_clk_period)
        SoCCore.__init__(self, platform,
                         cpu_type=cpu.name,
                         clk_freq=sys_clk_freq,
                         integrated_rom_size=24*1024,
                         integrated_main_ram_size=12*1024,
                         csr_data_width=32,
                         with_uart=False,
                         **kwargs)
        self.submodules.crg = CRG(platform.request(platform.default_clk_name))
        self.submodules.gpio_led = gpio.GPIOOut(platform.request("user_led"))
        self.submodules.uart_phy = uart.RS232PHYModel(platform.request("serial"))
        self.submodules.uart = uart.UART(self.uart_phy)
        self.add_csr("uart")
        self.add_interrupt("uart")
        self.add_constant("ROM_BOOT_ADDRESS", self.mem_map['main_ram'])
        self.submodules.spi_master = SPIMaster(platform.request('spi'), data_width=40,
                                               sys_clk_freq=sys_clk_freq, spi_clk_freq=1e3)
