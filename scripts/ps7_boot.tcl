set project_name [lindex $argv 0]
connect
targets -set -filter {name =~ "ARM*#0"}
rst
stop
source build/$project_name/gateware/$project_name.gen/sources_1/ip/Zynq/ps7_init.tcl
ps7_init
ps7_post_config

dow [lindex $argv 1]
con
fpga [lindex $argv 2]
