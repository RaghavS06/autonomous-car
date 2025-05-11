import time
import numpy as np
import matplotlib.pyplot as plt
from mpu6050 import mpu6050

# Initialize the sensor (MPU6050)
sensor = mpu6050(0x68)  # You can change the address to 0x69 if needed

# Rolling average window (adjust to smooth the data more or less)
ROLLING_WINDOW = 10

# Set up Matplotlib plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 6))

# Create lines for each axis (X, Y, Z)
line_x, = ax.plot([], [], label='X', color='r')
line_y, = ax.plot([], [], label='Y', color='g')
line_z, = ax.plot([], [], label='Z', color='b')

# Setting the limits for time and acceleration
ax.set_xlim(0, 100)  # Time window of 100 readings
ax.set_ylim(-2, 2)   # Accelerometer range (-2g to 2g)
ax.set_title("Smoothed Accelerometer Data")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Acceleration (g)")

ax.legend()

# Store data for plotting
time_data = []
x_data = []
y_data = []
z_data = []

# Function to apply rolling average
def rolling_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Start reading the sensor data
start_time = time.time()

try:
    while True:
        # Get accelerometer data
        accel_data = sensor.get_accel_data()
        x = accel_data['x']
        y = accel_data['y']
        z = accel_data['z']

        # Append data to lists
        elapsed_time = time.time() - start_time
        time_data.append(elapsed_time)
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

        # Smooth data using rolling average (if enough data points are available)
        if len(time_data) > ROLLING_WINDOW:
            smoothed_x = rolling_average(x_data, ROLLING_WINDOW)
            smoothed_y = rolling_average(y_data, ROLLING_WINDOW)
            smoothed_z = rolling_average(z_data, ROLLING_WINDOW)
            smoothed_time = time_data[ROLLING_WINDOW-1:]  # Adjust time axis to ma>
        else:
            smoothed_x = x_data
            smoothed_y = y_data
            smoothed_z = z_data
            smoothed_time = time_data

        # Update plot
        line_x.set_xdata(smoothed_time)
        line_x.set_ydata(smoothed_x)
        line_y.set_xdata(smoothed_time)
        line_y.set_ydata(smoothed_y)
        line_z.set_xdata(smoothed_time)
        line_z.set_ydata(smoothed_z)

        # Keep the latest 100 points on the graph
        if len(time_data) > 100:
            time_data.pop(0)
            x_data.pop(0)
            y_data.pop(0)
            z_data.pop(0)

        plt.draw()
        plt.pause(0.1)

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

finally:
    plt.ioff()  # Turn off interactive mode
    plt.show()
