import observation
import etc
import math

from observation import Observation
import numpy as np

params = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 400.0, 'filter_high': 750.0, 'filter_zero': 3781.0, 'point_src': 'g2v', 'star_ab_mag': 5, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 'omit', 'surf_brightness': 'omit', 'ext_mag': 'omit', 
          'conditions': 5.0, 'seeing': 5.0, 'sqm': 20.87, 'desired_snr': 20.0, 'source_type': 'point'}

# params1 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
#           'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
#           'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
#           'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'point_src': 'google', 'star_ab_mag': 5,'star_dist_p': 1.0, 
#           'star_lum': 1.0, 'star_temp': 5800, 'dist': 'omit', 'surf_brightness': 'omit', 'ext_mag': 'omit', 
#           'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'point'}


params2 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'extended_src': 'NGC7714', 'star_dist_p': 1.0, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 1500, 'surf_brightness': 'include', 'ext_mag': 12.74, 
          'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'extended'}


# params3 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
#           'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
#           'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
#           'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'extended_src': 'NGC7714', 'star_dist_p': 1.0, 
#           'star_lum': 1.0, 'star_temp': 5800, 'dist': 1500, 'surf_brightness': 'include', 'ext_mag': 'omit', 
#           'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'testing'}





obs = observation.Observation(params)
# obs1 = observation.Observation(params1)
obs2 = observation.Observation(params2)
# obs3 = observation.Observation(params3)


test_exposure = 1


counts = etc.calc_counts(obs)
print('The sensor reports', counts, 'counts per second')

# counts1 = etc.calc_counts(obs1)
# print('The sensor reports', counts1, 'counts per second')

# counts2 = etc.calc_counts(obs2)
# print('The sensor reports', counts2, 'counts per second')

# counts3 = etc.calc_counts(obs3)
# print('The sensor reports', counts3, 'counts per second')




signal_values = etc.spreadCounts(obs, counts, 1)
noise_values = etc.generateNoise(obs ,test_exposure)
bg_values = etc.generateBG_TEST(obs)


# bg_values = etc.generateBG_TEST(obs)

print("signal values: ", signal_values)
print("noise values: ", noise_values)
print("bg values: ", bg_values)

final_sensor_array = etc.overfullCheck(signal_values+noise_values+bg_values, obs)
print("The peak number of counts in the simulated image is: ", np.max(final_sensor_array))
print("The minimum number of counts in the simulated image is: ", np.min(final_sensor_array))




SNR_ref = etc.get_snr_ref(counts, test_exposure, bg_values, obs)
print(SNR_ref)

exposure_time = etc.calculateReqTime(1050, SNR_ref, test_exposure, counts, obs, bg_values)
print(exposure_time)
