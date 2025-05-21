# Smart Glasses for Visually Impaired

A comprehensive assistive technology solution designed to enhance independence and quality of life for visually impaired individuals through advanced computer vision, sensor technology, and real-time feedback systems.

## Overview

This project implements smart glasses that combine Raspberry Pi 5 and Arduino Uno to create a wearable device that helps visually impaired users navigate their environment, recognize objects and people, and receive contextual information about their surroundings. The system uses multiple sensors and AI-powered computer vision to provide audio and haptic feedback to users.

![Smart Glasses Prototype](https://exampled Recognition**: Uses a high-resolution camera and custom-trained YOLO model to identify and classify objects in real-time, prioritizing contextually important items like vehicles, pedestrians, or obstacles
- **Obstacle Detection**: Ultrasonic sensors mounted on the glasses measure distance to obstacles and provide haptic feedback through vibration motors
- **Navigation Assistance**: GPS module integrated with Google Maps API provides turn-by-turn directions via audio feedback
- **Scene Understanding**: AI models process images to generate contextual descriptions of complex environments
- **Face Recognition**: Identifies familiar people and stores new faces for future reference
- **Emergency Alert System**: Detects potential emergencies and sends alerts with GPS location to predefined contacts

## Hardware Components

- Raspberry Pi 5 (main processing unit)
- Arduino Uno (sensor management)
- Camera Module (object and face recognition)
- Ultrasonic Sensors (HC-SR04) for obstacle detection
- GPS Module (Neo-6M) for location tracking
- Vibration Motors for haptic feedback
- Bluetooth/Wired Headphones for audio feedback

## System Architecture

The system follows a modular layered architecture:

1. **Sensor Layer**: Camera, ultrasonic sensors, GPS module
2. **Processing Layer**: 
   - Arduino UNO: Manages sensors and haptic feedback
   - Raspberry Pi: Handles computer vision, navigation, and decision making
3. **Feedback Layer**: Audio system and haptic feedback

## Implementation

The software implementation includes:
- Computer vision algorithms for object and face detection
- Text-to-speech conversion for audio feedback
- GPS navigation integration
- Emergency alert system
- Initial setup wizard for personalization

## Sustainability Features

- Energy-efficient components and power management
- Durable materials for longevity
- Regular firmware updates to extend device lifespan
- Social impact through improved accessibility and inclusion

## Future Enhancements

- Integration with smart home systems
- Expanded scene description capabilities
- Improved battery life and charging options
- Enhanced personalization features