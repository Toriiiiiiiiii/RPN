from typing import *
from error import *

TOK_ERR = "ERROR"
TOK_NUM = "NUMBER"
TOK_WRD = "WORD" 
TOK_OPR = "OPERATOR"
TOK_STR = "STRING"
TOK_EOF = "EOF"

class Token:
    def __init__(self, line: int, col: int, tokType: str, tokVal: Union[str, float, int, None]) -> None:
        self.line: int = line
        self.col: int  = col
        self.tokType: int = tokType
        self.tokVal: Union[str, float, int, None]  = tokVal

    def __repr__(self) -> str:
        return f"TOK({self.line}, {self.col}, {self.tokType}, {self.tokVal})"

class Lexer:
    def __init__(self, fileContents: str) -> None:
        self.fileContents: List[str] = list(fileContents)
        self.line: int = 0
        self.col: int  = 0

        self.tokens: List[Token] = []

        self.wordStart = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.numStart = "0123456789"
        self.operators = "+-*/%=><"
        self.wordBody = self.wordStart + self.numStart
        self.numBody = self.numStart + "."
        self.whiteSpace = " \n\t"
        self.stringMarkers = "\"'"

        self.performAnalysis()

    def current(self) -> Union[str, None]:
        if self.isEmpty(): return None

        return self.fileContents[0]

    def currentAndConsume(self) -> Union[str, None]:
        if self.isEmpty(): return None

        current: str = self.fileContents.pop(0)

        self.col += 1
        if current == "\n":
            self.col = 0
            self.line += 1

        return current

    def isEmpty(self) -> bool:
        return True if len(self.fileContents) == 0 else False

    def buildWord(self) -> Token:
        body: str = ""

        while self.current() in self.wordBody:
            body += self.currentAndConsume()

        return Token(self.line, self.col, TOK_WRD, body)

    def buildNum(self) -> Union[Token, None]:
        body: str = ""
        numDots = 0

        while self.current() in self.numBody:
            char: str = self.currentAndConsume()

            if char == ".":
                if numDots > 0: 
                    throwError("Invalid float format.")
                    return None
                else:
                    numDots += 1

            body += char

        return Token(self.line, self.col, TOK_NUM, float(body))

    def buildOperator(self) -> Union[Token, None]:
        body: str = self.currentAndConsume()

        if body == "-" and self.current() in self.numStart:
            tok: Token = self.buildNum()

            if tok != None:
                tok.tokVal *= -1
            
            return tok

        while self.current() in self.operators:
            body += self.currentAndConsume()

        return Token(self.line, self.col, TOK_OPR, body)

    def buildString(self) -> Token:
        body: str = ""
        stringMarker = self.currentAndConsume()

        while self.current() != stringMarker:
            body += self.currentAndConsume()

        self.currentAndConsume()
        return Token(self.line, self.col, TOK_STR, body)

    def performAnalysis(self) -> None:
        while not self.isEmpty():
            nextChar: str = self.current()

            if not nextChar:
                throwError(ERR_LEX_UNEXPECTEDEOF, "Unexpected end of file. This should not happen. Likely a lexer bug.")
                return
            
            if nextChar in self.wordStart:
                self.tokens.append( self.buildWord() )
            elif nextChar in self.numStart:
                tok: Union[None, Token] = self.buildNum()

                if not tok:
                    return

                self.tokens.append( tok )
            elif nextChar in self.operators:
                tok: Union[None, Token] = self.buildOperator()

                if not tok:
                    return

                self.tokens.append(tok)
            elif nextChar in self.whiteSpace:
                self.currentAndConsume()
            elif nextChar in self.stringMarkers:
                self.tokens.append(self.buildString())
            else:
                throwError(ERR_LEX_UNKNOWNTOK, f"Unknown character '{nextChar}'")
                return

        self.tokens.append(Token(self.line, self.col, TOK_EOF, "EOF"))
