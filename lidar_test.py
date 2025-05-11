import matplotlib.pyplot as plt
from rplidar import RPLidar
import numpy as np
import threading
import queue
import time

PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(PORT_NAME, timeout=10)
#lidar.set_motor_pwm(300)

data_queue = queue.Queue(maxsize=1)  # Always keep only latest scan


def lidar_worker():
    try:
        for scan in lidar.iter_scans():
            if not data_queue.full():
                data_queue.put(scan)
            else:
                # Remove old data and insert latest
                data_queue.get()
                data_queue.put(scan)
    except Exception as e:
        print(f"Lidar Error: {e}")

lidar_thread = threading.Thread(target=lidar_worker)
lidar_thread.daemon = True
lidar_thread.start()

plt.ion()
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')
ax.set_ylim(0, 2000)

try:
    while True:
        if not data_queue.empty():
            scan = data_queue.get()
            angles = [np.deg2rad(s[1]) for s in scan]
            distances = [s[2] for s in scan]

            ax.clear()
            ax.set_ylim(0, 2000)
            ax.scatter(angles, distances, color='b', s=10)
            plt.draw()
            plt.pause(0.05)
        else:
            time.sleep(0.01)

except KeyboardInterrupt:
    print("Stopping...")
