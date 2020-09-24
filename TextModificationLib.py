# Basic handling of strings and conversions necessary to convert String to Dictionary
# Used to do the conversion to Dictionary at the end
import ast


# TTR (Text to replace)
def replace(input_string, ttr, replace_with):
    return input_string.replace(ttr, replace_with)


# TTR (Text to remove)
def remove(input_string, ttr):
    step_1 = input_string.replace(ttr, "")
    return step_1


# Recombines a list file into a string
def recombine(list_text):
    list_to_str = ' '.join([str(elem) for elem in list_text])
    return list_to_str


# Splits a string int a list given a specified marker
def split(input_string, split_by):
    final_var = input_string.split(split_by)
    return final_var


def Unwrap(input_string, left_side, right_side, add_back_ending):
    input_string = input_string.strip(left_side)
    input_string = input_string.strip(right_side + ' \n')
    if add_back_ending:
        input_string = input_string + ' \n' + right_side
    return input_string


# Adds something to both sides, can be used with "" on the side you do not want anything in to add something to the
# beginning or end. IE: add_to_both_sides('gg', '', 'f') will net 'ggf'
def add_to_both_sides(input_string, left_side, right_side):
    input_string = left_side + input_string + right_side
    return input_string


# Turns a string variable into a dictionary This is my only external import in my entire script
def To_Dictionary(string):
    string_2 = ast.literal_eval(string)
    return string_2


def Read_file(file_to_read):
    try:
        # Opens file
        file = open(file_to_read, mode='r')
        # Reads file and saves it in Variable
        contents = file.read()
        # Close the file
        file.close()
        # Passes on the contents and makes sure the Global variable also has it
        return contents
    except FileNotFoundError:
        print('Error: File not Found')
        return None


# Checks the file for contents
def Check_File_Has_Contents(input_file):
    file = open(input_file, "r")
    # Sets the cursor essentially to 0 on the text file
    file.seek(0)
    # Check for any Text in the file
    data = file.read(100)
    # If there are no Characters then assume the file needs to be regenerated
    if len(data) == 0:
        setup = False
    # if not Just Boot normally.
    else:
        print("Mounting SpreadSheet!")
        setup = True
    return setup


def python_list_to_Human_list(text):
    # Grabs the text one line_number at a time to format it
    text_intermediate = str(text)
    # Removes extra space in beginning keeping with excessive use the text flying off into space
    text_intermediate = replace(text_intermediate, ', ', ',')
    # Removes Square bracket Left
    text_intermediate = remove(text_intermediate, '[')
    # Removes Square Bracket right
    text_intermediate = remove(text_intermediate, ']')
    # Removes single quote in values
    text_intermediate = remove(text_intermediate, "'")
    # Prints for Debugging (currently disabled)
    # print(text_intermediate)
    # Writes it and a new line_number at the end
    return text_intermediate


# Uses function .casefold() to make it lower case and do case-less matching to ensure it matches and makes things case
# insensitive
def make_lowercase(string):
    user_input = str(string)
    final_value = user_input.casefold()
    return final_value


# I found this online and do not fully understand the specifics, The code reads the raw data which is many times
# Faster for getting the line numbers in large files
def Count_Lines_Fast(file_name):
    # Opens the file raw
    f = open(file_name, 'rb')
    # sets lines equal to 0
    lines = 0
    # sets the buffer size
    buf_size = 1024 * 1024
    # Reads the file raw this is quick for large files
    read_f = f.read
    # takes the contents of read_f and gets buffer size
    buf = read_f(buf_size)
    # Past this point I can only guess as to it just counting the times new line is used and using that to get it's
    # line count This was the only reasonable way I could get the amount of lines
    while buf:
        # Finds out hw many \n things there are?
        lines += buf.count(b'\n')
        # Reads buffer size
        buf = read_f(buf_size)
    # Return Lines
    return lines


def RemoveCPPStyleComments(string_input):
    lines = split(string_input, '\n')
    lines_dict = {}
    number = 0
    for line in lines:
        lines_dict[number] = line
        number += 1
    for x in range(1, 2):
        for line in lines_dict:
            if '//' in lines_dict[line]:
                lines_dict[line] = None
    lines.clear()
    for each in lines_dict:
        if lines_dict[each] is not None:
            lines.append(lines_dict[each] + '\n')
    return lines
