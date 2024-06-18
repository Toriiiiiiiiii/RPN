from typing import *

ERR_IO_FILEERROR = 1

ERR_LEX_UNEXPECTEDEOF = 2
ERR_LEX_UNKNOWNTOK = 3

ERR_RUN_STACK = 4
ERR_RUN_REF = 5

def throwError(code: int, message: str):
    print(f"ERROR : {message} (Code {code}).")

