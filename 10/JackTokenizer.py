"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re

KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST = "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
KEYWORDS_DIC = {"class": "CLASS", "method": "METHOD", "function": "FUNCTION", "constructor": "CONSTRUCTOR", "int": "INT",
               "boolean": "BOOLEAN", "char": "CHAR", "void": "VOID", "var": "VAR", "static": "STATIC", "field": "FIELD",
               "let": "LET", "do": "DO", "if": "IF", "else": "ELSE", "while": "WHILE", "return": "RETURN",
               "true": "TRUE", "false": "FALSE", "null": "NULL", "this": "THIS"}

SYMBOLS_SET = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '#', '^'}


ASTRIX_COMMENT_PATTERN = r"(/\*|\*)"
COMMENT_IN_STRING_PATTERN = r'(?P<before>.*)"(?P<replace>.*)"(?P<after>.*)'
INLINE_COMMENT_PATTERN = r"(?P<command>.*?)(//.*?)"
IDENTIFIER_PATTERN = r"(?P<identifier>^[A-Za-z0-9_]+)(?P<reminder>.*)"


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    @staticmethod
    def _inline_comments_ignore(command) -> str:
        """if command is astrix comments - it's get ignored, if inline comment it's get cut of the command.

        Args:
            command (str): a valid jack command or comment.
        Returns:
            str: Fixed str of command not contain any comment.
        """
        command = command.strip()
        match = re.match(COMMENT_IN_STRING_PATTERN, command)
        if match is not None:
            command = command.replace('"' + match["replace"] + '"', "STRING_TO_REPLACE")
            command = JackTokenizer._inline_comments_ignore(command)
            return command.replace("STRING_TO_REPLACE", '"' + match["replace"] + '"')
        match1 = re.match(ASTRIX_COMMENT_PATTERN, command)
        if match1 is not None:
            return ""
        match2 = re.match(INLINE_COMMENT_PATTERN, command)
        if match2 is not None:
            command = match2["command"]  # cut an inline command from the line
        command = command.strip()  # get cleared of redundant spaces
        return command

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        script = input_stream.read()

        while "/*" in script and "*/" in script:
            comment_start_idx = script.index("/*")
            comment_end_idx = script.index("*/") + 2
            script = script[:comment_start_idx] + '\n' + script[comment_end_idx:]

        self.lines = []
        input_lines = script.splitlines()
        for command in input_lines:
            command = JackTokenizer._inline_comments_ignore(command)
            if not command:
                continue
            self.lines.append(command)

        self.line_counter = 0
        self.length = len(self.lines)
        self.current_line = self.lines[self.line_counter]
        self.current_token = None

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.line_counter != self.length

    def line_advance(self):
        if not self.current_line:
            self.line_counter += 1
            if self.line_counter == self.length:
                return
            self.current_line = self.lines[self.line_counter]

        while self.current_line[0].isspace():
            self.current_line = self.current_line[1:]

    def is_keyword(self) -> bool:
        for keyword in KEYWORDS_DIC:
            if self.current_line.startswith(keyword) and self.current_line[len(keyword)] == " ":
                self.current_token = keyword
                self.current_line = self.current_line[len(keyword):]
                self.line_advance()
                return True
        return False

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        assert self.has_more_tokens()

        if self.is_keyword():
            return

        if self.current_line[0] in SYMBOLS_SET:
            self.current_token = self.current_line[0]
            self.current_line = self.current_line[1:]
            self.line_advance()
            return

        if self.current_line[0] == '"':
            idx = self.current_line[1:].find('"')
            self.current_token = self.current_line[0:idx+2]
            self.current_line = self.current_line[idx+2:]
            self.line_advance()
            return

        if self.current_line[0].isdigit():
            idx = 0
            while self.current_line[idx].isdigit():
                idx += 1
            self.current_token = self.current_line[:idx]
            self.current_line = self.current_line[idx:]
            self.line_advance()
            return

        # identifier case:
        identifier_match = re.match(IDENTIFIER_PATTERN, self.current_line)
        assert identifier_match is not None
        self.current_token = identifier_match["identifier"]
        self.current_line = identifier_match["reminder"]
        self.line_advance()

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        assert len(self.current_token) > 0

        if self.current_token in KEYWORDS_DIC:
            return KEYWORD

        if self.current_token in SYMBOLS_SET:
            return SYMBOL

        if self.current_token.isnumeric() and 0 <= int(self.current_token) < 32767:
            return INT_CONST

        if self.current_token[0] == self.current_token[-1] == '"':
            return STRING_CONST

        # identifier case:
        else:
            return IDENTIFIER

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        assert self.token_type() == KEYWORD
        return KEYWORDS_DIC[self.current_token]

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        assert self.token_type() == SYMBOL
        return self.current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        assert self.token_type() == IDENTIFIER
        return self.current_token

    def int_val(self) -> int:
        """
        Returns:
            int: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        assert self.token_type() == INT_CONST
        return int(self.current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        assert self.token_type() == STRING_CONST
        return self.current_token[1:-1]
