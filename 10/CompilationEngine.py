"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *

_CLASS_VAR_DEC_TOKENS = {"static", "field"}
_SUBROUTINE_TOKENS = {"function", "method", "constructor"}
_PRIMITIVES = {"boolean", "int", "char", "void"}
_STATEMENTS_ENTRIES = {"do", "while", "if", "let", "return"}
_DOUBLE_MEANING_OPS = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
_BIN_OPS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
_UNARY_OPS = {'-', '~', '#', '^'}
_KEYWORD_CONSTANTS = {"this", "null", "true", "false"}
_TERMINAL_TOKENS = {"KEYWORD": "keyword", "SYMBOL": "symbol", "IDENTIFIER": "identifier",
                    "INT_CONST": "integerConstant", "STRING_CONST": "stringConstant"}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO,
                output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = JackTokenizer(input_stream)
        assert self.tokenizer.has_more_tokens()

        # init all the fields
        self.output_stream = output_stream
        self.tab_counter = 0
        self.tokenizer.advance()
        self.token = self.tokenizer.current_token
        self.token_type = self.tokenizer.token_type()

        # run the compilation process
        self.compile_class()

    def _write_tag(self, item: str, token_type=None) -> None:
        """ Write to output file the current XML command, whether if the current element is terminal or not

        :param item: a token to write if item is terminal, the non terminal element name
        :param token_type: the type of a token if item is a terminal element, o.w None
        """
        if token_type is None:  # no
            if item[0] != '/':
                self.output_stream.write("  " * self.tab_counter + f"<{item}>\n")
                self.tab_counter += 1
            else:
                self.tab_counter -= 1
                self.output_stream.write("  " * self.tab_counter + f"<{item}>\n")

        else:
            if token_type == _TERMINAL_TOKENS[STRING_CONST]:
                item = item[1:-1]

            elif item in _DOUBLE_MEANING_OPS:
                item = _DOUBLE_MEANING_OPS[item]

            self.output_stream.write("  " * self.tab_counter + f"<{token_type}> {item} </{token_type}>\n")

    def _eat(self, expected_token: str) -> None:
        """ The eat function as described in the vide, checks if the
            correct token is in place then writes the appropriate XML code in
            the file.
            Also assert the expected_token is valid according the semantics rules of Jack

        :param expected_token: the token/token type to analyze
        """
        # if the expected token is not stand with the current token name or if identifier stand with it's token type
        assert expected_token == self.token or expected_token == self.token_type

        self._write_tag(self.token, _TERMINAL_TOKENS[self.token_type])
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            self.token = self.tokenizer.current_token
            self.token_type = self.tokenizer.token_type()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._write_tag("class")
        self._eat(self.token)    # token = 'class'
        self._eat(IDENTIFIER)    # token = className
        self._eat('{')
        while self.token != "}":
            if self.token in _CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec()
            elif self.token in _SUBROUTINE_TOKENS:
                self.compile_subroutine()
        self._eat('}')
        self._write_tag("/class")


    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""

        self._write_tag("classVarDec")
        assert self.token in _CLASS_VAR_DEC_TOKENS
        self._eat(self.token)        # token = 'field' | 'static'

        if self.token in _PRIMITIVES:
            self._eat(self.token)      # token = type

        elif self.token_type == IDENTIFIER:
            self._eat(IDENTIFIER)      # token = className

        else:
            raise ValueError

        self._eat(IDENTIFIER)  # token = varName

        # eat the rest of all the varName declarations if exist:
        while self.token == ",":
            self._eat(',')
            self._eat(IDENTIFIER)  # token = varName
        self._eat(';')

        self._write_tag("/classVarDec")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""

        self._write_tag("subroutineDec")
        assert self.token in _SUBROUTINE_TOKENS
        self._eat(self.token)    # token = 'constructor' | 'function' | 'method'

        if self.token in _PRIMITIVES:
            self._eat(self.token)      # token = type

        elif self.token_type == IDENTIFIER:
            self._eat(IDENTIFIER)      # token = className

        else:
            raise ValueError

        self._eat(IDENTIFIER)  # token = subroutineName
        self._eat('(')
        self.compile_parameter_list()
        self._eat(')')
        self._write_tag("subroutineBody")
        self._eat('{')
        self.compile_var_dec()
        self.compile_statements()
        self._eat('}')
        self._write_tag("/subroutineBody")
        self._write_tag("/subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self._write_tag("parameterList")

        if self.token != ')':
            # read all the (type varName) pairs
            if self.token in _PRIMITIVES:
                self._eat(self.token)  # token = type
            elif self.token_type == IDENTIFIER:
                self._eat(IDENTIFIER)  # token = className
            else:
                raise ValueError

            self._eat(IDENTIFIER)  # token = varName
            while self.token == ",":
                self._eat(',')
                if self.token in _PRIMITIVES:
                    self._eat(self.token)  # token = type
                elif self.token_type == IDENTIFIER:
                    self._eat(IDENTIFIER)  # token = className
                else:
                    raise ValueError
                self._eat(IDENTIFIER)  # token = varName

        self._write_tag("/parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        while self.token == 'var':
            self._write_tag("varDec")
            self._eat(self.token)    # token = 'var'

            if self.token in _PRIMITIVES:
                self._eat(self.token)  # token = type

            elif self.token_type == IDENTIFIER:
                self._eat(IDENTIFIER)  # token = className

            else:
                raise ValueError

            self._eat(IDENTIFIER)  # token = varName
            # eat the rest of all the varName declarations if exist:
            while self.token == ",":
                self._eat(',')
                self._eat(IDENTIFIER)
            self._eat(';')
            self._write_tag("/varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self._write_tag("statements")

        while self.token in _STATEMENTS_ENTRIES:
            if self.token == "do":
                self.compile_do()

            elif self.token == "let":
                self.compile_let()

            elif self.token == "while":
                self.compile_while()

            elif self.token == "return":
                self.compile_return()

            else:  # self.token == "if":
                self.compile_if()

        self._write_tag("/statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_tag("doStatement")
        self._eat(self.token)    # token = 'do'

        # subroutineCall:
        self._eat(IDENTIFIER)  # token = subroutineName | className | varName
        if self.token == '.':
            self._eat(self.token)
            self._eat(IDENTIFIER)  # token = subroutineName
        self._eat('(')
        self.compile_expression_list()
        self._eat(')')

        self._eat(';')
        self._write_tag("/doStatement")


    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_tag("letStatement")
        self._eat(self.token)  # token = 'let'
        self._eat(IDENTIFIER)  # token = varName

        # slicing case - varName[expression]:
        if self.token == '[':
            self._eat('[')
            self.compile_expression()
            self._eat(']')

        self._eat('=')
        self.compile_expression()
        self._eat(';')
        self._write_tag("/letStatement")


    def compile_while(self) -> None:
        """Compiles a while statement."""

        self._write_tag("whileStatement")
        self._eat(self.token)  # token = 'while'
        self._eat('(')
        self.compile_expression()
        self._eat(')')
        self._eat('{')
        self.compile_statements()
        self._eat('}')
        self._write_tag("/whileStatement")


    def compile_return(self) -> None:
        """Compiles a return statement."""

        self._write_tag("returnStatement")
        self._eat(self.token)  # token = 'return'

        # expression-return case:
        if self.token != ';':
            self.compile_expression()
        self._eat(';')
        self._write_tag("/returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""

        self._write_tag("ifStatement")
        self._eat(self.token)  # token = 'if'
        self._eat('(')
        self.compile_expression()
        self._eat(')')
        self._eat('{')
        self.compile_statements()
        self._eat('}')

        # else case:
        if self.token == 'else':
            self._eat(self.token)  # token = 'else'
            self._eat('{')
            self.compile_statements()
            self._eat('}')

        self._write_tag("/ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_tag("expression")
        self.compile_term()
        while self.token in _BIN_OPS:
            self._eat(self.token)
            self.compile_term()
        self._write_tag("/expression")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self._write_tag("term")

        if self.token in _UNARY_OPS:
            self._eat(self.token)  # token = '-' | '~' | '#' | '^'
            self.compile_term()

        elif self.token in _KEYWORD_CONSTANTS or self.token_type in {INT_CONST, STRING_CONST}:
            self._eat(self.token)  # token = 'true' | 'false' | 'null' | 'this' | integerConstant | stringConstant

        elif self.token == '(':
            self._eat(self.token)      # token = ')'
            self.compile_expression()
            self._eat(')')

        elif self.token_type == IDENTIFIER:
            self._eat(IDENTIFIER)    # token = className | varName | subroutineName  

            if self.token == '[':
                self._eat(self.token)
                self.compile_expression()
                self._eat(']')

            # subroutineCall:
            elif self.token == '(':
                self._eat(self.token)
                self.compile_expression_list()
                self._eat(')')
                
            elif self.token == '.':
                self._eat(self.token)
                self._eat(IDENTIFIER)  # token = subroutineName
                self._eat('(')
                self.compile_expression_list()
                self._eat(')')
                          
        else:
            raise ValueError

        self._write_tag("/term")


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""

        self._write_tag("expressionList")

        # if list not empty:
        if self.token != ')':
            self.compile_expression()
            while self.token == ',':
                self._eat(self.token)
                self.compile_expression()

        self._write_tag("/expressionList")

