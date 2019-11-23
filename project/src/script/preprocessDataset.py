import os
import sys
import cv2 as cv

# Script converts img you get after finding interesting are
# to form that is good for CNN applying some filters.
# It resizes img to 64x64, extract borders by Sobel
# amd makes it black and white

if len(sys.argv) != 2:
    print('Usage: dir (script is recursive)')
    exit(0)

walk_dir = sys.argv[1]

print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

# for each file in the hierarchy
for root, subdirs, files in os.walk(walk_dir):

    for subdir in subdirs:
        print('\t- working in ' + subdir)

    for filename in files:
        file_path = os.path.join(root, filename)
        img = cv.imread(file_path)
        img = cv.resize(img, (64, 64))
        img = cv.Sobel(img, cv.CV_8UC1, 1, 1)  # get borders
        _, img = cv.threshold(img, 9, 255, cv.THRESH_BINARY)  # make it B&W only
        cv.imwrite(file_path, img)
