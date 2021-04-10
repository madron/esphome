import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, modbus
from esphome.const import (
    CONF_ACCURACY_DECIMALS,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_ID,
    CONF_MODEL,
    CONF_UNIT_OF_MEASUREMENT,
)
from .constants import MODEL


MODELS = MODEL.keys()
SENSOR_NAMES = []
for config in MODEL.values():
    SENSOR_NAMES += config.keys()
SENSOR_NAMES = set(SENSOR_NAMES)

AUTO_LOAD = ["modbus"]

sdm_ns = cg.esphome_ns.namespace("sdm")
Sdm = sdm_ns.class_("Sdm", cg.PollingComponent, modbus.ModbusDevice)


def validate_schema(schema):
    for name, config in schema.items():
        if isinstance(config, dict):
            try:
                default_config = MODEL[schema[CONF_MODEL]][name]
            except KeyError:
                msg = "[{}] is an invalid option for [sensor.sdm] model [{}]."
                raise cv.Invalid(msg.format(name, schema[CONF_MODEL]))
            if not CONF_UNIT_OF_MEASUREMENT in config and default_config.get(CONF_UNIT_OF_MEASUREMENT, None):
                config[CONF_UNIT_OF_MEASUREMENT] = default_config[CONF_UNIT_OF_MEASUREMENT]
            if not CONF_ICON in config and default_config.get(CONF_ICON, None):
                config[CONF_ICON] = default_config[CONF_ICON]
            if not CONF_ACCURACY_DECIMALS in config and default_config.get(CONF_ACCURACY_DECIMALS, None):
                config[CONF_ACCURACY_DECIMALS] = default_config[CONF_ACCURACY_DECIMALS]
            if not CONF_DEVICE_CLASS in config and default_config.get(CONF_DEVICE_CLASS, None):
                config[CONF_DEVICE_CLASS] = default_config[CONF_DEVICE_CLASS]
    return schema


SCHEMA = {
    cv.GenerateID(): cv.declare_id(Sdm),
    cv.Required(CONF_MODEL): cv.one_of(*MODELS),
}
for sensor_name in SENSOR_NAMES:
    SCHEMA[cv.Optional(sensor_name)] = sensor.SENSOR_SCHEMA


CONFIG_SCHEMA = (
    cv.Schema(SCHEMA)
    .add_extra(validate_schema)
    .extend(cv.polling_component_schema("60s"))
    .extend(modbus.modbus_device_schema(0x01))
)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield modbus.register_modbus_device(var, config)

    for sensor_name in MODEL[config[CONF_MODEL]].keys():
        if sensor_name in config:
            print(sensor_name)
            conf = config[sensor_name]
            sens = yield sensor.new_sensor(conf)
            print(sens)
            print(type(sens))
            # cg.add(var.add_sensor(sens))
