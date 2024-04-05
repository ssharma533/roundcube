
#!/usr/bin/env python3

import subprocess, sys
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
    # adds argument for "human-readable". Uses -H to provide help with printing size in human readable format.
    parser.add_argument("-H", "--human-readable", action='store_true', help="This help you to print sizes in human readable format (e.g., KB, MB, GB).")
    # adds argument for "target". set number of args to 1.
    parser.add_argument("target", nargs=1, help="Your target directory.")
    # Adds a new argument for the threshold size. This is an additional feature. Default value has been set as 0.
    parser.add_argument("-t", "--threshold", type=int, default=0, help="Specify a threshold size. Directories smaller than the threshold size will be not be represented in a bar garph.")
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
    This function uses subprocess to call `du -d 1 + location`, returns raw list """
    given_command = 'du -a ' + location # Command is stored in a variable along with the path to directory.
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
    This function gets list from du_sub, and returns dict {'directory': 0} where 0 is size. """
    # Creates an empty dictonary to store the size of dictonary.
    dictionary_directory = {}
    #Iterates over each line from the raw_dat dictionary.
    for component in raw_dat:
        #Separating the component into size and path by using tab character.
        size_of_dir, path_to_dir = component.split('\t')
        # This adds the path to directory and its size to the dictionary. Also, converts the size to an integer.
        dictionary_directory[path_to_dir] = int(size_of_dir)
    return dictionary_directory # Returns the dictionary.

    
def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

def create_dir_dict(raw_dat: list) -> dict:
    """
    This function gets list from call_du_sub, and returns dict {'directory': 0} where 0 is size. """
    # Creates an empty dictonary to store the size of dictonary.
    dictionary_directory = {}
    #Iterates over each line from the raw_dat dictionary.
    for component in raw_dat:
        # Checks if the component contains a tab character
        if '\t' in component:
            #Separating the component into size and path by using tab character.
            size_of_dir, path_to_dir = component.split('\t')
            # This adds the path to directory and its size to the dictionary. Also, converts the size to an integer.
            dictionary_directory[path_to_dir] = int(size_of_dir)
    return dictionary_directory # Returns the dictionary.
        
def format_final_bar_graph(final_bar_graph):
    """
    This function returns the formatted output of the final bar graph.
    """
    output = "Directory     Size    Bar Graph\n"
    output += "-------------------------------\n"
    for directory, size, bar in final_bar_graph:
        output += f"{directory:15} {size:8} {bar}\n"
    return output

def main():
    args = parse_command_args()
    raw_data = call_du_sub(args.target)
    directory_dictionary = create_dir_dict(raw_data)
    
    total_size_of_directory = sum(directory_dictionary.values())
    final_bar_graph = []

    for directory, size_of_directory in directory_dictionary.items():
        if size_of_directory >= args.threshold:
            percent = (size_of_directory / total_size_of_directory) * 100
            the_bar_graph = percent_to_graph(percent, args.length)
            bar_graph_str = f"{int(percent)}%    [{the_bar_graph}{' ' * (args.length - len(the_bar_graph))}]"
            final_bar_graph.append((directory, size_of_directory, bar_graph_str))
   
    formatted_output = format_final_bar_graph(final_bar_graph)        
    print(formatted_output)











# Calls the main function
if __name__ == "__main__":
    main()
