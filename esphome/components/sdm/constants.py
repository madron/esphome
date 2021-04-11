from esphome.const import (
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    ICON_CURRENT_AC,
    ICON_EMPTY,
    UNIT_AMPERE,
    UNIT_EMPTY,
    UNIT_HERTZ,
    UNIT_VOLT,
    UNIT_VOLT_AMPS,
    UNIT_VOLT_AMPS_REACTIVE,
    UNIT_VOLT_AMPS_REACTIVE_HOURS,
    UNIT_WATT,
    UNIT_WATT_HOURS,
)

MAXIMUM_REGISTERS_COUNT = 40
MODEL = dict(
    # https://www.eastroneurope.com/products/view/sdm120modbus
    # https://www.eastroneurope.com/images/uploads/products/manuals/SDM120_Series_Manual_.pdf
    # https://www.eastroneurope.com/images/uploads/products/protocol/SDM120-MODBUS_Protocol.pdf
    sdm120m=dict(
        voltage=dict(
            address=0x0000,
            unit_of_measurement=UNIT_VOLT,
            icon=ICON_EMPTY,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        current=dict(
            address=0x0006,
            unit_of_measurement=UNIT_AMPERE,
            icon=ICON_CURRENT_AC,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        active_power=dict(
            address=0x000C,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        apparent_power=dict(
            address=0x0012,
            unit_of_measurement=UNIT_VOLT_AMPS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        reactive_power=dict(
            address=0x0018,
            unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        power_factor=dict(
            address=0x001E,
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_EMPTY,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_POWER_FACTOR,
        ),
        frequency=dict(
            address=0x0046,
            unit_of_measurement=UNIT_HERTZ,
            icon=ICON_EMPTY,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_EMPTY,
        ),
        import_active_energy=dict(
            address=0x0048,
            unit_of_measurement=UNIT_WATT_HOURS,
            icon=ICON_EMPTY,
            device_class=DEVICE_CLASS_ENERGY,
            accuracy_decimals=0,
            multiply=1000,
        ),
        export_active_energy=dict(
            address=0x004A,
            unit_of_measurement=UNIT_WATT_HOURS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_ENERGY,
            multiply=1000,
        ),
        import_reactive_energy=dict(
            address=0x004C,
            unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE_HOURS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_ENERGY,
            multiply=1000,
        ),
        export_reactive_energy=dict(
            address=0x004E,
            unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE_HOURS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_ENERGY,
            multiply=1000,
        ),
        total_system_power_demand=dict(
            address=0x0054,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        maximum_total_system_power_demand=dict(
            address=0x0056,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        import_system_power_demand=dict(
            address=0x0058,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        maximum_import_system_power_demand=dict(
            address=0x005A,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        export_system_power_demand=dict(
            address=0x005C,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        maximum_export_system_power_demand=dict(
            address=0x005E,
            unit_of_measurement=UNIT_WATT,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
        ),
        current_demand=dict(
            address=0x0102,
            unit_of_measurement=UNIT_AMPERE,
            icon=ICON_CURRENT_AC,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        maximum_current_demand=dict(
            address=0x0108,
            unit_of_measurement=UNIT_AMPERE,
            icon=ICON_CURRENT_AC,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        total_active_energy=dict(
            address=0x0156,
            unit_of_measurement=UNIT_WATT_HOURS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_ENERGY,
            multiply=1000,
        ),
        total_reactive_energy=dict(
            address=0x0158,
            unit_of_measurement=UNIT_VOLT_AMPS_REACTIVE_HOURS,
            icon=ICON_EMPTY,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_ENERGY,
            multiply=1000,
        ),
    ),
    # https://www.eastroneurope.com/products/view/sdm120ct-modbus
    # https://www.eastroneurope.com/images/uploads/products/manuals/SDM120_User_manual_v2.pdf
    # https://www.eastroneurope.com/images/uploads/products/protocol/SDM120CT_Modbus_protocol.pdf
    # sdm120ct=dict(
    # ),
    # https://www.eastroneurope.com/products/view/sdm230modbus
    # https://www.eastroneurope.com/images/uploads/products/manuals/SDM230_Sereis_Manual.pdf
    # https://www.eastroneurope.com/images/uploads/products/protocol/SDM230-MODBUS_Protocol.pdf
    # sdm230m=dict(
    # ),
    # https://www.eastroneurope.com/products/view/sdm630modbus
    # https://www.eastroneurope.com/images/uploads/products/manuals/SDM630_Series_Manual.pdf
    # https://www.eastroneurope.com/images/uploads/products/protocol/SDM630_MODBUS_Protocol.pdf
    # sdm630=dict(
    # ),
)
