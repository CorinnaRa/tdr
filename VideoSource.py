#!/usr/bin/env python

import cv

class VideoSource:
    def __init__(self):
        self.capturing_device = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.capturing_device, cv.CV_CAP_PROP_FPS, 30)
        self.img = None
        #self.imageColor = cv.CreateImage([640,480], cv.IPL_DEPTH_8U, 3)

    def next(self):
        self.img = cv.QueryFrame(self.capturing_device)
        #cv.CvtColor(self.img, self.imageColor, cv.CV_GRAY2RGB)
        return self.img
        

       

