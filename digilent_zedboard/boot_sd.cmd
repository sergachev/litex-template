dcache off

fatload mmc 0 0x100000 fpga.bit
fpga loadb 0 0x100000 0x100000

fatload mmc 0 0x100000 bios.bin
go 0x100000
