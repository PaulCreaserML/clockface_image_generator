# clockface_image_generator
Generation of clock faces for a clock face reader

## Function

This code uses matplotlib to generator clock face images
It us quite old and needs updating
A companion csv file is also generated. This provides labels for training a neural network

## CSV

The labels are filename,  hour hand angle, minute hand angle, hour hand

Rather than using angles, the sin and cos each angle have been taken, so there are two parameters per handle angle
( The aim was to avoid step changes in the value )

## Status

This code from a few years ago, just for parctice purposes, so I am currently reviewing it
