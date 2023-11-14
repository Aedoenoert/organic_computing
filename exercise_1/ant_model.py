import random

import mesa
from agents import AntAgent, ParticleAgent


class AntModel(mesa.Model):
    def __init__(self, num_ants, grid_size, ant_step_size, ant_jump_size, init_center, p_particle):
        super().__init__()
        self.step_size = ant_step_size
        self.jump_size = ant_jump_size
        self.num_ants = num_ants
        self.grid = mesa.space.MultiGrid(grid_size[0], grid_size[1], False)
        self.schedule = mesa.time.RandomActivation(self)

        for i in range(self.num_ants):
            agent = AntAgent(agent_id=i, model=self, step_size=ant_step_size, jump_size=ant_jump_size)
            self.schedule.add(agent)
            if init_center:
                self.grid.place_agent(agent, (grid_size[0] // 2, grid_size[1] // 2))
            else:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

        for j in range(self.grid.width * self.grid.height):
            if random.random() <= p_particle:
                particle = ParticleAgent(particle_id=self.num_ants + j, model=self)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(particle, (x, y))

    def step(self):
        self.schedule.step()
