import RPi.GPIO as GPIO
import time

servo_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz for servo
pwm.start(0)

def set_angle(angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    print(f"Angle: {angle}°, Duty Cycle: {duty}%")
    time.sleep(0.5)

try:
    while True:
        angle = float(input("Enter angle (0 to 180): "))
        if 0 <= angle <= 180:
            set_angle(angle)
        else:
            print("Out of range")

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
