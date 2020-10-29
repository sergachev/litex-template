#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>
#include "main.h"


int main(void) {
	int i = 0;

	irq_setmask(0);
	irq_setie(1);
	uart_init();

	while (1) {
		puts("firmware running");
		gpio_led_out_write(i ++);
		busy_wait_us(1000 * 1000);
	}

	return 0;
}
