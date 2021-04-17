# -*- coding: utf-8 -*-
"""image.ipynb のコピー

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LDY8bRHe-l7Sg-vc-1T_wKEOQUF0yk63
"""

import os, sys, getopt
import tensorflow as tf
import math
import numpy as np

def tensor_to_png( image, filename):
  image_enc = tf.io.encode_png(image)
  fname = tf.constant(filename)
  fwrite = tf.io.write_file(fname, image_enc)


def image_add_circle(  np_image, x_m, y_m, radius, shade=255 ):
  for angle in range(0,360):
    x = int(radius * math.cos( angle*math.pi/180)) + x_m
    y = int(radius * math.sin( angle*math.pi/180)) + y_m
    np_image[x,y,0] = shade
    np_image[x,y,1] = shade
    np_image[x,y,2] = shade


def image_add_line(  np_image, x_m, y_m, length, angle, shade=255, thickness=1):

  for width in range( 0, thickness ):
    for r in range(0, length):

      x = -int( r * math.cos( angle*math.pi/180) ) + x_m
      y =  int( r * math.sin( angle*math.pi/180) ) + y_m

      np_image[x,y,0] = shade
      np_image[x,y,1] = shade
      np_image[x,y,2] = shade

      if width > 0:
        x = -int( r * math.cos( angle*math.pi/180) ) + x_m + width
        y =  int( r * math.sin( angle*math.pi/180) ) + y_m + width

        np_image[x,y,0] = shade
        np_image[x,y,1] = shade
        np_image[x,y,2] = shade

        x = -int( r * math.cos( angle*math.pi/180) ) + x_m - width
        y =  int( r * math.sin( angle*math.pi/180) ) + y_m - width

        np_image[x,y,0] = shade
        np_image[x,y,1] = shade
        np_image[x,y,2] = shade


def image_add_tick(  np_image, x_m, y_m, radius,step=6, tick_len=1, shade=255):
  for offset in range(0, tick_len ):
    for angle in range(0,360, step):
      x = int( ( radius + offset ) * math.sin( angle*math.pi/180) ) + x_m
      y = int( ( radius + offset ) * math.cos( angle*math.pi/180) ) + y_m
      np_image[x,y,0] = shade
      np_image[x,y,1] = shade
      np_image[x,y,2] = shade


def clock_face( diameter, hour, minute, hr_len, min_len, back_shade=255, hand_shade=255, thickness=1 ):
  np_image = np.full( ( ( diameter) , ( diameter),3), back_shade )
  x_m = int(diameter/2)
  y_m = int(diameter/2)
  image_add_line(    np_image, x_m, y_m, hr_len,  hour*30,  shade = hand_shade, thickness=thickness )
  image_add_line(    np_image, x_m, y_m, min_len, minute*6, shade = hand_shade, thickness=thickness )
  image = tf.convert_to_tensor( np_image, tf.float32 )
  image = tf.cast( image, dtype=tf.uint8 )
  return image

def clock_face_gen( sub_dir, file_handle, diameter, hour_len, minute_len, thickness=1 ):
    base_dir = os.getcwd()
    full_dir = os.path.join( base_dir, sub_dir )
    if not os.path.isdir(full_dir):
        os.mkdir(full_dir)

    for hour in range(0, 12 ):
        for minute in range( 0, 60):
            hour_precise = hour + minute/60
            image = clock_face( diameter, hour_precise, minute, hour_len, minute_len, 240, 30,  thickness=thickness )
            filename = "clock_" + str(hour) + "_" + str(minute) + "_" + str(hour_len) + "_" + str(minute_len)+ "_" + str(thickness) + "_0.png"
            filename_path = os.path.join(sub_dir, filename)
            csv_line =  filename_path + "," +  str( math.sin( math.radians(hour_precise*30))/1.01 )
            csv_line += "," + str( math.cos( math.radians(hour_precise*30))/1.01 )
            csv_line += "," + str( math.sin( math.radians(minute*6))/1.01 )
            csv_line += "," + str( math.cos( math.radians(minute*6))/1.01 ) + "\n'"
            file_handle.write(csv_line)
            tensor_to_png( image, filename_path )

def clock_multiface_gen( dir_name, file_handle, diameter, hand_len_min=70, hand_len_max=90, thickness_max=1 ):
  for thickness in range(  1, thickness_max+1):
    for percent in range(  hand_len_min, hand_len_max, 5):
      clock_face_gen( dir_name, file_handle, diameter, int(diameter*percent/300 ), int(diameter*percent/200 ), thickness=thickness )


def clock_multiface_gen_csv( dir_name, csv_file, diameter, hand_len_min=70, hand_len_max=90, thickness_max=1 ):
    # dir_name = os.path.join( curr_dir, dir )
    base_dir = os.getcwd()
    full_dir = os.path.join( base_dir, dir_name )
    #
    if not os.path.isdir(full_dir):
        os.mkdir(full_dir)
        print('Created directory {}.'.format(full_dir))

    with open( os.path.join( dir_name, csv_file ), 'w') as file_handle:
        file_handle.write("filename, hs, hc, ms, mc\n")
        clock_multiface_gen( dir_name, file_handle, diameter, thickness_max=thickness_max )



def main( argv ):
    """
    :param argv: Command line arguments
    """
    dir    = None # Destination directory
    csv    = None # CSV File

    try:
        opts, args = getopt.getopt(argv,"hd:c:",["dir=","csv"])
    except getopt.GetoptError:
        print('python createClockFaceRawTensorImageHandsOnly.py -d <dir> -c <csv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python createClockFaceTensorImageHandsOnly.py -d <dir> -c <csv>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-c", "--csv"):
            csv = arg

    if csv is None or dir is  None:
        print('python createClockFaceTensorImageHandsOnly.py -d <dir> -c <csv>')
        exit(2)

    print(" Directory ", dir  )
    clock_multiface_gen_csv(  dir, csv, 144, thickness_max=2 )


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('python createClockFaceTensorImageHandsOnly.py  -d <dir> -c <csv>')
        sys.exit(2)
    main(sys.argv[1:])