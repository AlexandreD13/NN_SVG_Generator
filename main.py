"""
Author:         Alexandre Desfosses
Creation date:  2023-07-14
Documentation:
References:
"""

from flask import Flask, render_template
from NN_SVG_Generator import svg

import argparse

# Setting up the application
app = Flask(__name__)


def cli(argv=None):
    """
    Description...

    :param argv: Injected CLI arguments.
    :return: None
    """

    parser = argparse.ArgumentParser(prog="NN_SVG_Generator",
                                     description="A neural network .svg generator")

    parser.add_argument("-f", "--filename", required=True, type=str,
                        nargs=1, help="The name of the .svg to create")

    parser.add_argument("-r", "--resolution", required=True, type=str,
                        nargs=1, help="The resolution of the .svg file")

    parser.add_argument("-nodes", "--nodes_in_layers", required=True, type=str,
                        nargs=1, help="Nb. of nodes in each layers (input, hidden, output)")

    parser.add_argument("-hidden", "--nb_hidden_layers", required=True, type=str,
                        nargs=1, help="Nb. of nodes in hidden layers")

    parser.add_argument("-colors", required=True, type=str,
                        nargs=1, help="Color of each layer (input, hidden, output, edge)")

    args = parser.parse_args(argv)

    filename = args.filename[0]
    resolution = args.resolution[0]
    nodes_in_layers = args.nodes_in_layers[0]
    nb_hidden_layers = int(args.nb_hidden_layers[0])
    colors = args.colors[0]

    svg.create_svg(filename, resolution, nodes_in_layers, nb_hidden_layers, colors)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    cli()
    app.run(debug=True)
