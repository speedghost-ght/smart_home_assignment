# NTU Dorm Smart Lighting Automation

This repository contains a ROS 2 Python package designed to automate Philips Hue smart lighting in Nanyang Technological University (NTU) student dormitories. By bridging ROS 2 and MQTT, the system enforces energy-efficient habits by adhering to a strict lighting schedule.

## System Architecture

The system utilizes a distributed architecture to bridge high-level robotic scheduling (ROS 2) with low-level IoT device control (Zigbee/MQTT).

```text
+-------------------------+         +------------------+         +----------------------+
|                         |         |                  |         |                      |
|  ROS 2 Node             |  MQTT   |  MQTT Broker     | Zigbee  |  Philips Hue Lights  |
|  (lighting_controller)  |<------->|  (Mosquitto)     |<------->|  (via Zigbee2MQTT)   |
|                         |         |                  |         |                      |
+-------------------------+         +------------------+         +----------------------+
            |
            v
+-------------------------+
|                         |
|  ROS 2 Topic            |
|  (~/light_state)        |
|                         |
+-------------------------+

##-----------------------------------------------------------------------------------------------------------------

## Problem Statement: NTU Dorm Smart Lighting Automation

At Nanyang Technological University (NTU), student dormitories are implementing energy-efficient automated room lighting.

### Current Challenges
- Lights left ON overnight or during the day, wasting electricity
- Inconsistent usage habits across students
- No centralized management or automation

### Solution Stack
- Philips Hue smart lights (Zigbee devices)
- MQTT broker for communication
- ROS 2 orchestration layer

## Your Task

Build a ROS 2 Python package that acts as a scheduled lighting controller for a dorm room.

### Requirements
The system must automatically:
- Turn lights **ON** at 8:00 PM (students return to rooms)
- Turn lights **OFF** at 8:00 AM (save daytime energy)

### Node Responsibilities
- Send commands to the light via MQTT
- Receive current light state from MQTT
- Publish light state into ROS 2


## Other Comments

The submission must include a proper README.md or quick start guide.

The README should clearly explain:

1. How to install dependencies
2. How to build the ROS 2 package
3. How to run the MQTT broker
4. How to run the ROS 2 node
5. How to test ON/OFF commands

The submission must also include an architecture section explaining how the system works.

### What We Want To See

We want to see how you:

1. Break down a problem
2. Structure a ROS 2 Python package
3. Use Git 
4. Write clean Python code
5. Work with MQTT
6. Think about system architecture
7. Explain your work clearly in a README


### How to submit 
1. Clone the repo
2. Complete the assignment
3. Push to your own GitHub repo
4. Share the repo link
