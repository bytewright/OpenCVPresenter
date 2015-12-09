# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import imutils
import time
import cv2


class OpenCVPresenter:
    def __init__(self, slidelist, useCamNumber):
        self.data = []
        self.minArea = 600
        self.currentSlideIndex = 0
        self.slideList = ["blabla", "bla2"]
        self.framecounter = 0
        self.detectMovement = True
        self.windowTitle = "presentation"
        self.keyframedistance = 50
        self.camera = cv2.VideoCapture(useCamNumber)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
        self.graykeyframe = None

    def getcontours(self, frame):
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if self.graykeyframe is None:
            self.graykeyframe = gray
            return []
        if self.framecounter >= self.keyframedistance:
            self.framecounter = 0
            self.graykeyframe = gray
        else:
            self.framecounter += 1

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(self.graykeyframe, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        return cnts

    def renderframe(self):
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            return "Error, nothing grabbed"
        if self.detectMovement:
            contours = self.getcontours(frame)
            for contour in contours:
                if cv2.contourArea(contour) < self.minArea:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, self.slideList[self.currentSlideIndex], (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow(self.windowTitle, frame)

    def run(self):
        print("yes")
        video_width = int(self.camera.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        video_height = int(self.camera.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        print("cam dimensions:"+str(video_width)+"/"+str(video_height))
        # initialize the first frame in the video stream
        while True:
            message = self.renderframe()
            #if message != "":
                #print(message)

            key = cv2.waitKey(1) & 0xFF
            # check for nextSlide
            if key == ord("a"):
                self.currentSlideIndex += 1
                if self.currentSlideIndex == len(self.slideList):
                    print("End of presentation reached")
                    self.currentSlideIndex -= 1
            if key == ord("s"):
                self.currentSlideIndex -= 1
                if self.currentSlideIndex < 0:
                    self.currentSlideIndex = 0
            # check for stop presentation
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                self.shutdown()
                break

    def shutdown(self):
        self.camera.release()
        cv2.destroyAllWindows()