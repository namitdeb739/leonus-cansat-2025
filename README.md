# LeoNUS Cansat 2025

## Introduction

The Cansat competition is a design-build-fly competition that provides teams with an opportunity to experience the design life-cycle of an aerospace system. The Cansat competition is designed to reflect a typical aerospace program on a small scale and includes all aspects of an aerospace program from the preliminary design review to post flight review. The mission and its requirements are designed to reflect various aspects of real world missions including telemetry, communications, and autonomous operations. Each team is scored throughout the competition on real-world deliverables such as schedules, design review presentations, and demonstration flights.

## Mission Overview

Design a Cansat that consists of a payload and a container that mounts on top of the rocket. The payload rests inside the container at launch and includes the nose cone as part of the payload.

The container with the payload shall deploy from the rocket when the rocket reaches peak altitude and the rocket motor ejection forces a separation. The container with the payload shall descend at a rate of no more than 20 meters/second using a parachute that automatically deploys at separation.

At 75% peak altitude, the payload shall separate from the container and descend using an auto-gyro descent control system until landing. The descent rate shall be 5 meters/second.

A video camera shall show the separation of the payload from the container and the auto-gyro functioning. A second video camera shall be pointing downward at 45 degrees from nadir and oriented north during descent and be spin stabilized so that the view of the earth is not rotating.

The Cansat shall collect sensor data during ascent and descent and transmit the data to a ground station at a 1Hz rate. The sensor data shall include interior temperature, battery voltage, altitude, auto-gyro rotation rate, acceleration, rate, magnetic field, and GPS position.

## Ground Station

### Requirements

| Requirement Number | Requirement |
|--------------------|-------------|
| G1 | The ground station shall command the Cansat to calibrate the altitude to zero when the Cansat is on the launch pad prior to launch. |
| G2 | The ground station shall generate csv files of all sensor data as specified in the Telemetry Requirements section. |
| G3 | Telemetry shall include mission time with 1 second resolution. |
| G4 | Configuration states such as zero altitude calibration software states shall be maintained in the event of a processor reset during launch and mission. |
| G5 | Each team shall develop their own ground station. |
| G6 | All telemetry shall be displayed in real time during ascent and descent on the ground station. |
| G7 | All telemetry shall be displayed in the International System of Units (SI) and the units shall be indicated on the displays. |
| G8 | Teams shall plot each telemetry data field in real time during flight. |
| G9 | The ground station shall include one laptop computer with a minimum of two hours of battery operation, XBEE radio and an antenna. |
| G10 | The ground station must be portable so the team can be positioned at the ground station operations site along the flight line. AC power will not be available at the ground station operations site. |
| G11 | The ground station software shall be able to command the payload to operate in simulation mode by sending two commands, SIMULATION ENABLE and SIMULATION ACTIVATE. |
| G12 | When in simulation mode, the ground station shall transmit pressure data from a csv file provided by the competition at a 1Hz interval to the Cansat. |
| G13 | The ground station shall use a tabletop or handheld antenna. |
| G14 | Because the ground station must be viewed in bright sunlight, the displays shall be designed with that in mind, including using larger fonts (14 point minimum), bold plot traces and axes, and a dark text on light background theme. |
| G15 | The ground system shall count the number of received packets. Note that this number is not equivalent to the transmitted packet counter, but it is the count of packets successfully received at the ground station for the duration of the flight. |
| G16 | The ground station shall be able to activate all mechanisms on command. |

---

## Installation & Setup

This project is cross-platform and should work on Windows, macOS, and Linux. Some hardware (e.g., XBee radio) may require additional drivers or permissions depending on your OS.

### Prerequisites

- **Python 3.10+** installed and available in your PATH.
- **XBee USB drivers** installed for your OS (see below).
- **Invoke** (`invoke` Python package) for task automation.

### 1. Clone the repository

```sh
git clone https://github.com/namitdeb739/leonus-cansat-2025.git
cd leonus-cansat-2025
```

### 2. Install dependencies

Use the provided `invoke` tasks to set up your environment.
If you haven't installed `invoke`, do so with:

```sh
pip install invoke
```

Then, to install all Python dependencies:

```sh
invoke install
```

### 3. Install XBee USB drivers

- **Windows:** Download and install from [Digi XBee Drivers](https://www.digi.com/support/knowledge-base/xctu-drivers).
- **macOS/Linux:** Usually plug-and-play. On Linux, you may need to add your user to the `dialout` group:

  ```sh
  sudo usermod -a -G dialout $USER
  ```

### 4. Running the Application

To start the ground station in laptop mode:

```sh
invoke runlaptop
```

Or in monitor mode:

```sh
invoke runmonitor
```

### 5. Development Utilities

To auto-restart the application on file changes (for development):

```sh
invoke watch --mode=laptop
```

### Notes

- If you encounter issues with serial ports or XBee communication, check your OS's device manager (Windows) or `/dev/tty*` (macOS/Linux).
- For Windows, ensure you use the correct COM port name (e.g., `COM3`).
- All dependencies are listed in `requirements.txt` and are installed via `invoke install`.

---
