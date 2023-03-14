from psychopy import visual, monitors, core, event
from pathlib import Path
import random 
import csv


mon = monitors.Monitor('acer')

mon._loadAll()

stim_folder = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

stimuli = ["Blurred 1.jpg", "Blurred 2.jpg", "Blurred 3.jpg", "Group.jpg", 
"Individual 1.jpg", "Individual 2.jpg", 'Individual 3.jpg']

demographics = []

pics_shown = [(0,0)] #will store tuples for each image; for each, index 0 has stim folder, index 1 has stim type

ratings = []

data = []

win = visual.Window(fullscr = True, monitor = mon) 

#demographic window:
#age: textbox
#sex and sexual orientation: MC 
#textbox_1 = visual.Textbox2(win, text = '', editable = True)




for i in range(4): #loop to cycle through the images and have ppts rate each one
    
    folder = random.choice(stim_folder) #folder of images in stimuli
    stim_type = random.choice(stimuli) #type of image (group, blurred, or indvidual)
    while (folder, stim_type) in pics_shown or folder in pics_shown[i] or stim_type in pics_shown[i]:
        folder = random.choice(stim_folder) 
        stim_type = random.choice(stimuli)

    path_to_image_file = Path("/Users/akhil/psychopy_project/Stimulis") / folder / stim_type

    # simply pass the image path to ImageStim to load and display:
    image_stim = visual.ImageStim(win, image=path_to_image_file)


    ratingScale = visual.RatingScale(
        win, 
        labels = ['unattractive', 'attractive'], 
        marker = 'circle',
        scale = None,
        low = 1, high = 1000,
        showValue = False,
        acceptText = "click to accept"
        )

    while ratingScale.noResponse:
        image_stim.draw()
        ratingScale.draw()
        win.flip()
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    choiceHistory = ratingScale.getHistory()

    pics_shown.append((folder, stim_type))
    ratings.append(rating)
    data.append([folder, stim_type, rating])
    
del pics_shown[0]


#make code that saves answers to a csv file
#make it so that a new one is made every time you run the code

csv_files = list(Path("csv_files").iterdir())
header = ["Image Folder", "Image Type", "Rating"]

if len(csv_files) == 0:
    with open(Path("csv_files")/'results0.csv', 'w', encoding='UTF8', newline= '') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)

else:
    index = str(len(csv_files))
    with open(Path("csv_files")/('results'+index+'.csv'), 'w', encoding='UTF8', newline= '') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)


# make a loop, have it loop through each picture and for each picture, give a slider to rate attractiveness
# and a next button to go to the next image
# then ask demographic questions to the participant and store their answers in a list
# and have a list/dictionary that stores the responses of the participants and then puts them in a file (csv maybe, ask about this)
#things to ask:
#   -should the images be randomized?
#   - what file should the results be stored in?
#   - is there anything else you want the code to do?

#Should it be somewhat in ZAPS format?
#   - would be useful, once we have the heart of the program we can add it to the frontend
#   - maybe add in catch-all trials to check if ppts are truly paying attention

#  totally randomize it; simplest thing to do is just have every trial be a random occurence
#  write files to a csv file; record image name, face, info about person
# you have all these variables(image name, etc.) that are written to a csv file

#demographic info: age, sex, sexual orientation