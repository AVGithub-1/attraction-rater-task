from psychopy import visual, monitors, core, event
from pathlib import Path
import random 
import csv
import re


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

m_vertices = [(-0.15,1), (0.15,1), (0.15,0.5), (0.3,0.5), (0,0), (-0.3,0.5),(-0.15,0.5)]

l_vertices = [(-0.65,1), (-0.35,1), (-0.35,0.5), (-0.2,0.5), (-0.5,0), (-0.8,0.5),(-0.65,0.5)]

r_vertices = [(0.35,1), (0.65,1), (0.65,0.5), (0.8,0.5), (0.5,0), (0.2,0.5),(0.35,0.5)]


def arrow_choice(stim):
    if stim == "Blurred 1.jpg":
        return l_vertices
    elif stim == "Blurred 2.jpg":
        return m_vertices
    elif stim == "Blurred 3.jpg":
        return r_vertices
    elif stim == "Group.jpg":
        return random.choice([m_vertices, r_vertices, l_vertices])
    else:
        return m_vertices

for i in range(20): #loop to cycle through the images and have ppts rate each one
    
    folder = random.choice(stim_folder) #folder of images in stimuli
    stim_type = random.choice(stimuli) #type of image (group, blurred, or indvidual)
    while (folder, stim_type) in pics_shown or folder in pics_shown[i] or stim_type in pics_shown[i]:
        folder = random.choice(stim_folder) 
        stim_type = random.choice(stimuli)

    path_to_image_file = Path("/Users/akhil/psychopy_project/Stimulis") / folder / stim_type

    # simply pass the image path to ImageStim to load and display:
    image_stim = visual.ImageStim(win, image=path_to_image_file)

    image_stim.draw()
    win.flip()
    core.wait(1)


    # Create a blank stimulus
    blank = visual.TextStim(win, text='')

    # Display the blank stimulus
    blank.draw()
    win.flip()
    core.wait(1)


    arrow_type = arrow_choice(stim_type)
    # Create a shape stimulus for the arrow
    arrow = visual.ShapeStim(win, vertices=arrow_type, lineColor='white', fillColor='white')

    # Display the arrow for 1 seconds
    arrow.draw()
    win.flip()
    core.wait(1)

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
        ratingScale.draw()
        win.flip()


    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    choiceHistory = ratingScale.getHistory()

    #update list of ratings and list of pictures already shown
    pics_shown.append((folder, stim_type))
    ratings.append(rating)

del pics_shown[0]



def update_data(folder, stim_type, rating):
    """
    this function uses regular expressions and string concatenation to update the data list with
    specificly-formatted information about each trial
    """
    image = stim_type - ".jpg" 

    pattern = r'[0-9]'

    image = re.sub(pattern, '', image)

    data.append([image, stim_type, rating])



#make code that saves answers to a csv file
#make it so that a new one is made every time you run the code

csv_files = list(Path("csv_files").iterdir())
header = ["Image", "Condition", "Face", "Subject Rating"]

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