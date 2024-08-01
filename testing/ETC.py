import counts as cts
from observation import Observation



def calc_counts(obs: Observation):
                
        if obs.type == "point":
            try:
                return cts.stellarSpec(obs.source, obs.ab_mag, obs.mirror_area, obs.filter_name)*obs.Q_efficiency
            except:
                
                try:
                    print("Unable to find source. Defaulting to black body.")
                    return cts.blackBody(obs.star_temp, obs.ab_mag, obs.mirror_area,obs.filter_name)*obs.Q_efficiency
                
                except:
                    print("Something else is wrong")
            
        elif obs.type == "extended":
            
            return cts.extSpec(obs.source, obs.library, obs.ext_mag, obs.mirror_area, obs.filter_name)*obs.Q_efficiency*obs.pixel_area
            
        else: print("source error when finding counts")   
        
        

def plot(obs: Observation):
    pass