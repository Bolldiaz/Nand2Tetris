"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

STATIC, FIELD, ARG, VAR = "STATIC", "FIELD", "ARG", "VAR"


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.class_table = dict()
        self.subroutine_table = dict()
        self.counters = {STATIC: 0, FIELD: 0, ARG: 0, VAR: 0}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_table = dict()
        self.counters[ARG] = self.counters[VAR] = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind == STATIC:
            self.class_table[name] = (type, kind, self.counters[STATIC])
            self.counters[STATIC] += 1

        elif kind == FIELD:
            self.class_table[name] = (type, kind, self.counters[FIELD])
            self.counters[FIELD] += 1

        elif kind == ARG:
            self.subroutine_table[name] = (type, kind, self.counters[ARG])
            self.counters[ARG] += 1

        elif kind == VAR:
            self.subroutine_table[name] = (type, kind, self.counters[VAR])
            self.counters[VAR] += 1

        else:
            raise ValueError

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        assert kind in self.counters

        return self.counters[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """

        if name in self.subroutine_table:
            return self.subroutine_table[name][1]

        if name in self.class_table:
            return self.class_table[name][1]

        else:
            return ''

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        assert name in self.class_table or name in self.subroutine_table

        if name in self.subroutine_table:
            return self.subroutine_table[name][0]

        return self.class_table[name][0]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        assert name in self.class_table or name in self.subroutine_table

        if name in self.subroutine_table:
            return self.subroutine_table[name][2]

        return self.class_table[name][2]
