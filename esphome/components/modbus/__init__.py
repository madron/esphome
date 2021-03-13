import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_ADDRESS
from esphome.core import coroutine

DEPENDENCIES = ["uart"]

modbus_ns = cg.esphome_ns.namespace("modbus")
Modbus = modbus_ns.class_("Modbus", cg.Component, uart.UARTDevice)
ModbusDevice = modbus_ns.class_("ModbusDevice")
MULTI_CONF = True

CONF_MODBUS_ID = "modbus_id"
CONF_DEVICES = "devices"
CONF_FUNCTION = "function"

ModbusFunctionCode = modbus_ns.enum("ModbusFunctionCode")
MODBUS_READ_FUNCTION = {
    "read_coils": ModbusFunctionCode.READ_COILS,
    "read_discrete_inputs": ModbusFunctionCode.READ_DISCRETE_INPUTS,
    "read_holding_registers": ModbusFunctionCode.READ_HOLDING_REGISTERS,
    "read_input_registers": ModbusFunctionCode.READ_INPUT_REGISTERS,
}
MODBUS_WRITE_FUNCTION = {
    "write_single_coil": ModbusFunctionCode.WRITE_SINGLE_COIL,
    "write_single_register": ModbusFunctionCode.WRITE_SINGLE_REGISTER,
    "write_multiple_registers": ModbusFunctionCode.WRITE_MULTIPLE_REGISTERS,
}

DEVICE_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_MODBUS_ID): cv.hex_int_range(min=1, max=247),
        cv.Optional(CONF_FUNCTION, default="read_input_registers"): cv.enum(
            MODBUS_READ_FUNCTION
        ),
    }
).extend(cv.polling_component_schema("60s"))

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Modbus),
            cv.Optional(CONF_DEVICES): cv.All(cv.ensure_list(DEVICE_SCHEMA)),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)


def to_code(config):
    cg.add_global(modbus_ns.using)
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)

    yield uart.register_uart_device(var, config)


def modbus_device_schema(default_address):
    schema = {
        cv.GenerateID(CONF_MODBUS_ID): cv.use_id(Modbus),
    }
    if default_address is None:
        schema[cv.Required(CONF_ADDRESS)] = cv.hex_uint8_t
    else:
        schema[cv.Optional(CONF_ADDRESS, default=default_address)] = cv.hex_uint8_t
    return cv.Schema(schema)


@coroutine
def register_modbus_device(var, config):
    parent = yield cg.get_variable(config[CONF_MODBUS_ID])
    cg.add(var.set_parent(parent))
    cg.add(var.set_address(config[CONF_ADDRESS]))
    cg.add(parent.register_device(var))
