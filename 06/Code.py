"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        bin_dest = ['0', '0', '0']
        if "A" in mnemonic:
            bin_dest[0] = '1'
        if "D" in mnemonic:
            bin_dest[1] = '1'
        if "M" in mnemonic:
            bin_dest[2] = '1'
        return "".join(bin_dest)


    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: 7-bit long binary code of the given mnemonic.
        """
        if mnemonic == "D<<":
            return "010110000"
        if mnemonic == "D>>":
            return "010010000"
        if mnemonic == "A<<":
            return "010100000"
        if mnemonic == "A>>":
            return "010000000"
        if mnemonic == "M<<":
            return "011100000"
        if mnemonic == "M>>":
            return "011000000"
        if mnemonic == "0":
            return "110101010"
        if mnemonic == "1":
            return "110111111"
        if mnemonic == "-1":
            return "110111010"
        if mnemonic == "D":
            return "110001100"
        if mnemonic == "A":
            return "110110000"
        if mnemonic == "M":
            return "111110000"
        if mnemonic == "1D":
            return "110001101"
        if mnemonic == "!A":
            return "110110001"
        if mnemonic == "!M":
            return "111110001"
        if mnemonic == "-D":
            return "110001111"
        if mnemonic == "-A":
            return "110110011"
        if mnemonic == "-A":
            return "111110011"
        if mnemonic == "D+1":
            return "110011111"
        if mnemonic == "A+1":
            return "110110111"
        if mnemonic == "M+1":
            return "111110111"
        if mnemonic == "D-1":
            return "110001110"
        if mnemonic == "A-1":
            return "110110010"
        if mnemonic == "M-1":
            return "111110010"
        if mnemonic == "D+A":
            return "110000010"
        if mnemonic == "D+M":
            return "111000010"
        if mnemonic == "D-A":
            return "110010011"
        if mnemonic == "D-M":
            return "111010011"
        if mnemonic == "A-D":
            return "110000111"
        if mnemonic == "M-D":
            return "111000111"
        if mnemonic == "D&A":
            return "110000000"
        if mnemonic == "D&M":
            return "111000000"
        if mnemonic == "D|A":
            return "110010101"
        if mnemonic == "D|M":
            return "111010101"

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        if mnemonic == "null":
            return "000"
        if mnemonic == "JGT":
            return "001"
        if mnemonic == "JEQ":
            return "010"
        if mnemonic == "JGE":
            return "011"
        if mnemonic == "JLT":
            return "100"
        if mnemonic == "JNE":
            return "101"
        if mnemonic == "JLE":
            return "110"
        if mnemonic == "JMP":
            return "111"
