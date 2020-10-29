.DEFAULT_GOAL := firmware

serial_port = /dev/ttyUSB0
soc_dir = build/
top_dir = $(PWD)
riscv_tools = riscv64-unknown-elf-gcc-8.3.0-2020.04.0-x86_64-linux-ubuntu14
export PATH := $(PWD)/$(riscv_tools)/bin:$(PATH)
vivado = vivado -nojournal -nolog -mode batch

prepare:
		wget -nc https://static.dev.sifive.com/dev-tools/$(riscv_tools).tar.gz
		tar xf $(riscv_tools).tar.gz --skip-old-files
		poetry install

clean:
		rm -rf build

update:
		git submodule update --remote && poetry update

firmware:
		poetry run python src/main.py

gateware:
		poetry run python src/main.py --build_gateware && \
		grep -i "All user specified timing constraints are met" $(soc_dir)/gateware/vivado.log

boot:
		poetry run litex_term --serial-boot --kernel $(soc_dir)/software/firmware/firmware.bin $(serial_port)

term:
		poetry run litex_term $(serial_port)

sim_build:
		poetry run python src/main.py --sim

sim:	sim_build
		poetry run python src/main.py --sim --run

flash:
		cd $(soc_dir)/gateware && $(vivado) -source ../../flash.tcl -tclargs platform1.mcs
