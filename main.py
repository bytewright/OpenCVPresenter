import argparse
import os
import OpenCVPresenter
import csv


__author__ = 'Bit'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# load slides from asset folder

rawslideList = []
for mFile in os.listdir("./assets/"):
    if mFile.endswith(".txt"):
        print(mFile)
        rawslideList.append(mFile)
        #slideList.append(open("./assets/"+mFile, 'r').read())

slideList = []
slideIndex = 0
for mFile in rawslideList:
    with open("./assets/"+mFile) as csvFile:
        slide = {'index': str(slideIndex)}
        slideIndex += 1
        dialect = csv.Sniffer().sniff(csvFile.read(1024), delimiters=";,")
        csvFile.seek(0)
        reader = csv.DictReader(csvFile, dialect=dialect)
        # i = 0
        for row in reader:
            row['index'] = str(slideIndex)
            slideList.append(row.copy())
        #     if(i == 0):
        #         slide['title'] = row['content']
        #     else:
        #         slide['content'+str(i)] = row['content']
        #     i += 1
        #
        # print(slide)

# for mSlide in slideList:
#     for row in mSlide:
#             print(row)
presenter = OpenCVPresenter.OpenCVPresenter(slideList, 0)

presenter.run()