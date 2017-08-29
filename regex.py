import parser, math
from constants import SCREEN_SIZE, Token

counter = None
total = None
manager = None

def circle_arrange(index, total):
    return  [int((math.cos((index * (2*math.pi))/total)
    * 500) + (SCREEN_SIZE[0]/2)),
    int((math.sin((index * (2*math.pi))/total)
    * 500) + (SCREEN_SIZE[1]/2))]

def add_value(previous, value):
    global counter
    counter += 1
    new_name = "q" + str(counter)
    new_circle = manager.add_node(new_name, circle_arrange(counter, total))
    new_circle.toggle_final()

    for circle in previous:
        if circle != None:
            circle.add_line(new_circle, str(value))
            circle.toggle_final(False)
    return new_circle

def recursive_parser(element, previous):
    global counter
    if previous == None:
        previous =  manager.add_node("Start", circle_arrange(0, total))

    element_type, value = element.get_element()
    if element_type == parser.Token_ENUM.TK_LETTER \
    or element_type == parser.Token_ENUM.TK_DIGIT:
        return add_value([previous], value)
    elif element_type == parser.Token_ENUM.OP_OR:
        previous_1 = add_value([previous], Token.EPSILON)
        previous_2 = add_value([previous], Token.EPSILON)
        new_1 = recursive_parser(value[0], previous_1)
        new_2 = recursive_parser(value[1], previous_2)
        return add_value([new_1, new_2], Token.EPSILON)
    elif element_type == parser.Token_ENUM.OP_KLEENE:
        mid_start = add_value([previous], Token.EPSILON)
        mid_end = recursive_parser(value, mid_start)
        mid_end.add_line(mid_start, Token.EPSILON)
        return add_value([mid_end, previous], Token.EPSILON)
    elif element_type == parser.Token_ENUM.OP_CONCAT:
        left = recursive_parser(value[0], previous)
        eps = add_value([left], Token.EPSILON)
        right = recursive_parser(value[1], eps)
        return add_value([right], Token.EPSILON)

def recursive_reflect(element):
    element_type, value = element.get_element()
    if element_type == parser.Token_ENUM.TK_LETTER \
    or element_type == parser.Token_ENUM.TK_DIGIT:
        return str(value)
    elif element_type == parser.Token_ENUM.OP_OR:
        r1 = recursive_reflect(value[0])
        r2 = recursive_reflect(value[1])
        return (r1 + Token.OR + r2)
    elif element_type == parser.Token_ENUM.OP_KLEENE:
        r1 = recursive_reflect(value)
        return ("("+r1+")"+Token.KLEENE)
    elif element_type == parser.Token_ENUM.OP_CONCAT:
        r1 = recursive_reflect(value[0])
        r2 = recursive_reflect(value[1])
        return (r2 + Token.AND + r1)

def reflection(regex):
    tree, _ = parser.parse(regex)
    return recursive_reflect(tree)

def regex_to_nfa(node_manager, regex):
    global counter
    global total
    global manager
    counter = 0
    tree, total = parser.parse(regex)
    manager = node_manager
    recursive_parser(tree, None)
