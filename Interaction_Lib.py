import TextModificationLib


def Prompt_feedback(text, Desensitize):
    if text is not 'None':
        print(text)
    prompt_input = input('>: ')
    if Desensitize:
        prompt_input = TextModificationLib.make_lowercase(prompt_input)
    return str(prompt_input)


def End_User_prompt(Index_of_commands):
    help_command = 'Unimplemented!'
    # Starts this variable off at False
    command_found: bool = False
    # Asks what you would like to do
    # Receives input for next action and stores it in the variable of the same name
    next_action = Prompt_feedback('What would you like to do?', True)
    # For everything in the list of commands
    for x in Index_of_commands:
        command_found = command_found
        # if it exists in commands
        if x in next_action:
            # For now print there was a match
            # lets it know it found a match by setting a boolean to true
            command_found: bool = True
            # Calls Command logic with the Argument next_action
            return next_action

    # If there is no command found
    if not command_found:
        # Print command not found
        print(f'Not found! Try again!', f'Please type {help_command}, for a list of commands, or check documentation!')
        # Run this prompt again
        End_User_prompt(Index_of_commands)
