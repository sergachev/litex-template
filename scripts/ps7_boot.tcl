connect
targets -set -filter {name =~ "ARM*#0"}
rst
stop
source [lindex $argv 0]
ps7_init
ps7_post_config

dow [lindex $argv 1]
fpga [lindex $argv 2]
con
