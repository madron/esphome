"""Tests for the modbus component."""

import esphome.config_validation as cv
from esphome import core
from esphome.components.modbus import CONFIG_SCHEMA


def test_setup_default(generate_main):
    generate_main("tests/component_tests/modbus/test_component_default.yaml")


def test_setup_custom(generate_main):
    main_cpp = generate_main("tests/component_tests/modbus/test_component_custom.yaml")
    assert "my_uart->set_baud_rate(9600);" in main_cpp
    assert "my_uart->set_tx_pin(10);" in main_cpp
    assert "my_uart->set_rx_pin(12);" in main_cpp
    assert "my_modbus->set_uart_parent(my_uart);" in main_cpp
    assert "my_modbus->set_setup_priority(12.3f);" in main_cpp


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
