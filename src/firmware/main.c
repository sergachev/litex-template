#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>
#include "main.h"


static void busy_wait_us(unsigned int ds) {
        timer0_en_write(0);
        timer0_reload_write(0);
        timer0_load_write(CONFIG_CLOCK_FREQUENCY / 1000000 * ds);
        timer0_en_write(1);
        timer0_update_value_write(1);
        while (timer0_value_read())
                timer0_update_value_write(1);
}


int main(void) {
    int i = 0;
    irq_setmask(0);
    irq_setie(1);
    uart_init();

    while (1) {
        gpio_led_out_write(i++);
        busy_wait_us(1000000);
    }

    return 0;
}
