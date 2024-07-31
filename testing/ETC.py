import matplotlib
# matplotlib.use('agg')   # very important for Flask, matplot does not work otherwise
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import scipy.constants

import numpy as np
import math


from spextra import SpecLibrary, Spextrum 

import testing.source_counts as cts


# constants
KB = scipy.constants.Boltzmann
H = scipy.constants.Planck
C = scipy.constants.c



class Calculator:
       
    
    def __init__(self, params):
        
        
        #--- camera parameters ---#
        self.sensor_X = int( params["sensor_x"] )
        self.sensor_Y = int( params["sensor_y"] )
        self.pixel_size = params["px_size"] * 10**(-6) #TODO: why?
        self.Q_efficiency = params["q_efficiency"]
        self.read_noise = params["read_noise"]
        self.gain = params["gain"]
        self.sensor_offset = params["offset"]
        self.dark_noise = params["dark_noise"]
        self.full_well = params["full_well"]
        
        # TODO: caculate sensor dimensions in...
        self.sensor_width = self.sensor_X * self.pixel_size
        self.sensor_height = self.sensor_Y * self.pixel_size
        
        
        #--- telescope parameters ---#
        self.scope_dia = params["scope_dia"]
        self.scope_focal = params["scope_focal"]
        self.plate_scale = params["plate_scale"]
        
        self.pixel_area = self.plate_scale**2 #arcsec^2
        self.mirror_area = np.pi * (self.scope_dia/2) ** 2
        self.f_ratio = self.scope_focal/self.scope_dia
        
        
        #--- filter parameters ---#
        
        self.filter_name = 'g'
        
        self.filter_low = params["filter_low"] * 10**(-9)  #TODO something else here, check with Ryan
        self.filter_high = params["filter_high"]  * 10**(-9)
        self.filter_zero = params["filter_zero"]
        
        self.filter_low_freq = C/self.filter_low
        self.filter_high_freq = C/self.filter_high
        self.filter_freq_band = self.filter_low_freq - self.filter_high_freq
        
        
        
        #--- determine target type ---#
        
        self.type = params["source_type"]
            
        # point source
        if self.type == "point":
            
            self.source = params["point_src"]
        
            self.ab_mag = params["star_ab_mag"]
            self.star_temp = params["star_temp"]
    
    
            self.seeing_cond = params["seeing"]
        
        
        # extended sources
        elif self.type == "extended":
            
            self.source = params["extended_src"]
            self.library = "brown"
            
            # self.surf_brightness = params["surf_brightness"]
            self.ext_mag = params["ext_mag"]
        
        # invalid source
        else: print("source error when determining target")
                
        
        #--- conditions ---#
        self.seeing_cond = params["seeing"] # doesn't affect extended sources
        self.sky_bright = params["sqm"]
        self.seeing_pixel = self.seeing_cond/self.plate_scale
    
            
        #--- signal to noise ---#
        self.snr = params["desired_snr"]
        
        
        
        
        
        
    def validate(self):

        if self.filter_high < self.filter_low:
            
            return "Low filter pass cannot be greater than high filter pass"
        
        else: return None          
                
                
            
    def calc_counts(self):
                
        if self.type == "point":
                        
            try:
                return cts.stellarSpec(self.source, self.ab_mag, self.mirror_area, self.filter_name)*self.Q_efficiency
            except:
                print("Unable to find source. Defaulting to black body.")
                return cts.blackBody(self.star_temp, self.ab_mag, self.mirror_area,self.filter_name)*self.Q_efficiency
        
        elif self.type == "extended":
            
            return cts.extSpec(self.source, self.library, self.ext_mag, self.mirror_area, self.filter_name)*self.Q_efficiency*self.pixel_area
            
        else: print("source error when finding counts")   