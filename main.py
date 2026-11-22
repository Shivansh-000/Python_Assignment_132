"""main.py - Household Energy Consumption and Conservation Tracker (Milestone 5 final)."""
import time
from energy_utils import (APPLIANCE_CATALOGUE, find_appliance, estimate_cost,
                          classify_usage, calculate_household_total,
                          save_records, read_records)
from appliance_usage import ApplianceUsage


def collect_usage():
    """Ask for appliances until DONE; invalid entries are reported and skipped."""
    records = []
    print("Available appliances:", ", ".join(APPLIANCE_CATALOGUE))
    print("Type DONE as the appliance name to finish.\n")
    while True:
        entered = input("Appliance name (or DONE): ").strip()
        if entered.upper() == "DONE":
            break
        name = find_appliance(entered)
        if name is None:
            print("  Rejected: '" + entered + "' is not in the catalogue.\n")
            continue

        try:
            units = int(input("Number of units: "))
            hours = float(input("Hours per day: "))
        except ValueError:                              # text typed instead of a number
            print("  Error: please enter numbers only (e.g. 2 units, 6.5 hours).\n")
            continue

        if units <= 0 or hours <= 0 or hours > 24:       # impossible usage values
            print("  Rejected: units must be >= 1 and hours must be between 0 and 24.\n")
            continue

        records.append(ApplianceUsage(name, APPLIANCE_CATALOGUE[name], hours, units))
        print("  Accepted:", name, "\n")
    return records


def generate_report():
    records = collect_usage()
    if not records:
        print("No valid records entered, nothing to save.")
        return

    total_kwh = calculate_household_total(records, days=30)
    total_cost = estimate_cost(total_kwh, tariff=6.50)

    print("\n===== Monthly Energy Report =====")
    print("Generated on :", time.strftime("%d-%m-%Y %H:%M:%S"))
    print("-" * 52)
    for record in records:
        record.display_summary()
    print("-" * 52)
    print(f"Household total : {total_kwh:.2f} kWh")
    print(f"Estimated cost  : Rs. {total_cost:.2f}")
    print(f"Usage level     : {classify_usage(total_kwh)}")

    save_records(records)                                # a) append to energy_records.txt
    print("\nRecords saved to energy_records.txt")


def show_saved_records():
    try:
        lines = read_records()                           # b) read the saved records
    except FileNotFoundError:                            # d) file missing
        print("\nNo saved records found yet (energy_records.txt does not exist).")
        print("Generate a report first so that records can be saved.")
        return
    print("\n===== Saved Records =====")
    print(f"{'Date & Time':<20}{'Appliance':<14}{'Units':>6}{'Hrs/day':>9}{'kWh':>9}{'Cost (Rs.)':>12}")
    for line in lines:
        stamp, name, units, hours, kwh, cost = line.strip().split(",")
        print(f"{stamp:<20}{name:<14}{units:>6}{hours:>9}{kwh:>9}{cost:>12}")


def main():
    while True:
        print("\n--- Household Energy Tracker ---")
        print("1. Enter appliance usage and generate report")
        print("2. View saved records")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            generate_report()
        elif choice == "2":
            show_saved_records()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
