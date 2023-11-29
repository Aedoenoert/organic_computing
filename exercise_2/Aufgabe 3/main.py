from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Checkbox

from models import SimpleModel
from agents import agent_portrayal


def main():
    grid_size = (50, 50)
    grid = CanvasGrid(agent_portrayal, grid_size[0], grid_size[1])
    visualization = ChartModule([{"Label": "Emergenz Partikel x", "Color": "Black"},
                                 {"Label": "Entropie Partikel x", "Color": "Black"},
                                 {"Label": "Emergenz Partikel y", "Color": "Green"},
                                 {"Label": "Entropie Partikel y", "Color": "Green"},
                                 {"Label": "Emergenz Partikel Nachbarn", "Color": "Orange"},
                                 {"Label": "Entropie Partikel Nachbarn", "Color": "Orange"},
                                 {"Label": "Emergenz Ameisen x", "Color": "Red"},
                                 {"Label": "Entropie Ameisen x", "Color": "Red"},
                                 {"Label": "Emergenz Ameisen y", "Color": "Blue"},
                                 {"Label": "Entropie Ameisen y", "Color": "Blue"},
                                 {"Label": "Emergenz Ameisen Tragend", "Color": "Pink"},
                                 {"Label": "Entropie Ameisen Tragend", "Color": "Pink"},
                                 ])
    model_params = {
        "grid_size": grid_size,
        "init_center": Checkbox('centralized initialisation?', value=False),
        "p_particle": Slider("Probability for particles", value=0.25, min_value=0.01, max_value=0.99, step=0.01),
        "num_ants": Slider('Number of ants', value=200, min_value=1, max_value=1000, step=10),
        "ant_jump_size": Slider('Jump size of ants', value=3, min_value=1, max_value=10)
    }
    simple_clustering(grid, visualization, model_params)


def simple_clustering(grid, visualization, model_params):
    model_params["ant_step_size"] = Slider('Step size of ants', value=1, min_value=1, max_value=10)
    server = ModularServer(SimpleModel, [grid, visualization], "SimpleAntModel", model_params=model_params)
    server.launch()



if __name__ == '__main__':
    main()
