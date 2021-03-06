import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.const import (
    CONF_ID,
    CONF_NUMBER,
    CONF_INVERTED,
    CONF_DATA_PIN,
    CONF_CLOCK_PIN,
)

DEPENDENCIES = []
MULTI_CONF = True

sn74hc595_ns = cg.esphome_ns.namespace("sn74hc595")

SN74HC595Component = sn74hc595_ns.class_("SN74HC595Component", cg.Component)
SN74HC595GPIOPin = sn74hc595_ns.class_("SN74HC595GPIOPin", cg.GPIOPin)

CONF_SN74HC595 = "sn74hc595"
CONF_LATCH_PIN = "latch_pin"
CONF_OE_PIN = "oe_pin"
CONF_SR_COUNT = "sr_count"
CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(SN74HC595Component),
        cv.Required(CONF_DATA_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_CLOCK_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_LATCH_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_OE_PIN): pins.gpio_output_pin_schema,
        cv.Optional(CONF_SR_COUNT, default=1): cv.int_range(1, 4),
    }
).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    data_pin = yield cg.gpio_pin_expression(config[CONF_DATA_PIN])
    cg.add(var.set_data_pin(data_pin))
    clock_pin = yield cg.gpio_pin_expression(config[CONF_CLOCK_PIN])
    cg.add(var.set_clock_pin(clock_pin))
    latch_pin = yield cg.gpio_pin_expression(config[CONF_LATCH_PIN])
    cg.add(var.set_latch_pin(latch_pin))
    if CONF_OE_PIN in config:
        oe_pin = yield cg.gpio_pin_expression(config[CONF_OE_PIN])
        cg.add(var.set_oe_pin(oe_pin))
    cg.add(var.set_sr_count(config[CONF_SR_COUNT]))


SN74HC595_OUTPUT_PIN_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_SN74HC595): cv.use_id(SN74HC595Component),
        cv.Required(CONF_NUMBER): cv.int_,
        cv.Optional(CONF_INVERTED, default=False): cv.boolean,
    }
)
SN74HC595_INPUT_PIN_SCHEMA = cv.Schema({})


@pins.PIN_SCHEMA_REGISTRY.register(
    CONF_SN74HC595, (SN74HC595_OUTPUT_PIN_SCHEMA, SN74HC595_INPUT_PIN_SCHEMA)
)
def sn74hc595_pin_to_code(config):
    parent = yield cg.get_variable(config[CONF_SN74HC595])
    yield SN74HC595GPIOPin.new(parent, config[CONF_NUMBER], config[CONF_INVERTED])
