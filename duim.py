#!/usr/bin/env python3
import subprocess
import argparse
import sys

def call_du_sub(target_directory):
    command = ['du', '-d', '1', target_directory]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode('utf-8').strip().split('\n')

def percent_to_graph(percent, total_chars):
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be a number between 0 and 100.")
    filled_chars = int((percent / 100) * total_chars)
    return '=' * filled_chars + ' ' * (total_chars - filled_chars)

def create_dir_dict(du_list):
    dir_dict = {}
    for line in du_list:
        size, dir_path = line.split('\t')
        dir_dict[dir_path] = int(size)
    return dir_dict

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action='store_true', help="Print sizes in human readable format (e.g., KB, MB, GB).")
    parser.add_argument("target", nargs=1, help="Specify the target directory.")
    args = parser.parse_args()
    return args

def main():
    args = parse_command_args()
    du_list = call_du_sub(args.target[0])
    sizes = create_dir_dict(du_list)
    total_size = sum(sizes.values())
    total_size_hr = total_size / 1024 if args.human_readable else total_size
    for dir_path, size in sizes.items():
        percent = (size / total_size) * 100
        size_hr = size / 1024 if args.human_readable else size
        print(f'{percent:.2f} % [{percent_to_graph(percent, args.length):<20}] {size_hr:.1f} M    {dir_path}')
    print(f'Total: {total_size_hr:.1f} M   {args.target[0]}')

if __name__ == '__main__':
    main()
