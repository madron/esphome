"""Tests for the sdm component setup."""


def test_setup_custom(generate_main):
    main_cpp = generate_main("tests/component_tests/sdm/test_setup_custom.yaml")
    assert "sdm_sdm->set_update_interval(500);" in main_cpp
    assert "sdm_sdm->set_parent(my_modbus);" in main_cpp
    assert "sdm_sdm->set_address(0x10);" in main_cpp
    assert 'sdm_sdm->set_model("sdm120m");' in main_cpp
    assert "sdm_sdm->add_group(0, 2, 4);" in main_cpp
    assert 'sensor_sensor->set_name("voltage");' in main_cpp
    assert 'sdm_sdm->add_register(0, "voltage", 0, 1, sensor_sensor);' in main_cpp
