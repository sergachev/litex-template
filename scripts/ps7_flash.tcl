source [lindex $argv 0]
source lib/zynq_flash/flash_writer.tcl
set flash_writer_elf lib/zynq_flash/zed_bin/flash_writer.elf
connect
targets -set -filter {name =~ "ARM*#0"}
flash_image [lindex $argv 1]