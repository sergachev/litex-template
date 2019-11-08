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
		git submodule update --remote

firmware:
		pipenv run python src/main.py

sim:    firmware
		pipenv run python src/main.py --run_sim
