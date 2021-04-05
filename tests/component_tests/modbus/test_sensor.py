"""Tests for the modbus sensor."""

import unittest
import pytest
import esphome.config_validation as cv
from esphome.components.modbus.sensor import ADDRESS_SCHEMA, CONFIG_SCHEMA
from esphome.core import CORE


def test_setup_default(generate_main):
    main_cpp = generate_main("tests/component_tests/modbus/test_sensor_default.yaml")
    assert "modbus_modbussensor->set_update_interval(60000);" in main_cpp
    assert "modbus_modbus->set_uart_parent(uart_uartcomponent);" in main_cpp
    assert "modbus_modbussensor->set_parent(modbus_modbus);" in main_cpp
    assert "modbus_modbussensor->set_address(0x01);" in main_cpp
    assert "modbus_modbus->register_device(modbus_modbussensor);" in main_cpp
    assert "modbus_modbus->set_uart_parent(uart_uartcomponent);" in main_cpp


def test_setup_custom(generate_main):
    main_cpp = generate_main("tests/component_tests/modbus/test_sensor_custom.yaml")
    assert "modbus_modbussensor->set_update_interval(500);" in main_cpp
    assert "my_modbus->set_uart_parent(my_uart);" in main_cpp
    assert "modbus_modbussensor->set_parent(my_modbus);" in main_cpp
    assert "modbus_modbussensor->set_address(0x10);" in main_cpp
    assert "my_modbus->register_device(modbus_modbussensor);" in main_cpp


class ModbusSensorTest(unittest.TestCase):
    def setUp(self):
        CORE.raw_config = dict()
        self.config = dict(addresses=[dict(sensor=dict(name="sensor"))])

    def test_default(self):
        validated = CONFIG_SCHEMA(self.config)
        assert validated["modbus_id"].is_declaration == False
        assert validated["modbus_id"].is_manual == False
        assert validated["device_id"] == 1
        assert validated["function"] == "read_input_registers"

    def test_modbus_id(self):
        self.config['modbus_id'] = "my_modbus"
        validated = CONFIG_SCHEMA(self.config)
        assert validated["modbus_id"].is_declaration == False
        assert validated["modbus_id"].is_manual == True

    def test_device_update_interval(self):
        self.config['update_interval'] = "5000ms"
        validated = CONFIG_SCHEMA(self.config)
        assert validated["update_interval"].milliseconds == 5000

    def test_device_id_default(self):
        self.config['device_id'] = 9
        validated = CONFIG_SCHEMA(self.config)
        assert validated["device_id"] == 9

    def test_device_id_too_low(self):
        self.config['device_id'] = 0
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert excinfo.value.msg == "value must be at least 1"
        assert excinfo.value.path == ["device_id"]

    def test_device_id_too_high(self):
        self.config['device_id'] = 248
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert excinfo.value.msg == "value must be at most 247"
        assert excinfo.value.path == ["device_id"]

    def test_function(self):
        self.config['function'] = "read_coils"
        validated = CONFIG_SCHEMA(self.config)
        assert validated["function"] == "read_coils"

    def test_device_function_ko(self):
        self.config['function'] = "unsupported_function"
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert (
            excinfo.value.msg
            == "Unknown value 'unsupported_function', valid options are 'read_coils', 'read_discrete_inputs', 'read_holding_registers', 'read_input_registers'."
        )
        assert excinfo.value.path == ["function"]

    def test_duplicate_address_1(self):
        self.config['addresses'] = [
            dict(address=1, sensor=dict(name="sensor")),
            dict(address=1, sensor=dict(name="sensor")),
        ]
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert excinfo.value.msg == "Duplicate address: 0x01."
        assert excinfo.value.path == ["addresses"]

    def test_duplicate_address_2(self):
        self.config['addresses'] = [
            dict(address=8, sensor=dict(name="sensor")),
            dict(address=5, sensor=dict(name="sensor")),
            dict(address=8, sensor=dict(name="sensor")),
            dict(address=5, sensor=dict(name="sensor")),
            dict(address=8, sensor=dict(name="sensor")),
            dict(address=1, sensor=dict(name="sensor")),
        ]
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert excinfo.value.msg == "Duplicate addresses: 0x05, 0x08."
        assert excinfo.value.path == ["addresses"]

    def test_addresses_response_size_ok(self):
        self.config['addresses'] = [
            dict(address=2, sensor=dict(name="sensor")),
            dict(address=252, address_type="16bit", sensor=dict(name="sensor")),
        ]
        CONFIG_SCHEMA(self.config)

    def test_addresses_response_size_too_big(self):
        self.config['addresses'] = [
            dict(address=252, address_type="32bit", sensor=dict(name="sensor")),
            dict(address=2, sensor=dict(name="sensor")),
        ]
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            CONFIG_SCHEMA(self.config)
        assert (
            excinfo.value.msg
            == "Requested data from address 0x02 to 0xFC is 254 bytes long: The maximum allowed is 253."
        )
        assert excinfo.value.path == ["addresses"]


class ModbusSensorAddressTest(unittest.TestCase):
    def setUp(self):
        CORE.raw_config = dict()
        self.config = dict(sensor=dict(name="sensor"))

    def test_address_default(self):
        validated = ADDRESS_SCHEMA(self.config)
        assert validated["address"] == 0

    def test_address_custom(self):
        self.config["address"] = 0x09
        validated = ADDRESS_SCHEMA(self.config)
        assert validated["address"] == 9

    def test_address_type_default(self):
        validated = ADDRESS_SCHEMA(self.config)
        assert validated["address_type"] == "16bit"

    def test_address_type_custom(self):
        self.config["address_type"] = "32bit"
        validated = ADDRESS_SCHEMA(self.config)
        assert validated["address_type"] == "32bit"

    def test_address_type_ko(self):
        self.config["address_type"] = "unsupported_address_type"
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            ADDRESS_SCHEMA(self.config)
        assert (
            excinfo.value.msg
            == "Unknown value 'unsupported_address_type', valid options are '16bit', '32bit'."
        )
        assert excinfo.value.path == ["address_type"]

    def test_sensor(self):
        config = dict(sensor=dict(name="sensor"))
        validated = ADDRESS_SCHEMA(config)
        assert validated["sensor"]["name"] == "sensor"

    def test_sensors(self):
        config = dict(sensors=[dict(name="sensor")])
        validated = ADDRESS_SCHEMA(config)
        assert validated["sensors"][0]["name"] == "sensor"

    def test_binary_sensors(self):
        config = dict(binary_sensors=[dict(name="sensor")])
        validated = ADDRESS_SCHEMA(config)
        assert validated["binary_sensors"][0]["name"] == "sensor"

    def test_no_sensor(self):
        config = dict()
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            ADDRESS_SCHEMA(config)
        assert (
            excinfo.value.msg
            == "Must contain exactly one of sensor, sensors, binary_sensors."
        )
        assert excinfo.value.path == []

    def test_too_many_sensors(self):
        config = dict(
            sensor=dict(name="sensor"),
            sensors=[dict(name="sensor")],
            binary_sensors=[dict(name="sensor")],
        )
        with pytest.raises(cv.MultipleInvalid) as excinfo:
            ADDRESS_SCHEMA(config)
        assert (
            excinfo.value.msg
            == "Cannot specify more than one of sensor, sensors, binary_sensors."
        )
        assert excinfo.value.path == []

