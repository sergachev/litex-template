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
- build complete Zedboard QSPI boot image: `make -f Makefile.zedboard`; flash with `program_flash` from Vitis or using U-Boot (description coming soon)
- build and flash complete Quickfeather boot images: `make -f Makefile.quickfeather flash`
- [Gowin AHB Flash access simulation](./gowin_flash_sim)
- other SoC/software/simulation examples in src: new description coming soon

#### External dependencies:
 - GNU Make
 - Python 3.9+
 - [poetry](https://python-poetry.org/)
 - For RISC-V cores: [RISC-V GNU toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain/releases)
 - For all Arm cores: [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
 - For Zynq to build U-Boot: [GNU Toolchain for the A-profile Architecture](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a/downloads)
 - For implementation on Xilinx FPGAs: [Xilinx Vivado](https://www.xilinx.com/support/download.html) (2020.2 to 2021.2 tested)
 - For implementation on Gowin FPGAs: [Gowin EDA](https://www.gowinsemi.com/en/support/download_eda/)
 - optional: [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build/releases) - yosys for synthesis, OpenOCD and openFPGALoader for programming, verilator and gtkwave for simulations
 - see [LiteX readme](https://github.com/enjoy-digital/litex/#quick-start-guide) for potential additional requirements like `json-c` and `libevent`

RISC-V GNU toolchain, GNU Arm Embedded Toolchain, GNU Toolchain for the A-profile Architecture, Vivado, Gowin EDA and OSS CAD Suite: add respective `bin` directories to `PATH`.

Tested on Ubuntu 20.04.
