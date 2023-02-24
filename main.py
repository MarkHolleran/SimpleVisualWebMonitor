import math
import time
import numpy as np
import cv2
from selenium import webdriver
from pathlib import Path
from PIL import Image

# Returns percent difference between reference and current images

class Monitor:

    def __init__(self,threshold,path,url):
        self.deltaThreshold = threshold
        self.path = Path(path)
        self.url = url

    def similarity(self):
        # reading images
        refImage = cv2.imread('reference.png', 0)
        currImage = cv2.imread('current.png', 0)

        # takes the absolute difference between the two images
        res = cv2.absdiff(refImage, currImage)

        # converts result to integer
        res = res.astype(np.uint8)

        # percentage difference number of pixels that are not 0
        percentage = (np.count_nonzero(res) * 100) / res.size

        return math.floor(percentage)

    def run(self):

        if not self.path.is_file():
            print('reference DNE, creating...')

            # Here Chrome  will be used
            driver = webdriver.Chrome()

            # Opening the website
            driver.get(self.url)
            # saves reference image
            driver.save_screenshot("reference.png")

        while True:
            try:
                # opens website
                driver = webdriver.Chrome()
                driver.get(self.url)
                # saves screenshot of current state of website
                driver.save_screenshot("current.png")

                # compares changes between reference and current images
                if self.similarity() < self.deltaThreshold:

                    print('no real changes')
                    time.sleep(30)
                    continue

                # if the difference is larger than 18%...
                else:

                    print("something changed")

                    refImage = Image.open("reference.png")
                    image = Image.open("current.png")

                    image.show()
                    refImage.show()

                    time.sleep(30)

                    break

            # To handle exceptions
            except Exception as e:
                print(e)


newMonitor = Monitor(18,'reference.png', "https://google.com")


newMonitor.run()