#ifndef SHAMROCK_DRIVE_DEVICES_H
#define SHAMROCK_DRIVE_DEVICES_H

#include <RobotLib.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

#include "DriveModuleConstants.h"

// Encoders
static QuadratureEncoder left_encoder; // 2-7/8" wheel, rotated 3 times, encoder output: 4192 -> K = 0.006464
static QuadratureEncoder right_encoder;// 2-7/8" wheel, rotated 3 times, encoder output: 4192 -> K = 0.006464


// Motors
static Motor left_motor;
static Motor right_motor;


//IMU


/**
 * Interrupt Handlers
 */
// Left Encoder
static void left_encoder_isr()
{
    left_encoder.process();
}

// Right Encoder
static void right_encoder_isr()
{
    right_encoder.process();
}


/**
 * Device Initialization
 */
static void device_init()
{
    // Initialize encoders
    left_encoder.begin(LEFT_ENCODER_A, LEFT_ENCODER_B, LEFT_ENCODER_CONST);
    right_encoder.begin(RIGHT_ENCODER_A, RIGHT_ENCODER_B, RIGHT_ENCODER_CONST);

    // Attach encoder interrupts
    attachInterrupt(digitalPinToInterrupt(LEFT_ENCODER_A), &left_encoder_isr, CHANGE);
    attachInterrupt(digitalPinToInterrupt(RIGHT_ENCODER_A), &right_encoder_isr, CHANGE);

    // Initialize the motors
    left_motor.begin(LEFT_A, LEFT_B, LEFT_ENABLE);
    right_motor.begin(RIGHT_A, RIGHT_B, RIGHT_ENABLE);
}


#endif