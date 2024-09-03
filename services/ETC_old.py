import matplotlib
matplotlib.use('agg')   # very important for Flask, matplot does not work otherwise

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import scipy.constants

#import scipy
import numpy as np
import math


import pyckles

from spextra import SpecLibrary, Spextrum 



# constants
KB = scipy.constants.Boltzmann
H = scipy.constants.Planck
C = scipy.constants.c


# global variables
apertureNumPixels = 0
bgValues = 0


class Calculator:
    
    def validate(self):
        
        if self.filter_high < self.filter_low:
            
            return "Low filter pass cannot be greater than high filter pass"
        
        else: return None
    
    
    
    def __init__(self, params):
        
        
        #--- camera parameters ---#
        self.sensor_X = int( params["sensor_x"] )  # cast to int for simpler calculation
        self.sensor_Y = int(params["sensor_y"])  # ...
        self.pixel_size = params["px_size"] * 10**(-6)
        self.Q_efficiency = params["q_efficiency"]
        self.read_noise = params["read_noise"]
        self.gain = params["gain"]
        self.sensor_offset = params["offset"]
        self.dark_noise = params["dark_noise"]
        self.full_well = params["full_well"]
        
        self.sensor_width = self.sensor_X * self.pixel_size
        self.sensor_height = self.sensor_Y * self.pixel_size
        
        
        #--- telescope parameters ---#
        self.scope_dia = params["scope_dia"]
        self.scope_focal = params["scope_focal"]
        self.plate_scale = params["plate_scale"]
        
        self.mirror_area = np.pi * (self.scope_dia/2) ** 2
        self.f_ratio = self.scope_focal/self.scope_dia
        
        
        #--- filter parameters ---#
        self.filter_low = params["filter_low"] * 10**(-9)  #TODO something else here, check with Ryan
        self.filter_high = params["filter_high"]  * 10**(-9)
        self.filter_zero = params["filter_zero"]
        
        self.filter_low_freq = C/self.filter_low
        self.filter_high_freq = C/self.filter_high
        self.filter_freq_band = self.filter_low_freq - self.filter_high_freq
        
        
        
        #--- determine target type ---#
        
        #--- point source parameters ---#
        self.star_dist = params["star_dist_p"]
        self.star_temp = params["star_temp"]
        self.star_dia_solar = 10000
        self.spectra = params["point_src"]
        
        self.star_dist_m = self.star_dist * 9.461 * 10**15
        self.star_dia = 1.392 * 10**9*self.star_dia_solar
        
        #--- conditions for point source only ---#
        self.seeing_cond = params["seeing"]
        
        
        #--- extended source parameters ---#
        self.surf_brightness = params["surf_brightness"]
        self.magnitude = params["magnitude"]
        
        
        #--- conditions for all ---#
        self.seeing_cond = params["seeing"]
        self.sky_bright = params["sqm"]
        self.seeing_pixel = self.seeing_cond/self.plate_scale
    
            
        #--- signal to noise ---#
        self.snr = params["desired_snr"]
        
        
        
        
               
        
        # #--- camera parameters ---#
        # self.sensor_X = int(params[0])  # cast to int for simpler calculation
        # self.sensor_Y = int(params[1])  # ...
        # self.pixel_size = params[2] * 10**(-6)
        # self.Q_efficiency = params[3]
        # self.read_noise = params[4]
        # self.gain = params[5]
        # self.sensor_offset = params[6]
        # self.dark_noise = params[7]
        # self.full_well = params[8]
        
        # self.sensor_width = self.sensor_X * self.pixel_size
        # self.sensor_height = self.sensor_Y * self.pixel_size
        
        
        # #--- telescope parameters ---#
        # self.scope_dia = params[9]
        # self.scope_focal = params[10]
        # self.plate_scale = params[11]
        
        # self.mirror_area = np.pi * (self.scope_dia/2) ** 2
        # self.f_ratio = self.scope_focal/self.scope_dia
        
        
        # #--- filter parameters ---#
        # self.filter_low = params[12] * 10**(-9)  #TODO something else here, check with Ryan
        # self.filter_high = params[13]  * 10**(-9)
        # self.filter_zero = params[14]
        
        # self.filter_low_freq = C/self.filter_low
        # self.filter_high_freq = C/self.filter_high
        # self.filter_freq_band = self.filter_low_freq - self.filter_high_freq
        
        
        # #--- target parameters
        # self.star_dist = params[15]
        # self.star_temp = params[16]
        # self.star_dia_solar = params[17]
        # self.pickle = params[18]
        
        # self.star_dist_m = self.star_dist * 9.461 * 10**15
        # self.star_dia = 1.392 * 10**9*self.star_dia_solar
        
        
        # #--- conditions ---#
        # self.seeing_cond = params[18+1]
        # self.sky_bright = params[19+1]
        # self.seeing_pixel = self.seeing_cond/self.plate_scale
        
        
        # #--- signal to noise ---#
        # self.snr = params[20]
        
    
        
    #-------------------- Calculation functions --------------------#

    def computeFOV(self) -> float:
        """
        Compute FOV using focal length, pixel size and sensor dimensions

        Returns:
            float: FOV area in arcseconds
        """
        
        # 206265 is the radian to arcsecond conversion factor
        FOV_width = 206265 * self.sensor_width * (1/self.scope_focal) 
        FOV_height = 206265 * self.sensor_height * (1/self.scope_focal)

        return FOV_width * FOV_height
    
    
    #function computing the integral of a function f using the trapezoidal rule, taking in the function and a step size.
    def computeIntegral(self, f, stepSize: float) -> float:
        """
        Computes the integral of a function using the trapezoidal rule

        Args:
            f (function): integrand
            stepSize (float): distance from one point to the next

        Returns:
            float: resulting integral
        """
        return (stepSize/2) * ( f[0] + f[-1] + 2*np.sum(f[1:-1]) )    
    
    

    def countsPerSecond(self) -> float:
        """
        Calculate counts per second...

        Returns:
            float: expected counts per second
        """
        
        T = self.star_temp
        
        #define wavelengths by dividing the bandpass range into 1000 equal parts
        wlB = np.linspace(self.filter_low,self.filter_high,1000)
        
        #define the step width as the distance between adjacent wavelength values
        stepWidth = (wlB[1]-wlB[0]) # distance from 1 point to the next = step size
        
        #Calculate the photon energies at every wavelength
        p_Energy = H*C/wlB
        
        #calculate the integrand under the Stefan-Boltzmann (SB) law, divided by the photon energies for total number of photons
        PB = ((2*np.pi*H*C**2)/(wlB**5))*(1/(np.exp((H*C)/(wlB*KB*T))-1))*(1/(p_Energy)) #coarse function values, 100 segments
        
        counts_per_second = self.computeIntegral(PB,stepWidth) * (4*np.pi*((self.star_dia/2)**2))/(4*np.pi*self.star_dist_m**2)*self.mirror_area*self.Q_efficiency/self.gain #electrons per second from the star on the sensor in photons/m^2

        return math.trunc(counts_per_second)

    
        
    def plot_light_curve_SB(self):
        """
            Generate light curve plot for a point source
            
            Saves a figure in the local directory './static'
        """

        T = self.star_temp  

        # wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
        # wlnm = wl * 10**9 

        # P = ((2*np.pi*H*C**2)/(wl**5))*(1/np.exp((H*C)/(wl*KB*T)-1))

        # plt.figure(figsize=(8, 6))
        # plt.plot(wlnm, P, label='Stellar Black Body', color='y')
        # plt.fill_between(wlnm, P, color='yellow', alpha=0.3, label='Stellar emission')

        # plt.axvline(x=self.filter_low*10**9, color='r', linestyle='--', label='filter cut on')
        # plt.axvline(x=self.filter_high*10**9, color='b', linestyle='--', label='filter cut off')

        # plt.fill_betweenx(y=np.linspace(min(P), max(P) + 1*10**14), x1=self.filter_low*10**9, x2=self.filter_high*10**9, color='lightblue', alpha=0.4, label='Filter band pass')

        # plt.title('Filtered Stellar Black Body Spectrum')
        # plt.xlabel('Wavelengh (nm)')
        # plt.ylabel('Power Density (W/m^3)')
        # plt.xlim(0,2000)
        # plt.ylim(0)
        # plt.legend()
        # plt.grid(True)
        
        
        
        
        
        
        
        
        # spec_lib = pyckles.SpectralLibrary("pickles")

        try:
            # spectra = spec_lib[self.pickle].data
            # wlnm = spectra["wavelength"]/10  # A to nm
            # P = spectra["flux"]
            
            lib = "pickles"
            spectra = self.spectra
            
            
            lib = "nebulae"
            spectra = "orion"

            # NEEDS TO BE FORMATTED AS "[library]/[spectra]"
            retrieve = lib + "/" + spectra
            sp = Spextrum(retrieve)         
            
            wlA = np.array( sp.waveset )
            flux = np.array( sp(wlA, flux_unit="PHOTLAM") )
            
            wlnm = wlA
            P = flux
            
        except: 
            wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
            wlnm = wl * 10**9 
            P = ((2*np.pi*H*C**2)/(wl**5))*(1/np.exp((H*C)/(wl*KB*T)-1))

        p_max = np.max(P)
        wl_max = np.max(wlnm)

        plt.figure(figsize=(8, 6))
        plt.plot(wlnm, P,label='Stellar Spectrum',color='y')

        plt.fill_between(wlnm, P, color = 'yellow', alpha = 0.3,label = 'Stellar emission')

        plt.axvline(x=self.filter_low*10**9, color='r', linestyle='--', label='filter cut on')
        plt.axvline(x=self.filter_high*10**9, color='b', linestyle='--', label='filter cut off')

        plt.fill_betweenx(y=np.linspace(min(P), max(P)+1*10**14), x1=self.filter_low*10**9, x2=self.filter_high*10**9, color='lightblue', alpha=0.4, label='filter band pass')

        plt.title('Filtered Stellar Spectrum')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Power Density (W/m^2)')
        plt.xlim(0,wl_max * 1.1)
        plt.ylim(0,p_max * 1.1)

        plt.legend()
        plt.grid(True)
        plt.show()
        
    
        plt.savefig('static/plot_light_curve_SB.png')
        
        
        
        
        
    #-------------------- Functions for SNR --------------------#
    
    
     #SPREAD COUNTS OVER A 2D GAUSSIAN
    #Takes in sensor dimensions, total counts to spread, and fwhm (seeing condition)
    def spreadCounts(self, sensorX, sensorY, totalCounts, fwhm, exposureTime):
        
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
    def generateNoise(self, sensorX, sensorY, darkCurrent, readNoise, offset, exposureTime):
        noiseValues = np.zeros([sensorY,sensorX])
        
        for x in range(sensorY):
            for y in range(sensorX):
                noiseValues[x,y] = np.random.normal(0,readNoise) + np.random.normal(0,darkCurrent)*exposureTime + offset

        return noiseValues
    
    
    
    #GENERATE SKY BACKGROUND EMISSION
    #Takes in sensor, telescope, sky and filter parameters and generates sky background signal based on exposure time and bortle scale
    def generateBG(self, sensorX, sensorY, skyMag, zeroFlux, mirrorArea, sensorGain, filterLow, filterHigh, sensorQE, freqPass, exposureTime):

        skyBG = np.zeros([sensorY,sensorX])
        skyFlux = zeroFlux*10**(-0.4*skyMag)*10**(-26)*(freqPass)*mirrorArea
        skyCounts = skyFlux/(H*C/(self.filter_low+((filterHigh-filterLow)/2)))*sensorQE*exposureTime/sensorGain #counts from the sky per second
        
        for x in range(sensorY):
            for y in range(sensorX):
                skyBG[x,y] = skyCounts

        return skyBG
    

    #CHECK FOR OVERFULL PIXELS
    #Takes in signal, bg noise and sensor noise and checks if any pixels exceed full well. Assumes perfect blooming correction of the sensor
    def overfullCheck(self, arrayTest, fullWell):
        for x in range(len(arrayTest)):
            for y in range(len(arrayTest[0])):
                if arrayTest[x,y] > fullWell:
                    arrayTest[x,y] = fullWell

        return arrayTest 
    


    #COMPUTE SIGNAL, NOISE, BACKGROUND ARRAYS FOR TEST IMAGE (1s):
    def aperture(self):
        
        x = int(self.sensor_X)
        y = int(self.sensor_Y)
        counts = self.countsPerSecond()
        
        test_exposure = 1 
        signal_values = self.spreadCounts(x,y,counts,self.seeing_pixel,test_exposure)
        noise_values= self.generateNoise(x,y,self.dark_noise,self.read_noise,self.sensor_offset,test_exposure)
        bg_values = self.generateBG(x,y,self.sky_bright,self.filter_zero,self.mirror_area,self.gain,self.filter_low,self.filter_high,self.Q_efficiency,self.filter_freq_band,test_exposure)
        final_sensor_array = self.overfullCheck(signal_values+noise_values+bg_values,self.full_well)
        
        global bgValues
        bgValues = bg_values
        
        
        
        
        #GENERATE APERTURE FOR MEASURING SNR
        aperture_rad = self.seeing_pixel*0.67
        aperture_center = (x/2,y/2)
        aperture_num_pixels = np.pi*aperture_rad**2
        
        global apertureNumPixels
        apertureNumPixels = aperture_num_pixels
        
        aperture_circle = patches.Circle(aperture_center,radius=aperture_rad, edgecolor = 'red', facecolor = 'none', linewidth = 1)
        plt.figure(figsize=(8, 6))
        plt.text(aperture_center[0]+8,aperture_center[1]+8, 'Measurement Aperture', verticalalignment='center',color='red')
        plt.imshow(final_sensor_array, cmap='gray', interpolation='nearest',vmin = 0)
        plt.gca().add_patch(aperture_circle)
        plt.colorbar(label='Counts')
        plt.title('Spread of Counts over Sensor')
        plt.xlabel('Number of pixels (X)')
        plt.ylabel('Number of pixels (Y)')
        plt.xlim(0,x)
        plt.ylim(0,y)
        plt.gca().set_aspect('equal')
        plt.savefig('static/spread_counts.png')
        
        return ( int(np.max(final_sensor_array)), int(np.min(final_sensor_array)) )  
                


    
    
    
    def computeSNR(self, exposureTime):
        
        signalCountsPerSec = self.countsPerSecond()
        return (signalCountsPerSec*exposureTime)/(np.sqrt(signalCountsPerSec*exposureTime+apertureNumPixels*(exposureTime*self.generateBG(self.sensor_X,self.sensor_Y,self.sky_bright,self.filter_zero,self.mirror_area,self.gain,self.filter_low,self.filter_high,self.Q_efficiency,self.filter_freq_band,exposureTime)[0][0]+self.read_noise**2+exposureTime*self.dark_noise)))
    
    
    def SNR_ref(self):
        
        counts_per_second = self.countsPerSecond()
        test_exposure = 1
        
        return (counts_per_second*test_exposure)/(np.sqrt(counts_per_second*test_exposure+apertureNumPixels*(test_exposure*bgValues[0][0]+self.read_noise**2+test_exposure*self.dark_noise)))
    
    
    
    #CHECK FOG LIMIT AND CALCULATE EXPOSURE TIME
    #If a star is too dim or the sky too bright, SNR will plateau. This code checks to see if the desired SNR is above this limit. Assumes maximum exposure time of 300 hours.
    #If Desired SNR is above the fog limit, a lower SNR must be input or better conditions observed.
    #This function iterates over SNR calculations until the desired SNR is achieved within a tolerance, default Tolerance = 1
    
    def calculateReqTime(self, expRef, tolerance = 1, maxTime = 1080000):
    
        desiredSNR = self.snr
        snrRef = self.SNR_ref()
    
        maxSNR = self.computeSNR(maxTime)
        currentSNR = snrRef

        if desiredSNR>maxSNR:
            return "SNR not achievable"


        else:
            while np.abs(desiredSNR-currentSNR)>tolerance:
                currentTime = expRef*(desiredSNR/currentSNR)**2
                currentSNR = self.computeSNR(currentTime)
                expRef = currentTime
                print("SNR is now: ",currentSNR)
                


            print("The calculated exposure time is: ")
            return currentTime
            
        
  