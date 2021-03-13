"""Tests for the modbus component."""

import esphome.config_validation as cv
from esphome import core
from esphome.components.modbus import CONFIG_SCHEMA


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
