"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """

        input_lines = input_file.read().splitlines()

        self.parser = []                            # the commands stack
        for command in input_lines:
            command = command.replace(" ","")       # cut all the spaces
            if not command or command[0] == "/":    # the line is comment
                continue
            idx = command.find("/")
            if idx != -1:
                command = command[:idx]             # cut the comment of the command
            self.parser.append(command)

        self.length = len(self.parser)              # the number of commands
        self.command_counter = 0                    # the default current command to parse

    def reset(self) -> None:
        """Reset the command counter to 0.
        """
        self.command_counter = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.command_counter != self.length

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.command_counter += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        command_init = self.parser[self.command_counter][0]
        if command_init == "@":       # A_COMMAND
            return "A_COMMAND"
        if command_init == "(":       # L_COMMAND
            return "L_COMMAND"
        return "C_COMMAND"            # C_COMMAND

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # todo check if command_type() is needed to be called
        if self.command_type() == "A_COMMAND":  # A_COMMAND
            return self.parser[self.command_counter][1:]

        return self.parser[self.command_counter][1:-1] # L_COMMAND

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        split_command = self.parser[self.command_counter].split("=")
        if len(split_command) == 1:     # means no "dest expression in command
            return ""
        return split_command[0]         # the "dest" expression


    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        command = self.parser[self.command_counter]
        equal_idx = command.find("=")
        if equal_idx != -1:
            command = command[equal_idx+1:]     # slice "dest=" expression of the command
        jump_idx = command.find(";")
        if jump_idx != -1:
            command = command[:jump_idx]        # slice ";jump" expression of the command
        return command

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        split_command = self.parser[self.command_counter].split(";")
        if len(split_command) == 1:     # means no "jump" expression in command
            return "null"
        return split_command[1]         # return "jump" expression
