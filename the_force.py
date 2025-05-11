import time
import threading
import queue
from rplidar import RPLidar
from mpu6050 import mpu6050
import pigpio


# ---------- Constants ----------
PORT_NAME = '/dev/ttyUSB0'
MOTOR_PIN = 17  # GPIO 17
MIN_DISTANCE_CM = 250  # Start motor spinning if object is closer than this
MAX_SPEED_DISTANCE_CM = 100  # Closest distance that corresponds to max motor speed
ESC_ARM_PULSE = 1200
ESC_MIN_SPIN = 1300
ESC_MAX_SPIN = 1700

# ---------- Initialize Components ----------
pi = pigpio.pi()
sensor = mpu6050(0x68)
lidar = RPLidar(PORT_NAME, timeout=10)

# Arm ESC
print("Arming ESC...")
pi.set_servo_pulsewidth(MOTOR_PIN, ESC_ARM_PULSE)
time.sleep(2)

# Setup shared queue
lidar_queue = queue.Queue(maxsize=1)

# ---------- Helper ----------
def map_distance_to_pwm(distance):
    if distance > MIN_DISTANCE_CM:
        return ESC_ARM_PULSE
    elif distance <= MAX_SPEED_DISTANCE_CM:
        return ESC_MAX_SPIN
    else:
        # Linear interpolation
        scale = (distance - MAX_SPEED_DISTANCE_CM) / (MIN_DISTANCE_CM - MAX_SPEED_>
        return ESC_MIN_SPIN + (ESC_MAX_SPIN - ESC_MIN_SPIN) * (1 - scale)

# ---------- Threads ----------
def lidar_worker():
    try:
        for scan in lidar.iter_scans():
            distances = [s[2] for s in scan if s[2] > 0]
            if distances:
                closest = min(distances)
                pwm_value = map_distance_to_pwm(closest)
                print(f"Closest: {closest:.1f} cm -> PWM: {pwm_value:.0f}")
                pi.set_servo_pulsewidth(MOTOR_PIN, pwm_value)
    except Exception as e:
        print(f"LiDAR Error: {e}")

# Start LiDAR thread
lidar_thread = threading.Thread(target=lidar_worker)
lidar_thread.daemon = True
lidar_thread.start()

# ---------- Main Loop (MPU only) ----------
try:
    while True:
        accel_data = sensor.get_accel_data()
        x, y, z = accel_data["x"] * 9.81, accel_data["y"] * 9.81, accel_data["z"] >
        print(f"Accel -> X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Shutting down...")
