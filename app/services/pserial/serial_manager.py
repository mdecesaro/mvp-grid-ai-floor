# app/serial_manager.py

import serial
import time
from app.services.pserial.commands import HANDSHAKE_COMMAND

class SerialManager:
    def __init__(self, port=None, baudrate=115200, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def set_port(self, port):
        self.port = port

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2) 
        except serial.SerialException as e:
            raise ConnectionError(f"Error connecting to the port {self.port}: {e}")

    def is_connected(self):
        return self.ser is not None and self.ser.is_open
    
    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_command(self, command):
        if not self.ser or not self.ser.is_open:
            raise ConnectionError("Serial connection is not open.")
        self.ser.write((command + '\n').encode())

    def read_line(self):
        if not self.ser or not self.ser.is_open:
            raise ConnectionError("Serial connection is not open.")
        return self.ser.readline().decode("utf-8").strip()

    def perform_handshake(self):
        self.send_command(HANDSHAKE_COMMAND)

        handshake_data = {
            "device": None,
            "version": None,
            "sensors": None,
            "ready": False
        }

        start_time = time.time()
        timeout = 3
        while time.time() - start_time < timeout:
            line = self.read_line()
            if not line:
                continue

            print("[ARDUINO]", line)

            if line.startswith("DEVICE:"):
                handshake_data["device"] = line.split(":")[1]

            elif line.startswith("VERSION:"):
                handshake_data["version"] = line.split(":")[1]

            elif line.startswith("SENSORS:"):
                handshake_data["sensors"] = int(line.split(":")[1])

            elif line == "READY":
                handshake_data["ready"] = True
                break

        return handshake_data if handshake_data["ready"] else None