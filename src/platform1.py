from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

from settings import device_model, speed_grade

io_std = IOStandard("LVCMOS33")

_io = [
    ("user_led", 0, Pins("D1 B1"), io_std),

    ("clk100", 0, Pins("V13"), io_std),

    ("serial", 0,
     Subsignal("tx", Pins("AB7")),
     Subsignal("rx", Pins("AB8")),
     io_std,
     ),

    ("spiflash", 0,  # clock needs to be accessed through STARTUPE2
     Subsignal("mosi", Pins("P22")),
     Subsignal("miso", Pins("R22")),
     Subsignal("vpp", Pins("P21")),
     Subsignal("hold", Pins("R21")),
     io_std,
     ),

    ("spi_cs_n", 0, Pins("T19"), io_std),

    ("pcie_x1", 0,
     Subsignal("rst_n", Pins("E1"), IOStandard("LVCMOS25")),
     Subsignal("clk_p", Pins("F6")),
     Subsignal("clk_n", Pins("E6")),
     Subsignal("rx_p", Pins("B10")),
     Subsignal("rx_n", Pins("A10")),
     Subsignal("tx_p", Pins("B6")),
     Subsignal("tx_n", Pins("A6"))
     ),
]

_connectors = []


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    def __init__(self):
        XilinxPlatform.__init__(self, "{}{}".format(device_model, speed_grade),
                                _io, _connectors, toolchain="vivado")
        self.add_platform_command("""
            set_property CFGBVS VCCO [current_design]
            set_property CONFIG_VOLTAGE 3.3 [current_design]
        """)
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
             "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format mcs -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.mcs"]

    def create_programmer(self):
        return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
