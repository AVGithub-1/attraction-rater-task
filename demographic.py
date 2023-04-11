from psychopy import gui, visual, core

#these are all the questions asked

questions = {
    'Age': ['Under 18', '18-22', '23-25', '26-30', '31-35', '36-40'], 
    'Describe Yourself': ['Male', 'Female', 'Non-Binary/Third Gender', 'Prefer to Self-Describe:', 'Prefer not to say', 'Other:'],
    'Sexual Orientation': ['Heterosexual(straight)', 'Homosexual(gay)', 'Bisexual', 'Other:', 'Prefer not to say'], 
    'Spanish/Hispanic/Latino': ['Yes', 'No'],
    'Races': ['White or Caucasian', 'Black or African American', 
              'American Indian/ Native American or Alaska Native', 'Asian', 
              'Native Hawaiian or Other Pacific Islander', 'Prefer not to say']
    }


def questionnaire():
   
    # # Display the demographic questionnaire
    # dialog = gui.DlgFromDict(questions, title='Demographic Questionnaire: Fill out all fields', screen = -1)

    # while True:
    #     cond1 = questions['Age'] == ''
    #     cond2 = questions['Gender'] == ['Male', 'Female', 'Other']
    #     cond3 = questions['Education'] == ['High School', 'College', 'Graduate School']
    #     cond4 = questions['Ethnicity'] == ''
    #     if (cond1 or cond2 or cond3 or cond4):
    #         dialog.show()
    #     else:
    #         core.quit()
    

    dialog = gui.Dlg(title = "Questionnaire")
    dialog.addText("Please Fill Out All Fields")
    dialog.addField('Subject Number:')
    dialog.addField(label = 'How old are you?', choices = questions['Age'])
    dialog.addField(label = 'How do you describe yourself?', choices = questions['Describe Yourself'])
    dialog.addField(label = 'If you answered Prefer to Self-Describe or Other:')
    dialog.addField(label = 'Which of the following best describes your sexual orientation?', choices = questions['Sexual Orientation'])
    dialog.addField(label = 'If you answered Other:')
    dialog.addField(label = 'Are you of Spanish, Hispanic or Latino Origin?', choices = questions["Spanish/Hispanic/Latino"])

    dialog.addText('Choose one or more races that you consider yourself to be:')
    for race in questions['Races']:
        dialog.addField(label = race, initial = False)

    dialog.addField(label = "Other:")
    
    dialog.show()

    return dialog.data
    #may need to add code to make the list of data more orderly

    
data = questionnaire()
def demographic_dict(data):
    """
    takes the demographic questionnaire answers, 
    cleans it up, and returns a new list of the participant's demographics
    """
    subject_demos = {'Subject #':'', 
                     'Age': '',
                     'Gender': '',
                     'SexOr': '',
                     'Hispanic': '',
                     'Races': ''} 
     
    subject_demos['Subject #'] = data[0]

    subject_demos['Age'] = data[1]

    if data[2] == 'Prefer to Self-Describe:' or data[2] == 'Other:':
        subject_demos['Gender'] = data[3]
    else:
        subject_demos['Gender'] = data[2]
    
    if data[4] == 'Other:':
        subject_demos['SexOr'] = data[5]
    else:
        subject_demos['SexOr'] = data[4]

    subject_demos['Hispanic'] = data[6]

    races = '' #will store all of the races the participant checked
    for i in range(7,13):
        if data[i] == True:
            races = races + '&' + questions['Races'][i-7]
    
    if data[13] != '':
        races = races + '&' + data[13]

    races = races[1:] #just removes leading character, which is a & sign

    subject_demos['Races'] = races

    return subject_demos

data_demo = demographic_dict(data)

