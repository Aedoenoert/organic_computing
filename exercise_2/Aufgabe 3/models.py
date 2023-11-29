import math
import numpy
import random
import mesa
from mesa.datacollection import DataCollector
from agents import SimpleAntAgent, SimpleParticle


class SimpleModel(mesa.Model):
    """
    Class for simulating simple ant clustering
    """

    def __init__(self, num_ants, grid_size, ant_step_size, ant_jump_size, init_center, p_particle) -> None:
        """
        Creates a new simple ant clustering model
        :param num_ants: number ant agents
        :param grid_size: size of simulation grid
        :param ant_step_size: amount of cells to be taken one step
        :param ant_jump_size: amount of steps which should be jumped
        :param init_center: initialise all ant agents in the center of the grid
        :param p_particle: probability  for spawning a particle agent for each cell
        """
        super().__init__()
        self.step_size = ant_step_size
        self.jump_size = ant_jump_size
        self.num_ants = num_ants
        self.grid = mesa.space.MultiGrid(grid_size[0], grid_size[1], False)
        self.schedule = mesa.time.RandomActivation(self)
        self.datacollector = DataCollector({
            'Emergenz Partikel x': 'emergence_particle_x',
            'Entropie Partikel x': 'entropy_particle_x',
            'Emergenz Partikel y': 'emergence_particle_y',
            'Entropie Partikel y': 'entropy_particle_y',
            'Emergenz Partikel Nachbarn': 'emergence_particle_n',
            'Entropie Partikel Nachbarn': 'entropy_particle_n',
            'Emergenz Ameisen x': 'emergence_ant_x',
            'Entropie Ameisen x': 'entropy_ant_x',
            'Emergenz Ameisen y': 'emergence_ant_y',
            'Entropie Ameisen y': 'entropy_ant_y',
            'Emergenz Ameisen Tragend': 'emergence_ant_c',
            'Entropie Ameisen Tragend': 'entropy_ant_c'})
        self.particle_list = []
        self.last_particle_entropy_x = 0
        self.last_particle_entropy_y = 0
        self.last_particle_entropy_n = 0
        self.last_ant_entropy_x = 0
        self.last_ant_entropy_y = 0
        self.last_ant_entropy_c = 0

        for i in range(self.num_ants):
            agent = SimpleAntAgent(agent_id=i, model=self, step_size=ant_step_size, jump_size=ant_jump_size)
            self.schedule.add(agent)
            if init_center:
                self.grid.place_agent(agent, (grid_size[0] // 2, grid_size[1] // 2))
            else:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

        for index, (agent, (x, y)) in enumerate(self.grid.coord_iter(), start=self.num_ants):
            if random.random() <= p_particle:
                particle = SimpleParticle(particle_id=index, model=self)
                self.grid.place_agent(particle, (x, y))
                self.particle_list.append(particle)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    @property
    def entropy_particle_x(self):
        p_list = numpy.zeros(50, dtype=int)
        entropy = 0
        for particle in self.particle_list:
            p_list[particle.x] += 1
        p_list = p_list[p_list != 0]
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / len(self.particle_list)) * math.log2(p_list[i] / len(self.particle_list))
        entropy = -entropy
        print(entropy)
        self.last_particle_entropy_x = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_particle_x(self):
        return self.last_particle_entropy_x - self.entropy_particle_x

    @property
    def entropy_particle_y(self):
        p_list = numpy.zeros(50, dtype=int)
        entropy = 0
        for particle in self.particle_list:
            p_list[particle.y] += 1
        p_list = p_list[p_list != 0]
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / len(self.particle_list)) * math.log2(p_list[i] / len(self.particle_list))
        entropy = -entropy
        print(entropy)
        self.last_particle_entropy_y = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_particle_y(self):
        return self.last_particle_entropy_y - self.entropy_particle_y

    @property
    def entropy_particle_n(self):   #entropy particle neighbors
        p_list = numpy.zeros(9, dtype=int)
        entropy = 0
        for particle in self.particle_list:
            p_list[particle.get_num_neighboring_particles()] += 1
        p_list = p_list[p_list != 0]
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / len(self.particle_list)) * math.log2(p_list[i] / len(self.particle_list))
        entropy = -entropy
        print(entropy)
        self.last_particle_entropy_n = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_particle_n(self): #emergence particle neighbors
        return self.last_particle_entropy_n - self.entropy_particle_n

    @property
    def entropy_ant_x(self):
        p_list = numpy.zeros(50, dtype=int)
        entropy = 0
        for agents in self.schedule.agents:
            if isinstance(agents, SimpleAntAgent):
                p_list[agents.pos[0]] += 1
        p_list = p_list[p_list != 0]
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / self.num_ants) * math.log2(p_list[i] / self.num_ants)
        entropy = -entropy
        print(entropy)
        self.last_ant_entropy_x = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_ant_x(self):
        return self.last_ant_entropy_x - self.entropy_ant_x

    @property
    def entropy_ant_y(self):
        p_list = numpy.zeros(50, dtype=int)
        entropy = 0
        for agents in self.schedule.agents:
            if isinstance(agents, SimpleAntAgent):
                p_list[agents.pos[1]] += 1
        p_list = p_list[p_list != 0]
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / self.num_ants) * math.log2(p_list[i] / self.num_ants)
        entropy = -entropy
        print(entropy)
        self.last_ant_entropy_y = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_ant_y(self):
        return self.last_ant_entropy_y - self.entropy_ant_y

    @property
    def entropy_ant_c(self): #entropy ant carrying
        p_list = numpy.zeros(2, dtype=int)
        entropy = 0
        for agents in self.schedule.agents:
            if isinstance(agents, SimpleAntAgent):
                if agents.loaded:
                    p_list[0] += 1
                else:
                    p_list[1] += 1
        p_list = p_list[p_list != 0]
        print(p_list)
        for i in range(0, len(p_list)):
            entropy += (p_list[i] / self.num_ants) * math.log2(p_list[i] / self.num_ants)
        entropy = -entropy
        print(entropy)
        self.last_ant_entropy_c = entropy
        return entropy if (self.schedule.steps > 1) else 0

    @property
    def emergence_ant_c(self): #emergence ant carrying
        return self.last_ant_entropy_c - self.entropy_ant_c