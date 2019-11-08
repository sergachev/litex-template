cmake_minimum_required(VERSION 3.1)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_C_COMPILER_WORKS 1)

project(firmware VERSION 1.0
        DESCRIPTION "Firmware for the SoC CPU"
        LANGUAGES C)

include_directories(SYSTEM ../../soc_basesoc_platform1/software/include)
include_directories(SYSTEM ../../lib/litex/litex/soc/software/include)
include_directories(SYSTEM ../../lib/litex/litex/soc/software/include/base)

add_executable(firmware
        main.c
        isr.c
        ../../soc_basesoc_platform1/software/include/generated/csr.h
)
