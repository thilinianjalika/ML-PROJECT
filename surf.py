from cv2 import SURF, imread
import sys
from scipy.cluster.vq import kmeans2, vq
from sklearn import svm
import numpy

features = []

if( len( sys.argv ) != 3 ):
    print ("Usage: $python surf.py imagelist.txt <i: 0...number_of_images-1>")

for im in open( sys.argv[ 1 ] ):
    img = imread( im.strip() )
    
    surf = SURF( 500 )
    keypoints, descriptors = surf.detectAndCompute( img, None )
    
    features.extend( descriptors )
    
    #for k in keypoints:
        #x, y = [ int( y ) for y in k.pt ]
        #circle( img, ( x, y ), 2, ( 0, 0, 255 ) )
    #imshow( "Features", img )
    #waitKey()
np_features = numpy.array( features )
centroids, labels = kmeans2( np_features, 50 )
print (labels)

counter = 0
X = []
Y = []
files = []

for im in open( sys.argv[ 1 ] ):
    files.append( im.strip() )
    counts = numpy.zeros( 50 )
    img = imread( im.strip() )
    k, d = surf.detectAndCompute( img, None )
    labels, _ = vq( numpy.array( d ), centroids )
    for i in labels:
        counts[ i ] += 1
    X.append( counts.tolist() )
    Y.append( counter )
    counter += 1
    
lin_clf = svm.LinearSVC()
lin_clf.fit( X, Y )
trial = int( sys.argv[ 2 ] )

print (files[ trial ], ": ", files[ lin_clf.predict( X[ trial ] ) ])