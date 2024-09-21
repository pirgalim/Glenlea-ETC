from spextra import Spextrum, SpecLibrary, Passband

import matplotlib
matplotlib.use('agg')   # very important for Flask, matplot does not work otherwise
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
import astropy.units as u

import io

from services.observation import Observation



def blackBody(starTemp,starMag,mirrorArea,filterName):

    blackBodySpec = Spextrum.black_body_spectrum(temperature = starTemp, amplitude = starMag*u.ABmag, filter_curve=filterName)

    starPhotons = blackBodySpec.photons_in_range(area=mirrorArea,filter_curve=filterName)

    wavelengths = blackBodySpec.waveset
    fluxes = blackBodySpec(wavelengths, flux_unit="PHOTLAM")

    filter = Passband(filterName) 

    filterWLS = filter.waveset
    filterPass = filter(filterWLS)

    # Plot filter transmission curve and black body spectrum

    fig, ax1 = plt.subplots()
    
    

    ax1.set_xlabel('Wavelength (Å)')
    ax1.set_ylabel('Flux (photons/sec/cm^2/Å)')
    stellarPlot, = ax1.plot(wavelengths, fluxes, label='Stellar Black Body Spectrum',color='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Filter Transmission Coefficient')
    filterPlot, = ax2.plot(filterWLS, filterPass, label= filterName + ' Filter Transmission',color='b')

    plt.title('Filtered Black Body Spectrum')
    plt.xlim(0,25000)
    ax2.set_ylim(0)
    ax1.set_ylim(0)

    plots = [stellarPlot,filterPlot]
    labels = [plot.get_label() for plot in plots]

    ax1.legend(plots,labels,loc='best')
    plt.grid(True) 
    #plt.show()
    
    # plt.savefig('static/plot_light_curve_SB.png')
    
    # matplot.pyplot.close()
    
   

    return starPhotons.value





def testPlot(starTemp,starMag,mirrorArea,filterName):
    blackBodySpec = Spextrum.black_body_spectrum(temperature = starTemp, amplitude = starMag*u.ABmag, filter_curve=filterName)

    starPhotons = blackBodySpec.photons_in_range(area=mirrorArea,filter_curve=filterName)

    wavelengths = blackBodySpec.waveset
    fluxes = blackBodySpec(wavelengths, flux_unit="PHOTLAM")

    filter = Passband(filterName) 

    filterWLS = filter.waveset
    filterPass = filter(filterWLS)

    # Plot filter transmission curve and black body spectrum

    fig, ax1 = plt.subplots()
    
    

    ax1.set_xlabel('Wavelength (Å)')
    ax1.set_ylabel('Flux (photons/sec/cm^2/Å)')
    stellarPlot, = ax1.plot(wavelengths, fluxes, label='Stellar Black Body Spectrum',color='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Filter Transmission Coefficient')
    filterPlot, = ax2.plot(filterWLS, filterPass, label= filterName + ' Filter Transmission',color='b')

    plt.title('Filtered Black Body Spectrum')
    plt.xlim(0,25000)
    ax2.set_ylim(0)
    ax1.set_ylim(0)

    plots = [stellarPlot,filterPlot]
    labels = [plot.get_label() for plot in plots]

    ax1.legend(plots,labels,loc='best')
    plt.grid(True) 
    # #plt.show()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    image_data = img_buffer.getvalue()
     
    return image_data




def stellarSpec(starClass,starMag,mirrorArea,filterName):

    starSpec = Spextrum("pickles/"+starClass).scale_to_magnitude(amplitude = starMag*u.ABmag, filter_curve=filterName)

    starPhotons = starSpec.photons_in_range(area=mirrorArea,filter_curve=filterName)

    wavelengths = starSpec.waveset
    fluxes = starSpec(wavelengths, flux_unit="PHOTLAM")

    filter = Passband(filterName) 

    filterWLS = filter.waveset
    filterPass = filter(filterWLS)

    # Plot filter transmission curve and stellar spectrum

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Wavelength (Å)')
    ax1.set_ylabel('Flux (photons/sec/cm^2/Å)')
    stellarPlot, = ax1.plot(wavelengths, fluxes, label='Stellar Spectrum',color='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Filter Transmission Coefficient')
    filterPlot, = ax2.plot(filterWLS, filterPass, label= filterName + ' Filter Transmission',color='b')

    plt.title('Filtered Stellar Spectrum')
    plt.xlim(0,25000)
    ax2.set_ylim(0)
    ax1.set_ylim(0)

    plots = [stellarPlot,filterPlot]
    labels = [plot.get_label() for plot in plots]

    ax1.legend(plots,labels,loc='best')
    plt.grid(True) 
    #plt.show()

    # plt.savefig('static/plot_light_curve_SB.png')

    return starPhotons.value





def extSpec(extClass,extLib,extMag, mirrorArea,filterName):

    # extSpec = Spextrum(extLib+"/"+extClass).scale_to_magnitude(amplitude = extMag*u.ABmag, filter_curve=filterName)
    
    extSpec = Spextrum(extLib+"/"+extClass).scale_to_magnitude(amplitude = extMag*u.ABmag, filter_curve=filterName)

    extPhotons = extSpec.photons_in_range(area=mirrorArea,filter_curve=filterName)

    wavelengths = extSpec.waveset
    fluxes = extSpec(wavelengths, flux_unit="PHOTLAM")

    filter = Passband(filterName) 

    filterWLS = filter.waveset
    filterPass = filter(filterWLS)

    # Plot filter transmission curve and stellar spectrum

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Wavelength (Å)')
    ax1.set_ylabel('Flux (photons/sec/cm^2/Å)')

    extLabel = extClass +" Source Spectrum"
    extPlot, = ax1.plot(wavelengths, fluxes, label=extLabel,color='r')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Filter Transmission Coefficient')
    filterPlot, = ax2.plot(filterWLS, filterPass, label= filterName + ' Filter Transmission',color='b')

    plt.title('Filtered Extended Source Spectrum')
    plt.xlim(0,25000)
    ax2.set_ylim(0)
    ax1.set_ylim(0)

    plots = [extPlot,filterPlot]
    labels = [plot.get_label() for plot in plots]

    ax1.legend(plots,labels,loc='best')
    plt.grid(True) 
    #plt.show()

    # plt.savefig('static/plot_light_curve_SB.png')

    return extPhotons.value











#GENERATE SKY BACKGROUND EMISSION

def generateBG(sensorX, sensorY, skyMag, filterName, mirrorArea, sensorGain, sensorQE, pixelArea, obsType):

    # Define Background as a black body plus an emission line corresponding to sulfur lamp emission
    # TO-DO: Update flux to correspond with real emision

    bgSpec = Spextrum("sky/MR").scale_to_magnitude(amplitude = skyMag*u.ABmag, filter_curve=filterName)

    bgPhotons = bgSpec.photons_in_range(area=mirrorArea,filter_curve=filterName)

    print("The sensor receives:", bgPhotons.value*sensorGain*sensorQE*pixelArea, "counts per second per pixel due to light pollution.")

    wavelengths = bgSpec.waveset
    fluxes = bgSpec(wavelengths, flux_unit="PHOTLAM")

    filter = Passband(filterName) 

    filterWLS = filter.waveset
    filterPass = filter(filterWLS)

    # Plot filter transmission curve and black body spectrum

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Wavelength (Å)')
    ax1.set_ylabel('Flux (photons/sec/cm^2/Å)')
    bgPlot, = ax1.plot(wavelengths, fluxes, label='Background Sky Emission',color='g')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Filter Transmission Coefficient')
    filterPlot, = ax2.plot(filterWLS, filterPass, label= filterName + ' Filter Transmission',color='b')

    plt.title('Filtered Black Body Spectrum')
    plt.xlim(0,25000)
    ax2.set_ylim(0)
    ax1.set_ylim(0,0.05)

    plots = [bgPlot,filterPlot]
    labels = [plot.get_label() for plot in plots]

    ax1.legend(plots,labels,loc='best')
    plt.grid(True) 
    #plt.show()

    if obsType == "extended":

        return bgPhotons.value*sensorGain*sensorQE*pixelArea
    
    elif obsType == "point":

        bgValues = np.zeros([sensorY,sensorX])

        for x in range(sensorY):
            for y in range(sensorX):
                bgValues[x,y] = bgPhotons.value*sensorGain*sensorQE*pixelArea

        return bgValues
    
    
    
    







def aperture(obs: Observation, final_sensor_array):
        
        x = int(obs.sensor_X)
        y = int(obs.sensor_Y)
        # counts = obs.countsPerSecond()
        
        # test_exposure = 1 
        # signal_values = obs.spreadCounts(x,y,counts,obs.seeing_pixel,test_exposure)
        # noise_values= obs.generateNoise(x,y,obs.dark_noise,obs.read_noise,obs.sensor_offset,test_exposure)
        # bg_values = obs.generateBG(x,y,obs.sky_bright,obs.filter_zero,obs.mirror_area,obs.gain,obs.filter_low,obs.filter_high,obs.Q_efficiency,obs.filter_freq_band,test_exposure)
        # final_sensor_array = obs.overfullCheck(signal_values+noise_values+bg_values,obs.full_well)
        
        # global bgValues
        # bgValues = bg_values
        
        
        
        
        #GENERATE APERTURE FOR MEASURING SNR
        aperture_rad = obs.seeing_pixel*0.67
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
        
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        image_data = img_buffer.getvalue()
        
        return image_data
        # plt.savefig('static/spread_counts.png')
        
        # return ( int(np.max(final_sensor_array)), int(np.min(final_sensor_array)) )  