import os, argparse
import serial
input_pipename = "/tmp/promini_serial_fifo_in"
output_pipename = "/tmp/promini_serial_fifo_out"
try:
    os.mkfifo(input_pipename)
except OSError, e:
    print "Failed to create FIFO: %s" % e
try:
    os.mkfifo(output_pipename)
except OSError, e:
    print "Failed to create FIFO: %s" % e

DEFAULT_BAUDRATE = 9600

parser = argparse.ArgumentParser()

parser.add_argument("-p","--path", required=True, help="path to the sensor")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()
ser = None

# open serial port
ser = serial.Serial(args.path, baudrate=DEFAULT_BAUDRATE)
ser.flushInput()
while True:
    #listen for commands from the pipe, this will block
    in_fifo = open(input_pipename,'r')
    # send command and retrieve response
    cmd = in_fifo.readline()
    in_fifo.close()
    ser.write(cmd)
    resp = ser.readline().strip()
    sensor_val = int(resp)
    print "sensor_val=", sensor_val
    out_fifo = open(output_pipename, 'w')
    out_fifo.write("%d\n")
    out_fifo.close()

#fifo = open(filename, 'w')
# write stuff to fifo
#print >> fifo, "hello"
#fifo.close()
#os.remove(filename)
#os.rmdir(tmpdir)/tmp/tmpApM6Vf/myfifo
