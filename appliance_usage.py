"""appliance_usage.py - ApplianceUsage class (Milestone 3, now using energy_utils)."""
import energy_utils


class ApplianceUsage:
    days_in_month = 30

    def __init__(self, appliance_name, power_watts, hours_per_day, units=1):
        self.appliance_name = appliance_name
        self.power_watts = power_watts
        self.hours_per_day = hours_per_day
        self.units = units

    def calculate_kwh(self):
        return energy_utils.calculate_kwh(self.power_watts, self.hours_per_day,
                                          self.units, ApplianceUsage.days_in_month)

    def calculate_cost(self, tariff=energy_utils.DEFAULT_TARIFF):
        return energy_utils.estimate_cost(self.calculate_kwh(), tariff)

    def display_summary(self, tariff=energy_utils.DEFAULT_TARIFF):
        print(f"{self.appliance_name:<14} x{self.units}  {self.hours_per_day:>5} h/day  "
              f"{self.calculate_kwh():>8.2f} kWh  Rs. {self.calculate_cost(tariff):>8.2f}")

    def __str__(self):
        return (f"{self.units} x {self.appliance_name} ({self.power_watts} W) "
                f"for {self.hours_per_day} h/day over {ApplianceUsage.days_in_month} days")
