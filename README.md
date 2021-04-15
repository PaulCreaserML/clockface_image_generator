# Clock face Image Generator

Generation of clock faces for a clock face reader

There are many potential models including

## Categorical

Hour 0-11 = 12  Categories
Minutes   =  Single output for regression

One of the challenges is the step change from 11->0 and 59->0

## Regression 1

Hour 0-11 = 12  Single output for regression
Minutes   =  Single output for regression

One of the challenges is the step change from 11->0 and 59->0

## Regression 2

2 outputs per parameter

Hour      sin and cos 
Minutes   sin and cos

The hour can be the digit hour ( 0, 1, 2, etc...) or it can be the analogue hour. An analogue displays the hour in a form such as 12.5.
The minute is encoded in the hour hand angle.

### Challenge

Creating an accurate model, with perfect data is relatively simple. However creating a robust model, which can is robust to different clock faces, real time images from a web cam is a little different. 

# Function

There are two scripts for generating clock faces. One uses matplotlib and the other tensors to generate clock faces.

It iss quite old and needs updating. A companion csv file is also generated. This provides labels for training a neural network.

A better approach might be to generate everything on the fy during training, this includes clock face, hands etc...

# CSV

The labels are filename,  hour hand angle ( cos, sin ), minute hand angle ( cos, sin)

Rather than using angles, the sin and cos each angle have been taken, so there are two parameters per handle angle
( The aim was to avoid step changes in the value )

## Status

This code from a few years ago, just for parctice purposes, so I am currently reviewing it
