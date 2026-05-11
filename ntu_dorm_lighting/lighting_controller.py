#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json
from datetime import datetime

class LightingController(Node):
    def __init__(self):
        super().__init__('dorm_lighting_controller')

        # For easy configuration without changing code
        self.declare_parameter('mqtt_broker', 'localhost')
        self.declare_parameter('mqtt_port', 1883)
        self.declare_parameter('mqtt_topic_set', 'dorm/light/set')
        self.declare_parameter('mqtt_topic_state', 'dorm/light/state')

        self.broker = self.get_parameter('mqtt_broker').value
        self.port = self.get_parameter('mqtt_port').value
        self.topic_set = self.get_parameter('mqtt_topic_set').value
        self.topic_state = self.get_parameter('mqtt_topic_state').value

        # ROS 2 Publisher for broadcasting the light state to the ROS network
        self.state_pub = self.create_publisher(String, '~/light_state', 10)

        # Initialize MQTT Client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message

        try:
            self.mqtt_client.connect(self.broker, self.port, 60)
            self.mqtt_client.loop_start() # Run MQTT network loop in a background thread
        except Exception as e:
            self.get_logger().error(f"Failed to connect to MQTT broker at {self.broker}:{self.port}. Error: {e}")

        # Scheduler Timer
        self.timer = self.create_timer(60.0, self.check_schedule)
        
        # State tracker to ensure we only send the command once per transition period
        self.last_action_hour = -1

        self.get_logger().info("NTU Dorm Lighting Controller Node Started.")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.get_logger().info(f"Connected to MQTT broker successfully.")
            client.subscribe(self.topic_state)
        else:
            self.get_logger().error(f"MQTT connection failed with code {rc}")

    def on_mqtt_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        self.get_logger().info(f"Light State Update Received via MQTT: {payload}")
        
        # Publish the received MQTT state into the ROS 2
        ros_msg = String()
        ros_msg.data = payload
        self.state_pub.publish(ros_msg)

    def set_light(self, state: str):
        # Format typical for Zigbee2MQTT and smart home hubs
        payload = json.dumps({"state": state.upper()})
        self.mqtt_client.publish(self.topic_set, payload)
        self.get_logger().info(f"Schedule Triggered: Commanded light to turn {state.upper()}")

    def check_schedule(self):
        now = datetime.now()
        current_hour = now.hour

        # 8:00 PM (20:00) - Turn ON
        if current_hour == 20 and self.last_action_hour != 20:
            self.set_light('ON')
            self.last_action_hour = 20
            
        # 8:00 AM (08:00) - Turn OFF
        elif current_hour == 8 and self.last_action_hour != 8:
            self.set_light('OFF')
            self.last_action_hour = 8

        # Reset the action tracker at midnight to arm the scheduler for new day
        if current_hour == 0:
            self.last_action_hour = -1

def main(args=None):
    rclpy.init(args=args)
    node = LightingController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt, shutting down...")
    finally:
        node.mqtt_client.loop_stop()
        node.mqtt_client.disconnect()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
