from spextra import Spextrum, SpecLibrary, Passband

import matplotlib
# matplotlib.use('agg')   # very important for Flask, matplot does not work otherwise
import matplotlib.pyplot as plt

import numpy as np
import astropy.units as u


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
    plt.show()

    return starPhotons.value





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
    plt.show()


    return starPhotons.value





def extSpec(extClass,extLib,extMag,mirrorArea,filterName):

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
    plt.show()


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
    plt.show()

    if obsType == "extended":

        return bgPhotons.value*sensorGain*sensorQE*pixelArea
    
    elif obsType == "point":

        bgValues = np.zeros([sensorY,sensorX])

        for x in range(sensorY):
            for y in range(sensorX):
                bgValues[x,y] = bgPhotons.value*sensorGain*sensorQE*pixelArea

        return bgValues