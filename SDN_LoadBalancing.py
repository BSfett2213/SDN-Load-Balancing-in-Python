import numpy as np
import random
import matplotlib.pyplot as plt

# Simulation parameters
num_devices = 5
num_apps_per_device = 3
total_bandwidth = 100  # Total available bandwidth
time_slots = 20  # Total time slots for the simulation

# Structure to simulate user using apps with different start and end times, and apps using different bandwidths
class Application:
    def __init__(self, app_id):
        self.app_id = app_id
        self.bandwidth = random.randint(5, 20)  # Random bandwidth between 5 and 20 units
        self.start_time = random.randint(0, time_slots // 2)  # Random start time in first half
        self.end_time = random.randint(self.start_time + 1, time_slots)  # End time after start
        self.active = False # Initially keeping apps inactive

    def is_active(self, t):
        # Check if the app is active at time t
        return self.start_time <= t < self.end_time


# Define edge devices with applications
class EdgeDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.apps = [Application(app_id=f"App-{device_id}-{i}") for i in range(num_apps_per_device)]


# Round Robin Scheduler
def round_robin(devices, t):
    # Collect all active applications
    active_apps = [app for device in devices for app in device.apps if app.is_active(t)]
    total_active = len(active_apps)
    if total_active == 0:
        return {}  # No active apps, return an empty dictionary
    allocation = total_bandwidth // total_active
    allocation_per_app = {app.app_id: allocation for app in active_apps}
    return allocation_per_app


# Simplified Proportional Fair Scheduler
def proportional_fair_scheduler(devices, t):
    # Collect all active applications
    active_apps = [app for device in devices for app in device.apps if app.is_active(t)]
    total_active = len(active_apps)
    if total_active == 0:
        return {}  # No active apps return null
    # Assign bandwidth proportionally
    total_weight = sum(random.random() for _ in active_apps)  # Assign random weights
    allocation_per_app = {}
    for app in active_apps:
        weight = random.random()
        allocation = int((weight / total_weight) * total_bandwidth)  # Proportional allocation
        allocation_per_app[app.app_id] = allocation
    return allocation_per_app


def run_simulation(algorithm):
    devices = [EdgeDevice(device_id=i) for i in range(num_devices)]
    bandwidth_usage = {f"Time-{t}": {} for t in range(time_slots)}

    for t in range(time_slots):
        if algorithm == "round_robin":
            allocations = round_robin(devices, t)
        elif algorithm == "proportional_fair":
            allocations = proportional_fair_scheduler(devices, t)
        bandwidth_usage[f"Time-{t}"] = allocations

    return bandwidth_usage


# Plotting total bandwidth allocation vs Time
def plot_bandwidth_allocation(bandwidth_usage, algorithm_name):
    time_series = []
    bandwidth_series = []

    for time, allocation in bandwidth_usage.items():
        time_series.append(int(time.split('-')[-1]))
        bandwidth_series.append(sum(allocation.values()))  # Total bandwidth allocated at each time

    plt.plot(time_series, bandwidth_series, label=algorithm_name)


# Running the simulation for both algorithms
bandwidth_rr = run_simulation("round_robin")
bandwidth_pfs = run_simulation("proportional_fair")

# Plot results
plt.figure(figsize=(10, 5))
plot_bandwidth_allocation(bandwidth_rr, "Round Robin")
plot_bandwidth_allocation(bandwidth_pfs, "Proportional Fair")

plt.xlabel("Time Slot")
plt.ylabel("Total Bandwidth Allocated")
plt.legend()
plt.title("Bandwidth Allocation Comparison (Round Robin vs Proportional Fair)")
plt.show()
