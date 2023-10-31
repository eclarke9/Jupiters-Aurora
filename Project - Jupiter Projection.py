# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:47:53 2023

@author: ellie
"""

import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from astropy.io import fits
import os

#Starting by making a function to create a binary image.
#input_map = the initial input image of aurora
#percentile_value = can be changed to get binary images at different brightness thresholds
#plot_histogram = showing brightness in histogram
def create_binary_map(input_map, percentile_value, plot_histogram=False):

    #Flatten data to 1D array and find date and time image was taken for title
    image = data.flatten()
    #image = image[100:10000]
    #date = hdulist[0].header['udate']

    #Calculate the brightness threshold based on the percentile
    brightness_threshold = np.percentile(image, percentile_value * 100)

    #Creating the binary map
    #Any area above brightness threshold given value 1, any area below given value 0 
    binary_map = np.where(data >= brightness_threshold, 1, 0)

    #Plotting the histogram
    if plot_histogram:
        histogram = plt.hist(image, bins=30)
        plt.axvline(brightness_threshold, color='black', label='99th percentile')
        plt.yscale('log')
        plt.xlabel('Brightness Value')
        plt.ylabel('Number of Pixels')
        plt.legend()
        plt.title('Histogram '+date)
        plt.show()

    return binary_map

#Want to run through all the files in a specific folder
#Defining the path to the folder with all the necessary files
folder_paths = [r"C:\Users\ellie\Project Data\STIS\2017\007\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\036\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\037\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\038\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\079\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\080\derived",
                r"C:\Users\ellie\Project Data\STIS\2017\081\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\139\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\140\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\141\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\190\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\191\derived",
               r"C:\Users\ellie\Project Data\STIS\2017\192\derived"]

#Initialize variables
sum_binary_maps = None
num_observations = 0

#Create list of all the files in the folder containing data
for folder_path in folder_paths:
    file_list = os.listdir(folder_path)

    #Making sure to only include the fits files
    fits_files = [file for file in file_list if file.endswith(".fits")]
    
    #Opening each fits file in the folders
    for fits_file in fits_files:
        hdulist = fits.open(os.path.join(folder_path, fits_file))
        
        #Picking which hemishpere to deal with from the headers
        hemisph = hdulist[0].header['hemisph']
        if hemisph != 'north':
            continue
        
        #Taking the time and date of image for title
        data = hdulist[0].data
        date = hdulist[0].header['udate']
    
        #Plotting histogram and binary image
        #Have commented histogram and binary maps to save time running code
        binary_map = create_binary_map(data, percentile_value=0.99)#, plot_histogram=True)
        #plt.imshow(binary_map, cmap='gray')
        #plt.title('Binary Image '+date)
        #plt.colorbar()
        # plt.show()
        
        #Creating an empty guide in the shape of each individual binary map to layer the maps in
        if sum_binary_maps is None:
            sum_binary_maps = np.zeros_like(binary_map)

        #Adding each of the binary maps to the sum
        sum_binary_maps += binary_map
        num_observations += 1

#Need to divide the sum of binary maps by the number of observations
final_result = sum_binary_maps / num_observations
#Putting the axes into the right units (degrees - lat&long)
array = np.full(final_result.shape, 4)
image = final_result / array

#Plotting the binary image of all datasets layered on top of each other
plt.imshow(image, cmap='viridis', extent=[0, 360, 180, 0])#, norm=colors.LogNorm())
plt.gca().invert_yaxis()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Percentage of Observations with Pixels Brighter\nthan the 99th Percentile (Northern Hemisphere)')#' (Log Scale)')
plt.colorbar()
plt.show()


#Creating a list of the 12 different threshold values for the plots
#Used colorbar from binary image above to decide what 12 values to select
#Northern hemisphere
threshold_values = [0.18, 0.165, 0.15, 0.135, 0.12, 0.105, 0.09, 0.075, 0.06, 0.045, 0.03, 0.015]
#Southern hemisphere
#threshold_values = [0.12, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

#Create a 3x4 grid of binary images
fig, axes = plt.subplots(3, 4, figsize=(10, 5))

#Flatten the axes array
axes = axes.ravel()

#Creating function to plot each binary image over a certain threshold brightness value
#Enumerate will associate each threshold value with its corresponding subplot 
for i, threshold in enumerate(threshold_values):
    binary_image = np.where(image > threshold, 1, 0)
    ax = axes[i]
    ax.imshow(binary_image, cmap='gray', extent=[0, 360, 180, 0])
    ax.invert_yaxis()
    fig.suptitle('Binary Images at Multiple Brightness Thresholds (Northern Hemisphere)', fontsize=14)
    ax.set_title(f'Threshold = {threshold:.3f}')
    ax.set(xlabel='Longitude', ylabel='Latitude')
    ax.label_outer()
    
plt.show()


#Creating a projection of the binary images onto a globe like Jupiter
def jupiter_aurora_image():
    image

    #Define the semimajor and semiminor axes, don't want default ellipse shape
    image_globe = ccrs.Globe(semimajor_axis=285000., semiminor_axis=229000.,ellipse=None)
    
    #Map projection
    image_proj = ccrs.PlateCarree(globe=image_globe)

    #Setting extent of projection - limiting it
    image_extent = (180, -180, 90, -90)

    return image, image_globe, image_proj, image_extent

#Function to run projection
def proj():
    image, globe, crs, extent = jupiter_aurora_image()
    
    #Necessary to make rectangle be projected onto sphere
    os.environ["PROJ_IGNORE_CELESTIAL_BODY"] = "YES"

    #What projection you want: NorthPolarStereo, etc
    #Change central_latitude to -90 for southern hemisphere
    projection = ccrs.NearsidePerspective(central_latitude=90, satellite_height=4000000000)
    
    #Plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    ax.imshow(image, transform=crs, extent=extent, cmap='viridis')
    plt.title("Jupiter's Aurora\n(North Pole Perspective)")
    plt.show() 
    
proj()
  
