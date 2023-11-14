import mesa


class AntAgent(mesa.Agent):
    def __init__(self, agent_id, model: mesa.Model, step_size, jump_size):
        super().__init__(agent_id, model)
        self.loaded = False
        self.carried_particle = None
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

    def pick_up(self, particle: mesa.Agent) -> None:
        self.carried_particle = particle
        self.loaded = True
        self.model.grid.remove_agent(particle)

    def drop(self, position):
        self.model.grid.place_agent(self.carried_particle, position)
        self.carried_particle = None
        self.loaded = False

    def find_empty_pos(self):
        empty_spot = None
        radius = 1
        while empty_spot is None:
            pos_iter = self.model.grid.iter_neighborhood(pos=self.pos, moore=True, include_center=False, radius=radius)
            empty_spots = list(filter(lambda position: self.model.grid.is_cell_empty(position), pos_iter))
            if empty_spots:
                empty_spot = empty_spots[0]
            else:
                if radius >= self.model.grid.width:
                    raise Exception('No empty Slot was found!')
                radius += 1
        return empty_spot


def pos_occupied(agents) -> bool:
    if len(agents) > 1:
        num_ants = sum(1 for agent in agents if isinstance(agent, AntAgent))
        if num_ants < len(agents):
            return True
    return False


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, AntAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        color = "blue"
        if agent.loaded:
            color = "red"
        portrayal["Color"] = color
        return portrayal
    elif isinstance(agent, ParticleAgent):
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "grey"
        return portrayal
    else:
        raise Exception('Agent not supported!')


class ParticleAgent(mesa.Agent):
    def __init__(self, particle_id, model):
        super().__init__(particle_id, model)

    def step(self) -> None:
        pass
