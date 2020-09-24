import TextModificationLib


# Opens the file in read/write/append mode, Usually only need append/read write is self destructive so you need to set
# the override to be 1 if you wish to use w or w+
def Change_File_Mode(mode, override):
    # Checks to See if w is in mode
    if "w" not in mode:
        # If w is not in mode close the file and reopen with mode variable
        file = open('ConfigFile.cfg', mode)
        return file
    elif 'w' in mode and override != 1:
        print("""This mode is destructive to the config file and therefore you have to override this message...
              Please be warned and only do it if you plan on regenerating the config files afterwards. Under most normal 
              circumstances use a or a+ to write to the file please change the third variable to add a 0 or a 1""")
        return False
    elif 'w' in mode and override == 1:
        # I think I have used this once so far...
        file = open('ConfigFile.cfg', mode)
        return file


# This writes to the config file, it ensures that the conventions of the file are maintained so it is compatible with
# the parser
def write_to_cfg(text, var_name, value, dictionary):
    if var_name in dictionary:
        print(var_name + " is already in config, checking if value is different")
        if dictionary.get(var_name, "None") == value:
            print(value + " is already in config")
            return False
        else:
            old_var = dictionary[var_name]
            print(old_var + "= old variable")
            print("Value has been changed, adding Updated Value")
            TextModificationLib.remove(text, f'"{var_name}" = "{old_var}";\n')
            config_file = Change_File_Mode("a", 0)
            config_file.write(f'"{var_name}" = "{value}";\n')
            return True

    else:
        config_file = Change_File_Mode("w", 1)
        config_file.write(f'"{var_name}" = "{value}";\n')
        config_file.close()
        return True


def Backup_Config(input_things, file_name):
    config_backup = open(file_name, "w+")
    config_backup.write(str(input_things))
    config_backup.close()
    return True


def Parse_Config_file():
    # Turn Config file into a dictionary, will improve later
    # Turn the text file into string
    config_intermediate = TextModificationLib.Read_file("ConfigFile.cfg")
    print(config_intermediate)
    # Removes my Mark
    config_intermediate: object = TextModificationLib.remove(config_intermediate,
                                                             "Created by Donovan Strawhacker 2020 for The Class of "
                                                             "Samuel Oppel.")
    # Replaces = with Semicolons
    config_intermediate = TextModificationLib.replace(config_intermediate, "=", ":")
    config_intermediate = TextModificationLib.replace(config_intermediate, ";", ",")
    config_intermediate = TextModificationLib.add_to_both_sides(config_intermediate, "{", "}")
    config_dict = TextModificationLib.To_Dictionary(config_intermediate)
    print("Parsing Complete")
    return config_dict


File = Parse_Config_file()
print(File)
