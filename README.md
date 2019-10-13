### Template project for [litex](https://github.com/enjoy-digital/litex) - based SoCs

Contains a small but complete example SoC project (firmware + gateware) and a very minimal
environment to build it.

#### Details:
- `litex`-related repositories are registered as git submodules so that their
exact versions are tracked
- a `pipenv` environment is used so that your system is kept untoched, 
you can have several such projects using different versions of `litex` 
repositories etc.
- `litex` packages are installed in the development mode, so that they can be edited directly without re-installations
- aims to be very simple and compact (compared to [litex-buildenv](https://github.com/timvideos/litex-buildenv))

#### How to use:
0. Clone this repository **recursively**.
1. Start with `make prepare && make gateware`. 
2. Edit the SoC configuration and code in `src/`. 
3. Tweak `litex` cores in `lib/`.
4. Look at the targets in the `Makefile` and adjust them as necessary.

#### Dependencies:
 - make, wget, tar
 - Python 3
 - pipenv
 - Vivado
 - optional: yosys, verilator, other litex-related tools
