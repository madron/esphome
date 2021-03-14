import collections
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_ADDRESS
from esphome.components import modbus
from esphome.core import coroutine

AUTO_LOAD = ["modbus"]

CONF_MODBUS_ID = "modbus_id"
CONF_DEVICE_ID = "device_id"
CONF_FUNCTION = "function"
CONF_ADDRESSES = "addresses"
CONF_ADDRESS_TYPE = "address_type"

FunctionCode = modbus.modbus_ns.enum("FunctionCode")
READ_FUNCTION = {
    "read_coils": FunctionCode.READ_COILS,
    "read_discrete_inputs": FunctionCode.READ_DISCRETE_INPUTS,
    "read_holding_registers": FunctionCode.READ_HOLDING_REGISTERS,
    "read_input_registers": FunctionCode.READ_INPUT_REGISTERS,
}
WRITE_FUNCTION = {
    "write_single_coil": FunctionCode.WRITE_SINGLE_COIL,
    "write_single_register": FunctionCode.WRITE_SINGLE_REGISTER,
    "write_multiple_registers": FunctionCode.WRITE_MULTIPLE_REGISTERS,
}
AddressType = modbus.modbus_ns.enum("AddressTypeCode")
ADRESS_TYPE = {
    "16bit": AddressType.ADDRESS_TYPE_16BIT,
    "32bit": AddressType.ADDRESS_TYPE_32BIT,
}

ModbusSensor = modbus.modbus_ns.class_(
    "ModbusSensor", cg.PollingComponent, modbus.ModbusDevice
)


def validate_addresses(value):
    addresses = [x[CONF_ADDRESS] for x in value]
    duplicate_addresses = [
        str(address)
        for address, count in collections.Counter(addresses).items()
        if count > 1
    ]
    if duplicate_addresses:
        if len(duplicate_addresses) == 1:
            msg = "Duplicate address"
        else:
            msg = "Duplicate addresses"
        raise cv.Invalid("{}: {}.".format(msg, ", ".join(duplicate_addresses)))
    return value


ADDRESS_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.Optional(CONF_ADDRESS, default=0): cv.hex_int_range(min=0, max=9999),
            cv.Optional(CONF_ADDRESS_TYPE, default="16bit"): cv.enum(ADRESS_TYPE),
        }
    ),
)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ModbusSensor),
            cv.GenerateID(CONF_MODBUS_ID): cv.use_id(modbus.Modbus),
            cv.Optional(CONF_DEVICE_ID, default=1): cv.hex_int_range(min=1, max=247),
            cv.Optional(CONF_FUNCTION, default="read_input_registers"): cv.enum(
                READ_FUNCTION
            ),
            cv.Required(CONF_ADDRESSES): cv.All(
                cv.ensure_list(ADDRESS_SCHEMA),
                cv.Length(min=1),
                validate_addresses,
            ),
        }
    ).extend(cv.polling_component_schema("60s")),
)


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
