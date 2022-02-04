"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    counter = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.file_name = ""

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
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nAM=M-1\nA=M-1\nM=D+M\n")

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
            self.output_stream.write(f"@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nM=-1\n@END_IF_{CodeWriter.counter}\n"
                                     f"D;JEQ\n@SP\nA=M-1\nM=0\n(END_IF_{CodeWriter.counter})\n")
            CodeWriter.counter += 1

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
                      f"@X_NEG_{CodeWriter.counter}\n" \
                      "D;JLT\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_TRUE_{CodeWriter.counter}\n" \
                      "D;JLE\n" \
                      f"@NORMAL_CASE_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(X_NEG_{CodeWriter.counter})\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_FALSE_{CodeWriter.counter}\n" \
                      "D;JGE\n" \
                      f"(NORMAL_CASE_{CodeWriter.counter})\n" \
                      f"@y\n" \
                      f"D=M\n" \
                      f"@x\n" \
                      f"D=M-D\n" \
                      f"@IF_ANS_TRUE_{CodeWriter.counter}\n" \
                      "D;JGT\n" \
                      f"@IF_ANS_FALSE_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_TRUE_{CodeWriter.counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=-1\n" \
                      f"@END_IF_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_FALSE_{CodeWriter.counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=0\n" \
                      f"(END_IF_{CodeWriter.counter})\n"
            self.output_stream.write(gt_code)
            CodeWriter.counter += 1

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
                      f"@X_NEG_{CodeWriter.counter}\n" \
                      "D;JLT\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_FALSE_{CodeWriter.counter}\n" \
                      "D;JLE\n" \
                      f"@NORMAL_CASE_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(X_NEG_{CodeWriter.counter})\n" \
                      "@y\n" \
                      "D=M\n" \
                      f"@IF_ANS_TRUE_{CodeWriter.counter}\n" \
                      "D;JGE\n" \
                      f"(NORMAL_CASE_{CodeWriter.counter})\n" \
                      f"@y\n" \
                      f"D=M\n" \
                      f"@x\n" \
                      f"D=M-D\n" \
                      f"@IF_ANS_TRUE_{CodeWriter.counter}\n" \
                      "D;JLT\n" \
                      f"@IF_ANS_FALSE_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_TRUE_{CodeWriter.counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=-1\n" \
                      f"@END_IF_{CodeWriter.counter}\n" \
                      "0;JMP\n" \
                      f"(IF_ANS_FALSE_{CodeWriter.counter})\n" \
                      "@SP\n" \
                      "A=M-1\n" \
                      "M=0\n" \
                      f"(END_IF_{CodeWriter.counter})\n"
            self.output_stream.write(lt_code)
            CodeWriter.counter += 1

        if command == "and":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=D&M\n")

        if command == "or":
            self.output_stream.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=D|M\n")

        if command == "not":
            self.output_stream.write("@SP\nA=M-1\nM=!M\n")

    def writeInit(self) -> None:
        """
            write the initialization of asm file
        """
        # SP=256          // initialize the stack pointer to 0x0100
        # call Sys.init   // invoke Sys.init
        self.output_stream.write("@256\nD=A\n@SP\nM=D\n")
        self.writeCall("Sys.init", 0)

    def writeLabel(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        label command.

        Args:
            command (str): a label command.
        """
        self.output_stream.write(f"({self.cur_tranlated_func}${command})\n")

    def writeGoto(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        goto command.

        Args:
            command (str): a goto command.
        """
        self.output_stream.write(f"@{self.cur_tranlated_func}${command}\n0;JMP\n")

    def writeIf(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        if-goto command.

        Args:
            command (str): a if-goto command.
        """
        self.output_stream.write(f"@SP\nM=M-1\nA=M\nD=M\n@{self.cur_tranlated_func}${command}\nD;JNE\n")

    def writeCall(self, func_name: str, n_args: int) -> None:
        """Writes the assembly code that is the translation of the given
        call command.

        Args:
            func_name (str): the called function name command.
            n_args (int): function's number of args.
        """
        call_command = f"@retAddress_{func_name}_{CodeWriter.counter}_{n_args}\n" \
                       "D=A\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@LCL\n" \
                       "D=M\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@ARG\n" \
                       "D=M\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@THIS\n" \
                       "D=M\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@THAT\n" \
                       "D=M\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@SP\n" \
                       "D=M\n" \
                       f"@{n_args + 5}\n" \
                       "D=D-A\n" \
                       "@ARG\n" \
                       "M=D\n" \
                       "@SP\n" \
                       "D=M\n" \
                       "@LCL\n" \
                       "M=D\n" \
                       f"@{func_name}\n" \
                       "0;JMP\n" \
                       f"(retAddress_{func_name}_{CodeWriter.counter}_{n_args})\n"
        self.output_stream.write(call_command)
        CodeWriter.counter += 1

    def writeFunction(self, func_name: str, n_args: int) -> None:
        """Writes the assembly code that is the translation of the given
        function command.

        Args:
            func_name (str): the called function name command.
            n_args (int): function's number of args.
        """
        self.cur_tranlated_func = func_name
        func_command = f"({func_name})\n" \
                       f"@{n_args}\n" \
                       "D=A\n" \
                       "@counter\n" \
                       "M=D\n" \
                       f"({func_name}$LOOP)\n" \
                       "@counter\n" \
                       "D=M\n" \
                       f"@{func_name}$STOP\n" \
                       "D;JEQ\n" \
                       "@0\n" \
                       "D=A\n" \
                       "@SP\n" \
                       "M=M+1\n" \
                       "A=M-1\n" \
                       "M=D\n" \
                       "@counter\n" \
                       "M=M-1\n" \
                       f"@{func_name}$LOOP\n" \
                       "0;JMP\n" \
                       f"({func_name}$STOP)\n"

        self.output_stream.write(func_command)

    def writeReturn(self) -> None:
        """Writes the assembly code that is the translation of the given
        return command.

        """
        return_command = "@LCL\n" \
                         "D=M\n" \
                         "@frame\n" \
                         "M=D\n" \
                         "@5\n" \
                         "A=D-A\n" \
                         "D=M\n" \
                         "@retAddr\n" \
                         "M=D\n" \
                         "@SP\n" \
                         "A=M-1\n" \
                         "D=M\n" \
                         "@ARG\n" \
                         "A=M\n" \
                         "M=D\n" \
                         "@ARG\n" \
                         "D=M+1\n" \
                         "@SP\n" \
                         "M=D\n" \
                         "@1\n" \
                         "D=A\n" \
                         "@frame\n" \
                         "A=M-D\n" \
                         "D=M\n" \
                         "@THAT\n" \
                         "M=D\n" \
                         "@2\n" \
                         "D=A\n" \
                         "@frame\n" \
                         "A=M-D\n" \
                         "D=M\n" \
                         "@THIS\n" \
                         "M=D\n" \
                         "@3\n" \
                         "D=A\n" \
                         "@frame\n" \
                         "A=M-D\n" \
                         "D=M\n" \
                         "@ARG\n" \
                         "M=D\n" \
                         "@4\n" \
                         "D=A\n" \
                         "@frame\n" \
                         "A=M-D\n" \
                         "D=M\n" \
                         "@LCL\n" \
                         "M=D\n" \
                         "@retAddr\n" \
                         "A=M\n" \
                         "0;JMP\n"
        self.output_stream.write(return_command)

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
