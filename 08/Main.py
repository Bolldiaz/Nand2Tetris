"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

# todo This project should be constructed gradually, according to the instructions.
# The final project should always include a call to Sys.init in every translation!
# This means that the BasicLoop, FibonacciSeries, SimpleFunction tests are not supposed to work with your final submission.


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))

    # initialization:
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    code_writer.set_file_name(input_filename)

    # for each vm command - split it, and write it in the output file as asm command:
    while parser.has_more_commands():
        output_file.write(parser.print_command())
        com_type = parser.command_type()
        if com_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.arg1())
        elif com_type == "C_POP" or com_type == "C_PUSH":
            code_writer.write_push_pop(com_type, parser.arg1(), parser.arg2())
        elif com_type == "C_LABEL":
            code_writer.writeLabel(parser.arg1())
        elif com_type == "C_GOTO":
            code_writer.writeGoto(parser.arg1())
        elif com_type == "C_IF":
            code_writer.writeIf(parser.arg1())
        elif com_type == "C_FUNCTION":
            code_writer.writeFunction(parser.arg1(), parser.arg2())
        elif com_type == "C_CALL":
            code_writer.writeCall(parser.arg1(), parser.arg2())
        elif com_type == "C_RETURN":
            code_writer.writeReturn()

        # advance to the next command:
        parser.advance()



if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        # write the init of an asm output file
        code_writer = CodeWriter(output_file)
        code_writer.writeInit()
        # translates the vm input files into a single asm file
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)