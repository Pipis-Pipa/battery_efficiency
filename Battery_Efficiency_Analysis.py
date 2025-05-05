import streamlit as st

# Battery Efficiency & IMO Regulatory Performance Evaluation Tool (Streamlit Version)

def calculate_bess_efficiency(battery_energy_kwh, sfoc_tonnes_per_kwh, fuel_energy_density_mj_per_tonne, co2_emission_factor_tonnes_per_tonnefuel):
    fuel_saved_tonnes = battery_energy_kwh * sfoc_tonnes_per_kwh
    energy_saved_mj = fuel_saved_tonnes * fuel_energy_density_mj_per_tonne
    co2_saved_tonnes = fuel_saved_tonnes * co2_emission_factor_tonnes_per_tonnefuel
    battery_energy_mj = battery_energy_kwh * 3.6
    efficiency_ratio = energy_saved_mj / battery_energy_mj if battery_energy_mj > 0 else 0
    return fuel_saved_tonnes, energy_saved_mj, co2_saved_tonnes, efficiency_ratio

def calculate_cii(fc_j_tonnes, cf_j, dwt, distance_nm):
    m = fc_j_tonnes * 1000 * cf_j
    w = dwt * distance_nm
    cii = m / w if w > 0 else 0
    return cii

def calculate_roi(fuel_saved_tonnes_per_day, fuel_price_per_tonne, capex, opex_per_year):
    annual_savings = fuel_saved_tonnes_per_day * fuel_price_per_tonne * 300
    net_savings = annual_savings - opex_per_year
    roi = net_savings / capex if capex > 0 else 0
    payback_years = capex / net_savings if net_savings > 0 else float('inf')
    return annual_savings, roi, payback_years

def calculate_eexi(p_me, sfoc_me, cf, v_ref, dwt, eexi_ref):
    numerator = p_me * sfoc_me * cf
    denominator = v_ref * dwt
    attained_eexi = numerator / denominator if denominator > 0 else 0
    is_compliant = attained_eexi <= eexi_ref
    return attained_eexi, is_compliant

def estimate_savings_percent_model(original_consumption_tpd, saving_percent, fuel_price_per_tonne):
    daily_savings = original_consumption_tpd * (saving_percent / 100)
    annual_savings_tonnes = daily_savings * 300
    cost_savings = annual_savings_tonnes * fuel_price_per_tonne
    return daily_savings, annual_savings_tonnes, cost_savings

# Streamlit UI
st.title("Battery Efficiency & IMO Performance Calculator")

battery_energy_kwh = st.number_input("Battery Energy (kWh/day)", value=1200)
sfoc_tonnes_per_kwh = st.number_input("SFOC (tonnes/kWh)", value=0.00022, format="%f")
fuel_energy_density = st.number_input("Fuel Energy Density (MJ/tonne)", value=42700)
co2_factor = st.number_input("CO₂ Factor (tCO₂/t fuel)", value=3.17)

fuel_consumed_annual = st.number_input("Annual Fuel Consumption (tonnes)", value=31200)
dwt = st.number_input("Deadweight (DWT)", value=61614)
distance_nm = st.number_input("Annual Distance Sailed (NM)", value=100000.0)

fuel_saved_tpd = st.number_input("Fuel Saved per Day (tonnes)", value=10.4)
fuel_price = st.number_input("Fuel Price (USD/tonne)", value=601.0)
capex = st.number_input("CAPEX (USD)", value=800000)
opex = st.number_input("OPEX/year (USD)", value=12000)

p_me = st.number_input("Main Engine Power (kW)", value=23000)
sfoc_me = st.number_input("Main Engine SFOC (g/kWh)", value=170)
cf_eexi = st.number_input("Fuel CO₂ Factor (g/g)", value=3.114)
v_ref = st.number_input("Reference Speed (knots)", value=18.5)
eexi_ref = st.number_input("IMO Reference EEXI", value=16.5)

saving_percent = st.slider("Fuel Saving Percentage (Estimate)", min_value=0, max_value=20, value=10)
original_consumption_tpd = st.number_input("Original Fuel Consumption (tonnes/day)", value=104.0)

# Calculations
fuel_saved_tonnes, energy_saved_mj, co2_saved_tonnes, eff_ratio = calculate_bess_efficiency(
    battery_energy_kwh, sfoc_tonnes_per_kwh, fuel_energy_density, co2_factor)
cii = calculate_cii(fuel_consumed_annual, co2_factor, dwt, distance_nm)
annual_savings, roi, payback = calculate_roi(fuel_saved_tpd, fuel_price, capex, opex)
eexi, compliance = calculate_eexi(p_me, sfoc_me, cf_eexi, v_ref, dwt, eexi_ref)
daily_savings, annual_savings_tonnes, cost_savings = estimate_savings_percent_model(
    original_consumption_tpd, saving_percent, fuel_price)

# Display Results
st.subheader("Battery Efficiency")
st.write(f"Fuel Saved: {fuel_saved_tonnes:.2f} tonnes/day")
st.write(f"Energy Saved: {energy_saved_mj:.2f} MJ/day")
st.write(f"CO₂ Saved: {co2_saved_tonnes:.2f} tonnes/day")
st.write(f"Efficiency Ratio: {eff_ratio:.2f} MJ/MJ")

st.subheader("Carbon Intensity Indicator (CII)")
st.write(f"Attained CII: {cii:.6f} gCO₂/DWT·nm")

st.subheader("Return on Investment (ROI)")
st.write(f"Annual Savings: ${annual_savings:,.2f}")
st.write(f"ROI: {roi:.2%}")
st.write(f"Payback Period: {payback:.2f} years")

st.subheader("Energy Efficiency Existing Ship Index (EEXI)")
st.write(f"Attained EEXI: {eexi:.2f} gCO₂/ton·nm")
st.write(f"IMO Compliant: {'Yes' if compliance else 'No'}")

st.subheader("Percent-Based Fuel & Cost Savings Estimate")
st.write(f"Daily Fuel Savings: {daily_savings:.2f} tonnes")
st.write(f"Annual Fuel Savings: {annual_savings_tonnes:.2f} tonnes")
st.write(f"Estimated Annual Cost Savings: ${cost_savings:,.2f}")
