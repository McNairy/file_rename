import argparse
from colorama import Fore, Back, Style
import csv
import os
import re
import time

log_file = f'log_{time.time()}.csv'


def create_log_file(log_file):
    with open(f'{log_file}', mode='w') as file:
        fieldnames = ['old_path', 'new_path']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        try:
            writer.writeheader()
        except Exception as ex:
            print(ex)

# Convert string argument to boolean


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


# Rename a single file in a directory.
# TODO: Make OS agnostic.
def file_rename(dir, filename, search, replace):
    if dir == '.':
        dir = os.getcwd()

    old_path = f'{dir}/{filename[0]}'
    new_name = filename[0].replace(search[0], replace[0])
    new_path = f'{dir}/{new_name}'

    try:
        os.rename(old_path, new_path)
        print(Fore.YELLOW +
              f'Rename of the file "{old_path}" to "{new_path}" is complete.')

        csv_write(new_path, old_path, log_file)
    except Exception as ex:
        print(ex)

# Rename all files in a directory (not recursive).


def files_rename(dir, search, replace):
    if dir == '.':
        dir = os.getcwd()

    try:
        for filename in os.listdir(dir):
            # Only try to rename files that match searh parameter
            if filename.find(search[0]) != -1:
                old_path = f'{dir}/{filename}'
                new_name = filename.replace(search[0], replace[0])
                new_path = f'{dir}/{new_name}'
                os.rename(old_path, new_path)
                print(
                    Fore.YELLOW + f'Rename of the file "{old_path}" to "{new_path}" is complete.')
                csv_write(new_path, old_path, log_file)
            else:
                continue

    except Exception as ex:
        print(ex)


def csv_write(new_path, old_path, filename='log'):
    with open(f'{filename}', mode='a') as file:
        fieldnames = ['old_path', 'new_path']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        try:
            writer.writerow({'old_path': old_path, 'new_path': new_path})
        except Exception as ex:
            print(ex)


parser = argparse.ArgumentParser(description='File rename options')
parser.add_argument('-f', '--file', metavar='', nargs='+',
                    help='Name of file to be renamed')
parser.add_argument('-s', '--search', metavar='', nargs='+',
                    help='Search for character(s) to substitute')
parser.add_argument('-r', '--replace', metavar='', nargs='+',
                    help='Replacement character(s)')
parser.add_argument('-d', '--dir',  metavar='',
                    help='Path to directory where file can be found')
parser.add_argument('-a', '--all',  metavar='', default="false", nargs='+',
                    help='Rename all files in the directory (not recursive)')

args = parser.parse_args()

# https://docs.python.org/3/library/__main__.html
if __name__ == "__main__":
    # execute only if run as a script
    create_log_file(log_file)
    if str2bool(args.all[0]) == True:
        files_rename(args.dir, args.search, args.replace)
    else:
        file_rename(args.dir, args.file, args.search, args.replace)
