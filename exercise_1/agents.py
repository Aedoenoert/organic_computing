import random
import mesa


class AntAgent(mesa.Agent):
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
        self.carried_particle = None
        self.loaded = False

    def move(self) -> None:
        raise NotImplementedError()


class ParticleAgent(mesa.Agent):
    def __init__(self, particle_id, model) -> None:
        super().__init__(particle_id, model)

    def step(self) -> None:
        pass


class SimpleAntAgent(AntAgent):
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
    def __init__(self, particle_id, model) -> None:
        super().__init__(particle_id, model)


class AdvancedAntAgent(AntAgent):
    def __init__(self, agent_id, model, jump_size) -> None:
        super().__init__(agent_id, model)
        self.loaded = False
        self.carried_particle = None
        self.jump_size = jump_size

    def step(self) -> None:
        position = self.pos
        agents_at_current_pos = self.model.grid.get_cell_list_contents(position)
        occupied = pos_occupied(agents_at_current_pos)
        # print(agents_at_current_pos, occupied)
        if not self.loaded and occupied:
            particles = list(
                filter(lambda a: isinstance(a, (StoneParticle, NutParticle, LeaveParticle)), agents_at_current_pos))
            particle = random.choice(particles)
            if random.random() <= self.model.p_pick(particle):
                self.pick_up(particle)
        elif self.loaded and not occupied:
            if random.random() <= self.model.p_drop(self.carried_particle, position):
                self.drop(position)
        self.move()

    def move(self) -> None:
        neighboring_cells = list(self.model.grid.get_neighborhood(pos=self.pos, moore=True))
        content = self.model.grid.get_cell_list_contents(neighboring_cells)
        ants = list(filter(lambda c: isinstance(c, AdvancedAntAgent), content))
        for ant in ants:
            if neighboring_cells.count(ant.pos):
                neighboring_cells.remove(ant.pos)
        if neighboring_cells:
            self.model.grid.move_agent(self, random.choice(neighboring_cells))


class StoneParticle(ParticleAgent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.shape = 2
        self.weight = 3


class NutParticle(ParticleAgent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.shape = 1
        self.weight = 2


class LeaveParticle(ParticleAgent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.shape = 3
        self.weight = 1


def pos_occupied(agents) -> bool:
    if len(agents) > 1:
        num_ants = sum(1 for agent in agents if isinstance(agent, (SimpleAntAgent, AdvancedAntAgent)))
        if num_ants < len(agents):
            return True
    return False


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, (SimpleAntAgent, AdvancedAntAgent)):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"
        color = "blue"
        if agent.loaded:
            color = "red"
        portrayal["Color"] = color
        return portrayal
    elif isinstance(agent, NutParticle):
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "brown"
        return portrayal
    elif isinstance(agent, LeaveParticle):
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "green"
        return portrayal
    elif isinstance(agent, StoneParticle):
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"
        portrayal["Color"] = "grey"
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


def create_particle_agent(agent_id, agent_type, model) -> ParticleAgent:
    if agent_type == 1:
        return StoneParticle(unique_id=agent_id, model=model)
    elif agent_type == 2:
        return NutParticle(unique_id=agent_id, model=model)
    elif agent_type == 3:
        return LeaveParticle(unique_id=agent_id, model=model)
    else:
        raise Exception('Error during random choice of Agent!')
