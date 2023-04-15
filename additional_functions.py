from psychopy import visual, monitors, core, event
from pathlib import Path
import random 
import csv
import re



m_vertices = [(-0.15,1), (0.15,1), (0.15,0.5), (0.3,0.5), (0,0), (-0.3,0.5),(-0.15,0.5)]

l_vertices = [(-0.65,1), (-0.35,1), (-0.35,0.5), (-0.2,0.5), (-0.5,0), (-0.8,0.5),(-0.65,0.5)]

r_vertices = [(0.35,1), (0.65,1), (0.65,0.5), (0.8,0.5), (0.5,0), (0.2,0.5),(0.35,0.5)]


def arrow_choice(stim):
    if stim == "Faceless 1.jpg":
        return l_vertices
    elif stim == "Faceless 2.jpg" or stim == "Zendaya":
        return m_vertices
    elif stim == "Faceless 3.jpg":
        return r_vertices
    elif stim == "Group.jpg":
        return random.choice([m_vertices, r_vertices, l_vertices])
    else:
        return m_vertices
    
def update_data(folder, stim_type, rating, arrow_type, data_list):
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

    data_list.append([image, condition, face, rating])
    

def new_csv(header, data, index, data_demo):
    with open(Path("csv_files")/('results'+index+'.csv'), 'w', encoding='UTF8', newline= '') as f:
        writer = csv.writer(f)

        writer.writerow(header)

        # write multiple rows
        for d in data:
            writer.writerow(list(data_demo.values())+ d)
