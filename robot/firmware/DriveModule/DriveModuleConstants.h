#ifndef DRIVE_MODULE_CONSTS_H
#define DRIVE_MODULE_CONSTS_H

// Encoder Constants
#define LEFT_ENCODER_A 3
#define LEFT_ENCODER_B 12
#define RIGHT_ENCODER_A 2
#define RIGHT_ENCODER_B 11
#define LEFT_ENCODER_CONST (float)(0.006464)
#define RIGHT_ENCODER_CONST (float)(0.006464)

// Motor Constants
#define LEFT_ENABLE     10
#define LEFT_A          5
#define LEFT_B          8
#define RIGHT_ENABLE    9
#define RIGHT_A         7
#define RIGHT_B         6

// Timing Constants
#define MILLIS_PER_SECOND 1000
#define LOOP_RATE   200
#define LOOP_PERIOD (float)((1.0f * MILLIS_PER_SECOND) / (float)LOOP_RATE)


#endif