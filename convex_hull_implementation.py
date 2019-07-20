
#------------------------------------#
# Author: Yueh-Lin Tsou              #
# Update: 7/20/2019                  #
# E-mail: hank630280888@gmail.com    #
#------------------------------------#

"""---------------------------------------------
Implement Convex Hull by using Graham's Scan
---------------------------------------------"""

# Import OpenCV Library, numpy and command line interface
from random import randint # random function for generate points
from math import atan2 # calculate theta
import numpy as np
import argparse
import cv2

# -------------------------- Gnenerate random points -------------------------- #
def create_points(number,min=0,max=500):
	return [[randint(min,max),randint(min,max)] for _ in range(number)]

# ------------------------ calculate theta for sorting ------------------------ #
def theta(p):
	return atan2(p[1]-start[1],p[0]-start[0])

# ----------- calculate distance from start points when same theta ------------ #
def distance(p):
    return (p[1]-start[1])**2 + (p[0]-start[0])**2

# -------------------- sort points with theta and distance -------------------- #
def MergeSort(points, result, begin, end):
    if(begin>=end): return

    mid = (end - begin)//2+begin
    begin_1, end_1 = begin, mid
    begin_2, end_2 = mid+1, end

    MergeSort(points, result, begin_1, end_1)
    MergeSort(points, result, begin_2, end_2)

    k = begin
    while(begin_1 <= end_1 and begin_2 <= end_2):
        if(theta(points[begin_1])<theta(points[begin_2])):
            result[k] = points[begin_1]
            begin_1 = begin_1+1
            k = k+1
        elif(theta(points[begin_1])== theta(points[begin_2])):
            if(distance(points[begin_1])>distance(points[begin_2])):
                result[k] = points[begin_1]
                begin_1 = begin_1+1
                k = k+1
            else:
                # result[k] = points[begin_2]
                begin_2 = begin_2+1
                # k = k+1
        else:
            result[k] = points[begin_2]
            begin_2 = begin_2+1
            k = k+1

    while(begin_1 <= end_1):
        result[k] = points[begin_1]
        begin_1 = begin_1+1
        k = k+1

    while(begin_2 <= end_2):
        result[k] = points[begin_2]
        begin_2 = begin_2+1
        k = k+1

    for k in range(begin, end+1):
        points[k] = result[k]

# -------------------- canvex hull or not -------------------- #
def judge(p1, p2, p3):
    return (p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])

# -------------------- Graham's Scan Algorithm -------------------- #
def graham_scan(points):
    global start
    start = None

    # find first points (bottommost + leftmost)
    for i, (x,y) in enumerate(points):
        if start is None or y < start[1]:
            start = points[i]
        if start[1] == y and start[0] > x:
            start = points[i]

	# remove start point form the points group
    del points[points.index(start)]

	# sort the points by theta and distance
    result = len(points)*[None]
    MergeSort(points, result, 0, len(points)-1)

	# Graham's Scan Algorithm
    hull=[start,points[0]]
    for p in (points[1:]):
        while judge(hull[-2], hull[-1], p) <= 0:
            del hull[-1]
        hull.append(p)

    return hull

# -------------------- function to draw the random points -------------------- #
def draw_points(image, points):
    for i in range(len(points)):
        cv2.circle(image,(points[i][0], points[i][1]), 2, (0, 255, 0), 3)


if __name__ == '__main__':
    # command line >> python convex_hull_test.py

	# generate points
	pts=create_points(50)
	# generate black image
	blank_image = np.zeros((600,600,3), np.uint8)
	# calculate convex hull by using graham scan
	hull=graham_scan(pts)
	# draw convex hull and points
	contour_img = cv2.drawContours(blank_image, [np.asarray(hull)], -1, (255,0,0), 3)
	draw_points(blank_image, pts)

	# show the result
	cv2.imshow("result", blank_image)

	k = cv2.waitKey(0)
	if k == 27:         # wait for ESC key to exit
		cv2.destroyAllWindows()
