import element, automaton, pickle, math, pyperclip
from constants import Color, Custom_Event, Graph_State, SCREEN_SIZE
from pygame import event, QUIT

class Node_Manager:
    def __init__(self):
        self.circles = []
        self.selected = None
        self.dragged = None #Not too sure about this one

    def add_node(self, text, pos=(500,500), lines=None, color=Color.BLUE,
    final=False):
        assert(text is not None)

        #Second part of this if violates internal coupling
        if not text or self.dragged is not None:
            return None
        if self.find_circle_name(text) is not None:
            event.post(event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
                    message="Node already exists."))
            return None
        circle = element.Circle(text, pos, lines, color, final)
        self.circles.append(circle)
        return circle

    def clear(self):
        del self.circles[:]
        self.select(None)

    #TODO: KILL IT WITH FIRE
    def delete_element(self, element):
        assert(element is not None)

        tmp = []
        for circle in self.circles:
            for line in circle.lines:
                if element in [line.circle_a, line.circle_b, line]:
                    tmp.append(line)
        for circle in self.circles:
            for x in tmp:
                try:
                    circle.lines.remove(x)
                except:
                    continue
        self.select(None) #Remove selection after erasing
        if element in self.circles:
            self.circles.remove(element)

    def find_circle_name(self, text):
        assert(text is not None)

        for circle in self.circles:
            if circle.text == text:
                return circle
        return None

    def find_circle_pos(self, pos):
        assert(pos is not None)

        for circle in self.circles:
            if circle.is_clicked(pos):
                return circle
        return None

    def find_element_pos(self, pos):
        assert(pos is not None)

        found = self.find_circle_pos(pos)
        if found is not None:
            return found, "circle"

        for node in self.circles:
            for transition in node.lines:
                if transition.is_clicked(pos):
                    return transition, "line"
        return None, None

    def find_transition(self, graph_state, circle_a, circle_b, text):
        if graph_state == Graph_State.DFA:
            return circle_a.has_transition(text)
        else:
            transition = circle_a.has_transition(text, circle_b)
            if transition is not None and node is circle_a:
                return transition
            return None

    def select(self, node):
        if self.selected is not None:
            self.selected.toggle_selected()

        if node is not None:
            node.toggle_selected()
        self.selected = node

    def add_transition(self, state, node_b, text):
        assert(node_b is not None)
        assert(text is not None)
        assert(state is not None)

        if self.selected is None:
            event.post(event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
                    message="No initial node selected."))
            return False
        if self.find_transition(state, self.selected, node_b, text) is not None:
            event.post(event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
                    message="Transition already exists."))
            return False
        self.selected.add_line(node_b, text)
        self.select(None)
        return True

    def start_drag(self, element):
        assert(element is not None)

        self.dragged = element

    def drag_element(self, pos):
        assert(pos is not None)

        if self.dragged is not None:
            self.dragged.update_pos(pos)

    def stop_drag(self):
        self.dragged = None

    def change_state(self, graph_state):
        if graph_state == Graph_State.DFA:
            graph_state = Graph_State.NFA
        elif graph_state == Graph_State.NFA:
            graph_state = Graph_State.PDA
        else:
            graph_state = Graph_State.DFA
        event.post(
            event.Event(Custom_Event.UPDATE_GRAPH_STATE,
            state=graph_state)
        )
        return graph_state

    def construct_circles(self, nodes, starting, finals):
        self.clear()
        total = len(nodes)
        for index, node in enumerate(nodes):
            pos =  [int((math.cos((index * (2*math.pi))/total)
            * 500) + (SCREEN_SIZE[0]/2)),
            int((math.sin((index * (2*math.pi))/total)
            * 500) + (SCREEN_SIZE[1]/2))]
            self.add_node(node, pos=pos, final=(node in finals))

        for value, node in nodes.items():
            for text, node2 in node.items():
                if node2 is not None:
                    circle = self.find_circle_name(value)
                    circle_b = self.find_circle_name(node2)
                    circle.add_line(circle_b, text)
                    if circle.text == starting:
                        self.select(circle)

    #Run should be in another class
    def run_command(self, graph_state, message):
        if len(message) > 0:
            if message[0] == "clear":
                self.clear()
                return True
            elif message[0] == "exit":
                event.post(event.Event(QUIT))
                return True
            elif message[0] == "edit":
                if self.selected is not None:
                    self.selected.edit(message[1])
                    return True
                return False
            elif message[0] == "save":
                try:
                    self.save(message[1], graph_state)
                    return True
                except Exception as e:
                    event.post(
                        event.Event(Custom_Event.UPDATE_TEMP_MESSAGE, message=str(e))
                    )
                    return False
            elif message[0] == "load":
                try:
                    self.load(message[1])
                    return True
                except Exception as e:
                    event.post(
                        event.Event(Custom_Event.UPDATE_TEMP_MESSAGE, message=str(e))
                    )
                    return False
            elif message[0] == "change":
                if self.change_state(graph_state) == Graph_State.DFA:
                    nodes, s, f = automaton.nfa_to_dfa(self.circles, self.selected.text)
                    self.construct_circles(nodes, s, f)
                return True
            elif message[0] == "union":
                n, s, f = automaton.union(message[1], message[2], self.circles)
                self.construct_circles(n, s, f)
                return True
            elif "inter" in message[0]:
                n, s, f = automaton.intersection(message[1], message[2], self.circles)
                self.construct_circles(n, s, f)
                return True
            elif "compl" in message[0]:
                if self.selected is None:
                    event.post(
                        event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
                        message="Starting node must be selected.")
                    )
                else:
                    n, s, f = automaton.complement(self.circles, self.selected.text)
                    self.construct_circles(n, s, f)
                    return True
            elif "diff" in message[0]:
                circle1, n, s, f = automaton.difference(message[1], message[2], self.circles)
                self.construct_circles(n, s, f)

                n2, s2, f2 = automaton.intersection(message[1], s, circle1, self.circles)
                self.construct_circles(n2, s2, f2)
                return True
            elif "regex" in message[0]:
                self.clear()
                self.change_state(Graph_State.DFA)
                automaton.regex_to_nfa(self, message[1])
                self.select(self.find_circle_name("Start"))
                return True
            elif "refl" in message[0]:
                result = automaton.reflection(message[1])
                event.post(
                    event.Event(Custom_Event.UPDATE_TEMP_MESSAGE_TIME,
                    message=result, time=8)
                )
                pyperclip.copy(result)
                return True
            else:
                if self.selected is None:
                    event.post(
                        event.Event(Custom_Event.UPDATE_TEMP_MESSAGE,
                        message="Starting node must be selected.")
                    )
                else:
                    automaton.run(graph_state, message[0],
                    self.circles, self.selected.text)
                    return False

    #Save and load should be in another class
    def save(self, name, state):
        dump = {}
        dump["circles"] = []
        for circle in self.circles:
            dump["circles"].append(circle.save())
        dump["selected"] = self.selected.text
        dump["state"] = state
        with open(name, 'wb') as handle:
            pickle.dump(dump, handle)

    def load(self, name):
        with open(name, 'rb') as handle:
            dump = pickle.load(handle)
        self.clear()

        for circle in dump["circles"]:
            self.add_node(circle["text"], pos=circle["pos"], final=circle["final"])

        event.post(
            event.Event(Custom_Event.UPDATE_GRAPH_STATE,
            state=dump["state"])
        )

        for circle in dump["circles"]:
            circle_a = self.find_circle_name(circle["text"])
            if circle["text"] == dump["selected"]:
                self.select(circle_a)
            for line in circle["lines"]:
                circle_b = self.find_circle_name(line["circle_b"])
                circle_a.add_line(circle_b, line["text"])
