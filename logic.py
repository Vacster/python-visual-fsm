import pygame, node_manager, input_manager
from element import Circle, Line
from constants import Graph_State
from constants import Custom_Event as ce

graph_state = Graph_State.DFA
EVENT_LIST = [pygame.MOUSEBUTTONUP,
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONDOWN,
    pygame.KEYDOWN,
    ce.RUN_COMMAND,
    ce.UPDATE_GRAPH_STATE]

nodes = node_manager.Node_Manager()
input_m = input_manager.Input_Manager()

def init():
    pygame.event.post(
        pygame.event.Event(ce.UPDATE_GRAPH_MESSAGE, message=graph_state)
    )

    pygame.event.post(
        pygame.event.Event(ce.DRAW_CIRCLES, circles=nodes.circles)
    )

def update():
    global graph_state
    for event in pygame.event.get(EVENT_LIST):
        if event.type == pygame.MOUSEBUTTONDOWN:
            found, element = nodes.find_element_pos(event.pos)
            if event.button == 1 and found is not None:
                nodes.select(found)
                nodes.start_drag(found)
        if event.type == pygame.MOUSEMOTION:
            nodes.drag_element(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            found, element = nodes.find_element_pos(event.pos)
            if event.button == 1:
                if found is None:
                    node_text = input_m.get_message()
                    if nodes.add_node(node_text, pos=event.pos) is not None:
                        input_m.take_input()
            elif event.button == 2:
                if found is not None and element != "line":
                    node_text = input_m.get_message()
                    if not node_text:
                        found.toggle_final()
                    else:
                        if nodes.add_transition(graph_state, found, node_text):
                            input_m.take_input()
            elif event.button == 3:
                if found is not None:
                    nodes.delete_element(found)
                else:
                    nodes.select(None)
            nodes.stop_drag()
        if event.type == pygame.KEYDOWN:
            input_m.take_input(event.unicode)
        if event.type == ce.RUN_COMMAND:
            if nodes.run_command(graph_state, event.message):
                input_m.take_input()
        if event.type == ce.UPDATE_GRAPH_STATE:
            graph_state = event.state
            pygame.event.post(
                pygame.event.Event(ce.UPDATE_GRAPH_MESSAGE,
                message=graph_state)
            )
