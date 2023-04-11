from psychopy import visual, monitors, core, event
from pathlib import Path
import random 
import csv
import re
from demographic import questionnaire, data_demo


mon = monitors.Monitor('acer')

mon._loadAll()

stim_folder = []
for i in range(1,4):#51):
    stim_folder.append(str(i)) #this adds every number from 1 to 50 to the folder list

stimuli = ["Faceless 1.jpg", "Faceless 2.jpg", "Faceless 3.jpg", "Group.jpg", 
"Individual 1.jpg", "Individual 2.jpg", 'Individual 3.jpg']


pics_shown = [(0,0)] #will store tuples for each image; for each, index 0 has stim folder, index 1 has stim type

ratings = []

data = [] # data will be stored in lists containing: image and corresponding folder, condition, face, rating



win = visual.Window(fullscr = True, monitor = mon) 



m_vertices = [(-0.15,1), (0.15,1), (0.15,0.5), (0.3,0.5), (0,0), (-0.3,0.5),(-0.15,0.5)]

l_vertices = [(-0.65,1), (-0.35,1), (-0.35,0.5), (-0.2,0.5), (-0.5,0), (-0.8,0.5),(-0.65,0.5)]

r_vertices = [(0.35,1), (0.65,1), (0.65,0.5), (0.8,0.5), (0.5,0), (0.2,0.5),(0.35,0.5)]


def arrow_choice(stim):
    if stim == "Faceless 1.jpg":
        return l_vertices
    elif stim == "Faceless 2.jpg":
        return m_vertices
    elif stim == "Faceless 3.jpg":
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

    if condition == "Faceless" or condition == 'Group':
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
        for d in data:
            writer.writerow(list(data_demo.values())+ d)


def run_experiment(iterations):

    for i in range(iterations): #loop to cycle through the images and have ppts rate each one
        
        folder = random.choice(stim_folder) #folder of images in stimuli
        stim_type = random.choice(stimuli) #type of image (group, blurred, or indvidual)
        arrow_type = arrow_choice(stim_type)
        while (folder, stim_type, arrow_type) in pics_shown: #or folder in pics_shown[i] or stim_type in pics_shown[i]:
            folder = random.choice(stim_folder) 
            stim_type = random.choice(stimuli)
            arrow_type = arrow_choice(stim_type)

        #gets the path of the specific stimuli
        #Note: the string in Path() will have to be changed to the specific directory this project is in on your
        #computer
        path_to_image_file = Path("/Users/akhil/attraction-rater-task/Stimulis") / folder / stim_type

        # simply pass the image path to ImageStim to load and display:
        image_stim = visual.ImageStim(win, image=path_to_image_file)

        image_stim.draw()
        win.flip()
        core.wait(1)

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
        pics_shown.append((folder, stim_type, arrow_type))
        ratings.append(rating)

        update_data(folder, stim_type, rating, arrow_type)

    del pics_shown[0]

    #this part of the function makes a new csv file and puts all of the subject's data in it
    csv_files = list(Path("csv_files").iterdir())
    header = ["Subject #", "Age", "Gender", "SexOr", "Hispanic", "Races", "Image", 
              "Condition", "Face", "Subject Rating"]


    if len(csv_files) == 0:
        with open(Path("csv_files")/'results0.csv', 'w', encoding='UTF8', newline= '') as f:
            writer = csv.writer(f)


            writer.writerow(header)

            # write multiple rows
            for d in data:
                writer.writerow(list(data_demo.values())+ d)

    else:
        index = str(len(csv_files))
        directory = Path("csv_files") 

        # Specify the filename of the CSV file
        filename = "results" + index + ".csv"

        # Check if the file exists in the directory
        csv_file_path = directory / filename

        if csv_file_path.is_file():
            new_csv(header, data, index)

        else:
            index = str(len(csv_files)+1)
            new_csv(header, data, index)

run_experiment(2)


# One thing to fix: There may be something wrong with the while loop 
# because in results11.csv, Group_2 face 2c and Group_1 face 2b repeats