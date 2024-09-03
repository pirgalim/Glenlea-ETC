import services.counts as cts
from services.observation import Observation

import numpy as np

# def validate(obs: Observation):
        
#         if obs.filter_high < obs.filter_low:
            
#             return "Low filter pass cannot be greater than high filter pass"
        
#         else: return None



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
        
        return cts.extSpec(obs.source, obs.library, obs.ext_mag, obs.dist, obs.mirror_area, obs.filter_name)*obs.Q_efficiency*obs.pixel_area
        
    else: print("source error when finding counts")   
        
        







#SPREAD COUNTS OVER A 2D GAUSSIAN
#Takes in sensor dimensions, total counts to spread, and fwhm (seeing condition)
def spreadCounts(obs: Observation, counts: float, exposureTime: float) -> float: 
    
    fwhm = obs.seeing_pixel
    sensorX = obs.sensor_X
    sensorY = obs.sensor_Y
    totalCounts = counts
    
    
    sigma = fwhm/(2*np.sqrt(2*np.log(2)))
    signalValues = np.zeros([sensorY,sensorX])
    centerX = sensorY/2
    centerY = sensorX/2

    for x in range(sensorY):
        for y in range(sensorX):
            signalValues[x,y] = (1/(2*np.pi*sigma**2))*np.exp((-((x-centerX)**2+(y-centerY)**2))/(2*sigma**2))

        signalValues = signalValues*(totalCounts/signalValues.sum())*exposureTime
        return signalValues




#GENERATE CCD NOISE
#Takes in sensor parameters and generates signal noise based on exposure time
def generateNoise(obs: Observation, exposureTime):
    
    obsType = obs.type
    sensorX = obs.sensor_X
    sensorY = obs.sensor_Y
    darkCurrent = obs.dark_noise
    readNoise = obs.read_noise
    offset = obs.sensor_offset
    
    
    
    if obsType == "point": # Point Source
    
        noiseValues = np.zeros([sensorY,sensorX])
    
        for x in range(sensorY):
            for y in range(sensorX):
                noiseValues[x,y] = np.random.normal(0,readNoise) + np.random.normal(0,darkCurrent)*exposureTime + offset

        return noiseValues
    
    elif obsType == "extended": # Extended source

        noiseValues = readNoise + (darkCurrent*exposureTime) + offset
        return noiseValues








#CHECK FOR OVERFULL PIXELS
#Takes in signal, bg noise and sensor noise and checks if any pixels exceed full well. Assumes perfect blooming correction of the sensor
def overfullCheck(arrayTest, obs: Observation):
    
    obsType = obs.type
    fullWell = obs.full_well

    if obsType == "point": # Point Source

        for x in range(len(arrayTest)):
            for y in range(len(arrayTest[0])):
                if arrayTest[x,y] > fullWell:
                    arrayTest[x,y] = fullWell

        return arrayTest
    
    elif obsType == "extended": # Extended Source

        if arrayTest.all() > fullWell:
            arrayTest = fullWell

        return arrayTest
    
    
    
def computeSNR(obs: Observation, exposureTime, counts, bg_values):

    obsType = obs.type
    signalCountsPerSec = counts
    apertureNumPixels = obs.aperture_num_pixels
    
    
    # change this to accept obs later, then counts will do the assigning variables part
    
    # sensor_X = obs.sensor_X
    # sensor_Y = obs.sensor_Y
    # sky_bright = obs.sky_bright
    # filter_zero = obs.filter_zero
    # mirror_area = obs.mirror_area
    # gain = obs.gain
    # filter_low = obs.filter_low
    # filter_high = obs.filter_high
    # Q_efficiency = obs.Q_efficiency
    # filter_freq_band = obs.filter_freq_band
    # obs_type = obs.type
    readNoise = obs.read_noise
    darkNoise = obs.dark_noise
    
    


    if obsType == "point": # Point source

        return (signalCountsPerSec*exposureTime)/(np.sqrt(signalCountsPerSec*exposureTime+apertureNumPixels*(exposureTime*bg_values[0][0]+readNoise**2+exposureTime*darkNoise)))
    
    elif obsType == "extended": # Extended

        return (signalCountsPerSec*exposureTime)/(np.sqrt(signalCountsPerSec*exposureTime+(exposureTime*bg_values+readNoise**2+exposureTime*darkNoise)))
   

    
    
def get_snr_ref( counts_per_second, test_exposure, bg_values, obs: Observation):
    
    
    obs_type = obs.type
    aperture_num_pixels = obs.aperture_num_pixels
    read_noise = obs.read_noise
    dark_noise = obs.dark_noise
    
    
    if obs_type == "point": # Point Source

        return (counts_per_second*test_exposure)/(np.sqrt(counts_per_second*test_exposure+aperture_num_pixels*(test_exposure*bg_values[0][0]+read_noise**2+test_exposure*dark_noise)))


    elif obs_type == "extended": # Extended Source

        return (counts_per_second*test_exposure)/(np.sqrt(counts_per_second*test_exposure+(test_exposure*bg_values+read_noise**2+test_exposure*dark_noise)))
       
        

            
            
            
            
#CHECK FOG LIMIT AND CALCULATE EXPOSURE TIME
#If a star is too dim or the sky too bright, SNR will plateau. This code checks to see if the desired SNR is above this limit. Assumes maximum exposure time of 300 hours.
#If Desired SNR is above the fog limit, a lower SNR must be input or better conditions observed.
#This function iterates over SNR calculations until the desired SNR is achieved within a tolerance, default Tolerance = 1          
def calculateReqTime(desiredSNR, snrRef, expRef, counts, obs: Observation, bg_values, tolerance = 1, maxTime = 1080000):
    
    # maxSNR = computeSNR(maxTime, counts, obs.aperture)
    
    maxSNR = computeSNR(obs, maxTime, counts, bg_values)
    
    currentSNR = snrRef

    if desiredSNR>maxSNR:
        return "SNR not achievable"


    else:
        while np.abs(desiredSNR-currentSNR)>tolerance:
            currentTime = expRef*(desiredSNR/currentSNR)**2
            currentSNR = computeSNR(obs, currentTime, counts, bg_values)
            expRef = currentTime
            print("SNR is now: ", currentSNR)
            


        print("The calculated exposure time is: ", currentTime)
        
        
        exposure_time = "The required exposure time is {:.4f} seconds".format(currentTime)
        
        
        return exposure_time           
            
            
            
            
            
            
            
def generateBG_TEST(obs: Observation):
    
    
    sensor_X = obs.sensor_X
    sensor_Y = obs.sensor_Y
    sky_bright = obs.sky_bright
    mirror_area = obs.mirror_area
    gain = obs.gain
    Q_efficiency = obs.Q_efficiency
    obs_type = obs.type
    pixel_area = obs.pixel_area
    filter_name = obs.filter_name
    
    # result = cts.generateBG(sensor_X, sensor_Y, sky_bright, filter_name, mirror_area, gain, Q_efficiency, pixel_area, obs_type)
    
    # result1 = cts.generateBG(sky_bright, filter_name, mirror_area, gain, Q_efficiency).value*Q_efficiency*pixel_area
    
    
    result = cts.generateBG(sensor_X, sensor_Y, sky_bright, filter_name, mirror_area, gain, Q_efficiency, pixel_area, obs_type)*Q_efficiency*pixel_area

    
    print("bg result: ", result)
    
    return result
            
            
            
    # def calc_counts(obs):
                
    #     if obs.type == "point":
                        
    #         try:
    #             return cts.stellarSpec(obs.source, obs.ab_mag, obs.mirror_area, obs.filter_name)*obs.Q_efficiency
    #         except:
    #             print("Unable to find source. Defaulting to black body.")
    #             return cts.blackBody(obs.star_temp, obs.ab_mag, obs.mirror_area,obs.filter_name)*obs.Q_efficiency
        
    #     elif obs.type == "extended":
            
    #         return cts.extSpec(obs.source, obs.library, obs.ext_mag, obs.mirror_area, obs.filter_name)*obs.Q_efficiency*obs.pixel_area
            
    #     else: print("source error when finding counts")   
    
    
    
    
    

