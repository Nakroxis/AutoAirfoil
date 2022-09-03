import os
from time import sleep, time
import requests
from bs4 import BeautifulSoup
import numpy as np
import json

##TODO: add option to download airfoil image and dat file

class AirfoilDB():

    def __init__(self):
        
        self.emptySearchHalf="http://airfoiltools.com/search/index?m%5BtextSearch%5D=&m%5BmaxCamber%5D=&m%5BminCamber%5D=&m%5BmaxThickness%5D=&m%5BminThickness%5D=&m%5Bgrp%5D=&m%5Bsort%5D=1&m%5Bpage%5D="
        self.emptySearchOHalf="&m%5Bcount%5D=1638"
        self.reynoldsList=[50*1000,100*1000,200*1000,500*1000,1000*1000]
        
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
            np.save("airfoilKeys.npy",np.array(self.airfoilKeys))
        self.airfoilKeys=np.load("airfoilKeys.npy")

    def parseAirfoilData(rawData):

        
        # with open("test/testData.html",'r') as testData:
        testSoup= BeautifulSoup(rawData,"html.parser")
        scs=testSoup.find_all("script")
        if len(scs)==0:
            return []
        for sc in scs:
            if "$.jqplot" in str(sc):
                plotsc= str(sc)
                break

        indexes=[   plotsc.find('liftdrag'),
                    plotsc.find('liftaoa'),
                    plotsc.find('momentaoa'),
                    plotsc.find('dragaoa'),
                    plotsc.find('effaoa'),
                    -1]

        data=[]
        for i in range(len(indexes)-1):
            rawSlice=plotsc[indexes[i]:indexes[i+1]]
            start=rawSlice.find("[[[")
            end=rawSlice.find("{")
            dataslice=rawSlice[start:end]
            dataslice=dataslice.replace("],],],","]]]")
            dataslice=dataslice.replace(",]","]")
            dataslice=dataslice.replace("\n","")
            dataslice=dataslice.replace(" ","")
            dataslice=dataslice.replace("'","'")
            try:
                evaled=json.loads(dataslice)
                data.append(evaled)
            except:
                print("unusable format")

        return data


    def downloadDataPoints(self,key):
        if not os.path.exists(f"data/{key}.npy") :
            url="http://airfoiltools.com/polar/plot?a="
            #url + name-reynold_colorcode or name-reynold-n5_colorcode, name-reynold_colorcode or name-reynold-n5_colorcode,...
            flag=True
            for rey in self.reynoldsList:
                url+="xf-"+key+f"-{rey}_ffffff,xf-"+key+f"-{rey}-n5_ffffff,"
            url=url.removesuffix(",")
            response=requests.get(url)
            data=AirfoilDB.parseAirfoilData(response.content)
            if len(data)>0:
                np.save(f"data/{key}.npy",np.array(data,dtype=object))

    def downloadAll(self):
        i=0
        start=time()
        if len(self.airfoilKeys)==0:
            self.UpdateKeys()
        for key in self.airfoilKeys:
            i+=1
            if i%10 ==0:
                print(f"progress={(i+1)/1638*100},time elapsed={time()-start}")
            self.downloadDataPoints(key)
        

foildb=AirfoilDB()
foildb.downloadAll()