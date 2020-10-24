import argparse
from colorama import Fore, Back, Style
import csv
import os


def file_rename_undo(dir, filename):
    path = f'{dir}/{filename[0]}'
    with open(f'{path}', mode='r') as file:
        reader = csv.DictReader(file)
        line_count = 0
        for row in reader:
            if line_count == 0:
                # print(f'Column names are: {", ".join(row)}')
                line_count += 1
            try:
                print(
                    Fore.YELLOW + f'Renaming \"{row["new_path"]}\" to \"{row["old_path"]}\"...')
                os.rename(row["new_path"], row["old_path"])
                print(Fore.YELLOW + 'done.')
            except Exception as ex:
                print(Fore.RED + 'failed.')
                print(ex)
            line_count += 1


parser = argparse.ArgumentParser(description='Undo file rename options')
parser.add_argument('-f', '--file', metavar='', nargs='+',
                    help='Name of log file')
parser.add_argument('-d', '--dir',  metavar='',
                    help='Path to directory where file can be found')

args = parser.parse_args()

# https://docs.python.org/3/library/__main__.html
if __name__ == "__main__":
    # execute only if run as a script
    file_rename_undo(args.dir, args.file)
