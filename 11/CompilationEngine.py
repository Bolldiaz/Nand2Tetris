"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *
from SymbolTable import *
from VMWriter import *

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

_VM_UNARY_OPS_ = {'-': 'NEG', '~': "NOT", '#': "shiftright", '^': "shiftleft"}

_VM_BIN_OPS = {'+': "ADD", '-': "SUB", '&': "AND", '|': "OR", '<': "LT", '>': "GT", '=': "EQ"}


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
        self.symbol_table = SymbolTable()
        self.current_subroutine_type = ''
        self.vm_writer = VMWriter(output_stream)
        assert self.tokenizer.has_more_tokens()

        self.tokenizer.advance()
        self.token = self.tokenizer.current_token
        self.token_type = self.tokenizer.token_type()

        # run the compilation process
        self.class_name = ''
        self.counter = 0
        self.counter_let = 0
        self.compile_class()

    def _advancer(self) -> None:
        """ The eat function as described in the vide, checks if the
            correct token is in place then writes the appropriate XML code in
            the file.
            Also assert the expected_token is valid according the semantics rules of Jack

        :param expected_token: the token/token type to analyze
        """

        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            self.token = self.tokenizer.current_token
            self.token_type = self.tokenizer.token_type()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self._advancer()    # token = 'class'
        self.class_name = self.token
        self._advancer()    # token = className
        self._advancer()    # token = '{'

        # creates a class_symbol table and add all fields and variables mentioned at the declaration
        while self.token != "}":
            if self.token in _CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_dec()
            elif self.token in _SUBROUTINE_TOKENS:
                self.compile_subroutine()
        
        self._advancer()    # token = '}'

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        assert self.token in _CLASS_VAR_DEC_TOKENS

        kind = self.token
        self._advancer()        # token = 'field' | 'static'

        type = self.token  
        self._advancer()  # token = type

        name = self.token
        self._advancer()  # token = varName
        
        self.symbol_table.define(name, type, kind.upper())
        # eat the rest of all the varName declarations if exist:
        while self.token == ",":
            self._advancer()    # token = ','
            name = self.token
            self._advancer()  # token = varName

            self.symbol_table.define(name, type, kind.upper())
        
        self._advancer()    # token = ';'

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        assert self.token in _SUBROUTINE_TOKENS
        self.symbol_table.start_subroutine()

        self.current_subroutine_type = self.token
        self._advancer()    # token = 'constructor' | 'function' | 'method'

        return_val_type = self.token
        self._advancer()      # token = type

        subroutine_name = self.token
        self._advancer()  # token = subroutineName

        if self.current_subroutine_type == "method":
            self.symbol_table.define("this", return_val_type, ARG)

        self._advancer()    # token = '('

        self.compile_parameter_list()

        self._advancer()    # token = ')'
        
        self._advancer()    # token = '{'

        self.compile_var_dec()

        n_vars = self.symbol_table.var_count(VAR)

        self.vm_writer.write_function(f"{self.class_name}.{subroutine_name}", n_vars)

        if self.current_subroutine_type == "method":
            self.vm_writer.write_push(ARG, 0)
            self.vm_writer.write_pop(POINTER, 0)

        elif self.current_subroutine_type == "constructor":
            n_fields = self.symbol_table.var_count(FIELD)
            self.vm_writer.write_push(CONST, n_fields)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop(POINTER, 0)

        self.compile_statements()

        self._advancer()    # token = '}'

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """

        if self.token != ')':
            # read all the (type varName) pairs
            type = self.token
            self._advancer()  # token = type

            name = self.token
            self._advancer()  # token = varName

            self.symbol_table.define(name, type, ARG)

            while self.token == ",":
                self._advancer()  # token = ','

                type = self.token
                self._advancer()  # token = type

                name = self.token
                self._advancer()  # token = varName

                self.symbol_table.define(name, type, ARG)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""

        while self.token == 'var':
            kind = self.token
            self._advancer()    # token = 'var'
            
            type = self.token
            self._advancer()  # token = type

            name = self.token
            self._advancer()  # token = varName

            self.symbol_table.define(name, type, kind.upper())

            # eat the rest of all the varName declarations if exist:
            while self.token == ",":
                self._advancer()    # token = ','

                name = self.token
                self._advancer()  # token = varName

                self.symbol_table.define(name, type, kind.upper())

            self._advancer()    # token = ';'

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """

        while self.token in _STATEMENTS_ENTRIES:
            if self.token == "do":
                self.compile_do()

            elif self.token == "let":
                self.counter_let +=1
                self.compile_let()

            elif self.token == "while":
                self.compile_while()

            elif self.token == "return":
                self.compile_return()

            else:  # self.token == "if":
                self.compile_if()

    def compile_do(self) -> None:
        """Compiles a do statement."""

        self._advancer()    # token = 'do'

        # subroutineCall:
        self.compile_expression()  # subroutineCall is same as expression call

        self.vm_writer.write_pop(TEMP, 0)

        self._advancer()    # token = ';'

    def compile_let(self) -> None:
        """Compiles a let statement."""
        array_flag = False

        self._advancer()  # token = 'let'

        name = self.token
        self._advancer()  # token = varName

        # slicing case - varName[expression]:
        if self.token == '[':
            array_flag = True

            kind = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self.vm_writer.write_push(kind, index)  # push arrayName
            self._advancer()    # token = '['
            self.compile_expression()               # push i
            self._advancer()    # token = ']'
            self.vm_writer.write_arithmetic("ADD")

        self._advancer()    # token = '='
        self.compile_expression()

        if array_flag:
            self.vm_writer.write_pop(TEMP, 0)
            self.vm_writer.write_pop(POINTER, 1)
            self.vm_writer.write_push(TEMP, 0)
            self.vm_writer.write_pop(THAT, 0)

        else:
            kind = self.symbol_table.kind_of(name)
            index = self.symbol_table.index_of(name)
            self.vm_writer.write_pop(kind, index)  # push arrayName
        self._advancer()    # token = ';'

    def compile_while(self) -> None:
        """Compiles a while statement."""
        counter = self.counter
        self.counter += 1

        self._advancer()  # token = 'while'
        self.vm_writer.write_label(f"while_{counter}")
        self._advancer()    # token = '('
        self.compile_expression()
        self._advancer()    # token = ')'
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(f"end_while_{counter}")
        self._advancer()    # token = '{'
        self.compile_statements()
        self._advancer()    # token = '}'
        self.vm_writer.write_goto(f"while_{counter}")
        self.vm_writer.write_label(f"end_while_{counter}")

    def compile_return(self) -> None:
        """Compiles a return statement."""

        self._advancer()  # token = 'return'

        # expression-return case:
        if self.token != ';':
            self.compile_expression()
        elif self.current_subroutine_type == "constructor":
            self.vm_writer.write_push(POINTER, 0)
        else:  # void method/function
            self.vm_writer.write_push(CONST, 0)

        self.vm_writer.write_return()

        self._advancer()    # token = ';'

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        counter = self.counter
        self.counter += 1

        self._advancer()  # token = 'if'
        self._advancer()    # token = '('
        self.compile_expression()
        self._advancer()    # token = ')'
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(f"else_{counter}")
        self._advancer()    # token = '{'
        self.compile_statements()
        self._advancer()    # token = '}'
        self.vm_writer.write_goto(f"end_if.else_{counter}")

        # else case:
        self.vm_writer.write_label(f"else_{counter}")
        if self.token == 'else':
            self._advancer()  # token = 'else'
            self._advancer()    # token = '{'
            self.compile_statements()
            self._advancer()    # token = '}'

        self.vm_writer.write_label(f"end_if.else_{counter}")

    def compile_expression(self) -> None:
        """Compiles an expression."""

        self.compile_term()
        while self.token in _BIN_OPS:
            bin_op = self.token
            self._advancer()  # token = _BIN_OPS

            self.compile_term()
            if bin_op == '*':
                self.vm_writer.write_call("Math.multiply", 2)
            elif bin_op == '/':
                self.vm_writer.write_call("Math.divide", 2)
            else:
                self.vm_writer.write_arithmetic(_VM_BIN_OPS[bin_op])

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

        if self.token in _UNARY_OPS:
            un_op = self.token
            self._advancer()  # token = '-' | '~' | '#' | '^'
            self.compile_term()
            self.vm_writer.write_arithmetic(_VM_UNARY_OPS_[un_op])

        elif self.token in _KEYWORD_CONSTANTS:
            if self.token == "this":
                self.vm_writer.write_push(POINTER, 0)
            elif self.token == 'true':
                self.vm_writer.write_push(CONST, 0)
                self.vm_writer.write_arithmetic("NOT")
            else:
                self.vm_writer.write_push(CONST, 0)

            self._advancer()  # token = 'true' | 'false' | 'null' | 'this'

        elif self.token_type == INT_CONST:
            self.vm_writer.write_push(CONST, self.token)
            self._advancer()  # token = integerConst

        elif self.token_type == STRING_CONST:
            s = self.token[1:-1]
            length = len(s)
            self.vm_writer.write_push(CONST, length)
            self.vm_writer.write_call("String.new", 1)  # create an empty string size of s
            for c in s:
                self.vm_writer.write_push(CONST, ord(c))
                self.vm_writer.write_call("String.appendChar", 2)
            self._advancer()

        elif self.token == '(':
            self._advancer()    # token = ')'
            self.compile_expression()
            self._advancer()    # token = ')'

        elif self.token_type == IDENTIFIER:
            identifier_name = self.token
            self._advancer()    # token = className | varName | subroutineName  

            if self.token == '[':
                kind = self.symbol_table.kind_of(identifier_name)
                index = self.symbol_table.index_of(identifier_name)
                self.vm_writer.write_push(kind, index)  # push arrayName
                self._advancer()  # token = '['
                self.compile_expression()  # push i
                self._advancer()  # token = ']'
                self.vm_writer.write_arithmetic("ADD")
                self.vm_writer.write_pop(POINTER, 1)
                self.vm_writer.write_push(THAT, 0)

            # subroutineCall:
            elif self.token == '(':
                self._advancer()
                self.vm_writer.write_push(POINTER, 0)
                n_args = self.compile_expression_list()
                self._advancer()    # token = ')'
                self.vm_writer.write_call(f"{self.class_name}.{identifier_name}", n_args+1)
                
            elif self.token == '.':
                self._advancer()  # token = '.'
                subroutine_name = self.token
                self._advancer()  # token = subroutineName

                kind = self.symbol_table.kind_of(identifier_name)
                if kind != '':      # a method call -> push this
                    index = self.symbol_table.index_of(identifier_name)
                    self.vm_writer.write_push(kind, index)  # push 'this' to the stack

                self._advancer()    # token = '('
                n_args = self.compile_expression_list()
                self._advancer()    # token = ')'

                if kind != '':      # a method call
                    type = self.symbol_table.type_of(identifier_name)
                    self.vm_writer.write_call(f"{type}.{subroutine_name}", n_args + 1)

                else:               # a class function
                    self.vm_writer.write_call(f"{identifier_name}.{subroutine_name}", n_args)

            else:  # identifier is a variable
                kind = self.symbol_table.kind_of(identifier_name)
                index = self.symbol_table.index_of(identifier_name)
                self.vm_writer.write_push(kind, index)
                          
        else:
            raise ValueError

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""

        counter = 0
        # if list not empty:
        if self.token != ')':
            self.compile_expression()
            counter += 1
            while self.token == ',':
                self._advancer()
                self.compile_expression()
                counter += 1

        return counter
