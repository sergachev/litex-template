.DEFAULT_GOAL := firmware

serial_port = /dev/ttyUSB0
soc_dir = build/
top_dir = $(PWD)
riscv_ver = 2021.09.21
export PATH := $(PWD)/riscv/bin:$(PATH)
vivado = vivado -nojournal -nolog -mode batch

prepare:
	wget -nc -q https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/$(riscv_ver)/riscv64-elf-ubuntu-20.04-nightly-$(riscv_ver)-nightly.tar.gz
	tar xf riscv64-elf-ubuntu-20.04-nightly-$(riscv_ver)-nightly.tar.gz --skip-old-files
	poetry install

clean:
	rm -rf build

update:
	git submodule update --remote && poetry update

firmware:
	poetry run python src/main.py

gateware:
	poetry run /usr/bin/time -f "%E" python src/main.py --build_gateware && \
	grep -i "All user specified timing constraints are met" $(soc_dir)/gateware/vivado.log; notify-send "done"

boot:
	poetry run litex_term --serial-boot --kernel $(soc_dir)/software/firmware/firmware.bin $(serial_port)

term:
	poetry run litex_term $(serial_port)

sim_build:
	poetry run python src/main.py --sim

sim:	sim_build
	poetry run python src/main.py --sim --run

flash:
	cd $(soc_dir)/gateware && $(vivado) -source ../../flash.tcl -tclargs platform1.mcs; notify-send "done"
