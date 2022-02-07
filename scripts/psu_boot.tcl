connect

targets -set -nocase -filter {name =~ "PSU"}
stop
mwr 0xffca0010 0x0
mwr 0xff5e0200 0x0100
rst -system

targets -set -nocase -filter {name =~ "PSU"}
mwr 0xFFCA0038 0x1FF

target -set -filter {name =~ "MicroBlaze PMU"}
dow [lindex $argv 0]
con

source [lindex $argv 1]
targets -set -nocase -filter {name =~ "PSU"}
psu_init
after 500
psu_post_config
after 500
psu_ps_pl_reset_config
after 500
psu_ps_pl_isolation_removal
after 500
mwr 0xffff0000 0x14000000
mwr 0xFD1A0104 0x380E

targets -set -filter {name =~ "Cortex-A53 #0"}
dow [lindex $argv 2]
fpga [lindex $argv 3]
con
