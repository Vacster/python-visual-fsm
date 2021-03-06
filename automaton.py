import regex, PDA
from pygame import event
from functools import reduce
from constants import Graph_State, Token, Custom_Event

class DFA:
    def __init__(self, transitionFunction, initialState, finalStates):
        self.delta = transitionFunction
        self.q0 = initialState
        self.F = finalStates
    def deltaHat(self, state, inputString):
        for a in inputString:
            state = self.delta[state][a]
        return state
    def inLanguage(self, inputString):
        return self.deltaHat(self.q0, inputString) in self.F
    def states(self):
        l = [self.q0]
        for x in self.deep_check(self.q0, "val", []):
            if x not in l and x is not None:
                l.append(x)
        return l
    def deep_check(self, name, looking, done=None):
        try:
            for key, val in self.delta[name].items():
                if val != name:
                    if done is not None:
                        if val not in done:
                            done.append(val)
                            for x in self.deep_check(val, looking, done):
                                yield x
                    else:
                        for x in self.deep_check(val, looking):
                            yield x
                yield val if looking == "val" else key
        except:
            pass
    def finals(self):
        return list(set(self.F).intersection(self.states()))
    def alphabet(self):
        a = []
        for x in self.deep_check(self.q0, "key"):
            if x not in a and x is not None:
                a.append(x)
        return a

class NFA:
    def __init__(self, transitionFunction, initialState, finalStates):
        self.delta = transitionFunction
        self.q0 = initialState
        self.F = set(finalStates)
    def deltaHat(self, state, inputString):
        states = set([state])
        for a in inputString:
            newStates = set([])
            for state in states:
                try:
                    newStates = newStates | self.delta[state][a]
                except KeyError: pass
            states = newStates
        return states
    def inLanguage(self, inputString):
        return len(self.deltaHat(self.q0, inputString) & self.F) > 0
    def alphabet(self):
        return reduce(lambda a,b:set(a)|set(b), [list(x.keys()) for x in list(self.delta.values())])

def nfa_to_dfa(circles, initial):
    N = NFA(get_events(Graph_State.NFA, circles), initial, get_finals(circles))
    q0 = frozenset([N.q0])
    Q = set([q0])
    unprocessedQ = Q.copy()
    delta = {}
    F = []
    Sigma = N.alphabet()

    while len(unprocessedQ) > 0:
        qSet = unprocessedQ.pop()
        delta[qSet] = {}
        for a in Sigma:
            nextStates = reduce(lambda x,y: x|y, [N.deltaHat(q,a) for q in qSet])
            if len(nextStates) > 0:
                nextStates = frozenset(nextStates)
                delta[qSet][a] = nextStates
                if not nextStates in Q:
                    Q.add(nextStates)
                    unprocessedQ.add(nextStates)
    for qSet in Q:
        if len(qSet & N.F) > 0:
            F.append(qSet)

    #Complex unpacking of frozensets going on
    F = [list(x) for x in F]
    finals = []
    for f in F:
        final_name = ""
        for x in f:
            final_name += x
        finals.append(final_name)
    q0, = q0
    states = {}
    for node, data in delta.items():
        name_a = ""
        tmp_dict = {}
        for c in node:
            name_a += c

        if len(data.items()) > 0:
            for text, circle_b in data.items():
                name_b = ""
                for c in circle_b:
                    name_b += c
                tmp_dict[name_b] = text
            states[name_a] = tmp_dict
        else:
            states[name_a] = None

    return states, q0, finals

def get_events(state, circles, reach=None):
    tmp_dict = dict()
    for circle in circles:
        if state == Graph_State.DFA:
            tmp = dict()
            if not circle.lines:
                tmp_dict[circle.text] = {}
            else:
                for line in circle.lines:
                    for x in line.text.split(Token.OR):
                        tmp[x] = line.circle_b.text
                if tmp:
                    tmp_dict[circle.text] = tmp
        else:
            tmp = dict()
            tmp_2 = dict()
            for y, eps_circle in get_epsilon(circle):
                tmp.setdefault(y,[]).append(eps_circle)
            for key, val in tmp.items():
                tmp_2[key] = set(val)
            if tmp_2:
                tmp_dict[circle.text] = tmp_2

    return tmp_dict

def get_epsilon(circle):
    for line in circle.lines:
        for x in line.text.split(Token.OR):
            if x == Token.KLEENE:
                for y, z in get_epsilon(line.circle_b):
                    yield y, z
            else:
                yield x, line.circle_b.text

def get_finals(circles):
    return list(
                map(lambda node: node.text,
                    list(
                        filter(lambda node: node.is_final(), circles))))

def get_pda_transititions(circles):
    transitions = []
    for circle in circles:
        for line in circle.lines:
            for text in line.text.split("|"):
                if text == Token.EPSILON:
                    transitions.append(PDA.Transition(line.circle_a.text, line.circle_b.text, None, None, None))
                else:
                    message = text.split("/")
                    left_side = message[0].split(";")
                    condition = None if left_side[0] == Token.EPSILON else left_side[0]
                    stack = None if left_side[1] == Token.EPSILON else left_side[1]
                    right_side = None if message[1] == Token.EPSILON else message[1].split(",")

                    transitions.append(PDA.Transition(line.circle_a.text, line.circle_b.text, condition, stack, right_side))
    return transitions

def glc_to_pda(file_name):
    pda = PDA.pda_from_file(file_name)
    transitions = []
    for t in pda:
        tmp_string = ""
        tmp_string += (t.condition if t.condition is not None else Token.EPSILON)+";"
        tmp_string += (t.stack if t.stack is not None else Token.EPSILON)+"/"
        first = False
        if t.push is not None:
            for x in t.push:
                if first:
                    tmp_string += ","
                tmp_string += x
                first = True
        else:
            tmp_string += Token.EPSILON
        transitions.append(tmp_string)
    return transitions

def run(state, message, circles, starting, extra=None):
    states = get_events(state, circles)
    finals = get_finals(circles)
    result = None
    try:
        if state == Graph_State.DFA:
            result = str(DFA(states, starting, finals).inLanguage(message))
        elif state == Graph_State.NFA:
            result = str(NFA(states, starting, finals).inLanguage(message))
        elif state == Graph_State.PDA:
            pda = PDA.PDA([x.text for x in circles], get_pda_transititions(circles), finals, starting)
            result = str(pda.solve(message))
        elif state == Graph_State.PDA_E:
            pda = PDA.PDA([x.text for x in circles], get_pda_transititions(circles), finals, starting)
            result = str(pda.solve(message, stack=PDA.Stack(extra), empty=True))
    except Exception as e:
        print(e)
        result = "False"
    event.post(
        event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
        message=result)
    )

def union(start1, start2, circles):
    return cross_product(start1, start2, circles, bool.__or__)

def intersection(start1, start2, circles, circles2=None):
    return cross_product(start1, start2, circles, bool.__and__, circles2)

def cross_product(start1, start2, circles, accept_method, circles2=None):
    states = get_events(Graph_State.DFA, circles)
    finals = get_finals(circles)
    D1 = DFA(states, start1, finals)
    if circles2 is None:
        D2 = DFA(states, start2, finals)
    else:
        states2 = get_events(Graph_State.DFA, circles2)
        finals2 = get_finals(circles2)
        D2 = DFA(states2, start2, finals2)

    alphabet = ['0', '1']
    #
    # alphabet = D1.alphabet()
    #
    # alphabet.extend(D2.alphabet())
    # alphabet = list(set(alphabet))

    transitions = {}
    print(D1.states())
    for state1 in D1.states():
        for state2 in D2.states():
            transitions[state1+","+state2] = {}
            for a in alphabet:
                try:
                    tr1 = D1.deltaHat(state1, a)
                except Exception as e:
                    print(e)
                    tr1 = "_"
                try:
                    tr2 = D2.deltaHat(state2, a)
                except Exception as e:
                    print(e)
                    tr2 = "_"

                transitions[state1+","+state2][a] = (tr1+","+tr2)
                if (tr1+","+tr2) not in transitions:
                    transitions[tr1+","+tr2] = {}

    states = {}
    for key1, val1 in transitions.items():
        if key1 != "_,_":
            states[key1] = {}
            if val1:
                for key2, val2 in val1.items():
                    if val2 != "_,_":
                        states[key1][key2] = val2

    start = (D1.q0+","+D2.q0)
    accepts = []
    for x in states:
        s = x.split(",")
        a1 = s[0] in D1.finals()
        a2 = s[1] in D2.finals()
        if accept_method(a1, a2):
            accepts.append(x)

    # reachable = [start]
    # reachable.extend(get_reachables(states, start))
    # reachable = list(set(reachable))
    # keys = []
    # for key, val in states.items():
    #     if key not in reachable:
    #         keys.append(key)
    # for key in keys:
    #     del states[key]]
    return states, start, accepts

#This function is stupidly buggy
def get_reachables(states, name, dones=[]):
    try:
        for key, val in states[name].items():
            if val != name and val not in dones:
                for x in get_reachables(states, val):
                    yield x
            dones.append(val)
            yield val
    except:
        pass

#Buggy
def get_alphabet(states, name):
    try:
        for key, val in states[name].items():
            if name != val:
                for x in get_alphabet(states, val):
                    yield x
            yield key
    except:
        pass

def complement(circles, starting):
    states = get_events(Graph_State.DFA, circles)
    finals = get_finals(circles)
    #Gotta turn it around for algorithm

    # alphabet = list(set(get_alphabet(states, starting)))
    alphabet = ['1', '0']
    hole_created = False
    #Hole
    for key, val in states.items():
        for a in alphabet:
            if a not in val.keys():
                states[key][a] = "β"
                hole_created = True

    reachables = [starting]
    reachables.extend(set(get_reachables(states, starting)))
    if hole_created:
        if "β" not in reachables:
            reachables.extend("β")
        states["β"] = {}
        for a in alphabet:
            states["β"][a] = "β"
    for node in reachables:
        if node not in states:
            states[node] = {}
            for a in alphabet:
                states[node][a] = "β"
    #Switch finals around
    finals = [x for x in reachables if x not in finals]
    return states, starting, finals

def difference(start1, start2, circles):
    states = get_events(Graph_State.DFA, circles)
    reachable1 = [start1]
    reachable1.extend(list(get_reachables(states, start1)))
    reachable1 = list(set(reachable1))

    reachable2 = [start2]
    reachable2.extend(set(get_reachables(states, start2)))
    reachable2 = list(set(reachable2))

    circle1 = []
    circle2 = []
    for circle in circles:
        if circle.text in reachable1:
            circle1.append(circle)
        if circle.text in reachable2:
            circle2.append(circle)
    n, s, f = complement(circle2, start2)

    return circle1, n, s, f

def regex_to_nfa(node_manager, reg):
    regex.regex_to_nfa(node_manager, reg)

def reflection(reg):
    return regex.reflection(reg)
