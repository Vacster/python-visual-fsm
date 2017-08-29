
class Token:
    def __init__(self, lexema, token_id):
        self.lexema = lexema
        self.token_id = token_id

class Token_ENUM:
    TK_EOF = 0
    TK_LETTER = 1
    TK_DIGIT = 2
    OP_OR = 3
    OP_KLEENE = 4
    TK_LEFT_PAR = 5
    TK_RIGHT_PAR = 6
    OP_CONCAT = 7
