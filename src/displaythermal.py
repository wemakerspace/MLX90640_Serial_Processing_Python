import serial
import numpy as np
import cv2
import math


ser = serial.Serial("/dev/ttyACM0", 115200)

if ser.is_open == False:
	ser.open()

nmin = 0
nmax = 255

frames = 0
index = 0
temp = 0
while True:
	frames+=1
	recv = ser.readline()
	recv = recv.rstrip() #strip the return character

	#next job, split on , stick the data in an array
	data = np.fromstring(recv, dtype=float, count=-1, sep=',') #get the data
	#print(data)


	heatmap = np.zeros((24,32,3), np.uint8) #create the blank image to work from
	#add to the image
	index = 0
	if len(data) == 768: #Check we have good data!
		for y in range (0,24):
			for x in range (0,32):
				val = (data[index]*10)-100
				if math.isnan(val):
					val = 0
				if val > 255:
					val=255
				#print(index)
				#print(data)

				heatmap[y,x] = (val,val,val)
	
				if(y == 12) and (x == 16):
					temp = data[index]

				index+=1

	heatmap = cv2.rotate(heatmap, cv2.ROTATE_90_CLOCKWISE)#rotate
	heatmap = cv2.flip(heatmap, 1 ) #flip heatmap
	heatmap = cv2.normalize(heatmap,None,nmin,nmax,cv2.NORM_MINMAX)
	heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
	heatmap = cv2.resize(heatmap,(240,320),interpolation=cv2.INTER_CUBIC)


	# Display the resulting frame
	cv2.namedWindow('Thermal',cv2.WINDOW_NORMAL)
	# display black box for our data
	cv2.rectangle(heatmap, (0, 0),(90, 15), (0,0,0), -1)
	# put text in the box
	cv2.putText(heatmap,'Temp: '+str(temp), (10, 10),\
	cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0, 255, 255), 1, cv2.LINE_AA)

	# draw crosshairs
	cv2.line(heatmap,(120,150),(120,170),(0,0,0),1) #vline
	cv2.line(heatmap,(110,160),(130,160),(0,0,0),1) #hline


	cv2.imshow('Thermal',heatmap)

	res = cv2.waitKey(1)
	#print(res)

	if res == 113: #q
		break
	if res == 97: #a
		nmin += 10
		print(nmin)
	if res == 122: #z
		nmin -= 10
		print(nmin)
	if res == 115: #s
		nmax += 10
		print(nmax)
	if res == 120: #x
		nmax -= 10
		print(nmax)



cv2.destroyAllWindows()

