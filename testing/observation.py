import scipy.constants
import numpy as np

# constants
KB = scipy.constants.Boltzmann
H = scipy.constants.Planck
C = scipy.constants.c

import astropy.units as u



class Observation:
    
    # these should be manually adjusted if any changes are made to the number of input fields
    fields = { "camera": 9, "telescope": 3, "filter": 3, "point": 2, "extended": 2, "conditions": 2, "snr": 1 }
       
    @classmethod
    def field_count(self):
        return sum( self.fields.values() )
    
    # TODO: perhaps main can have a function to validate this count with the count from form.py? 
    
    @classmethod
    def param_count(self, param: str):
        if param in self.fields: 
            return self.fields[param]
        
        
    
    
        
    
    
    def __init__(self, params: dict):
        
        
        #--- camera parameters ---#
        self.sensor_X = int( params["sensor_x"] )
        self.sensor_Y = int( params["sensor_y"] )
        self.pixel_size = params["px_size"] * 10**(-6)
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
        self.scope_dia = params["scope_dia"]*u.m #telescope diameter in metres
        self.scope_focal = params["scope_focal"]
        self.plate_scale = params["plate_scale"]
        
        self.pixel_area = self.plate_scale**2 #arcsec^2
        self.mirror_area = np.pi * (self.scope_dia/2) ** 2
        self.f_ratio = self.scope_focal/self.scope_dia
        
        
        #--- filter parameters ---#
        
        self.filter_name = 'g' 
        # TODO:
        
        self.filter_low = params["filter_low"] * 1*10**(-9)  #TODO something else here, check with Ryan
        self.filter_high = params["filter_high"]  * 1*10**(-9)
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
            self.seeing_pixel = self.seeing_cond/self.plate_scale
        
        
        # extended sources
        elif self.type == "extended":
            
            self.source = params["extended_src"]
            self.library = "brown"
            
            self.dist = params["dist"]
            self.ext_mag = params["ext_mag"]
            
            
            
            self.seeing_pixel = 5/self.plate_scale
        
        # invalid source
        else: 
            print("source error when determining target")
            # TODO: default black body?
        
               
        
        #--- conditions ---#
        # self.seeing_cond = params["seeing"] # doesn't affect extended sources
        self.sky_bright = params["sqm"]
        # self.seeing_pixel = self.seeing_cond/self.plate_scale
    
            
        #--- signal to noise ---#
        self.snr = params["desired_snr"]
        
  
        
        #GENERATE APERTURE FOR MEASURING SNR
        self.aperture_rad = self.seeing_pixel*0.67
        self.aperture_center = (self.sensor_X/2,self.sensor_Y/2)
        self.aperture_num_pixels = np.pi*self.aperture_rad**2
        
        
        
        
        
        
    def validate(self):

        if self.filter_high < self.filter_low:
            
            return "Low filter pass cannot be greater than high filter pass"
        
        else: return None          
                
                


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
    