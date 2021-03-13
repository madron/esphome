import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_ADDRESS
from esphome.components import sensor, modbus
from esphome.core import coroutine

AUTO_LOAD = ["modbus"]

CONF_MODBUS_ID = "modbus_id"
CONF_DEVICE_ID = "device_id"
CONF_FUNCTION = "function"

ModbusFunctionCode = modbus.modbus_ns.enum("ModbusFunctionCode")
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

ModbusSensor = modbus.modbus_ns.class_(
    "ModbusSensor", cg.PollingComponent, modbus.ModbusDevice
)


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(ModbusSensor),
        cv.GenerateID(CONF_MODBUS_ID): cv.use_id(modbus.Modbus),
        cv.Optional(CONF_DEVICE_ID, default=1): cv.hex_int_range(min=1, max=247),
        cv.Optional(CONF_FUNCTION, default="read_input_registers"): cv.enum(
            MODBUS_READ_FUNCTION
        ),
    }
).extend(cv.polling_component_schema("60s"))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield register_modbus_device(var, config)


@coroutine
def register_modbus_device(var, config):
    parent = yield cg.get_variable(config[CONF_MODBUS_ID])
    cg.add(var.set_parent(parent))
    cg.add(var.set_address(config[CONF_DEVICE_ID]))
    cg.add(parent.register_device(var))
