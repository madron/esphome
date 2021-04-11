#include "sdm.h"
#include "esphome/core/log.h"

namespace esphome {
namespace sdm {

static const char *TAG = "sdm";
static const uint8_t READ_REGISTERS_FUNCTION = 0x04;

void Sdm::add_group(uint16_t start_address, uint16_t register_count, uint16_t response_size) {
  this->groups_.push_back({start_address, register_count, response_size});
}

void Sdm::add_register(uint16_t group_index, const char *name, uint16_t response_index, float multiply, sensor::Sensor *sensor) {
  this->groups_[group_index].registers.push_back({name, response_index, multiply, sensor});
}

void Sdm::on_modbus_data(const std::vector<uint8_t> &data) {
  auto get_32bit_float = [&](size_t i) -> float {
    float res;
    ((uint8_t*)&res)[3]= data[i + 0];
    ((uint8_t*)&res)[2]= data[i + 1];
    ((uint8_t*)&res)[1]= data[i + 2];
    ((uint8_t*)&res)[0]= data[i + 3];
    return res;
  };

  Group group;
  Register reg;
  float value;
  for (uint16_t group_index = 0; group_index < this->groups_.size(); group_index++) {
    group = this->groups_[group_index];
    if (data.size() == group.response_size) {
      ESP_LOGV(TAG, "Got response for group %d", group_index);
      for (uint16_t register_index = 0; register_index < group.registers.size(); register_index++) {
        reg = group.registers[register_index];
        value = get_32bit_float(reg.response_index);
        if (reg.multiply != 1.0)
          value = value * reg.multiply;
        if (reg.sensor != nullptr)
          reg.sensor->publish_state(value);
      }
      // Send request for next group
      if (group_index < this->groups_.size())
        this->send(READ_REGISTERS_FUNCTION, this->groups_[group_index + 1].start_address, this->groups_[group_index + 1].register_count);
    }
  }
}

void Sdm::update() {
  if (this->groups_.size() > 0) {
    this->send(READ_REGISTERS_FUNCTION, this->groups_[0].start_address, this->groups_[0].register_count);
  }
}

void Sdm::dump_config() {
  ESP_LOGCONFIG(TAG, "Sdm:");
  ESP_LOGCONFIG(TAG, "  Model: %s", this->model_);
  ESP_LOGCONFIG(TAG, "  Address: 0x%02X", this->address_);
  for (uint16_t i = 0; i < this->groups_.size(); i++) {
    ESP_LOGCONFIG(TAG, "  Group %d:", i);
    ESP_LOGCONFIG(TAG, "    start_address: 0x%04X", this->groups_[i].start_address);
    ESP_LOGCONFIG(TAG, "    register_count: %d", this->groups_[i].register_count);
    ESP_LOGCONFIG(TAG, "    response_size: %d", this->groups_[i].response_size);
    for (uint16_t r = 0; r < this->groups_[i].registers.size(); r++) {
      ESP_LOGCONFIG(TAG, "    %s:", this->groups_[i].registers[r].name);
      ESP_LOGCONFIG(TAG, "      response_index: %d:", this->groups_[i].registers[r].response_index);
      ESP_LOGCONFIG(TAG, "      multiply: %f:", this->groups_[i].registers[r].multiply);
      LOG_SENSOR("      ", "sensor", this->groups_[i].registers[r].sensor);
    }
  }
}

}  // namespace sdm
}  // namespace esphome
