# currently rewriting Jupyter file
import matplotlib.pyplot as plt
import scipy.constants
plt.style.use('seaborn-poster')
import matplotlib.patches as patches
import scipy
import numpy as np
import math


# import base64
# from io import BytesIO
# from matplotlib.figure import Figure


#from PIL import Image




# sensor parameters, hard coded for now, will allow for user input later
pixel_size = 9 * 10**(-6) # add comments later
Q_efficiency = 0.5*0.95
read_noise = 13
gain = 0.92
sensor_offset = 50
dark_noise = 0.03
full_well = 60000
sensor_X = 400
sensor_Y = 267

sensor_width = sensor_X * pixel_size
sensor_height = sensor_Y * pixel_size


# observatory parameters, same thing
scope_dia = 0.3556
mirror_area = np.pi * (scope_dia/2) ** 2
scope_focal = 2.563
f_ratio = scope_focal/scope_dia
plate_scale = 0.75


# filters, same thing
filter_low = 500 * 1 * 10**(-9)
filter_low_freq = scipy.constants.c/filter_low

filter_high = 650 * 1 * 10**(-9)
filter_high_freq = scipy.constants.c/filter_high

filter_zero = 3781
filter_freq_band = filter_low_freq - filter_high_freq


# target, most likely custom, add bounds checking

star_dist = 1487.4
star_dist_m = star_dist * 9.461 * 10**15
star_temp = 5500
star_dia_solar = 1
star_dia = 1.392 * 10**9*star_dia_solar


# compute FOV

FOV_width = 206265 * sensor_width * (1/scope_focal)
FOV_height = 206265 * sensor_height * (1/scope_focal)
FOV_area = FOV_width * FOV_height


# sky parameters, again custom/dropdown

sky_bright = 20.87
seeing_cond = 5
seeing_pixel = seeing_cond/plate_scale



#def load_preset(event):


def OLD_plot_light_curve_SB():

    kB = scipy.constants.Boltzmann
    h = scipy.constants.Planck
    c = scipy.constants.c
    T = star_temp   # pass in function

    wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
    wlnm = wl * 10**9 

    P = ((2*np.pi*h*c**2)/(wl**5))*(1/np.exp((h*c)/(wl*kB*T)-1))


    plt.figure(figsize=(8, 6))
    plt.plot(wlnm, P, label='Stellar Black Body', color='y')
    plt.fill_between(wlnm, P, color='yellow', alpha=0.3, label='Stellar emission')

    plt.axvline(x=filter_low*10**9, color='r', linestyle='--', label='filter cut on')
    plt.axvline(x=filter_high*10**9, color='b', linestyle='--', label='filter cut off')

    plt.fill_betweenx(y=np.linspace(min(P), max(P) + 1*10**14), x1=filter_low*10**9, x2=filter_high*10**9, color='lightblue', alpha=0.4, label='Filter band pass')

    plt.title('Filtered Stellar Black Body Spectrum')
    plt.xlabel('Wavelengh (nm)')
    plt.ylabel('Power Density (W/m^3)')
    plt.xlim(0,2000)
    plt.ylim(0)

    plt.legend()
    plt.grid(True)
    plt.show()
    
    
def plot_light_curve_SB():
       
    
    kB = scipy.constants.Boltzmann
    h = scipy.constants.Planck
    c = scipy.constants.c
    T = star_temp   # pass in function

    wl = np.linspace(1 * 10**(-8), 5 * 10**(-6), 10000)
    wlnm = wl * 10**9 

    P = ((2*np.pi*h*c**2)/(wl**5))*(1/np.exp((h*c)/(wl*kB*T)-1))


    plt.figure(figsize=(8, 6))
    plt.plot(wlnm, P, label='Stellar Black Body', color='y')
    plt.fill_between(wlnm, P, color='yellow', alpha=0.3, label='Stellar emission')

    plt.axvline(x=filter_low*10**9, color='r', linestyle='--', label='filter cut on')
    plt.axvline(x=filter_high*10**9, color='b', linestyle='--', label='filter cut off')

    plt.fill_betweenx(y=np.linspace(min(P), max(P) + 1*10**14), x1=filter_low*10**9, x2=filter_high*10**9, color='lightblue', alpha=0.4, label='Filter band pass')

    plt.title('Filtered Stellar Black Body Spectrum')
    plt.xlabel('Wavelengh (nm)')
    plt.ylabel('Power Density (W/m^3)')
    plt.xlim(0,2000)
    plt.ylim(0)

    plt.legend()
    plt.grid(True)
    plt.savefig('static/my_plot.png')
    
    
    
