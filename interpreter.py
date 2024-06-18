from parser import *
from typing import *
from error import *

class RuntimeValue:
    def __init__(self, type:str, value) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

class Interpreter:
    def __init__(self, program: ASTNode) -> None:
        self.program = program
        self.functions: Dict[str, ASTNode] = {}

        self.stack: list = []

        self.findAndRemoveFunctions()
        self.run(program.children)

    def push(self, value: RuntimeValue) -> None:
        self.stack.append(value)

    def pop(self) -> RuntimeValue:
        if len(self.stack) == 0:
            throwError(ERR_RUN_STACK, "Stack underflow")
            exit(1)

        return self.stack.pop()

    def findAndRemoveFunctions(self) -> None:
        nodePointer = 0

        while nodePointer < len(self.program.children):
            node = self.program.children[nodePointer]

            if node.nodeType == "FN":
                self.functions[node.value] = node
                self.program.children.pop(nodePointer)

                continue

            nodePointer += 1

    def run(self, program: List[ASTNode], scope = {}) -> None:
        for node in program:
            # print(node)
            if node.nodeType == "WRD":
                if node.value == "print":
                    print(self.pop())

                elif node.value == "return":
                    return
                elif node.value in self.functions:
                    toRun = self.functions[node.value].children
                    self.run(toRun, scope = scope.copy())
                elif node.value in scope:
                    self.push(scope[node.value])
                else:
                    throwError(ERR_RUN_REF, f"Undefined reference to '{node.value}'")
                    exit(1)

            if node.nodeType == "NUM":
                self.push(RuntimeValue("NUM", node.value))

            if node.nodeType == "STR":
                self.push(RuntimeValue("STR", node.value))

            if node.nodeType == "IF":
                condition = node.children[0]
                self.run(condition, scope=scope.copy())

                result = self.pop()
                if result.value:
                    self.run(node.children[1], scope=scope)
                else:
                    self.run(node.children[2], scope=scope)

            if node.nodeType == "WHILE":
                condition = node.children[0]
                self.run(condition, scope=scope.copy())

                while self.pop().value:
                    self.run(node.children[1], scope=scope)
                    self.run(condition, scope=scope)

            if node.nodeType == "VAR":
                scope[node.value] = self.pop() 

            if node.nodeType == "OPR":
                b = self.pop()
                a = self.pop()

                if a.type != b.type:
                    return

                match node.value:
                    case "+":        
                        match a.type:
                            case "NUM":
                                self.push(RuntimeValue("NUM", float(a.value) + float(b.value)))

                    case "-":
                        match a.type:
                            case "NUM":
                                self.push(RuntimeValue("NUM", float(a.value) - float(b.value)))

                    case "*":
                        match a.type:
                            case "NUM":
                                self.push(RuntimeValue("NUM", float(a.value) * float(b.value)))

                    case "/":
                        match a.type:
                            case "NUM":
                                self.push(RuntimeValue("NUM", float(a.value) / float(b.value)))

                    case "%":
                        match a.type:
                            case "NUM":
                                self.push(RuntimeValue("NUM", float(a.value) % float(b.value)))


                    case "==":
                        self.push(RuntimeValue("NUM", 1 if a.value == b.value else 0))

                    case "<":
                        self.push(RuntimeValue("NUM", 1 if float(a.value) < float(b.value) else 0))

                    case ">":
                        self.push(RuntimeValue("NUM", 1 if float(a.value) > float(b.value) else 0))
