SAMPLE_SIZE = 50    # This is the default image size for the aperture

#TODO: default gain
GAIN = 1
OFFSET = 1

### TODO: remember to update these in the forms section as well - class SelectForm(FlaskForm):



### CAMERA TEMPLATES ###

asi6200mm = { 'name':"asi6200mm", 'sensor_x': SAMPLE_SIZE, 'sensor_y': SAMPLE_SIZE, 'px_size': 3.86, 
             'q_efficiency': 0.475, 'read_noise': 1.5, 'gain': 0.779, 
             'offset': 500, 'dark_noise': 0.0010, 'full_well': 51000 }

atik = { 'name':"atik", 'sensor_x': SAMPLE_SIZE, 'sensor_y': SAMPLE_SIZE, 'px_size': 3.86, 
             'q_efficiency': 0.475, 'read_noise': 1.5, 'gain': 0.779, 
             'offset': 500, 'dark_noise': 0.0010, 'full_well': 51000 }


sbig = { 'name':"sbig", 'sensor_x': SAMPLE_SIZE, 'sensor_y': SAMPLE_SIZE, 'px_size': 9, 
             'q_efficiency': 0.95, 'read_noise': 3.7, 'gain': 0.779, 
             'offset': 500, 'dark_noise': 0.3, 'full_well': 74000 }



### TELESCOPE TEMPLATES ###

cdk14 = { 'name':"cdk14", 'scope_dia': 0.356, 'scope_focal': 2.563, 'plate_scale': '' }



### FILTER PRESETS ###
# def pickles(): 
    
#     file = open("./static/presets/pickles.csv")
#     presets = []
    
#     for line in file:    
#         csvs = line.strip().split(",")
#         presets.append( (csvs[1], [csvs[2]]) )
        
#     file.close()
#     return presets











### LIST OF CAMERAS ###
cameras = [asi6200mm, atik, sbig]


### LIST OF TELESCOPES ###
telescopes = [cdk14]



#TODO: add some test cases for template validation - maybe display an error when running?
# I think I made it key-value so check those exceptions