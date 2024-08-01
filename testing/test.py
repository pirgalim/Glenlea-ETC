import observation
import etc

from observation import Observation

params = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'point_src': 'g2v', 'star_ab_mag': 5, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 'omit', 'surf_brightness': 'omit', 'ext_mag': 'omit', 
          'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'point'}

params1 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'point_src': 'google', 'star_dist_p': 1.0, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 'omit', 'surf_brightness': 'omit', 'ext_mag': 'omit', 
          'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'point'}


params2 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'extended_src': 'NGC7714', 'star_dist_p': 1.0, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 1500, 'surf_brightness': 'include', 'ext_mag': 12.74, 
          'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'extended'}


params3 = {'camera': 'asi6200mm', 'sensor_x': 40.0, 'sensor_y': 40.0, 'px_size': 3.76, 'q_efficiency': 0.475, 
          'read_noise': 1.5, 'gain': 0.779, 'offset': 500.0, 'dark_noise': 0.001, 'full_well': 51000.0, 
          'telescope': 'cdk350', 'scope_dia': 0.3175, 'scope_focal': 1.57, 'plate_scale': 0.488, 'filter': 'test', 
          'filter_low': 4900.0, 'filter_high': 5600.0, 'filter_zero': 37810.0, 'extended_src': 'NGC7714', 'star_dist_p': 1.0, 
          'star_lum': 1.0, 'star_temp': 5800, 'dist': 1500, 'surf_brightness': 'include', 'ext_mag': 'omit', 
          'conditions': 3.0, 'seeing': 3.0, 'sqm': 4.0, 'desired_snr': 20.0, 'source_type': 'testing'}





obs = observation.Observation(params)





counts = etc.calc_counts(obs)


print( Observation.field_count() )

print( Observation.param_count("camera") )



print( counts )



