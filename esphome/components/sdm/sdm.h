#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/modbus/modbus.h"

namespace esphome {
namespace sdm {

struct Register {
  const char *name;
  uint16_t response_index;
  float multiply;
  sensor::Sensor *sensor;
};

struct Group {
  uint16_t start_address;
  uint16_t register_count;
  uint16_t response_size;
  std::vector<Register> registers;
};


class Sdm : public PollingComponent, public modbus::ModbusDevice {
 public:
  void set_model(const char *model) { model_ = model; }
  void add_group(uint16_t start_address, uint16_t register_count, uint16_t response_size);
  void add_register(uint16_t group_index, const char *name, uint16_t response_index, float multiply, sensor::Sensor *sensor);
  void update() override;
  void on_modbus_data(const std::vector<uint8_t> &data) override;
  void dump_config() override;

 protected:
  const char *model_;
  std::vector<Group> groups_;
};

}  // namespace sdm
}  // namespace esphome
