# ToteBot: Autonomous Stair-Climbing Assistant
**Course:** Multidisciplinary Projects in Computer Engineering II - CSU Fullerton  
**Team:** Kevin Serafin, Willie Jarin, Leo, Tommy Nguyen

## 🚀 Project Overview
ToteBot is an articulated, sensor-driven robotic platform designed to autonomously navigate residential staircases. It assists the elderly and those with mobility limitations by safely transporting heavy loads (up to 50 lbs) between floors, reducing the risk of stair-related falls.

## 🧠 Software Architecture (Autonomous Mode)
The system operates on a closed-loop control flow using the following sensor fusion:
- **Vision (Logitech Webcam):** Handles yaw alignment using Canny Edge detection and Hough Line Transforms to square the robot to the stairs.
- **Distance (Arducam ToF):** Provides millimeter-level depth data to trigger the lifting actuators at a precise threshold.
- **Stability (MPU-6050 IMU):** Monitors pitch and roll in real-time to maintain platform leveling via a PID loop.

## 🛠 Repository Structure
- `/src`: Core logic for sensor modules and actuator control.
- `/tests`: Calibration scripts for ToF, IMU, and Motor drivers.
- `/docs`: Progress reports, architecture diagrams, and CAD references.

## 📦 Requirements
- Raspberry Pi 5
- Arducam ToF SDK
- OpenCV (Python)
- NumPy
