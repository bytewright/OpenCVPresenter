import argparse
import os
import OpenCVPresenter

__author__ = 'Bit'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# load slides from asset folder

slideList = []
for mFile in os.listdir("./assets/"):
    if mFile.endswith(".txt"):
        slideList.append(open("./assets/"+mFile, 'r').read())

for txtFile in slideList:
    print(txtFile)

presenter = OpenCVPresenter.OpenCVPresenter(slideList, 0)

presenter.run()