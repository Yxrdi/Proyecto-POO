# Import necessary modules
from csv import reader  # Import the 'reader' function from the 'csv' module to read CSV files
from os import walk  # Import the 'walk' function from 'os' module to traverse directories
import pygame  # Import the 'pygame' module to use its functions for game development

# Function to import a CSV layout (terrain map)
def import_csv_layout(path):
	terrain_map = []  # Create an empty list to store the terrain map layout
	with open(path) as level_map:  # Open the file at the provided 'path'
		layout = reader(level_map,delimiter = ',')  # Use 'reader' to read the CSV, splitting by commas
		for row in layout:  # Iterate through each row in the CSV layout
			terrain_map.append(list(row))  # Convert each row to a list and append to 'terrain_map'
		return terrain_map  # Return the complete terrain map

# Function to import all images from a folder
def import_folder(path):
	surface_list = []  # Create an empty list to store the surfaces (images)

	# Traverse the folder at the provided 'path'
	for _,__,img_files in walk(path):
		for image in img_files:  # Iterate through each image file in the folder
			full_path = path + '/' + image  # Construct the full path to the image file
			image_surf = pygame.image.load(full_path).convert_alpha()  # Load the image and apply transparency
			surface_list.append(image_surf)  # Add the image surface to the list

	return surface_list  # Return the list of image surfaces
