# example: xsct ps7_boot.tcl build/digilent_zedboard/gateware/digilent_zedboard.gen/sources_1/ip/Zynq/ps7_init.tcl build/digilent_zedboard/software/bios/bios.elf build/digilent_zedboard/gateware/digilent_zedboard.bit

connect
targets -set -filter {name =~ "ARM*#0"}
rst
stop
source [lindex $argv 0]
ps7_init
ps7_post_config

dow [lindex $argv 1]
con
fpga [lindex $argv 2]
