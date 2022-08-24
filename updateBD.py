import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import numpy as np


class DBUpdate():

    def __init__(self):
        
        self.emptySearchHalf="http://airfoiltools.com/search/index?m%5BtextSearch%5D=&m%5BmaxCamber%5D=&m%5BminCamber%5D=&m%5BmaxThickness%5D=&m%5BminThickness%5D=&m%5Bgrp%5D=&m%5Bsort%5D=1&m%5Bpage%5D="
        self.emptySearchOHalf="&m%5Bcount%5D=1638"

        
        if os.path.exists("airfoilKeys.npy"):
            self.airfoilKeys=np.load("airfoilKeys.npy")
        else:
            self.airfoilKeys=[]

    def UpdateKeys(self):
        i=0
        while True:
            response=requests.get(self.emptySearchHalf+str(i)+self.emptySearchOHalf)
            if len(self.airfoilKeys)>=1638:
                print("Scraped all airfoil names.")
                break
            else:
                print(f"progress={len(self.airfoilKeys)/1638*100}%")
            page=response.content
            soup=BeautifulSoup(page,"html.parser")
            titles=soup.find_all("h3")

            for title in titles:
                strTag=str(title)
                if not "class" in strTag:
                    strTag=strTag[4:-5]
                    self.airfoilKeys.append(strTag[1:].split(")")[0])
            i+=1

            airfoilKeys=np.save("airfoilKeys.npy",np.array(airfoilKeys))

    