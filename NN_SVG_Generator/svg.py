"""
Author:         Alexandre Desfosses
Creation date:  2023-07-14
Documentation:
References:
Information:    At a resolution of 2000 x 1200 pixels :
                    - nb_hidden_layers = maximum 6
                    - nb_nodes = maximum 16

                At a resolution of 4000 x 2400 pixels :
                    - nb_hidden_layers = maximum 10
                    - nb_nodes = maximum 24
"""

from svgwrite import Drawing, px

PADDING: int = 50
CAPTION_HEIGHT: int = 100
NODE_VERTICAL_SPACING: int = 20
NODE_STROKE_WIDTH: int = 2

layers_xpos: list = []
input_ypos: list = []
output_ypos: list = []
hidden_ypos: list = []


def create_svg(name: str, resolution: str, nodes_in_layers: str, nb_hidden_layers: int, colors: str):
    SVG_WIDTH: int = int(resolution.split("x")[0])
    SVG_HEIGHT: int = int(resolution.split("x")[1])

    NODES_IN_INPUT: int = int(nodes_in_layers.split(" ")[0])
    NODES_IN_HIDDEN: int = int(nodes_in_layers.split(" ")[1])
    NODES_IN_OUTPUT: int = int(nodes_in_layers.split(" ")[2])

    INPUT_NODE_COLOR: str = colors.split(" ")[0].lower()
    OUTPUT_NODE_COLOR: str = colors.split(" ")[1].lower()
    HIDDEN_NODE_COLOR: str = colors.split(" ")[2].lower()
    EDGE_COLOR: str = colors.split(" ")[3].lower()

    layer_sizes = [NODES_IN_INPUT]
    for layer in range(0, nb_hidden_layers):
        layer_sizes.append(NODES_IN_HIDDEN)
    layer_sizes.append(NODES_IN_OUTPUT)

    NB_LAYERS_TOTAL: int = 1 + nb_hidden_layers + 1

    # Find an appropriate node radius
    node_radius: list = []
    for layer in layer_sizes:
        node_radius.append(min(find_node_radius(layer, SVG_HEIGHT), 50))

    # Draw
    drawing = Drawing(filename=f"static/{name}.svg", debug=True, size=(f"{SVG_WIDTH}px", f"{SVG_HEIGHT}px"))
    write_captions(drawing, (SVG_WIDTH, SVG_HEIGHT), NB_LAYERS_TOTAL)
    find_io_ypos(node_radius[0], "i", SVG_HEIGHT, NODES_IN_INPUT)
    find_hidden_ypos(node_radius[1:-1], SVG_HEIGHT, NODES_IN_HIDDEN, nb_hidden_layers)
    find_io_ypos(node_radius[-1], "o", SVG_HEIGHT, NODES_IN_OUTPUT)
    connect_layers(drawing, EDGE_COLOR)
    draw_io_layer(drawing, node_radius[0], "i", NODES_IN_INPUT, INPUT_NODE_COLOR)
    draw_hidden_layers(drawing, node_radius[1:-1], NODES_IN_HIDDEN, nb_hidden_layers, HIDDEN_NODE_COLOR)
    draw_io_layer(drawing, node_radius[-1], "o", NODES_IN_OUTPUT, OUTPUT_NODE_COLOR)

    drawing.save()


def find_node_radius(nb_node_largest_layer, height):
    return (height - (PADDING * 2) - CAPTION_HEIGHT - (nb_node_largest_layer - 2) * NODE_VERTICAL_SPACING) / \
        (nb_node_largest_layer * 2)


def write_captions(drawing, resolution: tuple, nb_layers_total: int):
    """

    :param resolution:
    :param drawing:
    :return:
    """

    horizontal_div_width: float = (resolution[0] - (PADDING * 2)) / nb_layers_total
    text = drawing.add(drawing.g(font_size=32, fill="white"))
    for i in range(0, nb_layers_total):
        layers_xpos.append(PADDING + (horizontal_div_width / 2) + horizontal_div_width * i)
        if i == 0:
            text.add(drawing.text("Input Layer", (layers_xpos[i] - len("Input Layer") * 7, resolution[1] - PADDING)))
        elif i == nb_layers_total - 1:
            text.add(drawing.text("Output Layer", (layers_xpos[i] - len("Output Layer") * 7, resolution[1] - PADDING)))
        else:
            text.add(
                drawing.text(f"Hidden Layer #{i}", (layers_xpos[i] - len("Hidden Layer") * 9, resolution[1] - PADDING)))


def find_io_ypos(node_radius, input_output, height: int, nb_node_in_layer: int):
    """

    :param height:
    :param node_radius:
    :param input_output:
    :return:
    """

    global layer_list
    if input_output == "i":
        layer_list = input_ypos
    elif input_output == "o":
        layer_list = output_ypos

    for i in range(0, nb_node_in_layer):
        layer_list.append(PADDING + node_radius + (node_radius + NODE_VERTICAL_SPACING + node_radius) * i)
    remaining_space = (height - 2 * PADDING - CAPTION_HEIGHT - (layer_list[-1] + node_radius)) / 2

    for index in range(0, len(layer_list)):
        layer_list[index] += remaining_space


def draw_io_layer(drawing, node_radius, input_output, nb_node_in_layer: int, node_color: str):
    """

    :param drawing:
    :param node_radius:
    :param input_output:
    :return:
    """

    global index_x, layer_list
    if input_output == "i":
        layer_list = input_ypos
        index_x = 0
    elif input_output == "o":
        layer_list = output_ypos
        index_x = -1

    shapes = drawing.add(drawing.g(id="shapes", fill=node_color))

    for i in range(0, nb_node_in_layer):
        circle = drawing.circle(center=(layers_xpos[index_x], layer_list[i]),
                                r=f"{node_radius}px", stroke=node_color,
                                stroke_width=f"{NODE_STROKE_WIDTH}px")
        shapes.add(circle)


def find_hidden_ypos(node_radius, height: int, nb_node_in_layer: int, nb_hidden_layers: int):
    """

    :param node_radius:
    :return:
    """

    for layer_index in range(0, nb_hidden_layers):
        layer = []
        for i in range(0, nb_node_in_layer):
            layer.append(PADDING + node_radius[layer_index] +
                         (node_radius[layer_index] + NODE_VERTICAL_SPACING +
                          node_radius[layer_index]) * i)
        remaining_space = (height - 2 * PADDING - CAPTION_HEIGHT - (layer[-1] + node_radius[0])) / 2

        for index in range(0, len(layer)):
            layer[index] += remaining_space

        hidden_ypos.append(layer)


def draw_hidden_layers(drawing, node_radius, nb_node_in_layer: int, nb_hidden_layers: int, node_color: str):
    """

    :param drawing:
    :param node_radius:
    :return:
    """

    shapes = drawing.add(drawing.g(id="shapes", fill=node_color))
    for layer_index in range(0, nb_hidden_layers):
        for i in range(0, nb_node_in_layer):
            circle = drawing.circle(center=(layers_xpos[layer_index + 1], hidden_ypos[layer_index][i]),
                                    r=f"{node_radius[layer_index]}px", stroke=node_color,
                                    stroke_width=f"{NODE_STROKE_WIDTH}px")
            shapes.add(circle)


def connect_layers(drawing, edge_color):
    y_pos = [input_ypos]
    for layer in hidden_ypos:
        y_pos.append(layer)
    y_pos.append(output_ypos)

    edge = drawing.add(drawing.g(id="edge", stroke=edge_color))
    for x in range(len(layers_xpos) - 1):
        for y1 in range(len(y_pos[x])):
            for y2 in range(len(y_pos[x + 1])):
                edge.add(drawing.line(start=(layers_xpos[x] * px, y_pos[x][y1] * px),
                                      end=(layers_xpos[x + 1] * px, y_pos[x + 1][y2] * px)))
