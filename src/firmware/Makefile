include ../include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

TARGET   = firmware
OBJECTS  = isr.o main.o
CFLAGS += -Wall -Wextra

all: $(TARGET).bin

# pull in dependency info for *existing* .o files
-include $(OBJECTS:.o=.d)

$(TARGET).elf: $(OBJECTS)
	$(LD) $(LDFLAGS) \
		-T $(FIRMWARE_DIRECTORY)/linker.ld \
		-N -o $@ \
		 ../libbase/crt0-$(CPU)-ctr.o \
		$(OBJECTS) \
		-L../libbase \
		-L../libcompiler_rt \
		-lbase-nofloat -lcompiler_rt
	chmod -x $@

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@
	chmod -x $@
ifeq ($(CPUENDIANNESS),little)
	$(PYTHON) -m litex.soc.software.mkmscimg $@ -o $(TARGET).fbi --little -f
else
	$(PYTHON) -m litex.soc.software.mkmscimg $@ -o $(TARGET).fbi -f
endif

%.o: $(FIRMWARE_DIRECTORY)/%.c
	$(compile)

%.o: %.S
	$(assemble)

clean:
	$(RM) $(OBJECTS) $(OBJECTS:.o=.d) $(TARGET).elf $(TARGET).bin $(TARGET).lst .*~ *~

.PHONY: all clean
