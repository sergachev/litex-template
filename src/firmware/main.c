#include <stdio.h>
#include <irq.h>
#include <uart.h>
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


#define SPI_CTRL_START 0x1U
#define SPI_CTRL_LENGTH (1U<<8U)
#define SPI_STATUS_DONE 0x1U

#define SPI_MAX_BYTES 5


int8_t spi_read(uint8_t reg_addr, uint8_t *data, uint16_t len)
{
    spi_master_mosi_write((uint64_t) reg_addr << ((SPI_MAX_BYTES - 1) * 8U));
    spi_master_control_write(
            SPI_CTRL_START |
            (8U * 1 * SPI_CTRL_LENGTH));
    busy_wait_us(1);
    while ((spi_master_status_read() & SPI_STATUS_DONE) == 0)
        busy_wait_us(1);

    uint8_t chunk_size;
    while (len > 0) {
        if (len > SPI_MAX_BYTES)
            chunk_size = SPI_MAX_BYTES;
        else
            chunk_size = len;
        len -= chunk_size;

        spi_master_control_write(
                SPI_CTRL_START |
                (8U * chunk_size * SPI_CTRL_LENGTH));
        busy_wait_us(1);
        while ((spi_master_status_read() & SPI_STATUS_DONE) == 0)
            busy_wait_us(1);
        unsigned long long int rx = spi_master_miso_read();
        for (int i = 0; i < chunk_size; i++)
            data[i] = (rx >> ((chunk_size - 1 - i) * 8U)) & 0xFFU;
        data += chunk_size;
    }

    return 0;
}


int main(void) {
    int i = 0;
    irq_setmask(0);
    irq_setie(1);
    uart_init();

    puts("firmware started");
    uint8_t x;
    spi_master_loopback_write(1);
    spi_read(0x59, (uint8_t *) &x, 1);
    printf("%x", x);

    while (1) {
        gpio_led_out_write(i++);
        busy_wait_us(1000000);
    }

    return 0;
}
