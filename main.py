import sys
import os

from typing import *
from error import *
from lexer import *
from parser import *
from interpreter import *

def readFile(path: str) -> Union[str, None]:
    try:
        file = open(path, "r")
        contents = file.read()
        file.close()

        return contents
    except Exception as e:
        throwError(ERR_IO_FILEERROR, f"Could not read file '{path}'")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        exit(1)

    fileContents = readFile(sys.argv[1])

    if not fileContents:
        quit(1)

    lexer = Lexer(fileContents)

    parser = Parser(lexer.tokens)

    with open("ast.txt", "w") as f:
        f.write(parser.program.__repr__())

    interpreter = Interpreter(parser.program)
