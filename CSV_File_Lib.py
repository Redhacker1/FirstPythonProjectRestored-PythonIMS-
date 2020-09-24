# My Text Modification Library
# My Command line library
import Interaction_Lib
import TextModificationLib
import time


def retrieve_line_list(file_contents, line_number, LFS):
    line_contents = file_contents.get(line_number)
    if LFS:
        line_contents = line_contents.split(',')
        return line_contents
    else:
        return line_contents


def retrieve_line_string(file_contents, line_number, LFS):
    if LFS:
        return file_contents.get(line_number)
    else:
        return TextModificationLib.python_list_to_Human_list(file_contents.get(line_number))


def get_line_list(line, LFS):
    if LFS:
        formatted_line = line.split(',')
        return formatted_line
    else:
        return line


def get_line_string(line, LFS):
    if LFS:
        return line
    else:
        line = TextModificationLib.python_list_to_Human_list(line)
        return line


def average_list(List):
    Max_lines_Average = 0
    for value in List:
        Max_lines_Average += value
    if Max_lines_Average is not 0:
        Max_lines_Average = Max_lines_Average / len(List)
    return Max_lines_Average


def import_csv(filename, ForceLFS):
    DeltaTime_Maxlines = []
    DeltaTime_CSVOpen = []
    DeltaTime_Readline = []
    DeltaTime_RemoveNewLine = []
    DeltaTime_Splitstring = []
    LFS = False
    if ForceLFS:
        LFS = True
    File_contents = {'LFS_Enabled': LFS}
    MaxlinesBegin = time.time()
    MaxLines = TextModificationLib.Count_Lines_Fast(filename)
    MaxlinesEnd = time.time()
    DeltaTime_Maxlines.append(MaxlinesEnd - MaxlinesBegin)
    CSVOpenBegin = time.time()
    CSV_file = open(filename)
    CSVOpenEnd = time.time()
    DeltaTime_CSVOpen.append(CSVOpenEnd - CSVOpenBegin)
    for x in range(1, MaxLines):
        ReadlineBegin = time.time()
        file_line = CSV_file.readline()
        ReadlineEnd = time.time()
        DeltaTime_Readline.append(ReadlineEnd - ReadlineBegin)
        RemoveNewLineBegin = time.time()
        file_line = TextModificationLib.remove(file_line, '\n')
        RemoveNewLineEnd = time.time()
        DeltaTime_RemoveNewLine.append(RemoveNewLineEnd - RemoveNewLineBegin)
        if not LFS:
            SplitStringBegin = time.time()
            file_line = file_line.split(',')
            SplitStringEnd = time.time()
            DeltaTime_Splitstring.append(SplitStringEnd - SplitStringBegin)
        # Set the dictionary equal to the line
        File_contents[x] = file_line
    CSV_file.close()
    return File_contents


# Write back to file
def write_back_to_csv(file_contents_imported, Filename, LFS):
    # Open the file and clear it, making it again if necessary hence the +
    test_file = open(Filename, "w+")
    if 0 in file_contents_imported:
        if LFS:
            text = file_contents_imported[0]
            test_file.write(text + '\n')
        else:
            text = TextModificationLib.python_list_to_Human_list(file_contents_imported[0])
            test_file.write(text + '\n')
    # Writes each line back if it is not line 0, there is a weird bug I had to fix and the != 0: and statements above
    # fix it
    if LFS:
        for line in file_contents_imported:
            text = str(file_contents_imported[line])
            test_file.write(text + '\n')
    else:
        for line in file_contents_imported:
            if line != 0:
                # Goes through the Function take a look at the text modification library
                text = TextModificationLib.python_list_to_Human_list(file_contents_imported[line])
                # adds new line to each of the lines of text to format it correctly
                test_file.write(text + '\n')
            else:
                pass
    # runs the parse_file function to reload the file and reflect the newest changes
    test_file.close()
    import_csv(Filename, ForceLFS=LFS)


def get_csv_header(file_contents_imported):
    # Sets this to file_contents_imported and gets the first one since it is where the file starts not zero this is
    # done to match Text editors and also allows me to slip in these params .get allows me to get a 'none' response
    # if it equals none
    file_params = retrieve_line_list(file_contents_imported, 1, "none")
    Answer = "yes"  # Interaction_Lib.Prompt_feedback(f'Does {file_params} sound correct?', True)
    if file_params == "none":
        # run make params
        file_params = make_csv_header(file_params)
    elif 'yes' not in Answer:
        print(Answer)
        prompt_input = Interaction_Lib.Prompt_feedback('Do you need to create or delete Parameters?', True)
        if 'delete' in prompt_input:
            file_params = delete_csv_header(file_params)
        if 'create' in prompt_input:
            file_params = make_csv_header(file_params)
        file_contents_imported[1] = file_params
    return file_params


def delete_csv_header(file_params):
    file_parameters_temp = file_params
    param_to_delete = Interaction_Lib.Prompt_feedback('Please enter Parameter to remove.', False)
    file_parameters_temp.remove(param_to_delete)
    file_params = file_parameters_temp
    Prompt = Interaction_Lib.Prompt_feedback('Would you like to delete another?', True)
    if 'yes' in Prompt:
        delete_csv_header(file_params)
    elif 'y' in Prompt:
        delete_csv_header(file_params)
    else:
        return file_params


def make_csv_header(file_params):
    # Enter the amount you want
    number_of_params = Interaction_Lib.Prompt_feedback("How many Parameters do you need?", True)
    number_of_params = int(number_of_params)
    # Repeat for the amount of times specified
    for x in range(0, number_of_params):
        # Appends to file_params while letting the user know which parameter it is.
        file_params.append(Interaction_Lib.Prompt_feedback(f"Parameter number {x}", False))
    return file_params


def search_csv(file_contents_imported):
    # Grabs the input to search for
    term = Interaction_Lib.Prompt_feedback('Search term', False)
    if term == 'exit:':
        return 1
    # Goes through the list
    searches = 0
    for line in file_contents_imported:
        try:
            # Checks if the term is in the line_number
            line_contents = file_contents_imported[line]
            # if the term is in line_contents
            if term in line_contents:
                # If it is Prints the line_number and contents
                print(f'Row# {line}, {line_contents}')
                # increment searches
                searches = + 1
        except TypeError:
            pass
    # If there are no searches recorded print no hits found
    if searches == 0:
        print('No Hits found!')


def read_lines(file_contents_imported, start_line, end_line):
    lines_read_dict = {}
    for x in range(start_line, end_line + 1):
        lines_read_dict[x] = read_line(file_contents_imported, x)
    return lines_read_dict


def read_line(file_contents_imported, line):
    print(file_contents_imported[1])
    return file_contents_imported.get(line)


def delete_one_line(file_contents_imported, line):
    if line != 1:
        del file_contents_imported[line]
    else:
        answer = Interaction_Lib.Prompt_feedback('Are you sure you would like to delete your header? You cannot'
                                                 'modify the CSV properly without it!', True)
        if 'yes' in answer:
            del file_contents_imported[line]


def delete_multiple_lines(file_contents_imported, start_line, end_line):
    for x in range(start_line, end_line):
        delete_one_line(file_contents_imported, x)
        print(f"Line {x} Deleted!")


def write_csv(file_contents_imported, fields, Write_on_exit, LFS):
    stop = False
    number_of_lines = 0
    # While stop is not equal to true or while not stop.
    for _ in file_contents_imported:
        number_of_lines += 1
    while not stop:
        field_line = []
        for each in fields:
            number_of_lines += 1
            Field_answer = Interaction_Lib.Prompt_feedback(f'What would you like to put under {each}?', False)
            field_line.append(Field_answer)
        is_empty = file_contents_imported.get(number_of_lines, 'Empty')
        if is_empty == 'Empty':
            field_line = get_line_string(field_line, LFS)
            print(field_line)
            file_contents_imported[number_of_lines] = field_line
        else:
            print('Error, line taken Please try again')
        exit_loop = Interaction_Lib.Prompt_feedback("stop writing?", True)
        # will stop loop if you type yes in there
        if "yes" in exit_loop:
            print("Stopping")
            # Use if you want to mimic the old behavior of the function, NOTE; much slower due to how this handles
            # writing compared to the old one, I recommend waiting until you save to write these changes
            if Write_on_exit:
                write_back_to_csv(file_contents_imported, "Text_modified.csv", LFS)
            stop = True
    return file_contents_imported


def sort_dictionary(file_contents_imported: dict, column: int, LFS: bool, Write_on_exit: bool):
    percent_done: int
    prev_percent = 0
    # Stores a bunch off Lists either that hold either list or string data depending on whether or not "LFS" is enabled
    ListDict = {}
    # Gets the maximum lines in the dictionary
    max_lines: int = len(file_contents_imported)
    # Gets the current line (Starts at 2 to account for what I call the header or the items you want filled in)
    CurrentLine = 2
    # The header is the first line of the CSV, reserved for fields
    header = retrieve_line_string(file_contents_imported, 1, True)
    # The finished sorted dictionary
    Sorted_dict = {1: header}

    # For each of the lines in Dictionary
    for line_number in range(0, max_lines):
        # Gets the Contents held within file contents imported
        line_contents = retrieve_line_list(file_contents_imported, line_number + 1, LFS)
        # Get the column that I am searching through
        value_current = line_contents[column]
        # Benchmarking code
        percent_done = int((line_number / max_lines) * 100)
        if percent_done > prev_percent:
            print(f"{percent_done}% Done")
            prev_percent = percent_done
        # If the value is not in the dictionary add it and add the line it was found in
        if value_current in ListDict:
            if LFS:
                line_contents = TextModificationLib.python_list_to_Human_list(line_contents)
            ListDict[value_current].append(line_contents)
        # If it already Exists add it to a preexisting dictionary that stores the related value
        else:
            ListDict[value_current] = []
            if LFS:
                line_contents = TextModificationLib.python_list_to_Human_list(line_contents)
            ListDict[value_current].append(line_contents)

    print("Assembling dictionaries")
    # Combine the Lists into one finished dictionary
    for Array_key in ListDict:
        Array: list = ListDict[Array_key]
        for Line in Array:
            if Line != header:
                file_contents_imported[CurrentLine] = Line
                CurrentLine += 1
    # if I want to return it return it.
    if Write_on_exit:
        return file_contents_imported


def bubble_sort(file_contents_imported, column, LFS, Write_on_exit):
    column = column - 1
    value_list = []
    sorted_lines = []
    Sorted_dict = {}
    Sorted_line_number = 0
    percent_done: int
    prev_percent = 0
    # Gets the maximum lines in the dictionary
    max_lines: int = len(file_contents_imported)

    for line_number in file_contents_imported:
        line_contents = retrieve_line_list(file_contents_imported, line_number, LFS)
        value_current = line_contents[column]
        if value_current not in value_list:
            value_list.append(value_current)

    for value_ideal in value_list:
        sorted_line_number = len(Sorted_dict)
        percent_done = int((sorted_line_number / max_lines) * 100)
        if percent_done > prev_percent:
            print(f"{percent_done}% Done")
            prev_percent = percent_done

        for line_number in file_contents_imported:
            line_contents = file_contents_imported[line_number]
            value_current = line_contents[column]
            if value_current == value_ideal:
                Sorted_line_number += 1
                Sorted_dict[Sorted_line_number] = line_contents
                sorted_lines.append(line_number)
    if Write_on_exit:
        return Sorted_dict


def header_to_column(file_header_imported, header_desired, subtract_1):
    row = 0
    for header in file_header_imported:
        print(header)
        row += 1
        print(row)
        if header_desired == header:
            if not subtract_1:
                return row
            if subtract_1:
                return row - 1


def modify(Parameter, line_to_modify, file_contents_imported, Write_on_exit, LFS):
    file_params = retrieve_line_list(file_contents_imported, 1, LFS)
    column = header_to_column(file_params, Parameter, False)
    old_line = retrieve_line_list(file_contents_imported, column, LFS)
    old_line[column] = Interaction_Lib.Prompt_feedback(
        f'What would you like to replace in {Parameter} on line {line_to_modify}. current value: '
        f'{file_contents_imported[line_to_modify][column]}', False)
    print(old_line)
    file_contents_imported[line_to_modify] = old_line
    if Write_on_exit:
        write_back_to_csv(file_contents_imported, "Text_modified.csv", LFS=LFS)
