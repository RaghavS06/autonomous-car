# 🚗 Autonomous RC Car 

<p align="center"> <img src="resources/IMG_4058.HEIC)" width="600"> </p>
<p align="center"> <img src="resources/IMG_4060.HEIC)" width="600"> </p>

## 📖 About
This project is a fully autonomous RC car built using a Raspberry Pi, LiDAR, and IMU sensors.
It performs real-time environment sensing, steering, and speed control without human input.

Designed for learning robotics, sensor fusion, and embedded systems development.

## ✨ Features
🔍 Obstacle Detection — real-time 360° scanning with RPLidar

🎯 Precise Steering Control — PWM-based servo steering

🛞 Throttle Management — DC motor speed control with L298N

🧭 Orientation Awareness — MPU6050-based tilt sensing

📈 Live Visualization (matplotlib)

🧠 Multithreaded Architecture for sensor and actuator synchronization

## 🛠 Hardware Used
### Component	Details

Raspberry Pi	(Model 4B)

RPLidar	A1 Model

MPU6050	Gyroscope + Accelerometer

L298N Motor Driver	Dual H-Bridge Controller

DC Motor	Brushed type, PWM control

Servo Motor	5V, standard rotation range

RC Car Chassis	(pre-built)

Power Supply	5V for motors and servos

## 🖥 Software Stack
Language: Python 3.9+

Key Libraries:

rplidar

smbus / smbus2

RPi.GPIO

numpy

matplotlib (optional, for plotting)


🔌 Wiring Diagram

(Add a labeled diagram showing how everything connects.)


📊 Example Outputs
LiDAR Mapping	MPU6050 Tilt Data
(Insert IMU graph here)

# 🧩 Future Enhancements
- 🛤 Path Planning and basic route optimization
- 🗺 SLAM Integration (Simultaneous Localization and Mapping)
- 🔋 Power Optimization for longer outdoor use
- 🖥 Web Dashboard for live telemetry viewing
