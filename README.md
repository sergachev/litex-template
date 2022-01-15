### Template project for [LiteX](https://github.com/enjoy-digital/litex) - based SoCs

Small complete example SoC project (firmware + gateware) and a lightweight environment to build and simulate it.

#### Features:
-  `LiteX`-related repositories are registered as git submodules so that their
exact versions are tracked
- a `poetry` environment is used to keep your system and user Python environments clean,
therefore you can have multiple such projects using different versions of `LiteX` 
repositories etc.
- `LiteX`-related packages are installed in the development mode so that they can be worked on easily
- simple and compact

#### How to use:
- clone this repository **recursively**
- use `make gateware` to run a Vivado implementation or `make sim` to run a simulation
- use `make boot` to load the compiled firmware over a serial port and get a serial terminal by means of litex_term
- edit the SoC in `src/`; adjust targets in the `Makefile`; tweak `LiteX` cores in `lib/`

#### External dependencies:
 - GNU Make
 - Python 3.9+
 - [poetry](https://python-poetry.org/)
 - For RISC-V cores [RISC-V GNU toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain/releases)
 - For implementation on Xilinx FPGAs: [Xilinx Vivado](https://www.xilinx.com/support/download.html) (2020.2 to 2021.2 tested)
 - For implementation on Gowin FPGAs: [Gowin EDA](https://www.gowinsemi.com/en/support/download_eda/)
 - Verilator for simulation (see [LiteX readme](https://github.com/enjoy-digital/litex/#quick-start-guide) for additional requirements like `libjson-c`) - can be installed via [Homebrew](https://formulae.brew.sh/formula/verilator)
 - optional: [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build/releases) - yosys for synthesis, OpenOCD and openFPGALoader for programming

RISC-V GNU toolchain, Vivado and OSS CAD Suite: add respective `bin` directories to `PATH`.

Tested on Ubuntu 20.04.
