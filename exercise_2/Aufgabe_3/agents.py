import random
import mesa


class AntAgent(mesa.Agent):
    """
    This is the basic AntAgent class where all other ant agents are inherited from
    """
    def __init__(self, agent_id, model) -> None:
        super().__init__(agent_id, model)
        self.loaded = False
        self.carried_particle = None

    def step(self) -> None:
        raise NotImplementedError()

    def pick_up(self, particle) -> None:
        self.carried_particle = particle
        self.loaded = True
        self.model.grid.remove_agent(particle)

    def drop(self, position) -> None:
        self.model.grid.place_agent(self.carried_particle, position)
        self.carried_particle.pos_list.append(position)
        self.carried_particle.x = position[0]
        self.carried_particle.y = position[1]
        self.carried_particle = None
        self.loaded = False

    def move(self) -> None:
        raise NotImplementedError()


class ParticleAgent(mesa.Agent):
    """
    This is the basic ParticleAgent class where all other particle agents are inherited from
    """
    def __init__(self, particle_id, model) -> None:
        super().__init__(particle_id, model)

    def step(self) -> None:
        pass


class SimpleAntAgent(AntAgent):
    """
    This is the Ant Agent class for the simple clustering simulation
    """
    def __init__(self, agent_id, model, step_size, jump_size) -> None:
        super().__init__(agent_id, model)
        self.step_size = step_size
        self.jump_size = jump_size

    def step(self) -> None:
        position = self.pos
        agents_at_current_pos = self.model.grid.get_cell_list_contents(position)
        if not self.loaded and pos_occupied(agents_at_current_pos):
            particle = list(filter(lambda agent: isinstance(agent, ParticleAgent), agents_at_current_pos))[0]
            self.pick_up(particle)
            self.jump()
        elif self.loaded and pos_occupied(agents_at_current_pos):
            self.drop(self.find_empty_pos())
            self.jump()
        else:
            for step in range(self.step_size):
                self.move()

    def jump(self) -> None:
        for jump in range(self.jump_size):
            for step in range(self.step_size):
                self.move()

    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_pos)

    def find_empty_pos(self) -> tuple[int, int]:
        empty_spot = None
        radius = 1
        while empty_spot is None:
            pos_iter = self.model.grid.iter_neighborhood(pos=self.pos, moore=True, include_center=False, radius=radius)
            empty_spots = list(filter(lambda position: self.model.grid.is_cell_empty(position), pos_iter))
            if empty_spots:
                empty_spot = random.choice(empty_spots)
            else:
                if radius >= self.model.grid.width:
                    raise Exception('No empty Slot was found!')
                radius += 1
        return empty_spot


class SimpleParticle(ParticleAgent):
    """
    This is the simple particle agent used in the simple clustering simulation
    """
    def __init__(self, particle_id, model) -> None:
        super().__init__(particle_id, model)
        self.x = 0
        self.y = 0
        self.pos_list = []
        self.pos_list.append(self.pos)

    def get_num_neighboring_particles(self) -> int:
        """
        This function returns the number of neighboring particles
        :return: int
        """
        neighbors = self.model.grid.get_neighbors(pos=(self.x, self.y), moore=True, include_center=False, radius=1)
        neighbors = filter(lambda agent: isinstance(agent, SimpleParticle), neighbors)
        return sum(1 for _ in neighbors)





def pos_occupied(agents) -> bool:
    if len(agents) > 1:
        num_ants = sum(1 for agent in agents if isinstance(agent, (SimpleAntAgent)))
        if num_ants < len(agents):
            return True
    return False


def agent_portrayal(agent):
    """
    This is the agent display function for the grid visualisation used by both clustering models
    :param agent: the agent to be portrayed
    :return: portrayal object
    """
    portrayal = {}
    if isinstance(agent, (SimpleAntAgent)):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        color = "blue"
        if agent.loaded:
            color = "red"
        portrayal["Color"] = color
        return portrayal
    elif isinstance(agent, SimpleParticle):
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "grey"
        return portrayal
    else:
        raise Exception('Agent not supported!', agent)


