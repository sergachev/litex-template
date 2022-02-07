### Template project for [LiteX](https://github.com/enjoy-digital/litex) - based SoCs

Various pieces and examples that are not in LiteX yet and a reproducible environment to build and use them.

#### Features:
- `LiteX`-related repositories are registered as git submodules so that their
exact versions are tracked
- a `poetry` environment is used to keep your system and user Python environments clean,
therefore you can have multiple such projects using different versions of `LiteX` 
repositories etc.
- `LiteX`-related packages are installed in the development mode so that they can be worked on easily
- simple and compact

#### How to use:
- clone this repository **recursively**
- check the dependencies below
- use one of the following:
  - A complete (gateware + Cortex-A9 firmware) workflow for Zynq-7000 demonstrated on [Digilent Zedboard](./digilent_zedboard)
  - Xilinx KV260: build all required binaries and run LiteX gateware and BIOS on Zynq Ultrascale+ / Cortex-A53 via JTAG: 
    `make -f Makefile.kv260 load`; use USB-serial terminal on the board (more detailed description coming)
  - Quicklogic Quickfeather - build and flash complete (gateware + BIOS on Cortex-M4) boot images: 
    `make -f Makefile.quickfeather flash`; serial terminal is on pins J3.2/J3.3
  - [Gowin AHB Flash access simulation](./gowin_flash_sim) with LiteX and Verilator
  - other SoC/software/simulation examples in src: new description coming soon

#### External dependencies - have to be in `PATH`:
 - GNU Make, [Ninja](https://ninja-build.org/), Python 3.9+, [poetry](https://python-poetry.org/) (Ubuntu 20.04 and similar: `apt install make ninja-build python3.9 python3-pip; pip install poetry`)
 - For RISC-V cores: [RISC-V GNU toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain/releases)
 - For all 32-bit ARM cores: [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) (arm-none-eabi) - 10.3-2021.10 tested
 - For 64-bit ZynqMP: [GNU Toolchain for the A-profile Architecture](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads) (aarch64-none-elf) - 10.3-2021.07 tested
 - For Xilinx Zynq(MP) to build U-Boot: [GNU Toolchain for the A-profile Architecture](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads) 
   (aarch64-none-linux for ZynqMP, arm-none-linux-gnueabihf for Zynq7000) - 10.3-2021.07 tested
 - For implementation on Xilinx devices: [Xilinx Vivado](https://www.xilinx.com/support/download.html) (2021.2 tested; for some Zynq-related tasks it is convenient to install it as Vitis configuration)
 - For implementation on Gowin devices: [Gowin EDA](https://www.gowinsemi.com/en/support/download_eda/)
 - optional: [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build/releases) - yosys for synthesis, OpenOCD and openFPGALoader for programming, verilator and gtkwave for simulations
 - see [LiteX readme](https://github.com/enjoy-digital/litex/#quick-start-guide) for potential additional requirements like `json-c` and `libevent`
