import os
import sys
from PIL import Image, ImageDraw


# this file's folder
currentDir = os.path.dirname(os.path.abspath(__file__))
workingDir = currentDir + '/output'
suffix = '-data'
files = ['scene1']

for file in files:
	origImage = workingDir + '/' + file + '.jpg'
	dataFilePath = workingDir + '/' + file + suffix + '.txt'
	dataFile = open(dataFilePath, 'r')
	lines = dataFile.readlines()
	dataFile.close()
	img = Image.open(origImage)
	h = img.size[1]
	draw = ImageDraw.Draw(img)
	for line in lines[1:]:
		coords = [int(l.strip()) for l in line.split(',')]
		print(coords)
		draw.rectangle(((coords[0], h - coords[1]), (coords[2], h-coords[3])))
	img.save(workingDir + '/' + file + '-box.jpg', "JPEG")
