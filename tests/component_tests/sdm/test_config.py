"""Tests for the sdm component config."""

import unittest
import esphome.config_validation as cv
from esphome.components.sdm.sensor import CONFIG_SCHEMA
from esphome.core import CORE


class ModbusSensorTest(unittest.TestCase):
    def setUp(self):
        CORE.raw_config = dict()

    def test_empty(self):
        config = dict()
        with self.assertRaises(cv.MultipleInvalid) as cm:
            CONFIG_SCHEMA(config)
        self.assertEqual(cm.exception.msg, "required key not provided")
        self.assertEqual(cm.exception.path, ["model"])

    def test_minimal(self):
        config = dict(model="sdm120m")
        validated = CONFIG_SCHEMA(config)
        self.assertTrue(validated["id"].is_declaration)
        self.assertFalse(validated["id"].is_manual)
        self.assertFalse(validated["modbus_id"].is_declaration)
        self.assertFalse(validated["modbus_id"].is_manual)
        self.assertEqual(validated["address"], 1)
        self.assertEqual(validated["update_interval"].seconds, 60)
        self.assertEqual(validated["model"], "sdm120m")

    def test_manual_id(self):
        config = dict(model="sdm120m", id="mysdm")
        validated = CONFIG_SCHEMA(config)
        self.assertTrue(validated["id"].is_declaration)
        self.assertTrue(validated["id"].is_manual)

    def test_modbus_id(self):
        config = dict(model="sdm120m", modbus_id="my_modbus")
        validated = CONFIG_SCHEMA(config)
        self.assertFalse(validated["modbus_id"].is_declaration)
        self.assertTrue(validated["modbus_id"].is_manual)

    def test_setup_priority(self):
        config = dict(model="sdm120m", setup_priority=99.9)
        validated = CONFIG_SCHEMA(config)
        self.assertEqual(validated["setup_priority"], 99.9)

    def test_address(self):
        config = dict(model="sdm120m", address=9)
        validated = CONFIG_SCHEMA(config)
        self.assertEqual(validated["address"], 9)

    def test_unsupported_model(self):
        config = dict(model="unsupported")
        with self.assertRaises(cv.MultipleInvalid) as cm:
            CONFIG_SCHEMA(config)
        self.assertEqual(
            cm.exception.msg,
            "Unknown value 'unsupported', valid options are 'sdm120m'.",
        )
        self.assertEqual(cm.exception.path, ["model"])

    def test_sensor_voltage(self):
        config = dict(model="sdm120m", voltage=dict(name="voltage"))
        validated = CONFIG_SCHEMA(config)
        self.assertEqual(validated["voltage"]["name"], "voltage")
        self.assertEqual(validated["voltage"]["unit_of_measurement"], "V")
        self.assertEqual(validated["voltage"]["accuracy_decimals"], 1)
        self.assertEqual(validated["voltage"]["device_class"], "voltage")

    def test_unsupported_sensor(self):
        config = dict(model="sdm120m", unsupported=dict(name="unsupported"))
        with self.assertRaises(cv.MultipleInvalid) as cm:
            CONFIG_SCHEMA(config)
        self.assertEqual(cm.exception.msg, "extra keys not allowed")
        self.assertEqual(cm.exception.path, ["unsupported"])
