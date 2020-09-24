# All imports go on top
# my own text Modification stuff
# my own CSV Handling Library
import CSV_File_Lib
import Interaction_Lib
import time

# Global Variables Below that
Index_of_commands = ['modify', 'duplicate', 'search', 'refresh', 'exit', 'read', 'write']
# Sets IDK to an integer Data-Type and sets it to 0
idk = 0
# Makes a Dictionary called file contents
file_contents = {}
# Not used but hopefully will be, essentially sets up a list named file_params
file_header = []
# creates and Sets Max line number to 1
max_line_number = 1
# Lines total, might not actually be used
lines_total = 0
LFSEnabled = None
file_name = 'TestDeleteCSV.csv'


# Functions After that...
def import_file(file_path, ForceLFS):
    global LFSEnabled
    file_internal = CSV_File_Lib.import_csv(file_path, ForceLFS)
    LFSEnabled = file_internal['LFS_Enabled']
    del file_internal['LFS_Enabled']
    return file_internal


def message_prompt(Text, Desensitize):
    Interaction_Lib.Prompt_feedback(Text, Desensitize=Desensitize)


def shell_prompt():
    Interaction_Lib.End_User_prompt(Index_of_commands)


def save_file(LFS):
    CSV_File_Lib.write_back_to_csv(file_contents, file_name, LFS=LFS)


def get_header():
    CSV_File_Lib.get_csv_header(file_contents)


def find():
    CSV_File_Lib.search_csv(file_contents)


# Defines End user prompt, the point bing to make this a nice CLI tool similar to the one used in Diskpart
# My favorite CLI tool, it uses commands like List Disk, select disk 3 etc. I like the simple nature of commands

# Look for commands and calls functions based on them


def command_logic(next_action):
    # Splits next_action up into words and puts them in a list
    syntax = next_action.split()
    # Essentially is a list of things to remove in the command, but makes it more readable for humans
    clean_command = ['line', 'each', 'for', 'column', 'in', 'parameter', 'on', 'row']
    for word in clean_command:
        if word in syntax:
            syntax.remove(word)
    # Exits if you wish to exit
    if 'exit' in next_action:
        pass
    # Modify the file by calling modify with the syntax required
    if 'modify' in next_action:
        print('modifying')
        if syntax[1] and syntax[2] is not None:
            pass
        print('Uh oh, No file line or parameter name! ')
    if 'print' in next_action or 'read' in next_action:
        if 'to' not in next_action:
            CSV_File_Lib.read_line(syntax[1], file_contents)
        else:
            pass


file_contents = import_file('Testfile_large.csv', True)
print('Imported')
file_header = CSV_File_Lib.get_csv_header(file_contents)

CSV_File_Lib.sort_dictionary(file_contents, 2, True, False)
