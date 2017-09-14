import json
from constants import Token

class Stack:
    def __init__(self, val=None):
        s = [Token.STACK] if val is None else [val]
        self.stack = s

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.peek() is not None:
            return self.stack.pop()
        else:
            return None

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None

    def pretty_print(self):
        print(self.stack)

class Transition:
    def __init__(self, init, end, condition, stack, push):
        self.init = init
        self.end = end
        self.condition = condition
        self.stack = stack
        self.push = push

    def pretty_print(self):
        print("S:", self.init, "\tE:", self.end, "\tC:", self.condition, "\tStack:", self.stack, "\tPush:", self.push)

    def is_free(self):
        return (self.condition is None) and (self.stack is None) and (self.push is None)

class PDA:
    def __init__(self, states, transitions, final_states, initial_state):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def solve(self, input_tape, state=None, stack=Stack(), empty=False):
        if state is None:
            state = self.initial_state

        # print("State: ", state, "\tInput: ", input_tape, "\tStack: ", stack.stack)

        if len(stack.stack) > 20:
            return False

        if input_tape is not None and len(input_tape) > 0:
            value = input_tape[0]
        else:
            value = None

        if state in self.final_states and value is None and not empty:
            return True

        if stack.peek() is None and empty and value is None:
            return True

        for transition in [t for t in self.transitions if t.init == state]:
            new_stack = Stack()
            if transition.is_free(): #Continue without paying anything
                new_stack.stack = stack.stack.copy()
                if self.solve(input_tape, transition.end, new_stack, empty=empty):
                    return True

            else:
                new_input = None
                new_stack.stack = stack.stack.copy()
                if transition.stack is None or transition.stack == stack.peek():
                    if transition.condition is None:
                        new_input = input_tape
                    elif transition.condition == value:
                        new_input = input_tape[1:]
                    elif (transition.condition is None and input_tape == ""):
                        new_input = ""
                else:
                    continue
                transition.pretty_print()

                if new_input is not None:
                    if transition.stack is not None:
                        new_stack.pop()
                    if transition.push is not None:
                        for push in reversed(transition.push):
                            if push is not None:
                                new_stack.push(push)

                    # print("Calling", "State: ", transition.end, "\tInput: ", new_input, "\tStack: ", new_stack.stack)
                    if self.solve(new_input, transition.end, new_stack, empty=empty):
                        return True
                else:
                    continue
        # print("Return False")
        return False

def pda_from_file(file_name):
    keys = []
    values = []
    transitions = []
    single_state = 'q'

    with open(file_name) as data_file:
        data = json.load(data_file)

    for key, val in data.items():
        keys.append(key)
        for obj in val:
            for char in obj:
                if char not in values:
                    values.append(char)

    for val in values:
        if val in keys:
            for arr in data[val]:
                t = Transition('q', 'q', None, val, arr)
                transitions.append(t)
        else:
            t = Transition('q', 'q', val, val, None)
            transitions.append(t)

    return transitions
#Test
# states = ['p', 'q', 'r']
# t1 = Transition('p', 'p', '0', Token.STACK, ['0',Token.STACK])
# t2 = Transition('p', 'p', '0', '0', ['0', '0'])
# t3 = Transition('p', 'q', None, Token.STACK, [Token.STACK])
# t4 = Transition('p', 'q', '1', '0', None)
# t5 = Transition('q', 'q', '1', '0', None)
# t6 = Transition('q', 'r', None, Token.STACK, [Token.STACK])
# transitions = [t1, t2, t3, t4, t5, t6]
# final_states = ['r']
# initial_state = 'p'
# pda = PDA(states, transitions, final_states, initial_state)
# print(pda.solve("1"))

# pda_from_file("glc.json")
