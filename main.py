import math
import time
import numpy as np
import cv2
from selenium import webdriver
from pathlib import Path
from PIL import Image

from notification import send_email


# Returns percent difference between reference and current images

class Monitor:

    def __init__(self, thresholds, links):

        self.links = links
        self.paths = []
        self.thresholds = thresholds
        self.chromeOptions = webdriver.ChromeOptions()
        self.chromeOptions.add_argument('--headless')
        self.chromeOptions.add_argument('window-size=1920,1440')
        self.chromeOptions.add_argument('--hide-scrollbars')

        for x in links:
            self.paths.append(Path(x))

    def similarity(self, current, reference):
        # reading images
        refImage = cv2.imread(reference)
        currImage = cv2.imread(current)

        # takes the absolute difference between the two images
        res = cv2.absdiff(refImage, currImage)

        # converts result to integer
        res = res.astype(np.uint8)

        # percentage difference number of pixels that are not 0
        percentage = (np.count_nonzero(res) * 100) / res.size
        print(percentage)
        return math.floor(percentage)

    def run(self):

        for link in self.paths:

            reference = ((str(link) + "reference.png").replace('\\', "").replace(':', ''))

            if not Path(reference).is_file():
                print('reference DNE, creating...')

                # Here Chrome  will be used
                driver = webdriver.Chrome(options=self.chromeOptions)

                # Opening the website
                driver.get(str(link))
                time.sleep(4)

                # saves reference image
                driver.save_screenshot(reference)

        while True:

            try:

                for threshold, link in enumerate(self.paths):

                    reference = (str(link) + "reference.png").replace("\\", "").replace(':', '')
                    current = (str(link) + "current.png").replace("\\", "").replace(':', '')

                    # opens website
                    driver = webdriver.Chrome(options=self.chromeOptions)
                    driver.get(str(link))
                    # saves screenshot of current state of website
                    time.sleep(4)
                    driver.save_screenshot(current)

                    # compares changes between reference and current images

                    comparison_result = self.similarity(current, reference)

                    if comparison_result < self.thresholds[threshold]:

                        print('no real changes', comparison_result)

                        continue

                    # if the difference is larger than 18%...
                    else:

                        print("something changed", comparison_result)

                        # send email here
                        send_email(self.links)

                        refImage = Image.open(reference)
                        image = Image.open(current)

                        image.show()
                        refImage.show()

                time.sleep(600)

            # To handle exceptions
            except Exception as e:
                print(e)


links = ["", ""]
thresholds = [2, 2]

newMonitor = Monitor(thresholds, links)
newMonitor.run()
