#!/usr/bin/env python3

import subprocess, sys
import os
import argparse



'''
OPS445 Assignment 2
Program: duim.py 
Author: "Sagar Sharma"
The python code in this file (duim.py) is original work written by
Sagar Sharma. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script intends to build a tool for inspecting directories. 
This tool displays the contents inside a directory and presents bar garph to demonstarte how much drive space they are using.
This tool has been given a name "du".

Date: 2024/03/23
'''

def parse_command_args():
    """
    This function creates the argument parser for three arguments:
    1. -l or --length: Defines the length of the graph.
    2. -H or --human-readable: This returns the size of the directory in human readable format.
    3. target: It mentions our targeted location of the directory.   
    """
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2023") # Creates an argument parser object.
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". Uses -H to provide help with printing size in human readable format.
    parser.add_argument("-H", "--human-readable", action='store_true', help="This help you to print sizes in human readable format (e.g., KB, MB, GB).")
    # add argument for "target". set number of args to 1.
    parser.add_argument("target", nargs=1, help="Provide us with your target directory.")
    args = parser.parse_args()  #Parses the command-line arguments.
    return args


def percent_to_graph(percent: int, total_chars: int) -> str:
    """
    This Function converts the given percentage into a bar graph.
     Returns a string: eg. '##  ' for 50 if total_chars == 4       """

    # Checks if given percentage falls within 0 to 100 range.
    if percent >= 0 and percent <= 100:
        bar_graph_fill = int((percent / 100) * total_chars + 0.5) # Calculates the number of hastags to represent the bar graph. Using + 0.5 for rounding the value to its closest integer.
        blank_space = total_chars - bar_graph_fill
        return '#' * bar_graph_fill + ' ' * blank_space #Returns bar graph.
    else:
        return "Percentage must be between 0 and 100." # Returns error message of percentage falls out of the range 0-100.  


def call_du_sub(location: str) -> list:
    """
    This function uses subprocess to execute command `du -d 1 + location`. The location refers to user specified directory.
    Eventually the function returns the output as a list. """
    given_command = 'du -d 1' + location # Command is stored in a variable along with the path to directory.
    sub_procc = subprocess.Popen(given_command, stdout= subprocess.PIPE, stderr = subprocess.PIPE, shell = True) #Created a process with subprocess module to run above command.
    stdout, stderr = sub_procc.communicate() # Communicating to get the output from subprocess.

    output_decode = stdout.decode('utf-8') # Decodes output using default endcode utf-8.
    lines_output = output_decode.split('\n') #Splitting decoded output into lines.

    sub_directory_list = [] # New list to store the subdirectories.

    # To iterate over each lines in the above output.
    for line in lines_output:
        index_of_firstSpace = line.find(' ')   # Finding the index number of first space character.
        path_to_directory = line[index_of_firstSpace + 1:] # Storing path to the directory from the line.

        # If the path from line is not same as the location provided,    
        if path_to_directory != location:
            sub_directory_list.append(path_to_directory)   # Adding directory to the list.
    return sub_directory_list


def create_dir_dict(raw_dat: list) -> dict:
    """
    This function gets list from call_du_sub, and returns dict {'directory': 0} where 0 is size. """
    # Creates an empty dictonary to store the size of dictonary.
    dictionary_directory = {}
    #Iterates over each line from the raw_dat dictionary.
    for component in raw_dat:
        #Separating the component into size and path by using tab character.
        size_of_dir, path_to_dir = component.split('\t')
        # This adds the path to directory and its size to the dictionary. Also, converts the size to an integer.
        dictionary_directory[path_to_dir] = int(size_of_dir)
    return dictionary_directory # Returns the dictionary.

        
def main():
    """ 
    This functions is the main function that executes and runs the overall script."""

    # This parses the arguments.
    args = parse_command_args()
    raw_dat = call_du_sub(args.target[0]) # Use of call_du_sub function to execute given du command which returns the output as list.
    dictionary_from_directory = create_dir_dict(raw_dat) #Use of create_dir_dict function.
    
    #Calculates total size of directories.
    total_dir_size = 0 #Puts initial value as 0.
    #Uses for loop to calculate the total size.
    for a_size in dictionary_from_directory.values():
        total_dir_size += a_size
    
    #Creates bar garph using the graph function.
    final_bar_graph = percent_to_graph(dictionary_from_directory, args.length)

    print(final_bar_graph) #Prints bar graph.

if __name__ == '__main__':
    main()
