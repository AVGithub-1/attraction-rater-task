from psychopy import gui, visual, core

# Define the demographic questionnaire; demographics asked should be changed
demographic_questions = {'Age': '', 'Gender': ['Male', 'Female', 'Other'], 'Education': ['High School', 'College', 'Graduate School'], 'Ethnicity': ''}

# Display the demographic questionnaire
dialog = gui.DlgFromDict(demographic_questions, title='Demographic Questionnaire')

# Store the demographic data
if dialog.OK:
    age = demographic_questions['Age']
    gender = demographic_questions['Gender']
    education = demographic_questions['Education']
    ethnicity = demographic_questions['Ethnicity']
else:
    core.quit()

# Use the demographic data for data processing and analysis
