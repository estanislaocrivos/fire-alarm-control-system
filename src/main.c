#include "main.h"

/* ========================================================================== */

typedef void (*task_fn_t)(void);

#define MAX_TASK_COUNT 5

struct task
{
    task_fn_t task_fn;
    uint16_t  period_ms;
    uint16_t  elapsed_ms;
    bool      ready;
};

static struct task   task_list[MAX_TASK_COUNT];
static uint8_t       task_count = 0;
static volatile bool tick_flag  = false;

void scheduler_dispatcher(void)
{
    for (uint8_t i = 0; i < task_count; i++)
    {
        if (task_list[i].ready)
        {
            task_list[i].ready = false;
            task_list[i].task_fn();
        }
    }
}

bool scheduler_add_task(task_fn_t task_fn, uint16_t period_ms)
{
    if (task_count >= MAX_TASK_COUNT)
    {
        return false;
    }
    task_list[task_count].task_fn    = task_fn;
    task_list[task_count].period_ms  = period_ms;
    task_list[task_count].elapsed_ms = 0;
    task_list[task_count].ready      = false;
    task_count += 1;
    return true;
}

/* ========================================================================== */

void tmr1_init(void)
{
    TCCR1A = 0;
    TCCR1B = (1 << WGM12) | (1 << CS11) | (1 << CS10);  // CTC mode, Prescaler
                                                        // 64
    OCR1A = 249;              // (16 MHz / (64 * 1000 Hz)) - 1 = 249
    TIMSK1 |= (1 << OCIE1A);  // Habilitar interrupción por comparación
}

ISR(TIMER1_COMPA_vect)
{
    for (uint8_t i = 0; i < task_count; i++)
    {
        task_list[i].elapsed_ms += 1;
        if (task_list[i].elapsed_ms >= task_list[i].period_ms)
        {
            task_list[i].ready      = true;
            task_list[i].elapsed_ms = 0;
        }
    }
    tick_flag = true;
}

/* ========================================================================== */

static struct gpio led_1
    = {.ops             = &PLATFORM_GPIO_OPS,
       .id              = GPIO_B4_ID,
       .type            = GPIO_DIGITAL,
       .direction       = GPIO_OUTPUT,
       .was_initialized = false};

static struct gpio led_2
    = {.ops             = &PLATFORM_GPIO_OPS,
       .id              = GPIO_B5_ID,
       .type            = GPIO_DIGITAL,
       .direction       = GPIO_OUTPUT,
       .was_initialized = false};

void task_led_1(void)
{
    led_1.ops->toggle(&led_1);
}

void task_led_2(void)
{
    led_2.ops->toggle(&led_2);
}

int main(void)
{
    tmr1_init();

    led_1.ops->initialize(&led_1);
    led_2.ops->initialize(&led_2);

    scheduler_add_task(task_led_1, 100);
    scheduler_add_task(task_led_2, 200);

    sei();

    while (1)
    {
        if (tick_flag)
        {
            tick_flag = false;
            scheduler_dispatcher();
        }
    }
}

/* ========================================================================== */
