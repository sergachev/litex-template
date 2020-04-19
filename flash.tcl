set file_name [lindex $argv 0]
open_hw_manager
connect_hw_server
open_hw_target
# TODO: the max frequency depends on the programmer model, 12 M is for the xilinx platform cable
# set_property PARAM.FREQUENCY 12000000 [get_hw_targets]
refresh_hw_target
set dev [lindex [get_hw_devices -of_objects [current_hw_target]] 0]
current_hw_device $dev
refresh_hw_device -update_hw_probes false $dev
create_hw_cfgmem -hw_device $dev [lindex [get_cfgmem_parts {mt25ql128-spi-x1_x2_x4}] 0]
set_property PROGRAM.BLANK_CHECK  0 [get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.ERASE  1 [get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.CFG_PROGRAM  1 [get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.VERIFY  1 [get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.CHECKSUM  0 [get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.ADDRESS_RANGE  {use_file} [ get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.FILES [list $file_name] [ get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.PRM_FILE {} [ get_property PROGRAM.HW_CFGMEM $dev]
set_property PROGRAM.UNUSED_PIN_TERMINATION {pull-none} [ get_property PROGRAM.HW_CFGMEM $dev]
create_hw_bitstream -hw_device $dev [get_property PROGRAM.HW_CFGMEM_BITFILE $dev]
program_hw_devices $dev
refresh_hw_device $dev
program_hw_cfgmem -hw_cfgmem [ get_property PROGRAM.HW_CFGMEM $dev]
boot_hw_device -disable_done_check -quiet $dev
