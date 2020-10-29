### Template project for [litex](https://github.com/enjoy-digital/litex)-based SoCs

Small complete example SoC project (firmware + gateware) and a lightweight environment to build it.

#### Features:
-  `litex`-related repositories are registered as git submodules so that their
exact versions are tracked
- a `poetry` environment is used to keep your system and user Python environments clean,
therefore you can have multiple such projects using different versions of `litex` 
repositories etc.
- `litex`-related packages are installed in the development mode so that they can be worked on easily
- overall simple and compact (compared to [litex-buildenv](https://github.com/timvideos/litex-buildenv))

#### How to use:
- clone this repository **recursively**
- use `make prepare` to prepare the Python environment and get RISC-V toolchain
- use `make gateware` to run a Vivado implementation or `make sim` to run a simulation
- use `make boot` to load the compiled firmware over a serial port and get a serial terminal
- edit the SoC in `src/`; adjust targets in the `Makefile`; tweak `litex` cores in `lib/`

#### Dependencies:
 - make, wget, tar
 - Python 3.8+
 - poetry
 - Vivado for implementation
 - Verilator for simulation
 - optional: yosys, other litex-related tools
