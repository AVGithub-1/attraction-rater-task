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

data = [] # data will be stored in lists containing: image and corresponding folder, condition, face, rating



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
    
def update_data(folder, stim_type, rating, arrow_type):
    """
    this function uses regular expressions and string concatenation to update the data list with
    specificly-formatted information about each trial

    Parameters:
    
    """
    condition = stim_type.replace('.jpg', '')
    condition = condition.replace(' ', '')

    pattern = r'[0-9]'

    condition = re.sub(pattern, '', condition)

    image = condition + "_" + folder

    face = folder 
    #initial value for face is the folder, next the specific face will be appended
    #the specific face will be denoted, from left to right, as a, b, or c

    if condition == "Blurred" or condition == 'Group':
        if arrow_type == l_vertices:
            face += 'a'
        elif arrow_type == m_vertices:
            face += 'b'
        elif arrow_type == r_vertices:
            face += 'c'
    
    if condition == "Individual":
        if stim_type.__contains__('1'):
            face += 'a'
        elif stim_type.__contains__('2'):
            face += 'b'
        elif stim_type.__contains__('3'):
            face += 'c'

    data.append([image, condition, face, rating])
    

def new_csv(header, data, index):
    with open(Path("csv_files")/('results'+index+'.csv'), 'w', encoding='UTF8', newline= '') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)


def run_experiment(iterations):

    for i in range(iterations): #loop to cycle through the images and have ppts rate each one
        
        folder = random.choice(stim_folder) #folder of images in stimuli
        stim_type = random.choice(stimuli) #type of image (group, blurred, or indvidual)
        while (folder, stim_type) in pics_shown or folder in pics_shown[i] or stim_type in pics_shown[i]:
            folder = random.choice(stim_folder) 
            stim_type = random.choice(stimuli)

        #gets the path of the specific stimuli
        #Note: the string in Path() will have to be changed to the specific directory this project is in on your
        #computer
        path_to_image_file = Path("/Users/akhil/psychopy_project/Stimulis") / folder / stim_type

        # simply pass the image path to ImageStim to load and display:
        image_stim = visual.ImageStim(win, image=path_to_image_file)

        image_stim.draw()
        win.flip()
        core.wait(1)


        # Create a blank stimulus as a buffer between the stimuli and the arrow
        # blank = visual.TextStim(win, text='')

        # # Display the blank stimulus
        # blank.draw()
        # win.flip()
        # core.wait(1)


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

        update_data(folder, stim_type, rating, arrow_type)

    del pics_shown[0]

    #this part of the function makes a new csv file and puts all of the subject's data in it
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
        directory = Path("/Users/akhil/psychopy_project/csv_files") 

        # Specify the filename of the CSV file
        filename = "results" + index + ".csv"

        # Check if the file exists in the directory
        csv_file_path = directory / filename

        if csv_file_path.is_file():
            new_csv(header, data, index)

        else:
            index = str(len(csv_files)+1)
            new_csv(header, data, index)

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


run_experiment(4)