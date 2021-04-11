"""Tests for the sdm component utils."""

import unittest
from esphome.components.sdm.sensor import CONFIG_SCHEMA
from esphome.components.sdm.utils import get_groups
from esphome.core import CORE


class GetGroupsTest(unittest.TestCase):
    def setUp(self):
        CORE.raw_config = dict()

    def test_no_sensors(self):
        config = dict(model="sdm120m")
        groups = get_groups(CONFIG_SCHEMA(config))
        self.assertEqual(groups, [])

    def test_1_group_1_sensor(self):
        config = dict(
            model="sdm120m",
            voltage=dict(name="main voltage"),
        )
        groups = get_groups(CONFIG_SCHEMA(config))
        self.assertEqual(len(groups), 1)
        group = groups[0]
        self.assertEqual(group["start_address"], 0)
        self.assertEqual(group["register_count"], 2)
        self.assertEqual(group["response_size"], 4)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "main voltage")
        self.assertEqual(register["name"], "voltage")
        self.assertEqual(register["response_index"], 0)
        self.assertEqual(register["multiply"], 1)

    def test_multiply(self):
        config = dict(
            model="sdm120m",
            total_active_energy=dict(name="total_active_energy"),
        )
        groups = get_groups(CONFIG_SCHEMA(config))
        self.assertEqual(len(groups), 1)
        group = groups[0]
        self.assertEqual(group["start_address"], 342)
        self.assertEqual(group["register_count"], 2)
        self.assertEqual(group["response_size"], 4)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "total_active_energy")
        self.assertEqual(register["name"], "total_active_energy")
        self.assertEqual(register["response_index"], 0)
        self.assertEqual(register["multiply"], 1000)

    def test_1_group_2_sensors(self):
        config = dict(
            model="sdm120m",
            current=dict(name="current"),
            power_factor=dict(name="power_factor"),
        )
        groups = get_groups(CONFIG_SCHEMA(config))
        self.assertEqual(len(groups), 1)
        group = groups[0]
        self.assertEqual(group["start_address"], 6)
        self.assertEqual(group["register_count"], 26)
        self.assertEqual(group["response_size"], 52)
        registers = group["registers"]
        self.assertEqual(len(registers), 2)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "current")
        self.assertEqual(register["response_index"], 0)
        register = registers[1]
        self.assertEqual(register["sensor"]["name"], "power_factor")
        self.assertEqual(register["response_index"], 48)

    def test_2_groups_3_sensors(self):
        config = dict(
            model="sdm120m",
            current=dict(name="current"),
            active_power=dict(name="active_power"),
            power_factor=dict(name="power_factor"),
        )
        groups = get_groups(CONFIG_SCHEMA(config), maximum_registers_count=10)
        self.assertEqual(len(groups), 2)
        group = groups[0]
        self.assertEqual(group["start_address"], 6)
        self.assertEqual(group["register_count"], 8)
        self.assertEqual(group["response_size"], 16)
        registers = group["registers"]
        self.assertEqual(len(registers), 2)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "current")
        self.assertEqual(register["response_index"], 0)
        register = registers[1]
        self.assertEqual(register["sensor"]["name"], "active_power")
        self.assertEqual(register["response_index"], 12)
        group = groups[1]
        self.assertEqual(group["start_address"], 30)
        self.assertEqual(group["register_count"], 2)
        self.assertEqual(group["response_size"], 4)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "power_factor")
        self.assertEqual(register["response_index"], 0)

    def test_3_groups_force_different_size(self):
        config = dict(
            model="sdm120m",
            current=dict(name="current"),
            power_factor=dict(name="power_factor"),
            frequency=dict(name="frequency"),
        )
        groups = get_groups(CONFIG_SCHEMA(config), maximum_registers_count=10)
        self.assertEqual(len(groups), 3)
        group = groups[0]
        self.assertEqual(group["start_address"], 6)
        self.assertEqual(group["register_count"], 2)
        self.assertEqual(group["response_size"], 4)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "current")
        self.assertEqual(register["response_index"], 0)
        group = groups[1]
        self.assertEqual(group["start_address"], 30)
        self.assertEqual(group["register_count"], 3)
        self.assertEqual(group["response_size"], 6)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "power_factor")
        self.assertEqual(register["response_index"], 0)
        group = groups[2]
        self.assertEqual(group["start_address"], 70)
        self.assertEqual(group["register_count"], 4)
        self.assertEqual(group["response_size"], 8)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "frequency")
        self.assertEqual(register["response_index"], 0)

    def test_size_exceding_maximum_registers_count(self):
        config = dict(
            model="sdm120m",
            voltage=dict(name="voltage"),
            active_power=dict(name="active_power"),
            apparent_power=dict(name="apparent_power"),
            power_factor=dict(name="power_factor"),
        )
        # both groups have register_count=14 which is the maximum
        # so adding 1 register to the second is not possible
        groups = get_groups(CONFIG_SCHEMA(config), maximum_registers_count=14)
        self.assertEqual(len(groups), 3)
        group = groups[0]
        self.assertEqual(group["start_address"], 0)
        self.assertEqual(group["register_count"], 2)
        self.assertEqual(group["response_size"], 4)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "voltage")
        self.assertEqual(register["response_index"], 0)
        group = groups[1]
        self.assertEqual(group["start_address"], 12)
        self.assertEqual(group["register_count"], 8)
        self.assertEqual(group["response_size"], 16)
        registers = group["registers"]
        self.assertEqual(len(registers), 2)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "active_power")
        self.assertEqual(register["response_index"], 0)
        register = registers[1]
        self.assertEqual(register["sensor"]["name"], "apparent_power")
        self.assertEqual(register["response_index"], 12)
        group = groups[2]
        self.assertEqual(group["start_address"], 30)
        self.assertEqual(group["register_count"], 3)
        self.assertEqual(group["response_size"], 6)
        registers = group["registers"]
        self.assertEqual(len(registers), 1)
        register = registers[0]
        self.assertEqual(register["sensor"]["name"], "power_factor")
        self.assertEqual(register["response_index"], 0)
