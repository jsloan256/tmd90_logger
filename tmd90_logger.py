import time
import serial
import signal
import numpy as np
import matplotlib.pyplot as plt

def handler(signum, frame):
    print(('Signal handler called with signal', signum))
    ser.close()
    f.close()
    exit()

signal.signal(signal.SIGINT, handler)

ser = serial.Serial()

ser.port = "/dev/tty.usbserial"
#ser.port = "/dev/ttyS2"
ser.baudrate = 2400
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

ser.open()
ser.isOpen()

f = open('logfile.txt', 'w')

f.write("t,T1,T2\n")
print("Capturing data (press control-C to stop)")
print("t,T1,T2\n")
out = ser.readline() # Purge

t_lst = []
T1_lst = []
T2_lst = []
Pl_lst =[]
Ph_lst = []

for i in range(390):
	if i < 120:
		Pl_lst.append(25)
		Ph_lst.append(200)
	elif i < 180:
		Pl_lst.append(150)
		Ph_lst.append(200)
	elif i < 210:
		Pl_lst.append(150)
		Ph_lst.append(231)
	elif i < 230:
		Pl_lst.append(217)
		Ph_lst.append(231)
	elif i < 250:
		Pl_lst.append(217)
		Ph_lst.append(245)
	elif i < 270:
		Pl_lst.append(217)
		Ph_lst.append(231)
	elif i < 300:
		Pl_lst.append(25)
		Ph_lst.append(231)
	else:
		Pl_lst.append(25)
		Ph_lst.append(200)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('time')
ax.set_ylabel('temp')
ax.set_title('IR Profile')
Pl_plot = ax.plot(range(390), Pl_lst, color='blue', lw=2)
Ph_plot = ax.plot(range(390), Ph_lst, color='red', lw=2)
ax.fill_between(range(390), Pl_lst, Ph_lst, color='blue', alpha=.25)
plt.ion()
plt.show()

t = 0
while 1:
#    time.sleep(1)

    out = ser.readline()
    out = out.decode(encoding='UTF-8')
    if (len(out) > 9):
        if (out[1] == 't'):
            t += 1
            T1 = out[2:8]
            T2 = out[11:17]
            print(str(t) + ": T1=" + str(T1) + ", T2=" + str(T2) + "\n")
            f.write(str(t) + "," + str(T1) + "," + str(T2) + "\n")
            if t == 1:
                t_lst.append(t)
                T1_lst.append(float(T1))
                T2_lst.append(float(T2))
                T1_plot = ax.plot(t_lst, T1_lst, color='green', lw=2)
                T2_plot = ax.plot(t_lst, T2_lst, color='yellow', lw=2)
                ax.figure.canvas.draw()
            else:
                t_lst.append(t)
                T1_lst.append(T1)
                T2_lst.append(T2)
                T1_plot[0].set_data(t_lst, T1_lst)
                T2_plot[0].set_data(t_lst, T2_lst)
                ax.figure.canvas.draw()
                
