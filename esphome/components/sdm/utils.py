from .constants import MAXIMUM_REGISTERS_COUNT, MODEL


def get_groups(config, maximum_registers_count=MAXIMUM_REGISTERS_COUNT):
    model_config = MODEL[config["model"]]
    registers = []
    for name in config.keys():
        if name in model_config:
            register = model_config[name]
            register["name"] = name
            registers.append(register)
    # sort by address
    registers.sort(key=lambda x: x["address"])
    # find groups
    groups = []
    while registers:
        group_registers = []
        while registers:
            test_sensors = group_registers + [registers[0]]
            if get_registers_count(test_sensors) > maximum_registers_count:
                break
            group_registers.append(registers.pop(0))
        start_address = group_registers[0]["address"]
        registers_count = get_registers_count(group_registers)
        register_list = []
        for register in group_registers:
            register_list.append(
                dict(
                    sensor=config[register["name"]],
                    name=register["name"],
                    response_index=(register["address"] - start_address) * 2,
                    multiply=register.get("multiply", 1),
                )
            )
        group = dict(
            start_address=start_address,
            register_count=registers_count,
            response_size=registers_count * 2,
            registers=register_list,
        )
        groups.append(group)
    # Check counts
    counts = [x["register_count"] for x in groups]
    while not len(counts) == len(set(counts)):
        groups = fix_groups(groups)
        counts = [x["register_count"] for x in groups]
    # Check maximum_registers_count
    if [x for x in groups if x["register_count"] > maximum_registers_count]:
        groups = get_groups(config, maximum_registers_count=maximum_registers_count - 1)
    return groups


def fix_groups(groups):
    for index, group in enumerate(groups[1:]):
        previous_counts = [x["register_count"] for x in groups[0 : index + 1]]
        if group["register_count"] in previous_counts:
            group["register_count"] += 1
            group["response_size"] += 2
    return groups


def get_registers_count(registers):
    if not registers:
        return 0
    first_address = registers[0]["address"]
    last_address = registers[-1]["address"]
    return (last_address - first_address) + 2
