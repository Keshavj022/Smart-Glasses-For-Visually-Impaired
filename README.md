# Smart Glasses for Visually Impaired

An innovative assistive technology solution designed to enhance independence, safety, and quality of life for visually impaired individuals through advanced computer vision, sensor integration, and real-time feedback systems.

![Smart Glasses Prototype](images/smart_glasses_prototype.) 
## Overview
This project implements wearable smart glasses that combine Raspberry Pi 5 and Arduino Uno to create a comprehensive assistive device. Using multiple sensors, AI-powered computer vision, and intuitive feedback mechanisms, the system helps visually impaired users navigate their environment, recognize objects and people, and receive contextual information about their surroundings.

## Features

### Core Capabilities

- **Real-time Object Detection & Recognition**: High-resolution camera with custom-trained YOLO model identifies and classifies objects, prioritizing contextually important items
- **Intelligent Obstacle Detection**: Strategically placed ultrasonic sensors measure distance to obstacles and trigger appropriate feedback
- **Advanced Navigation Assistance**: GPS module with Google Maps API integration provides turn-by-turn directions via audio feedback
- **Comprehensive Scene Understanding**: AI models process images to generate detailed descriptions of complex environments
- **Personalized Face Recognition**: Identifies familiar people and stores new faces with introduction detection
- **Emergency Alert System**: Detects potential dangers and sends alerts with GPS location to predefined emergency contacts

### User Experience

- **Intuitive Audio Feedback**: Clear, natural speech conveys information about surroundings, navigation, and detected objects
- **Directional Haptic Feedback**: Vibration motors indicate obstacle proximity and direction through tactile sensations
- **Personalized Setup Process**: Initial configuration captures user preferences, emergency contacts, and home location
- **Context-Aware Alerts**: Intelligent system only interrupts the user for important information or when specifically requested

## Hardware Components

- **Processing Units**:
  - Raspberry Pi 5 (main processing, computer vision, audio feedback)
  - Arduino Uno (sensor management, haptic feedback)
- **Sensors**:
  - Raspberry Pi Camera Module (object and face recognition)
  - Ultrasonic Sensors HC-SR04 (front, left, right obstacle detection)
  - GPS Module Neo-6M (location tracking and navigation)
- **Feedback Systems**:
  - Bluetooth/Wired Headphones (audio feedback)
  - Vibration Motors (haptic feedback for directional awareness)
- **Power**: Rechargeable battery pack for extended portable use

## System Architecture

The system follows a modular layered architecture for maintainability and extensibility:

1. **Sensor Layer**: Captures environmental data through camera, ultrasonic sensors, and GPS
2. **Processing Layer**:
   - Arduino processes sensor data and controls haptic feedback
   - Raspberry Pi handles computer vision, navigation, and decision-making
3. **Feedback Layer**: Delivers information through audio and haptic systems

## Software Implementation

- **Object Detection**: Custom-trained YOLO model for efficient real-time detection
- **Face Recognition**: Face encoding and matching system with learning capabilities
- **Navigation**: GPS data processing with Google Maps API integration
- **Text-to-Speech**: Natural language generation for clear audio feedback
- **Emergency System**: Automated alert system with location sharing
- **Setup Wizard**: User-friendly initial configuration process

## Sustainability Features

- **Energy Efficiency**: Optimized power management and low-power components
- **Durable Design**: Robust materials for extended product life
- **Updatable Software**: Regular firmware updates to improve functionality
- **Social Impact**: Enhances accessibility and promotes independence

## Installation and Setup

```
# Clone the repository
git clone https://github.com/yourusername/smart-glasses-vi.git

# Install required Python packages
cd smart-glasses-vi/raspberry_pi
pip install -r requirements.txt

# Install Arduino libraries
# Open Arduino IDE and install:
# - SoftwareSerial
# - TinyGPS++
```

## Future Enhancements

- Integration with smart home systems
- Enhanced scene description capabilities
- Improved battery life and charging options
- Public transportation integration
- Weather information and alerts

## Contributors

- Keshav Joshi
- Manish Kumar Saw
- Navneet Tiwari
- Udayan Pandey
