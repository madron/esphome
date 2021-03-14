"""Tests for the modbus sensor."""

import pytest
import esphome.config_validation as cv
from esphome.components.modbus.sensor import ADDRESS_SCHEMA, CONFIG_SCHEMA


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
    config = dict(addresses=[dict()])
    validated = CONFIG_SCHEMA(config)
    assert validated["modbus_id"].is_declaration == False
    assert validated["modbus_id"].is_manual == False
    assert validated["device_id"] == 1
    assert validated["function"] == "read_input_registers"


def test_modbus_id():
    config = dict(modbus_id="my_modbus", addresses=[dict()])
    validated = CONFIG_SCHEMA(config)
    assert validated["modbus_id"].is_declaration == False
    assert validated["modbus_id"].is_manual == True


def test_device_update_interval():
    config = dict(update_interval="5000ms", addresses=[dict()])
    validated = CONFIG_SCHEMA(config)
    assert validated["update_interval"].milliseconds == 5000


def test_device_id_default():
    config = dict(device_id=9, addresses=[dict()])
    validated = CONFIG_SCHEMA(config)
    assert validated["device_id"] == 9


def test_device_id_too_low():
    config = dict(device_id=0, addresses=[dict()])
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "value must be at least 1"
    assert excinfo.value.path == ["device_id"]


def test_device_id_too_high():
    config = dict(device_id=248, addresses=[dict()])
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "value must be at most 247"
    assert excinfo.value.path == ["device_id"]


def test_function():
    config = dict(function="read_coils", addresses=[dict()])
    validated = CONFIG_SCHEMA(config)
    assert validated["function"] == "read_coils"


def test_device_function_ko():
    config = dict(function="unsupported_function", addresses=[dict()])
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert (
        excinfo.value.msg
        == "Unknown value 'unsupported_function', valid options are 'read_coils', 'read_discrete_inputs', 'read_holding_registers', 'read_input_registers'."
    )
    assert excinfo.value.path == ["function"]


def test_duplicate_address_1():
    config = dict(
        addresses=[
            dict(address=1),
            dict(address=1),
        ]
    )
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "Duplicate address: 0x01."
    assert excinfo.value.path == ["addresses"]


def test_duplicate_address_2():
    config = dict(
        addresses=[
            dict(address=1),
            dict(address=5),
            dict(address=5),
            dict(address=8),
            dict(address=8),
            dict(address=8),
        ]
    )
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        CONFIG_SCHEMA(config)
    assert excinfo.value.msg == "Duplicate addresses: 0x05, 0x08."
    assert excinfo.value.path == ["addresses"]


def test_address_default():
    config = dict()
    validated = ADDRESS_SCHEMA(config)
    assert validated["address"] == 0


def test_address_custom():
    config = dict(address=0x09)
    validated = ADDRESS_SCHEMA(config)
    assert validated["address"] == 9


def test_address_type_default():
    config = dict()
    validated = ADDRESS_SCHEMA(config)
    assert validated["address_type"] == "16bit"


def test_address_type_custom():
    config = dict(address_type="32bit")
    validated = ADDRESS_SCHEMA(config)
    assert validated["address_type"] == "32bit"


def test_address_type_ko():
    config = dict(address_type="unsupported_address_type")
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        ADDRESS_SCHEMA(config)
    assert (
        excinfo.value.msg
        == "Unknown value 'unsupported_address_type', valid options are '16bit', '32bit'."
    )
    assert excinfo.value.path == ["address_type"]
