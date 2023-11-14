from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Checkbox

from ant_model import AntModel
from agents import agent_portrayal


def main():
    grid_size = (50, 50)
    grid = CanvasGrid(agent_portrayal, grid_size[0], grid_size[1])
    model_params = {
        "num_ants": Slider('Number of ants', value=200, min_value=1, max_value=1000),
        "grid_size": grid_size,
        "ant_step_size": Slider('Step size of ants', value=1, min_value=1, max_value=10),
        "ant_jump_size": Slider('Jump size of ants', value=1, min_value=1, max_value=10),
        "init_center": Checkbox('Init ants in center?', value=False),
        "p_particle": Slider("Probability for particles", value=0.40, min_value=0.01, max_value=0.99, step=0.01)
    }
    server = ModularServer(AntModel, [grid], "AntModel", model_params=model_params)
    server.launch()


if __name__ == '__main__':
    main()
