from error import *
from lexer import *
from typing import *

ASTNODE_INDENT = 0

class ASTNode:
    def __init__(self, line: int, col: int, nodeType: str, value: Union[str, int, float, None], children: list = []) -> None:
        self.line = line
        self.col = col
        self.nodeType = nodeType
        self.value = value
        self.children = children

    def __repr__(self) -> str:
        global ASTNODE_INDENT

        result =  f" " * ASTNODE_INDENT + f"NODE_{self.nodeType} (\n"

        ASTNODE_INDENT += 2
        result += f" " * ASTNODE_INDENT + f"LINE:     {self.line},\n"
        result += f" " * ASTNODE_INDENT + f"COL:      {self.col},\n"
        result += f" " * ASTNODE_INDENT + f"VAL:      {self.value},\n"
        result += f" " * ASTNODE_INDENT + f"CHILDREN: {self.children}\n"
        ASTNODE_INDENT -= 2

        result += f" " * ASTNODE_INDENT + ")"

        return result

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.lastToken = None
        self.tokens = tokens
        self.program = ASTNode(0, 0, "PROGRAM", "")

        self.program.children = self.parse()

    def getCurrent(self) -> Token:
        return self.tokens[0]

    def getCurrentAndConsume(self) -> Token:
        return self.tokens.pop(0)

    def isEmpty(self) -> bool:
        return len(self.tokens) == 0

    # TODO: Function syntax checking
    def buildFunctionDefinition(self) -> ASTNode:
        self.getCurrentAndConsume()

        functionName = self.getCurrentAndConsume()
        blockBody = self.parse(terminatorType=TOK_WRD, terminatorVals=["end"])

        return ASTNode(functionName.line, functionName.col, "FN", functionName.tokVal, blockBody)

    def buildIfElseStatement(self, useEnd = True) -> ASTNode:
        firstToken = self.getCurrentAndConsume()

        conditionBody = []
        currentToken = self.getCurrentAndConsume()

        while currentToken.tokVal != "then":
            conditionBody.append(currentToken)
            currentToken = self.getCurrentAndConsume()

        tempParser = Parser(conditionBody)
        codeBlock = self.parse(terminatorType=TOK_WRD, terminatorVals=["end", "else"] if useEnd else ["else"])

        children = []

        if self.lastToken.tokVal == "else":
            self.getCurrentAndConsume()
            if self.getCurrent().tokVal == "if":
                children += [[self.buildIfElseStatement()]]
            else:
                children.append(self.parse(terminatorType=TOK_WRD, terminatorVals=["end"]))

        return ASTNode(firstToken.line, firstToken.col, "IF", "", [tempParser.program.children, codeBlock] + children)

    def buildWhileLoop(self) -> ASTNode:
        firstToken = self.getCurrentAndConsume()

        conditionBody = []
        currentToken = self.getCurrentAndConsume()

        while currentToken.tokVal != "do":
            conditionBody.append(currentToken)
            currentToken = self.getCurrentAndConsume()

        tempParser = Parser(conditionBody)
        codeBlock = self.parse(terminatorType=TOK_WRD, terminatorVals=["end"])

        return ASTNode(firstToken.line, firstToken.col, "WHILE", "", [tempParser.program.children, codeBlock])

    def parse(self, terminatorType: str = "EOF", terminatorVals: List[str] = ["EOF"]) -> List[ASTNode]:
        result = []

        while not self.isEmpty():
            currentToken: Token = self.getCurrent()
            self.lastToken = currentToken

            if currentToken.tokType == terminatorType and currentToken.tokVal in terminatorVals:
                #print(currentToken.tokType, currentToken.tokVal)
                #print(self.lastToken)
                break

            if currentToken.tokType == TOK_ERR:
                break

            if currentToken.tokType == TOK_NUM:
                result.append( ASTNode(currentToken.line, currentToken.col, "NUM", currentToken.tokVal) )
            elif currentToken.tokType == TOK_OPR:
                if currentToken.tokVal == "->":
                    self.getCurrentAndConsume()
                    nameToken = self.getCurrentAndConsume()

                    result.append(ASTNode(currentToken.line, currentToken.col, "VAR", nameToken.tokVal))
                    continue

                result.append( ASTNode(currentToken.line, currentToken.col, "OPR", currentToken.tokVal) )
            elif currentToken.tokType == TOK_STR:
                result.append(ASTNode(currentToken.line, currentToken.col, "STR", currentToken.tokVal))
            elif currentToken.tokType == TOK_WRD:
                if currentToken.tokVal == "fn":
                    result.append(self.buildFunctionDefinition())
                elif currentToken.tokVal == "if":
                    result.append(self.buildIfElseStatement())
                elif currentToken.tokVal == "while":
                    result.append(self.buildWhileLoop())
                else:
                    result.append(ASTNode(currentToken.line, currentToken.col, "WRD", currentToken.tokVal))

            try:
                self.getCurrentAndConsume()
            except:
                return result

        return result
