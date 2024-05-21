# currently rewriting Jupyter file

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import scipy.constants
#plt.style.use('seaborn-poster')
import matplotlib.patches as patches
import scipy
import numpy as np
import math



# import base64
# from io import BytesIO
# from matplotlib.figure import Figure


#from PIL import Image


class Calculator:
    
    def __init__(self, params):
        
        #TODO verify all parameters first
        
        camera = params[0]
        telescope = params[1]
        filter = params[2]
        target = params[3]
        conditions = params[4]
        
        
        print(camera)
        print(telescope)
        print(filter)
        print(target)
        print(conditions)
        
        
        #--- camera parameters ---#
        self.pixel_size = camera[0]
        self.Q_efficiency = camera[1]
        self.read_noise = camera[2]
        self.gain = camera[3]
        self.sensor_offset = camera[4]
        self.dark_noise = camera[5]
        self.full_well = camera[6]
        self.sensor_X = camera[7]
        self.sensor_Y = camera[8]
        
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
        self.sky_bright = 20.87  #TODO add this to form?
        self.seeing_cond = conditions[0]
        self.seeing_pixel = self.seeing_cond/self.plate_scale
        
        
        
        #--- compute FOV ---#
        self.FOV_width = 206265 * self.sensor_width * (1/self.scope_focal)
        self.FOV_height = 206265 * self.sensor_height * (1/self.scope_focal)
        self.FOV_area = self.FOV_width * self.FOV_height
        
        
        
    def plot_light_curve_SB(self):

        kB = scipy.constants.Boltzmann
        h = scipy.constants.Planck
        c = scipy.constants.c
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
        #plt.show()
        plt.savefig('static/my_plot.png')
            
        
        
    def __str__(self):
        return str(self)


# class Camera:
    
#     def __init__(self, params):
        
        
#         # validate length of parameters first
        
#         self.pixel_size = params[0]
#         self.Q_efficiency = params[1]
#         self.read_noise = params[2]
#         self.gain = params[3]
#         self.sensor_offset = params[4]
#         self.dark_noise = params[5]
#         self.full_well = params[6]
#         self.sensor_X = params[7]
#         self.sensor_Y = params[8]
        
#         self.sensor_width = sensor_X * pixel_size
#         self.sensor_height = sensor_Y * pixel_size
        
#     def __str__(self):
        
#         return "testing..."


        
        
# class Telescope:
    
#     def __init__(self, params):
        
#         # validate
#         self.scope_dia = params[0]
#         self.scope_focal = params[1]
#         self.plate_scale = params[2]
        
#         self.mirror_area = np.pi * (scope_dia/2) ** 2
#         self.f_ratio = scope_focal/scope_dia
        
        
# class Filter:
    
#     def __init__(self, params):
    
#         # validate
#         self.filter_low = params[0] * 10**(-9)  #TODO something else here, check with Ryan
#         self.filter_high = params[1]  * 10**(-9)
#         self.filter_zero = params[2]
        
#         self.filter_low_freq = scipy.constants.c/filter_low
#         self.filter_high_freq = scipy.constants.c/filter_high
#         self.filter_freq_band = filter_low_freq - filter_high_freq
    
    
    



# sensor parameters, hard coded for now, will allow for user input later
# pixel_size = 9 * 10**(-6) # add comments later
# Q_efficiency = 0.5*0.95
# read_noise = 13
# gain = 0.92
# sensor_offset = 50
# dark_noise = 0.03
# full_well = 60000
# sensor_X = 400
# sensor_Y = 267

# sensor_width = sensor_X * pixel_size
# sensor_height = sensor_Y * pixel_size


# # observatory parameters, same thing
# scope_dia = 0.3556
# mirror_area = np.pi * (scope_dia/2) ** 2
# scope_focal = 2.563
# f_ratio = scope_focal/scope_dia
# plate_scale = 0.75


# # filters, same thing
# filter_low = 500 * 1 * 10**(-9)
# filter_low_freq = scipy.constants.c/filter_low

# filter_high = 650 * 1 * 10**(-9)
# filter_high_freq = scipy.constants.c/filter_high

# filter_zero = 3781
# filter_freq_band = filter_low_freq - filter_high_freq


# # target, most likely custom, add bounds checking

# star_dist = 1487.4
# star_dist_m = star_dist * 9.461 * 10**15
# star_temp = 5500
# star_dia_solar = 1
# star_dia = 1.392 * 10**9*star_dia_solar


# # compute FOV

# FOV_width = 206265 * sensor_width * (1/scope_focal)
# FOV_height = 206265 * sensor_height * (1/scope_focal)
# FOV_area = FOV_width * FOV_height


# # sky parameters, again custom/dropdown

# sky_bright = 20.87
# seeing_cond = 5
# seeing_pixel = seeing_cond/plate_scale



# def plot_light_curve_SB():

#     kB = scipy.constants.Boltzmann
#     h = scipy.constants.Planck
#     c = scipy.constants.c
#     T = star_temp   # pass in function

#     wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
#     wlnm = wl * 10**9 

#     P = ((2*np.pi*h*c**2)/(wl**5))*(1/np.exp((h*c)/(wl*kB*T)-1))

#     plt.figure(figsize=(8, 6))
#     plt.plot(wlnm, P, label='Stellar Black Body', color='y')
#     plt.fill_between(wlnm, P, color='yellow', alpha=0.3, label='Stellar emission')

#     plt.axvline(x=filter_low*10**9, color='r', linestyle='--', label='filter cut on')
#     plt.axvline(x=filter_high*10**9, color='b', linestyle='--', label='filter cut off')

#     plt.fill_betweenx(y=np.linspace(min(P), max(P) + 1*10**14), x1=filter_low*10**9, x2=filter_high*10**9, color='lightblue', alpha=0.4, label='Filter band pass')

#     plt.title('Filtered Stellar Black Body Spectrum')
#     plt.xlabel('Wavelengh (nm)')
#     plt.ylabel('Power Density (W/m^3)')
#     plt.xlim(0,2000)
#     plt.ylim(0)

#     plt.legend()
#     plt.grid(True)
#     #plt.show()
#     plt.savefig('static/my_plot.png')
    
    
# def print_data(params):
#     print(params)
