from services.observation import Observation
from services import etc

from services.observation import Observation
import numpy as np









# obs2 = Observation(params2)
# # obs3 = observation.Observation(params3)


# test_exposure = 1


# counts = etc.calc_counts(obs)
# print('The sensor reports', counts, 'counts per second')

# # counts1 = etc.calc_counts(obs1)
# # print('The sensor reports', counts1, 'counts per second')

# # counts2 = etc.calc_counts(obs2)
# # print('The sensor reports', counts2, 'counts per second')

# # counts3 = etc.calc_counts(obs3)
# # print('The sensor reports', counts3, 'counts per second')




# signal_values = etc.spreadCounts(obs, counts, 1)
# noise_values = etc.generateNoise(obs ,test_exposure)
# bg_values = etc.generateBG_TEST(obs)


# # bg_values = etc.generateBG_TEST(obs)

# print("signal values: ", signal_values)
# print("noise values: ", noise_values)
# print("bg values: ", bg_values)

# final_sensor_array = etc.overfullCheck(signal_values+noise_values+bg_values, obs)
# print("The peak number of counts in the simulated image is: ", np.max(final_sensor_array))
# print("The minimum number of counts in the simulated image is: ", np.min(final_sensor_array))




# SNR_ref = etc.get_snr_ref(counts, test_exposure, bg_values, obs)
# print(SNR_ref)

# exposure_time = etc.calculateReqTime(1050, SNR_ref, test_exposure, counts, obs, bg_values)
# print(exposure_time)













def check(result, expected):
    
    if(result == expected):
        print("passed")
    else:
        print("failed")






def counts(obs:Observation):
    
    counts = etc.calc_counts(obs)
    print(counts)





# mainline 


params = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 'telescope': 'cdk350', 
          'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'V', 'source_type': 'point', 
          'point_src': '', 'star_ab_mag': 1.0, 'star_temp': 100.0, 'extended_src': '', 
          'ext_mag': 'omit', 'conditions': 3.0, 'seeing': 3.0, 'sqm': 21.15, 'suggested_snr': 5.0, 'desired_snr': 5.0}

params1 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 'telescope': 'cdk350', 
          'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'V', 'source_type': 'point', 
          'point_src': '', 'star_ab_mag': 1.0, 'star_temp': 100000.0, 'extended_src': '', 
          'ext_mag': 'omit', 'conditions': 3.0, 'seeing': 3.0, 'sqm': 21.15, 'suggested_snr': 5.0, 'desired_snr': 5.0}


obs = Observation(params)
obs1 = Observation(params1)

counts(obs)
counts(obs1)