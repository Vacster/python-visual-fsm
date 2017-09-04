from constants import Token

class Stack:
    def __init__(self):
        self.stack = [Token.STACK]

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
        print(self.init, self.end, self.condition, self.stack, self.push)

    def is_free(self):
        return (self.condition is None) and (self.stack is None) and (self.push is None)

class PDA:
    def __init__(self, states, transitions, final_states, initial_state):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        print(states, initial_state, final_states)

    def solve(self, input_tape, state=None, stack=Stack()):
        if state is None:
            state = self.initial_state

        print("State: ", state, "\tInput: ", input_tape, "\tStack: ", stack.stack)

        if len(input_tape) > 0:
            value = input_tape[0]
        else:
            value = None

        if state in self.final_states and value is None:
            return True

        for transition in [t for t in self.transitions if t.init == state]:
            new_stack = Stack()
            if transition.is_free(): #Continue without paying anything
                new_stack.stack = stack.stack.copy()
                if self.solve(input_tape, transition.end, new_stack):
                    print("Calling for free")
                    return True

            else:
                new_input = None
                new_stack.stack = stack.stack.copy()

                if transition.stack is None or transition.stack == stack.peek():
                    if transition.condition is None:
                        new_input = input_tape
                    elif transition.condition == value:
                        new_input = input_tape[1:]

                if new_input is not None:
                    if transition.stack is not None:
                        new_stack.pop()
                    if transition.push is not None:
                        for push in reversed(transition.push):
                            new_stack.push(push)

                    print("Calling", "State: ", transition.end, "\tInput: ", new_input, "\tStack: ", new_stack.stack)
                    if self.solve(new_input, transition.end, new_stack):
                        return True
        return False
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
