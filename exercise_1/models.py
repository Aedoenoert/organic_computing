import math
import random
import mesa
from agents import SimpleAntAgent, SimpleParticle, create_particle_agent, AdvancedAntAgent


class SimpleModel(mesa.Model):
    """
    Class for simulating simple ant clustering
    """

    def __init__(self, num_ants, grid_size, ant_step_size, ant_jump_size, init_center, p_particle):
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

    def step(self):
        self.schedule.step()


def calc_euclidean_distance(particle_1, particle_2):
    return math.sqrt((particle_1.shape - particle_2.shape) ** 2 + (particle_1.weight - particle_2.weight) ** 2)


class AdvancedModel(mesa.Model):
    """
    Class for simulating advanced ant clustering
    """

    def __init__(self, num_ants, grid_size, init_center, p_particle, ant_jump_size, k_p=0.1, k_m=0.3,
                 alpha=0.5,
                 nhr=1):
        """
        Create an advanced ant clustering model.
        :param num_ants: number of ant agents
        :param grid_size: size of the simulation grid
        :param init_center: initialise all ant agents in the center of the grid
        :param p_particle: probability  for spawning a particle agent for each cell
        :param ant_jump_size: defines the radius when moving
        :param k_p: k+ value for pickup probability, defaults to 0.1
        :param k_m: k- value for drop probability, defaults to 0.3
        :param alpha: scaling for distance, must be in (0,1] defaults to 0.5
        :param nhr: neighborhood radius for LF-Similarity calc, 1 -> 9 neighbors,2 -> 25 neighbors, ... defaults to 1
        """
        super().__init__()
        if nhr >= grid_size[0] // 2 >= grid_size[1] // 2 or nhr >= grid_size[1] // 2 >= grid_size[0] // 2:
            raise Exception("Neighborhood radius too big!")

        self.num_agents = num_ants
        self.k_plus = k_p
        self.k_minus = k_m
        self.alpha = alpha
        self.radius = nhr
        self.grid = mesa.space.MultiGrid(grid_size[0], grid_size[1], True)
        self.schedule = mesa.time.RandomActivation(self)

        for i in range(self.num_agents):
            agent = AdvancedAntAgent(agent_id=i, model=self, jump_size=ant_jump_size)
            self.schedule.add(agent)
            if init_center:
                self.grid.place_agent(agent, (grid_size[0] // 2, grid_size[1] // 2))
            else:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

        for index, (agent, (x, y)) in enumerate(self.grid.coord_iter(), start=self.num_agents):
            if random.random() <= p_particle:
                particle_agent = create_particle_agent(agent_id=index, agent_type=random.choice([1, 2, 3]), model=self)
                self.grid.place_agent(particle_agent, (x, y))

    def p_pick(self, particle):
        return (self.k_plus / (self.k_plus + self.lf_neighborhood_sim(particle, particle.pos))) ** 2

    def p_drop(self, particle, pos):
        return (self.lf_neighborhood_sim(particle, pos) / (self.k_minus + self.lf_neighborhood_sim(particle, pos))) ** 2

    def lf_neighborhood_sim(self, particle, position):
        neighbors = self.grid.get_neighbors(pos=position, moore=True, include_center=True, radius=self.radius)
        neighbors = filter(lambda agent: not isinstance(agent, AdvancedAntAgent), neighbors)
        similarity = 0
        for neighbor in neighbors:
            similarity += 1 - calc_euclidean_distance(particle_1=neighbor, particle_2=particle) / self.alpha
        similarity /= (self.radius * 2 + 1) ** 2
        return max(0, similarity)

    def step(self):
        self.schedule.step()
