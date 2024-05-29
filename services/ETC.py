# currently rewriting Jupyter file

import matplotlib
matplotlib.use('agg')   #TODO very important for Flask

import matplotlib.pyplot as plt
import scipy.constants
import matplotlib.patches as patches
import scipy
import numpy as np
import math



# constants
kB = scipy.constants.Boltzmann
h = scipy.constants.Planck
c = scipy.constants.c




class Calculator:
    
    def __init__(self, params):
        
        #TODO verify all parameters first
        
        camera = params[0]
        telescope = params[1]
        filter = params[2]
        target = params[3]
        conditions = params[4]
        
        
        #--- camera parameters ---#
        self.sensor_X = camera[0]
        self.sensor_Y = camera[1]
        self.pixel_size = camera[2] * 10**(-6)
        self.Q_efficiency = camera[3]
        self.read_noise = camera[4]
        self.gain = camera[5]
        self.sensor_offset = camera[6]
        self.dark_noise = camera[7]
        self.full_well = camera[8]
        
        
        self.sensor_width = self.sensor_X * self.pixel_size
        self.sensor_height = self.sensor_Y * self.pixel_size
        
        
        #--- telescope parameters ---#
        self.scope_dia = telescope[0]
        self.scope_focal = telescope[1]
        self.plate_scale = telescope[2]
        
        self.mirror_area = np.pi * (self.scope_dia/2) ** 2
        self.f_ratio = self.scope_focal/self.scope_dia
        
        
        #--- filter parameters ---#
        self.filter_low = filter[0] * 10**(-9)  #TODO something else here, check with Ryan
        self.filter_high = filter[1]  * 10**(-9)
        self.filter_zero = filter[2]
        
        self.filter_low_freq = scipy.constants.c/self.filter_low
        self.filter_high_freq = scipy.constants.c/self.filter_high
        self.filter_freq_band = self.filter_low_freq - self.filter_high_freq
        
        
        #--- target parameters
        self.star_dist = target[0]
        self.star_temp = target[1]
        self.star_dia_solar = target[2]
        
        self.star_dist_m = self.star_dist * 9.461 * 10**15
        self.star_dia = 1.392 * 10**9*self.star_dia_solar
        
        
        #--- conditions ---#
        self.sky_bright = 21.75  #TODO add this to form?
        self.seeing_cond = conditions[0]
        self.seeing_pixel = self.seeing_cond/self.plate_scale
        
        
        
        
        

        
        


    def computeFOV(self):
        #===================== COMPUTE FOV (arcseconds) =====================
        #Using Focal length, pixel size and sensor dimensions
        
        FOV_width = 206265 * self.sensor_width * (1/self.scope_focal)
        FOV_height = 206265 * self.sensor_height * (1/self.scope_focal)
        FOV_area = FOV_width * FOV_height
        
        return FOV_area
    
    
    #function computing the integral of a function f using the trapezoidal rule, taking in the function and a step size.
    def computeIntegral(self, f, stepSize):
        return (stepSize/2)*(f[0]+f[-1]+2*np.sum(f[1:-1]))
    

    def countsPerSecond(self):
        
        T = self.star_temp
        
         #define wavelengths by dividing the bandpass range into 1000 equal parts
        wlB = np.linspace(self.filter_low,self.filter_high,1000)
        
        #define the step width as the distance between adjacent wavelength values
        stepWidth = (wlB[1]-wlB[0]) #distance from 1 point to the next = step size
        
        #Calculate the photon energies at every wavelength
        p_Energy = h*c/wlB
        
        #calculate the integrand under the Stefan-Boltzmann (SB) law, divided by the photon energies for total number of photons
        PB = ((2*np.pi*h*c**2)/(wlB**5))*(1/(np.exp((h*c)/(wlB*kB*T))-1))*(1/(p_Energy)) #coarse function values, 100 segments
        
        
                
        counts_per_second = self.computeIntegral(PB,stepWidth) * (4*np.pi*((self.star_dia/2)**2))/(4*np.pi*self.star_dist_m**2)*self.mirror_area*self.Q_efficiency/self.gain #electrons per second from the star on the sensor in photons/m^2

        return (math.trunc(counts_per_second))

    
        
        
        
        
    def plot_light_curve_SB(self):

        # kB = scipy.constants.Boltzmann
        # h = scipy.constants.Planck
        # c = scipy.constants.c
        T = self.star_temp   # pass in function

        wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
        wlnm = wl * 10**9 

        P = ((2*np.pi*h*c**2)/(wl**5))*(1/np.exp((h*c)/(wl*kB*T)-1))

        plt.figure(figsize=(8, 6))
        plt.plot(wlnm, P, label='Stellar Black Body', color='y')
        plt.fill_between(wlnm, P, color='yellow', alpha=0.3, label='Stellar emission')

        plt.axvline(x=self.filter_low*10**9, color='r', linestyle='--', label='filter cut on')
        plt.axvline(x=self.filter_high*10**9, color='b', linestyle='--', label='filter cut off')

        plt.fill_betweenx(y=np.linspace(min(P), max(P) + 1*10**14), x1=self.filter_low*10**9, x2=self.filter_high*10**9, color='lightblue', alpha=0.4, label='Filter band pass')

        plt.title('Filtered Stellar Black Body Spectrum')
        plt.xlabel('Wavelengh (nm)')
        plt.ylabel('Power Density (W/m^3)')
        plt.xlim(0,2000)
        plt.ylim(0)
        plt.legend()
        plt.grid(True)

        plt.savefig('static/my_plot.png')
        
        
        
        



    #def spreadCounts():
        
    
        
        
        
    
            
        
        
    def __str__(self):
        return str(self)
