"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        input_lines = input_file.read().splitlines()
        self.parser = []  # the commands stack
        for command in input_lines:
            if "/" in command:
                command = command[:command.find('/')]  # the line is comment
            if not command:
                continue
            command = command.strip()  # get cleared of redundant spaces
            self.parser.append(command)

        self.length = len(self.parser)  # the number of commands
        self.command_counter = 0  # the default current command to parse

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.command_counter != self.length

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        if self.has_more_commands():
            self.command_counter += 1

    def print_command(self) -> str:
        return f"\n// {self.parser[self.command_counter]}:\n\n"

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        cur_command = self.parser[self.command_counter]

        if cur_command[:6] == "return":
            return "C_RETURN"

        if len(cur_command.split()) == 1:
            return "C_ARITHMETIC"       # if command is an arithmetic, it contains only one word

        if cur_command[:4] == "push":
            return "C_PUSH"

        if cur_command[:3] == "pop":
            return "C_POP"

        if cur_command[:5] == "label":
            return "C_LABEL"

        if cur_command[:4] == "goto":
            return "C_GOTO"

        if cur_command[:7] == "if-goto":
            return "C_IF"

        if cur_command[:8] == "function":
            return "C_FUNCTION"

        if cur_command[:4] == "call":
            return "C_CALL"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            return self.parser[self.command_counter]

        split_command = self.parser[self.command_counter].split()
        return split_command[1]  # arg1 is command[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        split_command = self.parser[self.command_counter].split()
        return int(split_command[2])  # arg2 is command[2]
