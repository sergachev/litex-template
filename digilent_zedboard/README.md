### A complete LiteX implementation workflow for Zynq-7000

Features:
 - LiteX BIOS running on Cortex-A9 Arm core, talking to LiteX gateware over AXI/Wishbone
 - U-Boot with SPL enabling boot from QSPI flash or SD card

Howto:
 - look at the [top-level readme](../README.md), provide the required tools
 - build all binaries: `make -f Makefile.zedboard` from the top level
 - choose one of the boot options below and configure your board accordingly
 - option 1 - boot from SD card: format 1st partition as FAT32, copy these files to its root:
   - lib/u-boot/spl/boot.bin
   - lib/u-boot/u-boot.img
   - build/digilent_zedboard/boot.scr
   - build/digilent_zedboard/gateware/digilent_zedboard.bit **as fpga.bit**
   - build/digilent_zedboard/software/bios/bios.bin
 - option 2 - boot from QSPI flash: flash build/qspi.bin into board's memory one of these ways:
   - with `make -f Makefile.zedboard` via [zynq_flash](https://github.com/raczben/zynq_flash) (uses `xsct` from Vitis)
   - with `program_flash` - part of Vitis, needs FSBL binary
   - with U-Boot `sf` command [link](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842223/U-boot#U-boot-ProgrammingQSPIFlash)
 - option 3 - boot from JTAG

Notes:
 - there is nearly nothing specific to Zedboard in the current implementation, 
will work as is of with minimal changes on other Zynq boards
 - there are options for debugging over JTAG with either `xsct` or `openocd`+`gdb` (to be described)