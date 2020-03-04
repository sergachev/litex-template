.DEFAULT_GOAL := firmware

serial_port = /dev/ttyUSB0
soc_dir = soc_basesoc_platform1
riscv_tools = riscv64-unknown-elf-gcc-8.3.0-2019.08.0-x86_64-linux-ubuntu14
export PATH := $(PWD)/$(riscv_tools)/bin:$(PATH)

prepare:
		wget -nc https://static.dev.sifive.com/dev-tools/$(riscv_tools).tar.gz
		tar xf $(riscv_tools).tar.gz --skip-old-files
		pipenv install --dev

clean:
		rm -rf soc_*_platform*

update:
		git submodule update --remote

firmware:
		pipenv run python src/main.py

gateware:
		pipenv run python src/main.py --build_gateware && \
		grep -i "All user specified timing constraints are met" $(soc_dir)/gateware/vivado.log

boot:
		pipenv run litex_term --serial-boot --kernel $(soc_dir)/software/firmware/firmware.bin $(serial_port)

sim_build:
		pipenv run python src/main.py --sim

sim:	sim_build
		pipenv run python src/main.py --sim --run
