from tokens import Token_ENUM

class Element:
    def get_element(self):
        raise NotImplementedError("Get_element not implemented")

class Digit(Element):
    def __init__(self, number):
        self.number = number

    def get_element(self):
        return Token_ENUM.TK_DIGIT, self.number

    def printable(self, padding):
        print (padding,"digit: ",self.number)

class Letter(Element):
    def __init__(self, letter):
        self.letter = letter

    def get_element(self):
        return Token_ENUM.TK_LETTER, self.letter

    def printable(self, padding):
        print (padding,"letter: ",self.letter)

class Kleene(Element):
    def __init__(self, expression):
        self.expression = expression

    def get_element(self):
        return Token_ENUM.OP_KLEENE, self.expression

    def printable(self, padding):
        print (padding,"klenne: ")
        print(padding,"expr-"),self.expression.printable(padding+"\t")

class Concat(Element):
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

    def get_element(self):
        return Token_ENUM.OP_CONCAT, [self.left_expr, self.right_expr]

    def printable(self, padding):
        print (padding,"concat: ")
        print(padding,"left_expr:-"),self.left_expr.printable(padding+"\t")
        print(padding,"right_expr:-"),self.right_expr.printable(padding+"\t")

class Or(Element):
    def __init__(self, left_expr, right_expr):
        self.left_expr = left_expr
        self.right_expr = right_expr

    def get_element(self):
        return Token_ENUM.OP_OR, [self.left_expr, self.right_expr]

    def printable(self, padding):
        print (padding, "or: ")
        print(padding,"left_expr:-"),self.left_expr.printable(padding+"\t")
        print(padding,"right_expr:-"),self.right_expr.printable(padding+"\t")
