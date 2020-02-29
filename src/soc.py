from migen.genlib.io import CRG
from litex.soc.integration.soc_core import SoCCore
from litex.soc.cores import gpio, uart


class BaseSoC(SoCCore):
    csr_map = {
        "gpio_led": 14,
    }
    csr_map.update(SoCCore.csr_map)

    def __init__(self, platform, sim: bool, **kwargs):
        sys_clk_freq = int(1e9 / platform.default_clk_period)
        SoCCore.__init__(self, platform,
                         cpu_type='vexriscv',
                         clk_freq=sys_clk_freq,
                         with_uart=not sim,
                         **kwargs)
        self.submodules.crg = CRG(platform.request(platform.default_clk_name))
        self.submodules.gpio_led = gpio.GPIOOut(platform.request("user_led"))

        if sim:
            # Serial -----------------------------------------------------------------------------------
            self.submodules.uart_phy = uart.RS232PHYModel(platform.request("serial"))
            self.submodules.uart = uart.UART(self.uart_phy,
                                             tx_fifo_depth=kwargs["uart_fifo_depth"],
                                             rx_fifo_depth=kwargs["uart_fifo_depth"])
            self.add_csr("uart")
            self.add_interrupt("uart")
