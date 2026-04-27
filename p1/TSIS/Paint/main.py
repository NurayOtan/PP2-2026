import pygame
from datetime import datetime

WIDTH = 800
HEIGHT = 600
TOOLBAR = 80
CANVAS_H = HEIGHT - TOOLBAR

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)


def get_color(color_name):
    if color_name == "red":
        return (255, 0, 0)
    if color_name == "green":
        return (0, 255, 0)
    if color_name == "blue":
        return (0, 0, 255)
    if color_name == "black":
        return (0, 0, 0)
    return (0, 0, 0)


def canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR


def inside_canvas(pos):
    return 0 <= pos[0] < WIDTH and TOOLBAR <= pos[1] < HEIGHT


def make_rect(start, end):
    x1 = min(start[0], end[0])
    y1 = min(start[1], end[1])
    x2 = max(start[0], end[0])
    y2 = max(start[1], end[1])
    return pygame.Rect(x1, y1, x2 - x1, y2 - y1)


def make_circle(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    radius = int((dx * dx + dy * dy) ** 0.5)
    return start, radius


def draw_square(surface, start, end, color, size):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    side = max(abs(dx), abs(dy))

    if dx < 0:
        x = start[0] - side
    else:
        x = start[0]

    if dy < 0:
        y = start[1] - side
    else:
        y = start[1]

    rect = pygame.Rect(x, y, side, side)
    pygame.draw.rect(surface, color, rect, size)


def draw_right_triangle(surface, start, end, color, size):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    base = abs(x2 - x1)
    height = int(base * 0.866)

    if y2 < y1:
        height = -height

    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = ((x1 + x2) // 2, y1 + height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], size)


def draw_rhombus(surface, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]

    pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, start_pos, new_color):
    width = surface.get_width()
    height = surface.get_height()

    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    stack = [(x, y)]

    while len(stack) > 0:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


def draw_preview(surface, tool, start, end, color, size):
    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif tool == "rectangle":
        pygame.draw.rect(surface, color, make_rect(start, end), size)

    elif tool == "circle":
        center, radius = make_circle(start, end)
        pygame.draw.circle(surface, color, center, radius, size)

    elif tool == "square":
        draw_square(surface, start, end, color, size)

    elif tool == "right_triangle":
        draw_right_triangle(surface, start, end, color, size)

    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, start, end, color, size)

    elif tool == "rhombus":
        draw_rhombus(surface, start, end, color, size)


def draw_ui(screen, font, tool, color_name, brush_size):
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR))
    pygame.draw.line(screen, (150, 150, 150), (0, TOOLBAR), (WIDTH, TOOLBAR), 2)

    text1 = "Colors: R red | G green | B blue | K black"
    text2 = "Tools: P pencil | E eraser | L line | C circle | T rectangle | S square"
    text3 = "Y right triangle | U equilateral triangle | H rhombus | F fill | A text"
    text4 = "Size: 1 small | 2 medium | 3 large | Ctrl+S save | X clear | Esc exit"
    text5 = "Current: " + tool + " | color: " + color_name + " | size: " + str(brush_size)

    screen.blit(font.render(text1, True, BLACK), (10, 5))
    screen.blit(font.render(text2, True, BLACK), (10, 20))
    screen.blit(font.render(text3, True, BLACK), (10, 35))
    screen.blit(font.render(text4, True, BLACK), (10, 50))
    screen.blit(font.render(text5, True, BLACK), (10, 65))


def save_canvas(canvas):
    name = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, name)
    print("Saved:", name)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Paint")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 14)
    text_font = pygame.font.SysFont("Arial", 24)

    canvas = pygame.Surface((WIDTH, CANVAS_H))
    canvas.fill(WHITE)

    tool = "pencil"
    color_name = "blue"
    brush_size = 5

    drawing = False
    start_pos = None
    current_pos = None
    last_pos = None

    text_active = False
    text_pos = None
    text_value = ""

    running = True

    while running:
        ctrl = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]
        alt = pygame.key.get_pressed()[pygame.K_LALT] or pygame.key.get_pressed()[pygame.K_RALT]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl:
                    running = False

                elif event.key == pygame.K_F4 and alt:
                    running = False

                elif event.key == pygame.K_s and ctrl:
                    save_canvas(canvas)

                elif text_active:
                    if event.key == pygame.K_RETURN:
                        color = get_color(color_name)
                        rendered = text_font.render(text_value, True, color)
                        canvas.blit(rendered, text_pos)
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]

                    else:
                        text_value += event.unicode

                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_r:
                        color_name = "red"
                    elif event.key == pygame.K_g:
                        color_name = "green"
                    elif event.key == pygame.K_b:
                        color_name = "blue"
                    elif event.key == pygame.K_k:
                        color_name = "black"

                    elif event.key == pygame.K_p:
                        tool = "pencil"
                    elif event.key == pygame.K_e:
                        tool = "eraser"
                    elif event.key == pygame.K_l:
                        tool = "line"
                    elif event.key == pygame.K_c:
                        tool = "circle"
                    elif event.key == pygame.K_t:
                        tool = "rectangle"
                    elif event.key == pygame.K_s:
                        tool = "square"
                    elif event.key == pygame.K_y:
                        tool = "right_triangle"
                    elif event.key == pygame.K_u:
                        tool = "equilateral_triangle"
                    elif event.key == pygame.K_h:
                        tool = "rhombus"
                    elif event.key == pygame.K_f:
                        tool = "fill"
                    elif event.key == pygame.K_a:
                        tool = "text"

                    elif event.key == pygame.K_1:
                        brush_size = 2
                    elif event.key == pygame.K_2:
                        brush_size = 5
                    elif event.key == pygame.K_3:
                        brush_size = 10

                    elif event.key == pygame.K_x:
                        canvas.fill(WHITE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and inside_canvas(event.pos):
                    pos = canvas_pos(event.pos)

                    if tool == "fill":
                        flood_fill(canvas, pos, get_color(color_name))

                    elif tool == "text":
                        text_active = True
                        text_pos = pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = pos
                        current_pos = pos
                        last_pos = pos

            elif event.type == pygame.MOUSEMOTION:
                if drawing and inside_canvas(event.pos):
                    current_pos = canvas_pos(event.pos)

                    if tool == "pencil" or tool == "eraser":
                        if tool == "eraser":
                            color = WHITE
                        else:
                            color = get_color(color_name)

                        pygame.draw.line(canvas, color, last_pos, current_pos, brush_size)
                        pygame.draw.circle(canvas, color, current_pos, brush_size // 2)
                        last_pos = current_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False

                    if inside_canvas(event.pos):
                        end_pos = canvas_pos(event.pos)
                        color = get_color(color_name)

                        if tool != "pencil" and tool != "eraser":
                            draw_preview(canvas, tool, start_pos, end_pos, color, brush_size)

                    start_pos = None
                    current_pos = None
                    last_pos = None

        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR))

        if drawing and start_pos is not None and current_pos is not None:
            if tool != "pencil" and tool != "eraser":
                temp = canvas.copy()
                draw_preview(temp, tool, start_pos, current_pos, get_color(color_name), brush_size)
                screen.blit(temp, (0, TOOLBAR))

        if text_active:
            color = get_color(color_name)
            rendered = text_font.render(text_value + "|", True, color)
            screen.blit(rendered, (text_pos[0], text_pos[1] + TOOLBAR))

        draw_ui(screen, font, tool, color_name, brush_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()