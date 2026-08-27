# Circuit topology (single sensor per bus, low-side sensing):

INPUT_VOLTAGE_V = 12
ADC_REF_VOLTAGE_V = 5
ADC_MAX_LEVEL = 2**10 - 1
ADC_RES_VOLTAGE_V = ADC_REF_VOLTAGE_V / ADC_MAX_LEVEL
ADC_MARGIN_LSB = 2
ADC_MIN_MARGIN_VOLTAGE_V = ADC_MARGIN_LSB * ADC_RES_VOLTAGE_V

ADC_STANDBY_VOLTAGE_V = 2
ADC_ALARM_VOLTAGE_V = 4

R_SHUNT_OHM = 500

STANDARD_RESISTOR_POWER_RATING_W = 0.25

# Standby, case analysis:
# R_ALARM's branch is disconnected (switch open), so only R_EOL and
# R_SHUNT are in the loop. Solve R_EOL for the target ADC voltage at
# standby.

R_EOL_OHM = (
    R_SHUNT_OHM * (INPUT_VOLTAGE_V - ADC_STANDBY_VOLTAGE_V) / ADC_STANDBY_VOLTAGE_V
)
print(f"R_EOL_OHM = {R_EOL_OHM}")

standby_current_a = INPUT_VOLTAGE_V / (R_EOL_OHM + R_SHUNT_OHM)
standby_adc_voltage_v = standby_current_a * R_SHUNT_OHM
if standby_adc_voltage_v > ADC_MIN_MARGIN_VOLTAGE_V:
    print(f"standby_adc_voltage_v = {standby_adc_voltage_v} (detectable by the ADC)")
else:
    print(
        f"standby_adc_voltage_v = {standby_adc_voltage_v} (not detectable by the ADC)"
    )

pow_r_eol_standby_w = standby_current_a**2 * R_EOL_OHM
pow_r_shunt_standby_w = standby_current_a**2 * R_SHUNT_OHM
print(f"pow_r_eol_standby_w = {pow_r_eol_standby_w}")
print(f"pow_r_shunt_standby_w = {pow_r_shunt_standby_w}")

# Alarm, case analysis:
# R_ALARM connects in parallel with R_EOL (switch closed). Solve the
# equivalent parallel resistance for the target ADC voltage at alarm,
# then solve R_ALARM from that equivalent resistance and the
# already-known R_EOL -- two equations, two unknowns (R_EOL, R_ALARM),
# solved sequentially instead of simultaneously since the standby
# equation alone already pins down R_EOL.

r_eq_alarm_ohm = (
    R_SHUNT_OHM * (INPUT_VOLTAGE_V - ADC_ALARM_VOLTAGE_V) / ADC_ALARM_VOLTAGE_V
)
print(f"r_eq_alarm_ohm = {r_eq_alarm_ohm}")

R_ALARM_OHM = (r_eq_alarm_ohm * R_EOL_OHM) / (R_EOL_OHM - r_eq_alarm_ohm)
print(f"R_ALARM_OHM = {R_ALARM_OHM}")

alarm_current_a = INPUT_VOLTAGE_V / (r_eq_alarm_ohm + R_SHUNT_OHM)
alarm_adc_voltage_v = alarm_current_a * R_SHUNT_OHM
if alarm_adc_voltage_v < ADC_REF_VOLTAGE_V:
    print(f"alarm_adc_voltage_v = {alarm_adc_voltage_v} (within ADC range)")
else:
    print(f"alarm_adc_voltage_v = {alarm_adc_voltage_v} (saturates the ADC)")

alarm_branch_current_a = (INPUT_VOLTAGE_V - alarm_adc_voltage_v) / R_ALARM_OHM
pow_r_alarm_alarm_w = alarm_branch_current_a**2 * R_ALARM_OHM
pow_r_shunt_alarm_w = alarm_current_a**2 * R_SHUNT_OHM
print(f"pow_r_alarm_alarm_w = {pow_r_alarm_alarm_w}")
print(f"pow_r_shunt_alarm_w = {pow_r_shunt_alarm_w}")

if (
    pow_r_alarm_alarm_w > STANDARD_RESISTOR_POWER_RATING_W
    or pow_r_shunt_alarm_w > STANDARD_RESISTOR_POWER_RATING_W
):
    print(f"alarm power dissipation exceeds {STANDARD_RESISTOR_POWER_RATING_W}W")
else:
    print(f"alarm power dissipation within {STANDARD_RESISTOR_POWER_RATING_W}W")
