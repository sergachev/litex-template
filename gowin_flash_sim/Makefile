.DEFAULT_GOAL := sim
.PHONY: sim gtkwave clean

build:
	mkdir -p $@

build/prim_sim.v: build
	patch -o $@ $(GOWIN_SDK)/IDE/simlib/gw1n/prim_sim.v prim_sim.v.patch

sim: build/prim_sim.v
	poetry run python sim_flash.py

gtkwave:
	gtkwave build/sim/gateware/sim.vcd &

clean:
	rm -rf build
