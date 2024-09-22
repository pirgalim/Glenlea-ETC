SAMPLE_SIZE = 50



### CAMERA TEMPLATES ###

asi6200mm = { 'name':"asi6200mm", 'sensor_x': SAMPLE_SIZE, 'sensor_y': SAMPLE_SIZE, 'px_size': 3.86, 
             'q_efficiency': 0.475, 'read_noise': 1.5, 'gain': 0.779, 
             'offset': 500, 'dark_noise': 0.0010, 'full_well': 51000 }

atik = { 'name':"atik", 'sensor_x': SAMPLE_SIZE, 'sensor_y': SAMPLE_SIZE, 'px_size': 3.86, 
             'q_efficiency': 0.475, 'read_noise': 1.5, 'gain': 0.779, 
             'offset': 500, 'dark_noise': 0.0010, 'full_well': 51000 }



### TELESCOPE TEMPLATES ###

cdk14 = { 'name':"cdk14", 'scope_dia': 0.356, 'scope_focal': 2.563, 'plate_scale': '' }
















### LIST OF CAMERAS ###
cameras = [asi6200mm, atik]


### LIST OF TELESCOPES ###
telescopes = [cdk14]
