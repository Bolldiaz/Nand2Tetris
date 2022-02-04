"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.file_name = ""
        self.if_counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        # arithmetic commands:
        if command == "add":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=D+M\n")

        if command == "sub":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M-D\n")

        if command == "neg":
            self.output_stream.write("@SP\nA=M-1\nM=-M\n")

        if command == "shiftleft":
            self.output_stream.write("@SP\nA=M-1\nM=M<<\n")

        if command == "shiftright":
            self.output_stream.write("@SP\nA=M-1\nM=M>>\n")

        # logic commands:
        if command == "eq":
            self.output_stream.write(f"@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nM=-1\n@END_IF_{self.if_counter}\n"
                                     f"D;JEQ\n@SP\nA=M-1\nM=0\n(END_IF_{self.if_counter})\n")
            self.if_counter += 1

        if command == "gt":
            gt_code = f"@SP\n" \
                      "A=M-1\n" \
                      "D=M\n" \
                      "@y\n" \
                      "M=D\n" \
                      "@SP\n" \
                      "M=M-1\n" \
                      "A=M-1\n" \
                      "D=M\n" \
                      "@x\n" \
                      "M=D\n" \
                      f"@X_NEG_{self.if_counter}\n" \
                      "D;JLT\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_TRUE_{self.if_counter}\n" \
                      "D;JLE\n" \
                      f"@NORMAL_CASE_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(X_NEG_{self.if_counter})\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_FALSE_{self.if_counter}\n" \
                      "D;JGE\n" \
                      f"(NORMAL_CASE_{self.if_counter})\n" \
                      f"@y\n" \
                      f"D=M\n" \
                      f"@x\n" \
                      f"D=M-D\n" \
                      f"@IF_ANS_TRUE_{self.if_counter}\n" \
                      "D;JGT\n" \
                      f"@IF_ANS_FALSE_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_TRUE_{self.if_counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=-1\n" \
                      f"@END_IF_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_FALSE_{self.if_counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=0\n" \
                      f"(END_IF_{self.if_counter})\n"
            self.output_stream.write(gt_code)
            self.if_counter += 1

        if command == "lt":
            lt_code = f"@SP\n" \
                      "A=M-1\n" \
                      "D=M\n" \
                      "@y\n" \
                      "M=D\n" \
                      "@SP\n" \
                      "M=M-1\n" \
                      "A=M-1\n" \
                      "D=M\n" \
                      "@x\n" \
                      "M=D\n" \
                      f"@X_NEG_{self.if_counter}\n" \
                      "D;JLT\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_FALSE_{self.if_counter}\n" \
                      "D;JLE\n" \
                      f"@NORMAL_CASE_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(X_NEG_{self.if_counter})\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_TRUE_{self.if_counter}\n" \
                      "D;JGE\n" \
                      f"(NORMAL_CASE_{self.if_counter})\n" \
                      f"@y\n" \
                      f"D=M\n" \
                      f"@x\n" \
                      f"D=M-D\n" \
                      f"@IF_ANS_TRUE_{self.if_counter}\n" \
                      "D;JLT\n" \
                      f"@IF_ANS_FALSE_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_TRUE_{self.if_counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=-1\n" \
                      f"@END_IF_{self.if_counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_FALSE_{self.if_counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=0\n" \
                      f"(END_IF_{self.if_counter})\n"
            self.output_stream.write(lt_code)
            self.if_counter += 1
        
        if command == "and":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=D&M\n")

        if command == "or":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=D|M\n")

        if command == "not":
            self.output_stream.write("@SP\nA=M-1\nM=!M\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """

        # push command:
        if command == "C_PUSH":
            if segment == "constant":
                self.output_stream.write(f"@{index}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "local":
                self.output_stream.write(f"@{index}\nD=A\n@LCL\nA=D+M\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "this":
                self.output_stream.write(f"@{index}\nD=A\n@THIS\nA=D+M\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "that":
                self.output_stream.write(f"@{index}\nD=A\n@THAT\nA=D+M\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "argument":
                self.output_stream.write(f"@{index}\nD=A\n@ARG\nA=D+M\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "pointer":
                self.output_stream.write(f"@{index}\nD=A\n@3\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "temp":
                self.output_stream.write(f"@{index}\nD=A\n@5\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
            elif segment == "static":
                self.output_stream.write(f"@{self.file_name}.{index}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")

        # pop command:
        if command == "C_POP":
            if segment == "local":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@LCL\n"
                                         f"D=D+M\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "this":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@THIS\n"
                                         f"D=D+M\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "that":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@THAT\n"
                                         f"D=D+M\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "argument":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@ARG\n"
                                         f"D=D+M\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "pointer":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@3\n"
                                         f"D=D+A\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "temp":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@pop_val\nM=D\n@{index}\nD=A\n@5\n"
                                         f"D=D+A\n@tmp_addr\nM=D\n@pop_val\nD=M\n@tmp_addr\nA=M\nM=D\n")
            if segment == "static":
                self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@{self.file_name}.{index}\nM=D\n")

    def close(self) -> None:
        """Closes the output file."""
        self.output_stream.close()
