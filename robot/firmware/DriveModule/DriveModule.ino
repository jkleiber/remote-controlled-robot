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


// Track control loop timing
unsigned long last_loop_time;


/**
 * @brief Set up the program
 *
 */
void setup()
{
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

    // Receive commands from raspberry pi
    deserializeJson(control_pkt, Serial);

    // Control drivetrain
    float turn = control_pkt["turn"].as<float>();
    float power = control_pkt["power"].as<float>();
    left_motor.output(power + turn);
    right_motor.output(power - turn);

    // Wait for loop update time to elapse
    while((millis() - last_loop_time) < LOOP_PERIOD){}

    // Update timing tracker
    last_loop_time = millis();
}