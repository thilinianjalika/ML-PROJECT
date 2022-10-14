import cv2
import matplotlib.pyplot as plt
from curve_fit import fitPolynomial
import numpy as np
import sys
from curve_fit import yForX


def edgeConv( StrImg ):
	image = cv2.LoadImageM( StrImg )
	gray = cv2.CreateImage( cv2.GetSize(image), 8, 1 )
	edges = cv2.CreateImage( cv2.GetSize(image), 8, 1 )

	cv2.CvtColor( image, gray, cv2.CV_BGR2GRAY )
	cv2.Canny( gray, edges, 50, 200 )
	#print edges[399,699]
	return edges

def divPlot( edges, tileNoX = 3, tileNoY = 3 ):
	tileSizeX = int( edges.width / tileNoX )#149
	tileSizeY = int( edges.height / tileNoY )#105
	graphMat = [ [ [0] * 3 ] * tileNoY ] * tileNoX
	j = 0
	print ("edges.width,edges.height")
	print ('xtile='+str(tileSizeX)+' ytile='+str(tileSizeY))

	while j <= ( edges.height - tileSizeY ):
		print ('j=',j)
		i = 0
		while i <= ( edges.width - tileSizeX ):
			curveFit( edges, i, j, tileSizeX, tileSizeY, graphMat )
			print ('i=',i)
			i += tileSizeX
		j += tileSizeY
	return graphMat

def curveFit( edges, X, Y, tilesizeX, tilesizeY, graphMat ):
	xCoords = []
	yCoords = []
	try:
		for j in range( Y, Y + tilesizeY ):
			#print j
			for i in range( X, X + tilesizeX):
				if edges[ j, i ] == 255:
					yCoords.append( i % tilesizeX )
					xCoords.append( j % tilesizeY )
	except:
		print ('')
		#print "error!!"
		#print i,j
		#print X,Y,tilesizeX,tilesizeY
	#print i,j
	#print X,Y,tilesizeX,tilesizeY
	#print xCoords,yCoords
	# plt.plot( xCoords, yCoords, 'o' )
	# plt.show()
	if xCoords!=[]:	
		result = fitPolynomial( xCoords, yCoords, 3 )
		X1 = range( min( xCoords ), max( xCoords ) )
		Y1 = [ yForX( x,  result, 3 ) for x in X1 ]
		plt.plot( X1, Y1, 'k', xCoords, yCoords, 'o' )
		plt.show()
		graphMat[ int( Y / tilesizeY )-1 ][ int( X / tilesizeX )-1 ] = result
 
if __name__ == '__main__':
	#cv.SaveImage('display.jpg',edges)
	edges = edgeConv(sys.argv[1])
	divPlot(edges)
