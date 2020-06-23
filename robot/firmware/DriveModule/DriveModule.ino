/**
 * @file DriveModule.ino
 * @author Justin Kleiber (jkleiber8@gmail.com)
 * @brief Controlling Shamrock's drive train and providing
 *        data to the main board
 * @version 0.1
 * @date 2019-08-03
 *
 * @copyright Copyright (c) 2019
 *
 */


// Arduino dependencies
#include <ArduinoJson.h>
#include <RobotLib.h>

// Shamrock Drive Module Code
#include "Devices.h"
#include "DriveModuleConstants.h"
#include "SensorManagement.h"

// Arduino JSON packets
StaticJsonDocument<256> control_pkt;
char serial_buffer[256];

// Track control loop timing
unsigned long last_loop_time;


// Track motor power outputs
float turn = 0.0;
float power = 0.0;


/**
 * @brief Set up the program
 *
 */
void setup()
{
    // Initialize Serial.
    Serial.begin(115200);

    // Initialize the devices
    device_init();

    // Start loop timing
    last_loop_time = millis();
}


/**
 * @brief Main program loop
 *
 */
void loop()
{
    // Update sensor data
    sensor_update();

    // TODO: send sensor data to raspberry pi

    // Receive commands from raspberry pi.
    // Note: data must be sent with no newline or else
    // this will reset the power to 0 on the next loop.
    if(Serial.available() > 0)
    {
        // Collect JSON string
        Serial.readBytesUntil('\n', serial_buffer, 256);

        // Print buffer
        Serial.print(serial_buffer);

        // Deserialization
        DeserializationError error = deserializeJson(control_pkt, serial_buffer);

        if(error)
        {
            Serial.print(F("deserializeJson() failed: "));
            Serial.println(error.c_str());

            // Stop robot for safety.
            turn = 0.0;
            power = 0.0;
        }
        else
        {
            // Update the drivetrain controls.
            turn = control_pkt["turn"].as<float>();
            power = control_pkt["power"].as<float>();

            // Response (for testing).
            Serial.print(power);
            Serial.print("\t");
            Serial.println(turn);
        }
    }

    // Apply motor power using arcade drive.
    left_motor.output(power + turn);
    right_motor.output(power - turn);

    // Wait for loop update time to elapse
    while((millis() - last_loop_time) < LOOP_PERIOD){
        delay(1);
    }

    // Update timing tracker
    last_loop_time = millis();
}
