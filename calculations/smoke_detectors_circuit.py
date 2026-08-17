INPUT_VOLTAGE_V = 24
MIN_INPUT_VOLTAGE_V = 12
ADC_REF_VOLTAGE_V = 5
ADC_MAX_LEVEL = 2**10 - 1
ADC_RES_VOLTAGE_V = 5 / ADC_MAX_LEVEL
SMOKE_SENSOR_STANDBY_CURRENT_A = 150e-6
SMOKE_SENSOR_ALARM_CURRENT_A = 70e-3
N_SENSORS_PER_BUS = 1
R_SHUNT_OHM = 30
STANDBY_CURRENT_A = 2e-3

# Short-circuit in the bus, case analysis:

r_series_ohm = (INPUT_VOLTAGE_V - ADC_REF_VOLTAGE_V) * R_SHUNT_OHM / ADC_REF_VOLTAGE_V
print("r_series_ohm = ", r_series_ohm)

voltage_drop_series_v = (
    INPUT_VOLTAGE_V / (R_SHUNT_OHM + r_series_ohm)
    + N_SENSORS_PER_BUS * SMOKE_SENSOR_STANDBY_CURRENT_A
) * r_series_ohm
if INPUT_VOLTAGE_V - voltage_drop_series_v > MIN_INPUT_VOLTAGE_V:
    print(f"voltage_drop_v = {voltage_drop_series_v} (acceptable, within range)")
else:
    print(f"voltage_drop_v = {voltage_drop_series_v} (not acceptable)")

shortcircuit_current_a = INPUT_VOLTAGE_V / (r_series_ohm + R_SHUNT_OHM)
print(f"shortcircuit_current_a = {shortcircuit_current_a}")

# Open-circuit in the bus, case analysis:

oc_input_voltage_v = N_SENSORS_PER_BUS * SMOKE_SENSOR_STANDBY_CURRENT_A * R_SHUNT_OHM

if oc_input_voltage_v > ADC_RES_VOLTAGE_V:
    print(f"oc_input_voltage_v = {oc_input_voltage_v} (detectable by the ADC)")
else:
    print(f"oc_input_voltage_v = {oc_input_voltage_v} (not detectable by the ADC)")

# Bus okay, no alarm, case analysis:

r_eol_ohm = (
    INPUT_VOLTAGE_V
    - (STANDBY_CURRENT_A + N_SENSORS_PER_BUS * SMOKE_SENSOR_STANDBY_CURRENT_A)
    * (r_series_ohm + R_SHUNT_OHM)
) / (STANDBY_CURRENT_A)
print(f"r_eol_ohm = {r_eol_ohm}")

# Bus okay, alarm, case analysis:

alarm_adc_voltage_v = N_SENSORS_PER_BUS * SMOKE_SENSOR_ALARM_CURRENT_A * R_SHUNT_OHM
print(f"alarm_adc_voltage_v = {alarm_adc_voltage_v}")
