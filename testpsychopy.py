from psychopy import visual, monitors, core, event
from pathlib import Path
import random 
import csv
import re
from demographic import questionnaire, data_demo
from introduction import intro, mon, stim_folder, stimuli, win, mouse
from additional_functions import arrow_choice, new_csv, update_data

pics_shown = [(0,0)] #will store tuples for each image; for each, index 0 has stim folder, index 1 has stim type

ratings = []

data = [] # data will be stored in lists containing: image and corresponding folder, condition, face, rating

#for catch trial
path_to_zendaya = Path("/Users/akhil/attraction-rater-task/Stimulis/zendaya.jpg")
zendaya_intro = visual.ImageStim(win, image=path_to_zendaya, size=(0.6, 0.8))

#main experiment function
def run_experiment(iterations):

    intro()

    for i in range(iterations): #loop to cycle through the images and have ppts rate each one

        if i == int(iterations/2):
            folder = "None"
            stim_type = "Zendaya"
            arrow_type = arrow_choice(stim_type)
            image_stim = zendaya_intro
            
        else:
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
        arrow = visual.ShapeStim(win,color=[-1,-1,-1], vertices=arrow_type, lineColor='white', fillColor='white')

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
            acceptText = "click to accept",
            textColor = 'red',
            lineColor = 'red'
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

        update_data(folder, stim_type, rating, arrow_type, data)

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
            index = str(len(csv_files)+1)
            new_csv(header, data, index, data_demo)

        else:
            new_csv(header, data, index, data_demo)

run_experiment(3)


