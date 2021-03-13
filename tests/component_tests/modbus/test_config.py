"""Tests for the modbus component."""

import pytest
import esphome.config_validation as cv
from esphome import core
from esphome.components.modbus import CONFIG_SCHEMA, DEVICE_SCHEMA
from esphome.const import CONF_SETUP_PRIORITY

ADDRESSES = [dict(address=0)]


def test_empty():
    config = dict()
    validated = CONFIG_SCHEMA(config)
    assert validated["id"].is_declaration == True
    assert validated["id"].is_manual == False
    assert validated["uart_id"].is_declaration == False
    assert validated["uart_id"].is_manual == False


def test_manual_id():
    config = dict(id="mymodbus")
    validated = CONFIG_SCHEMA(config)
    assert validated["id"].is_declaration == True
    assert validated["id"].is_manual == True


def test_uart_id():
    config = dict(uart_id="myuart")
    validated = CONFIG_SCHEMA(config)
    assert validated["uart_id"].is_declaration == False
    assert validated["uart_id"].is_manual == True


def test_setup_priority():
    config = dict(setup_priority=99.9)
    validated = CONFIG_SCHEMA(config)
    assert validated["setup_priority"] == 99.9


def test_duplicated_modbus_id():
    "Duplicated modbus ids are permitted"
    config = dict(
        devices=[
            dict(modbus_id=1, addresses=ADDRESSES),
            dict(modbus_id=1, addresses=ADDRESSES),
        ]
    )
    validated = CONFIG_SCHEMA(config)
    assert len(validated["devices"]) == 2
    assert validated["devices"][0]["modbus_id"] == 1
    assert validated["devices"][1]["modbus_id"] == 1


def test_device_ok():
    config = dict(modbus_id=1, addresses=ADDRESSES)
    validated = DEVICE_SCHEMA(config)
    assert validated["modbus_id"] == 1
    assert validated["update_interval"].seconds == 60


def test_device_missing_modbus_id():
    config = dict(addresses=ADDRESSES)
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        DEVICE_SCHEMA(config)
    assert excinfo.value.msg == "required key not provided"
    assert excinfo.value.path == ["modbus_id"]


def test_device_modbus_id_too_low():
    config = dict(modbus_id=0, addresses=ADDRESSES)
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        DEVICE_SCHEMA(config)
    assert excinfo.value.msg == "value must be at least 1"
    assert excinfo.value.path == ["modbus_id"]


def test_device_modbus_id_too_high():
    config = dict(modbus_id=248, addresses=ADDRESSES)
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        DEVICE_SCHEMA(config)
    assert excinfo.value.msg == "value must be at most 247"
    assert excinfo.value.path == ["modbus_id"]


def test_device_update_interval():
    config = dict(modbus_id=1, update_interval="5000ms", addresses=ADDRESSES)
    validated = DEVICE_SCHEMA(config)
    assert validated["modbus_id"] == 1
    assert validated["update_interval"].milliseconds == 5000


def test_device_function():
    config = dict(modbus_id=1, function="read_coils", addresses=ADDRESSES)
    validated = DEVICE_SCHEMA(config)
    assert validated["function"] == "read_coils"


def test_device_function_default():
    config = dict(modbus_id=1, addresses=ADDRESSES)
    validated = DEVICE_SCHEMA(config)
    assert validated["function"] == "read_input_registers"


def test_device_function_ko():
    config = dict(modbus_id=1, function="unsupported_function")
    with pytest.raises(cv.MultipleInvalid) as excinfo:
        DEVICE_SCHEMA(config)
    assert (
        excinfo.value.msg
        == "Unknown value 'unsupported_function', valid options are 'read_coils', 'read_discrete_inputs', 'read_holding_registers', 'read_input_registers'."
    )
    assert excinfo.value.path == ["function"]
