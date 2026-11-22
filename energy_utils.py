"""energy_utils.py - helper functions for the Household Energy Tracker (Milestone 5 final)."""
import time
import os

APPLIANCE_CATALOGUE = {
    "LED Bulb": 12,
    "Ceiling Fan": 75,
    "Television": 120,
    "Refrigerator": 180,
    "AC": 1500,
}
DEFAULT_DAYS = 30
DEFAULT_TARIFF = 6.50
RECORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "energy_records.txt")


def find_appliance(entered_name):
    """Return the catalogue name matching the input (ignoring case), or None."""
    for name in APPLIANCE_CATALOGUE:
        if name.lower() == entered_name.strip().lower():
            return name
    return None


def calculate_kwh(power_watts, hours_per_day, units=1, days=DEFAULT_DAYS):
    """Monthly kWh = (W / 1000) x hours/day x units x days."""
    return (power_watts / 1000) * hours_per_day * units * days


def estimate_cost(kwh, tariff=DEFAULT_TARIFF):
    """Cost in rupees for the given kWh (default tariff Rs. 6.50)."""
    return kwh * tariff


def classify_usage(total_kwh):
    """Low (<150), Moderate (150-300) or High (>300)."""
    if total_kwh < 150:
        return "Low"
    elif total_kwh <= 300:
        return "Moderate"
    return "High"


def calculate_household_total(records, days=DEFAULT_DAYS):
    """Take a collection of ApplianceUsage records and return the household kWh."""
    total = 0
    for record in records:
        total += calculate_kwh(record.power_watts, record.hours_per_day, record.units, days)
    return total


# ---------------- Milestone 5: file handling ----------------
def save_records(records, tariff=DEFAULT_TARIFF, filename=RECORD_FILE):
    """Append each record to the text file (one comma-separated line per appliance)."""
    stamp = time.strftime("%d-%m-%Y %H:%M:%S")
    with open(filename, "a") as file:               # "a" = append, old data is kept
        for record in records:
            file.write(f"{stamp},{record.appliance_name},{record.units},"
                       f"{record.hours_per_day},{record.calculate_kwh():.2f},"
                       f"{record.calculate_cost(tariff):.2f}\n")


def read_records(filename=RECORD_FILE):
    """Return all saved lines. Raises FileNotFoundError if the file does not exist."""
    with open(filename, "r") as file:
        return file.readlines()
