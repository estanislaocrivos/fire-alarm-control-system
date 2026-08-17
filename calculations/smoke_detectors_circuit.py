INPUT_VOLTAGE_V = 24
MIN_SENSOR_VOLTAGE_V = 12
ADC_REF_VOLTAGE_V = 5
ADC_MAX_LEVEL = 2**10 - 1
ADC_RES_VOLTAGE_V = ADC_REF_VOLTAGE_V / ADC_MAX_LEVEL
ADC_MARGIN_LSB = 2
ADC_MIN_MARGIN_VOLTAGE_V = ADC_MARGIN_LSB * ADC_RES_VOLTAGE_V

SMOKE_SENSOR_STANDBY_CURRENT_A = 150e-6
SMOKE_SENSOR_ALARM_CURRENT_A = 70e-3
N_SENSORS_PER_BUS = 1

R_SHUNT_OHM = 56  # 4 resistors of 220 ohm in parallel => 55 ohm
EOL_STANDBY_CURRENT_A = 2e-3

# Bus okay, alarm, case analysis:
# Worst case: the single sensor on the bus alarms. R_SHUNT alone (no
# series current-limiting element in this iteration) must keep the ADC
# below its reference voltage, and still leave the sensor enough voltage
# to operate.

alarm_current_total_a = N_SENSORS_PER_BUS * SMOKE_SENSOR_ALARM_CURRENT_A
alarm_adc_voltage_v = alarm_current_total_a * R_SHUNT_OHM
if alarm_adc_voltage_v < ADC_REF_VOLTAGE_V:
    print(f"alarm_adc_voltage_v = {alarm_adc_voltage_v} (within ADC range)")
else:
    print(f"alarm_adc_voltage_v = {alarm_adc_voltage_v} (saturates the ADC)")

sensor_voltage_v = INPUT_VOLTAGE_V - alarm_current_total_a * R_SHUNT_OHM
if sensor_voltage_v > MIN_SENSOR_VOLTAGE_V:
    print(f"sensor_voltage_v = {sensor_voltage_v} (acceptable, within range)")
else:
    print(f"sensor_voltage_v = {sensor_voltage_v} (not acceptable)")

# Open-circuit in the bus, case analysis:
# The standby current (EOL contribution + the sensor's own quiescent
# draw) must stay resolvable above the ADC's noise floor.

standby_current_total_a = (
    EOL_STANDBY_CURRENT_A + N_SENSORS_PER_BUS * SMOKE_SENSOR_STANDBY_CURRENT_A
)
oc_adc_voltage_v = standby_current_total_a * R_SHUNT_OHM

if oc_adc_voltage_v > ADC_MIN_MARGIN_VOLTAGE_V:
    print(f"oc_adc_voltage_v = {oc_adc_voltage_v} (detectable by the ADC)")
else:
    print(f"oc_adc_voltage_v = {oc_adc_voltage_v} (not detectable by the ADC)")

# Bus okay, no alarm, case analysis:
# Solve for the R_EOL value whose own current contribution equals
# EOL_STANDBY_CURRENT_A, given the drop already caused by R_SHUNT at
# standby_current_total_a.

r_eol_ohm = (
    INPUT_VOLTAGE_V - standby_current_total_a * R_SHUNT_OHM
) / EOL_STANDBY_CURRENT_A
print(f"r_eol_ohm = {r_eol_ohm}")  # 10k + 1k + (1k | 1k) + 220 + 220 => 11940

# Short-circuit in the bus, case analysis:
# TODO: no series current-limiting element (fuse/PTC) is implemented in
# hardware yet, so R_SHUNT is the only resistance left in the loop under a
# dead short. A real short would expose the ADC pin to close to
# INPUT_VOLTAGE_V, well beyond its absolute maximum rating, and dump way
# more power into R_SHUNT than it can dissipate. These numbers only define
# the firmware's "short" classification threshold for now -- they don't
# validate any hardware protection, because there isn't any yet.

shortcircuit_current_a = INPUT_VOLTAGE_V / R_SHUNT_OHM
shortcircuit_adc_voltage_v = shortcircuit_current_a * R_SHUNT_OHM
shortcircuit_r_shunt_power_w = shortcircuit_current_a**2 * R_SHUNT_OHM
print(
    f"shortcircuit_current_a = {shortcircuit_current_a}, "
    f"shortcircuit_adc_voltage_v = {shortcircuit_adc_voltage_v}, "
    f"shortcircuit_r_shunt_power_w = {shortcircuit_r_shunt_power_w} "
    "(no HW protection yet, informational only)"
)
