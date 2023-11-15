from mesa_viz_tornado.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Checkbox

from models import SimpleModel, AdvancedModel
from agents import agent_portrayal


def main(simple):
    grid_size = (50, 50)
    grid = CanvasGrid(agent_portrayal, grid_size[0], grid_size[1])
    model_params = {
        "grid_size": grid_size,
        "init_center": Checkbox('centralized initialisation?', value=False),
        "p_particle": Slider("Probability for particles", value=0.25, min_value=0.01, max_value=0.99, step=0.01),
        "num_ants": Slider('Number of ants', value=200, min_value=1, max_value=1000, step=10),
        "ant_jump_size": Slider('Jump size of ants', value=3, min_value=1, max_value=10)
    }
    if simple:
        simple_clustering(grid, model_params)
    else:
        advanced_clustering(grid, model_params)


def simple_clustering(grid, model_params):
    model_params["ant_step_size"] = Slider('Step size of ants', value=1, min_value=1, max_value=10)
    server = ModularServer(SimpleModel, [grid], "SimpleAntModel", model_params=model_params)
    server.launch()


def advanced_clustering(grid, model_params):
    model_params["alpha"] = Slider('scale factor for distance measuring', value=0.5, min_value=0, max_value=1, step=0.1)
    server = ModularServer(AdvancedModel, [grid], "AdvancedAntModel", model_params=model_params)
    server.launch()


if __name__ == '__main__':
    user_input = input('Enter clustering type, available are: simple, advanced\nAwaiting input:')
    if user_input == 'simple':
        main(True)
    elif user_input == 'advanced':
        main(False)
    else:
        print('Invalid input!')
