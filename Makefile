serial_port = /dev/ttyUSB0
soc_dir = build
soc = poetry run python src/main.py

.DEFAULT_GOAL := $(soc_dir)/software/firmware/firmware.bin
.PHONY: clean $(soc_dir)/software/firmware/firmware.bin

.venv:
	poetry install

clean:
	rm -rf build

$(soc_dir)/software/firmware/firmware.bin: .venv
	$(soc)

gateware: .venv
	poetry run /usr/bin/time -f "%E" python src/main.py --build_gateware && \
	grep -i "All user specified timing constraints are met" $(soc_dir)/gateware/vivado.log; notify-send "done"

boot: $(soc_dir)/software/firmware/firmware.bin
	poetry run litex_term --serial-boot --kernel $< $(serial_port)

term:
	poetry run litex_term $(serial_port)

sim_build: .venv
	$(soc) --sim

sim: sim_build
	$(soc) --sim --run
