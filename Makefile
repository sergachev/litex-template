.DEFAULT_GOAL := firmware

soc_dir = soc_basesoc_platform1
riscv_tools = riscv64-unknown-elf-gcc-8.3.0-2019.08.0-x86_64-linux-ubuntu14
export PATH := $(PWD)/$(riscv_tools)/bin:$(PATH)

prepare:
		wget -nc https://static.dev.sifive.com/dev-tools/$(riscv_tools).tar.gz
		tar xf $(riscv_tools).tar.gz --skip-old-files
		pipenv install --dev

clean:
		rm -r $(soc_dir)

update:
		cd lib && cp -f litex/litex_setup.py . && python3 litex_setup.py update

firmware:
		pipenv run python src/main.py

gateware:
		pipenv run python src/main.py --build_gateware

boot:
		pipenv run litex_term --serial-boot --kernel $(soc_dir)/software/firmware/firmware.fbi /dev/ttyUSB0
