from additional_functions import arrow_choice, l_vertices, m_vertices, r_vertices
from settings import *
from psychopy import visual, monitors, core, event
from pathlib import Path
import random 



mon = monitors.Monitor('acer')

mon._loadAll()


stim_folder = []
for i in range(stim_folder_start,stim_folder_end+1):
    stim_folder.append(str(i)) #this adds every number from 1 to 50 to the folder list

stimuli = ["Faceless 1.jpg", "Faceless 2.jpg", "Faceless 3.jpg", "Group.jpg", 
"Individual 1.jpg", "Individual 2.jpg", 'Individual 3.jpg']


win = visual.Window(fullscr = True, monitor = mon, color=[1,1,1]) 
mouse = event.Mouse(win=win)



def intro():
     #consent form
    with open('consentinfo.txt', 'r') as file1:
        consent_text = file1.read()

    with open('consentinfo2.txt', 'r') as file2:
        consent_text2 = file2.read()

    consent1 = visual.TextBox2(win,color=[-1,-1,-1], text = consent_text, size = [1.5,None])
    consent2 = visual.TextBox2(win,color=[-1,-1,-1], text = consent_text2, size = [1.5,None])
    cont_button = visual.TextBox2(win,color=(-1,-1,-1), text = 'continue', fillColor='grey',
                               pos = (0,-.8), size = [0.15,0.15], alignment='center')
    
    path_to_image_file_1 = Path(stim_folder_path)/"1"/"Group.jpg"
    path_to_image_file_2 = Path(stim_folder_path)/"3"/"Faceless 1.jpg"

    practice1 = visual.TextBox2(win,color=[-1,-1,-1], pos=(0,0.5), text = 'The experiment will consist of several trials. In each trial, a photo with people\'s faces, will be shown for 1 s. Like this:')
    example_image = visual.ImageStim(win, image=path_to_image_file_1, size=(0.6, 0.8))

    practice2 = visual.TextBox2(win,color=[-1,-1,-1], pos=(0,0.5), text = 'After that, an arrow will appear for 1 s above the face that needs to be rated on. Like this:')
    example_arrow = visual.ShapeStim(win, vertices=m_vertices, lineColor='black', fillColor='black', pos=(0,-0.6))

    practice3 = visual.TextBox2(win,color=[-1,-1,-1], pos=(0,0.5), text = 'You will then need to rate the attractiveness of the face the arrow pointed to. You will form the rating by moving a mouse to set a marker on a continuous scale from unattractive to attractive.')
    example_rater = ratingScale = visual.RatingScale(
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
    
    practice4 = visual.TextBox2(win,color=[-1,-1,-1], alignment = 'center', text = 'Let\'s do a couple of trials to try!')

    catch_trial_text = visual.TextBox2(win,color=[-1,-1,-1], pos=(0,0.5), text = 'During the study, one of the trials will show a photo of Zendaya (shown below), when you see the photo here, please move the marker to the right of the scale.')
    path_to_zendaya = Path(stim_folder_path) / "zendaya.jpg"
    zendaya_intro = visual.ImageStim(win, image=path_to_zendaya, size= (0.8/aspect_ratio , 0.8), pos = (0,-0.2))


    while mouse.isPressedIn(cont_button) == False:
        consent1.draw()
        cont_button.draw()
        win.flip()
    

    mouse.clickReset()
    core.wait(0.5)

    while mouse.isPressedIn(cont_button) == False:
        consent2.draw()
        cont_button.draw()
        win.flip()

    mouse.clickReset()
    core.wait(0.5)
    #do practice trials
    while mouse.isPressedIn(cont_button) == False:
        practice1.draw()
        example_image.draw()
        cont_button.draw()
        win.flip()
    
    mouse.clickReset()
    core.wait(0.5)

    while mouse.isPressedIn(cont_button) == False:
        practice2.draw()
        example_arrow.draw()
        cont_button.draw()
        win.flip()
    
    mouse.clickReset()
    core.wait(0.5)

    while example_rater.noResponse:
        practice3.draw()
        example_rater.draw()
        win.flip()

    while mouse.isPressedIn(cont_button) == False:
        practice4.draw()
        cont_button.draw()
        win.flip()
    
    for i,j in zip([path_to_image_file_1, path_to_image_file_2],[m_vertices,l_vertices]):
    
        image_stim = visual.ImageStim(win, image=i)

        image_stim.draw()
        win.flip()
        core.wait(image_display_time)

        arrow = visual.ShapeStim(win,color=[-1,-1,-1], vertices=j, lineColor='black', fillColor='black')

        arrow.draw()
        win.flip()
        core.wait(arrow_display_time)

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

    while mouse.isPressedIn(cont_button) == False:
        catch_trial_text.draw()
        zendaya_intro.draw()
        cont_button.draw()
        win.flip()

    mouse.clickReset()
    core.wait(0.5)    
    
    practice_end = visual.TextBox2(win,color=[-1,-1,-1], text = 'Now, when you are ready to start, press continue', alignment='center')

    while mouse.isPressedIn(cont_button) == False:
        practice_end.draw()
        cont_button.draw()
        win.flip()

