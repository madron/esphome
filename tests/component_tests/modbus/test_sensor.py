"""Tests for the modbus sensor."""

import pytest
import esphome.config_validation as cv
from esphome.components.modbus.sensor import CONFIG_SCHEMA


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


def test_default():
    config = dict()
    validated = CONFIG_SCHEMA(config)
    assert validated["modbus_id"].is_declaration == False
    assert validated["modbus_id"].is_manual == False
    assert validated["device_id"] == 1
    assert validated["function"] == "read_input_registers"


def test_modbus_id():
    config = dict(modbus_id="my_modbus")
    validated = CONFIG_SCHEMA(config)
    assert validated["modbus_id"].is_declaration == False
    assert validated["modbus_id"].is_manual == True


def test_device_update_interval():
    config = dict(update_interval="5000ms")
    validated = CONFIG_SCHEMA(config)
    assert validated["update_interval"].milliseconds == 5000


def test_device_id_default():
    config = dict(device_id=9)
    validated = CONFIG_SCHEMA(config)
    assert validated["device_id"] == 9


def test_device_id_too_low():
    config = dict(device_id=0)
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "value must be at least 1"
    assert excinfo.value.path == ["device_id"]


def test_device_id_too_high():
    config = dict(device_id=248)
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "value must be at most 247"
    assert excinfo.value.path == ["device_id"]


def test_function():
    config = dict(function="read_coils")
    validated = CONFIG_SCHEMA(config)
    assert validated["function"] == "read_coils"


def test_device_function_ko():
    config = dict(function="unsupported_function")
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert (
        excinfo.value.msg
        == "Unknown value 'unsupported_function', valid options are 'read_coils', 'read_discrete_inputs', 'read_holding_registers', 'read_input_registers'."
    )
    assert excinfo.value.path == ["function"]
