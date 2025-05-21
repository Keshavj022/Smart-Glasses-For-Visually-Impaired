#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <Wire.h>

// Pin definitions
const int TRIG_PIN_FRONT = 2;
const int ECHO_PIN_FRONT = 3;
const int TRIG_PIN_LEFT = 4;
const int ECHO_PIN_LEFT = 5;
const int TRIG_PIN_RIGHT = 6;
const int ECHO_PIN_RIGHT = 7;
const int VIBRATION_MOTOR_FRONT = 8;
const int VIBRATION_MOTOR_LEFT = 9;
const int VIBRATION_MOTOR_RIGHT = 10;

// GPS module connection
SoftwareSerial gpsSerial(11, 12); // RX, TX
TinyGPSPlus gps;

// Constants
const float SPEED_OF_SOUND = 0.034; // cm/microsecond
const int DANGER_THRESHOLD = 20; // cm
const int ALERT_THRESHOLD = 50; // cm
const unsigned long GPS_UPDATE_INTERVAL = 5000; // 5 seconds

// Variables
unsigned long lastGpsUpdate = 0;
float lastLatitude = 0;
float lastLongitude = 0;

void setup() {
  // Initialize serial communications
  Serial.begin(9600);
  gpsSerial.begin(9600);
  
  // Initialize ultrasonic sensor pins
  pinMode(TRIG_PIN_FRONT, OUTPUT);
  pinMode(ECHO_PIN_FRONT, INPUT);
  pinMode(TRIG_PIN_LEFT, OUTPUT);
  pinMode(ECHO_PIN_LEFT, INPUT);
  pinMode(TRIG_PIN_RIGHT, OUTPUT);
  pinMode(ECHO_PIN_RIGHT, INPUT);
  
  // Initialize vibration motor pins
  pinMode(VIBRATION_MOTOR_FRONT, OUTPUT);
  pinMode(VIBRATION_MOTOR_LEFT, OUTPUT);
  pinMode(VIBRATION_MOTOR_RIGHT, OUTPUT);
  
  // Initial state - motors off
  digitalWrite(VIBRATION_MOTOR_FRONT, LOW);
  digitalWrite(VIBRATION_MOTOR_LEFT, LOW);
  digitalWrite(VIBRATION_MOTOR_RIGHT, LOW);
  
  Serial.println("Arduino initialized");
}

void loop() {
  // Check ultrasonic sensors
  checkUltrasonicSensors();
  
  // Update GPS data
  updateGPS();
  
  // Process any commands from Raspberry Pi
  processSerialCommands();
  
  delay(100); // Small delay to prevent overwhelming the system
}

void checkUltrasonicSensors() {
  // Check front sensor
  float distanceFront = getDistance(TRIG_PIN_FRONT, ECHO_PIN_FRONT);
  handleObstacle(distanceFront, VIBRATION_MOTOR_FRONT, "front");
  
  // Check left sensor
  float distanceLeft = getDistance(TRIG_PIN_LEFT, ECHO_PIN_LEFT);
  handleObstacle(distanceLeft, VIBRATION_MOTOR_LEFT, "left");
  
  // Check right sensor
  float distanceRight = getDistance(TRIG_PIN_RIGHT, ECHO_PIN_RIGHT);
  handleObstacle(distanceRight, VIBRATION_MOTOR_RIGHT, "right");
}

float getDistance(int trigPin, int echoPin) {
  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Send a 10μs pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Measure the response
  long duration = pulseIn(echoPin, HIGH);
  
  // Calculate distance in cm
  float distance = duration * SPEED_OF_SOUND / 2;
  
  return distance;
}

void handleObstacle(float distance, int motorPin, String direction) {
  // Handle obstacle detection
  if (distance <= DANGER_THRESHOLD) {
    // Dangerous obstacle - activate motor at full power
    analogWrite(motorPin, 255);
    
    // Send alert to Raspberry Pi
    Serial.print("OBSTACLE:");
    Serial.print(distance);
    Serial.print(":");
    Serial.println(direction);
  } 
  else if (distance <= ALERT_THRESHOLD) {
    // Close obstacle - activate motor at proportional power
    int intensity = map(distance, DANGER_THRESHOLD, ALERT_THRESHOLD, 255, 50);
    analogWrite(motorPin, intensity);
    
    // No need to alert Raspberry Pi for non-dangerous obstacles
  } 
  else {
    // No obstacle - turn off motor
    analogWrite(motorPin, 0);
  }
}

void updateGPS() {
  // Read GPS data
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      // Check if we have a valid location and if it's time to update
      if (gps.location.isValid() && millis() - lastGpsUpdate > GPS_UPDATE_INTERVAL) {
        lastGpsUpdate = millis();
        
        // Get current location
        float latitude = gps.location.lat();
        float longitude = gps.location.lng();
        
        // Only send update if location has changed significantly
        if (abs(latitude - lastLatitude) > 0.0001 || abs(longitude - lastLongitude) > 0.0001) {
          lastLatitude = latitude;
          lastLongitude = longitude;
          
          // Send GPS data to Raspberry Pi
          Serial.print("GPS:");
          Serial.print(latitude, 6);
          Serial.print(":");
          Serial.print(longitude, 6);
          Serial.print(":");
          Serial.print(gps.speed.kmph());
          Serial.print(":");
          Serial.println(gps.course.deg());
        }
      }
    }
  }
}

void processSerialCommands() {
  // Check if there are commands from Raspberry Pi
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "VIBRATE_FRONT") {
      // Vibrate front motor for 500ms
      digitalWrite(VIBRATION_MOTOR_FRONT, HIGH);
      delay(500);
      digitalWrite(VIBRATION_MOTOR_FRONT, LOW);
    }
    else if (command == "VIBRATE_LEFT") {
      // Vibrate left motor for 500ms
      digitalWrite(VIBRATION_MOTOR_LEFT, HIGH);
      delay(500);
      digitalWrite(VIBRATION_MOTOR_LEFT, LOW);
    }
    else if (command == "VIBRATE_RIGHT") {
      // Vibrate right motor for 500ms
      digitalWrite(VIBRATION_MOTOR_RIGHT, HIGH);
      delay(500);
      digitalWrite(VIBRATION_MOTOR_RIGHT, LOW);
    }
    // Add more commands as needed
  }
}
