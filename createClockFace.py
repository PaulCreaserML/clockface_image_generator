import os, sys, getopt
import math
import numpy as np
from itertools import product
import matplotlib.pyplot as plt


# Parameters of the clock hands
hand_widths = [.05, .05, .00]  # Hide seconds hand
# Hand Lengths
lengths = [1.0, 1.3, 1.5]
# Colors
colors = plt.cm.gray(np.linspace(0, 1, 4))[0:3]

def time_to_radians(time):
    """
    :param time: time to radians ( t[ hours, mins, secs ] )
    :return radians
    """
    rads = [0, 0, 0]
    rads[0] = time[0] * np.pi*2/12 + time[1] * np.pi*2/(60*12) # Hours hand rotates with minute hand
    rads[1] = time[1] * np.pi*2/60 # Minutes
    rads[2] = 0 # Seconds hand not supported
    return rads

def setup_axes():
    """
    """
    # Hard coded values
    fig_size = 25
    fig_dpi =  12
    plt.rcParams['toolbar'] = 'None'
    plt.ion()
    fig = plt.figure(figsize=(fig_size, fig_size), facecolor='w')
    fig.set_size_inches(6.0, 6.0)

    ax = plt.subplot(111, polar=True)
    ax.get_yaxis().set_visible(False)

    # 12 labels, clockwise
    marks = np.linspace(360. / 12, 360, 12, endpoint=True)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.grid(None)

    # These are the clock hands. We update the coordinates later.
    bars = ax.bar([10.0, 20.0, 0.0], lengths, width=hand_widths, bottom=0.0, color=colors, linewidth=0)
    return fig, ax, bars


def _update_bars(ax, bars, rotation, times, labels=True):
    rads = time_to_radians(times)
    ax.clear()
    marks = np.linspace( 360. / 12, 360, 12, endpoint=True)
    marks_rot = rotate( marks, rotation)
    mwow = ( marks_rot/30 )
    mwow = mwow.astype(int)
    ax.set_thetagrids(marks, mwow, fontsize=30)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.grid(None)

    if labels == False:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    rads[0] = rads[0] + rotation * np.pi*2/12
    rads[1] = rads[1] + rotation * np.pi*2/12

    bars = ax.bar([rads[0], rads[1], rads[0]], lengths, width=hand_widths, bottom=0.0, color=colors, linewidth=0)


def rotate(l, n):
    """
    :param argv: Command line arguments
    """
    start =  l[:len(l)-n]
    end   =  l[len(l)-n:]
    return np.append( end, start)

def init_clock():
    fig, ax, bars = setup_axes()
    return fig, ax, bars


def save_clock(fig, base_dir, sub_dir, filename_prefix, time):
    """
    :param fig: Matplotlib figure
    :param base_dir: Base-directory for image storage
    :param sub_dir:  Sub-directory for image storage
    :param filename_pre, subface time (12:00)
    :return Full path to image file
    """
    full_dir = os.path.join( base_dir, sub_dir )
    image_dir  = os.path.join(full_dir, 'clock-{:02d}.{:02d}.{:02d}'.format(*time))
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
        print('Created directory {}.'.format(image_dir))
    image_filename = os.path.join(image_dir, filename_prefix + 'clock-{:02d}.{:02d}.{:02d}.png'.format(*time))
    # You might want to change this, for different image sizes
    fig.savefig(image_filename, bbox_inches='tight')
    return image_filename


def set_clock(ax, bars, hours, minutes, seconds, rotation=0,
              show=False, labels= True):
    time = (hours, minutes, seconds)
    _update_bars(ax, bars, rotation, time, labels )

    if show:
        #plt.show()
        if labels == False:
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
        else:
            ax.axes.get_xaxis().set_visible(True)
            ax.axes.get_yaxis().set_visible(False)
        plt.draw()
        plt.pause(0.001)


def hour_hot_encode( hour ):
    """
    :param hour: Number of hours
    :return Hot encoding of hours (0->11)
    """
    encoded = [ 0 ] * 12
    if hour < 0 or hour > 11:
        raise Exception("Hour value out of range")
    encoded[hour-12] = 1
    return encoded

def minute_hot_encode( minute ):
    """
    :param minute: Number of minutes
    :return Hot encoding of minute ( 0->59)
    """
    encoded = [ 0 ] * 60
    if minute < 0 or minute > 59:
        raise Exception("Minute value out of range")
    encoded[minute] = 1
    return encoded

def clock_face_generation(dir_name, csv):
    """
    :param dir_name: Directory where to save clocks.
    :param csv: CSV Filename
    """

    # dir_name = os.path.join( curr_dir, dir )
    base_dir = os.getcwd()
    full_dir = os.path.join( base_dir, dir_name )
    #
    if not os.path.isdir(full_dir):
        os.mkdir(full_dir)
        print('Created directory {}.'.format(full_dir))
    #
    fig, ax, bars = init_clock()
    # Hour range
    hours = range( 0, 12 )
    # Minute Range
    minutes = range( 0, 60 )
    seconds = [0]
    times = [x for x in product(hours, minutes, seconds)]

    with open( os.path.join( dir_name, csv ), 'w') as file_handle:
        file_handle.write("filename, hs, hc, ms, mc, hrs, hrc\n")
        for t in times:
            print('Generating clock for time: {}'.format(t))

            set_clock(ax, bars, *t, rotation=0, show=True, labels=True)
            clock_filename = save_clock(fig, base_dir, dir_name, 'A', t)

            h  =  t[0] # hour_encode
            m  =  t[1]
            hm =  h + m/60.0
            h  =  30*h
            m  =  6*m # minute_encode(
            hm =  30*hm
            print( hm, h, m )

            # Old Code that needs checking ( Was this necessary)
            # Preprocessing the clock handle in a way to avoid step changes from 12->0, 59->0
            # 1.0001 scaling to prevent -1 or 1 saturated output
            csv_line =        str( math.sin( math.radians(hm))/1.0001 )
            csv_line += "," + str( math.cos( math.radians(hm))/1.0001 )
            csv_line += "," + str( math.sin( math.radians(m) )/1.0001 )
            csv_line += "," + str( math.cos( math.radians(m) )/1.0001 )
            csv_line += "," + str( math.sin( math.radians(h) )/1.0001 )
            csv_line += "," + str( math.cos( math.radians(h) )/1.0001 )

            # h sin, cos, m sin, cos
            print( clock_filename)
            full_csv_line = '{},{}\n'.format(clock_filename, csv_line )
            file_handle.write(full_csv_line)

            print('Generating clock for time: {}'.format(t))
            set_clock(ax, bars, *t, rotation=0, show=True, labels=False)
            clock_filename = save_clock(fig, base_dir, dir_name, 'B', t)
            # Store the index string: the filename, hour, and minute
            full_csv_line = '{},{}\n'.format(clock_filename, csv_line )
            file_handle.write(full_csv_line)

    print('Created {} clocks.'.format(len(times)))


def main( argv ):
    """
    :param argv: Command line arguments
    """
    dir = None # Destination directory
    csv = None # CSV File
    try:
        opts, args = getopt.getopt(argv,"hd:c:",["dir=","csv"])
    except getopt.GetoptError:
        print('python createClockFace.py -d <dir> -c <csv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python createClockFace.py -d <dir> -c <csv>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-c", "--csv"):
            csv = arg

    if csv is None or dir is  None:
        print('python createClockFace.py -d <dir> -c <csv>')
        exit(2)

    print(" Directory ", dir  )
    clock_face_generation( dir, csv)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('python createClockFace.py  -d <dir> -c <csv>')
        sys.exit(2)
    main(sys.argv[1:])
