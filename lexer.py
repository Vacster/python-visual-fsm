from tokens import *

input = ""
global_len = 0
contador = 0
character =  ''
def setInput(text):
    global input
    input = text
    global global_len
    global_len = len(input)
    global contador
    contador = 0

def getNextCharacter():
    global contador, global_len
    if contador < global_len:
        character = input[contador]
        contador += 1
        return character
    return '\0'

def getNextToken():
    global character
    character = getNextCharacter()
    while character == ' ' or character == '\n':
        character = getNextCharacter()
    if character == '\0':
        return Token(character, Token_ENUM.TK_EOF)

    if character.isalpha():
        return Token(character, Token_ENUM.TK_LETTER)
    if character.isdigit():
        return Token(character, Token_ENUM.TK_DIGIT )
    if character == '+':
        return Token(character, Token_ENUM.OP_OR )
    if character == '.':
        return Token(character, Token_ENUM.OP_CONCAT )
    if character == '*':
        return Token(character, Token_ENUM.OP_KLEENE )
    if character == '(':
        return Token(character, Token_ENUM.TK_LEFT_PAR )
    if character == ')':
        return Token(character, Token_ENUM.TK_RIGHT_PAR )

    raise ValueError("Syntax Error: Unexpected char ", character)
