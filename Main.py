import random
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import csv
import array
import psychopy


stim_folder = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

stimuli = ["Blurred 1.jpg", "Blurred 2.jpg", "Blurred 3.jpg", "Group.jpg", 
"Individual 1.jpg", "Individual 2.jpg", 'Individual 3.jpg']

photos=["a1","a2","a3","a4","b1","b2","b3","b4","c1","c2","c3","c4","d1","d2","d3","d4"]
numberRows = 4
numberCols = 4
inds = [(x,y) for x in range(numberRows) for y in range(numberCols)]
def make_random(Array):
    """
    this function is meant to take the photo array(or any array like it) and randomize
    it so that each image has different people and is a different type(blurred, group, etc.)
    of photo than the previous image in the array
    """
    toRet = []
    n = len(Array)
    for i in range(n): #iterates through the length of the array
        possible = [num for num in Array if num not in toRet]
        prev = poss = None
        while poss is None:
            next_val = random.choice(possible)
            if next_val == prev:
                return make_random(Array)
            if not toRet or (next_val[0] != toRet[-1][0] and next_val[1] != toRet[-1][1]):
                poss = next_val 
            prev = next_val
        toRet += poss,
    return toRet



ActualArray= [thing for thing in make_random(photos)]
print (ActualArray)

Result = []
n = 0

while n < 16:
    if n == 16:
        break

    ImageAddress = '/users/akhil/psychopy_project/' + ActualArray[n]+ '.jpg'
    ImageItself = Image.open(ImageAddress)
    ImageNumpyFormat = np.asarray(ImageItself)
    plt.imshow(ImageNumpyFormat)
    plt.draw()
    plt.pause(1) # pause how many seconds
    plt.close()
    test = input("How attractive are they? ")
    Result.append(test)

    n = n + 1


print (Result) 


data = pd.DataFrame({"Question" : ActualArray, "Answer" : Result})
data.to_csv("sample.csv", index=False)



