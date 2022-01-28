include ../include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

TARGET   = firmware
OBJECTS  = isr.o main.o
CFLAGS += -Wall -Wextra -Wno-strict-prototypes

all: $(TARGET).bin

# pull in dependency info for *existing* .o files
-include $(OBJECTS:.o=.d)

$(TARGET).elf: $(OBJECTS) crt0.o
	$(CC) $(LDFLAGS) \
		-T $(FIRMWARE_DIRECTORY)/linker.ld \
		-N -o $@ \
		crt0.o \
		$(OBJECTS) \
		-Wl,--whole-archive \
		-Wl,--gc-sections \
		-Wl,-Map,$@.map \
		-L ../libbase -L ../libc -lbase -lc
	chmod -x $@

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@
	chmod -x $@
ifeq ($(CPUENDIANNESS),little)
	$(PYTHON) -m litex.soc.software.mkmscimg $@ -o $(TARGET).fbi --little -f
else
	$(PYTHON) -m litex.soc.software.mkmscimg $@ -o $(TARGET).fbi -f
endif

VPATH = $(FIRMWARE_DIRECTORY):$(CPU_DIRECTORY)

%.o: $(FIRMWARE_DIRECTORY)/%.c
	$(compile)

%.o: %.S
	$(assemble)

clean:
	$(RM) $(OBJECTS) $(OBJECTS:.o=.d) $(TARGET).elf $(TARGET).bin $(TARGET).lst .*~ *~

.PHONY: all clean
