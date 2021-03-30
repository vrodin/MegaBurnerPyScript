import serial, sys, time
import serial.tools.list_ports as comtools

SIGNAL_OP_BEGIN = '&';
SIGNAL_OP_END = '%';
	
CHECK_COMMAND = "C"
READ_COMMAND  = "R"
ERASE_COMMAND = "E"
WRITE_COMMAND = "W"

fileData = []
ser = serial.Serial()
ser.baudrate = 115200

def wait4Signal(s):
	global ser
	c = ser.read()
	while c != s:
		c = ser.read()
		print(c, s)


def write():
	global ser, fileData
	totalLength = len(fileData)
	print (totalLength)
	for i in range(0, totalLength, 4096):
		writeCount = 0;
		nextBlock = i + 4096;
		if nextBlock <= totalLength :
			writeCount = 4096;
		else:
			writeCount = totalLength - i;
		ser.write(bytes(WRITE_COMMAND + str(i) + "," + str(128)  + "," + str(writeCount), "ASCII"));
		ser.flush();
		wait4Signal(bytes(SIGNAL_OP_BEGIN, "ASCII"));
				
		ser.write(bytearray(fileData[i:i + writeCount]));
		ser.flush();
		wait4Signal(bytes(SIGNAL_OP_END, "ASCII"));
	
def read(filePath):
	data = []
	with open(filePath, "wb") as f:
		for block in range(1024):
			ser.write(bytes((READ_COMMAND) + str(block) + "," + str(4096), "ASCII"));
			ser.flush();
			if block == 0:
				print(ser.read(4))
			f.write(ser.read(4096))
		f.close()

def erace():
	global ser
	ser.write(bytes(ERASE_COMMAND,"ASCII"));
	ser.flush();
	wait4Signal(bytes(SIGNAL_OP_END,"ASCII"));
	print("Erace done")

def main(argv):
	global ser, fileData
	ser.port = argv[0]
	ser.open()
	time.sleep(1)
	if argv[1] == 'E':
		erace()
	elif argv[1] == 'W':
		with open(argv[2], "rb") as f:
			fileData = f.read()
			write()
	elif argv[1] == 'R':
		read(argv[2]);
		
	ser.close()
	
if __name__ == "__main__":
   main(sys.argv[1:])

