"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
from math import pow
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def a_command(num: int) -> str:
    """ Creates a binary code of an A-command

    Args:
        num: an int symbolise a label or variable

    Returns: (str): the binary adapting code

    """

    bin_array = ['0']*16
    for i in range(14, -1, -1):
        res = pow(2, i)
        if num >= res:
            bin_array[15-i] = '1'
            num -= pow(2, i)

    return "".join(bin_array) + '\n'


def c_command(par: Parser) -> str:
    """ Creates a binary code of a C-command

    Args:
        par: A Parser

    Returns: (str): the binary adapting code

    """

    bin_code = '1'                      # the default entry of C-command
    bin_code += Code.comp(par.comp())   # add the comp expression
    bin_code += Code.dest(par.dest())   # add the dest expression
    bin_code += Code.jump(par.jump())   # add the jump expression
    return bin_code + '\n'



def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """

    par = Parser(input_file)
    tab = SymbolTable()

    # First Pass
    row_counter = 0
    while par.has_more_commands():
        if par.command_type() == "L_COMMAND":
            sym = par.symbol()
            tab.add_entry(sym, row_counter)
        else:
            row_counter += 1

        par.advance()

    par.reset()

    # Second Pass:
    var_counter = 16
    while par.has_more_commands():
        command_type = par.command_type()

        if command_type == "C_COMMAND":
            output_file.write(c_command(par))

        if command_type == "A_COMMAND":
            sym = par.symbol()

            if not sym.isnumeric():     # check if sym is number or variable
                if tab.contains(sym):
                    num = int(tab.get_address(sym))
                else:
                    tab.add_entry(sym, var_counter)
                    num = var_counter
                    var_counter += 1    # add the variable to the table and update the counter
            else:
                num = int(sym)

            output_file.write(a_command(num))

        par.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

