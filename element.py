import pygame, time, math
from constants import Color, Token, Pivot

pygame.font.init()

class Element:

    def __init__(self):
        self.RADIUS = 50
        self.FINAL_RADIUS = 75

    def draw(self, screen, selected):
        raise NotImplementedError("Draw not implemented")

    def is_clicked(self, pos):
        raise NotImplementedError("Is_clicked not implemented")

    def edit(self, test):
        raise NotImplementedError("Edit not implemented")

    def update_pos(self, pos):
        raise NotImplementedError("Update not implemented")

    def toggle_selected(self):
        raise NotImplementedError("Toggle_Selected not implemented")

class Circle(Element):

    def __init__(self, text, pos=(500,500), lines=None, color=Color.BLUE,
    final=False):
        super().__init__()
        self.text = text
        self.pos = pos
        self.lines = lines if lines is not None else [] #Prevents sharing
        self.color = color
        self.final = final
        self.font = pygame.font.SysFont("monospace", 30)
        self.rendered_font = self.font.render(text, 1, Color.WHITE)

    def update_pos(self, pos):
        self.pos = pos

    def is_clicked(self, pos):
        return math.sqrt(math.pow(pos[0] - self.pos[0], 2) +
                            math.pow(pos[1] - self.pos[1], 2)) < self.RADIUS

    def toggle_final(self, val=None):
        self.final = not self.final if val is None else val

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.RADIUS)
        if self.final:
            pygame.draw.circle(screen, self.color, self.pos, self.FINAL_RADIUS, 10)

        screen.blit(self.rendered_font, (self.pos[0] - self.rendered_font.get_width()/2,
                    self.pos[1] - self.rendered_font.get_height()/2))

    def edit(self, text):
        if self.text == text:
            raise ValueError("Circle name already exists.")
        self.text = text
        self.rendered_font = self.font.render(text, 1, Color.WHITE)

    def is_final(self):
        if self.final:
            return True
        for line in self.lines:
            for transition in line.text.split(Token.AND):
                if transition == Token.EPSILON:
                    if line.circle_b.is_final():
                        return True
        return False

    def toggle_selected(self):
        self.color = Color.RED if self.color == Color.BLUE else Color.BLUE

    def save(self):
        return {"text": self.text, "pos": self.pos, "final": self.final,
                "lines": [l.save() for l in self.lines]}

    def add_line(self, circle_b, text):
        self.lines.append(Line(self, circle_b, text))

    def has_transition(self, text, circle_b=None):
        for transition in self.lines:
            if circle_b is not None:
                if transition.circle_b is circle_b and transition.text == text:
                    return transition
            else:
                if transition.text == text:
                    return transition
        return None

class Line(Element):
    def __init__(self, circle_a, circle_b, text):
        super().__init__()
        self.circle_a = circle_a
        self.circle_b = circle_b
        self.text = text
        self.color = Color.LIGHT_GREY
        self.font = pygame.font.SysFont("monospace", 30)
        self.rendered_font = self.font.render(text, 1,  Color.WHITE)
        self.arrow_size = 25 #TODO: constant
        self.radians_dif = 2 * math.pi / 3 #TODO: constant
        self.CLICK_RANGE = 25

    def draw(self, screen):
        if self.circle_a != self.circle_b:
            start = self.circle_a.pos
            end_c = self.circle_b.pos

            pygame.draw.line(screen, self.color , start, end_c, 10)

            x = end_c[0] - start[0]
            y = end_c[1] - start[1]

            x = 1 if x == 0 else x
            y = 1 if y == 0 else y

            ratio = (100 if self.circle_b.final else 75) / math.sqrt(x * x + y * y)
            end = (end_c[0] - x * ratio, end_c[1] - y * ratio)

            rotation = math.atan2(start[1]-end[1],
                end[0]-start[0]) + (math.pi / 2)


            pygame.draw.polygon(screen, self.color,
            ((end[0] + self.arrow_size * math.sin(rotation),
            end[1] + self.arrow_size * math.cos(rotation)),
            (end[0] + self.arrow_size * math.sin(rotation - self.radians_dif),
            end[1] + self.arrow_size * math.cos(rotation - self.radians_dif)),
            (end[0] + self.arrow_size * math.sin(rotation + self.radians_dif),
            end[1] + self.arrow_size * math.cos(rotation + self.radians_dif))))

            screen.blit(self.rendered_font, (end[0] - self.arrow_size * math.sin(rotation),
            end[1] - self.arrow_size * math.cos(rotation)))
        else:
            x = self.circle_a.pos[0] - (self.rendered_font.get_width()/2)
            y = self.circle_a.pos[1] - (self.RADIUS * 2) - 30

            pygame.draw.circle(screen, self.color,
                (self.circle_a.pos[0],
                self.circle_a.pos[1] - self.RADIUS),
                self.RADIUS, 10)
            screen.blit(self.rendered_font, (x, y))

    def edit(self, text):
        self.text = text
        self.rendered_font = self.font.render(text, 1, Color.WHITE)

    #This seems very wrong but helps hierarchy
    def update_pos(self, pos):
        pass
    def toggle_final(self, val=None):
        pass

    def is_clicked(self, pos):
        if self.circle_a is not self.circle_b:
            dxL = self.circle_b.pos[0] - self.circle_a.pos[0]
            dyL = self.circle_b.pos[1] - self.circle_a.pos[1]
            dxP = pos[0] - self.circle_a.pos[0]
            dyP = pos[1] - self.circle_a.pos[1]

            squareLen = dxL * dxL + dyL * dyL
            dotProd   = dxP * dxL + dyP * dyL
            crossProd = dyP * dxL - dxP * dyL

            distance = math.fabs(crossProd) / math.sqrt(squareLen)
            return (distance <= self.CLICK_RANGE and dotProd >= 0 and
                    dotProd <= squareLen)
        else:
            return math.sqrt(((pos[0] - self.circle_a.pos[0]) ** 2) + \
            ((pos[1] - (self.circle_a.pos[1] - self.RADIUS)) ** 2)) < self.RADIUS

    #TODO: Too long
    def toggle_selected(self):
        self.color = Color.RED if self.color == Color.LIGHT_GREY else Color.LIGHT_GREY

    def save(self):
        return {"circle_b": self.circle_b.text, "text": self.text}

class Message:
    def __init__(self, text="", color=Color.BLACK, size=30,
    pivot=(Pivot.LEFT, Pivot.TOP)):
        self.text = text
        self.font = pygame.font.SysFont("monospace", size)
        self.label = self.font.render(text, 1, Color.BLACK)
        self.pivot = pivot

    def update(self, text, color=Color.BLACK):
        self.label = self.font.render(text, 1, color)

    def draw(self, screen, pos=(0,0)):
        screen.blit(self.label,
            (pos[0] - (self.label.get_width() * self.pivot[0]),
            pos[1] - (self.label.get_height() * self.pivot[1]))) #Top-left corner

class Temp_Message(Message):
     #There has to be a better way for this constructor
    def __init__(self, text="", color=Color.BLACK, size=30,
    pivot=(Pivot.LEFT, Pivot.TOP)):
        super().__init__(size=size, pivot=pivot)
        self.timer = 0
        self.time_delay = 3

    def update(self, text, time_delay=3):
        self.time_delay = time_delay
        self.timer = time.clock()
        self.label = self.font.render(text, 1, Color.BLACK)

    def draw(self, screen, pos):
        if self.timer > (time.clock() - self.time_delay):
            super().draw(screen, pos)
