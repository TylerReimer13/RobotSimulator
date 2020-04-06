import numpy as np
import random


class Landmark:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.color = 'g'
        self.icon = 'P'
        self.spotted = False
        self.info_dict = {
                           'time': [],
                           'angle': [],
                           'range': []
                          }


class Map:
    def __init__(self, x_dim, y_dim):
        self.x_dim = x_dim
        self.y_dim = y_dim


class Particle:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.icon = '.'
        self.color = 'k'


class ParticleFilter:
    def __init__(self, num_particles):
        self.num_particles = int(num_particles)
        self.particles = []

    def place_particles(self, x_dims, y_dims):
        for i in range(self.num_particles):
            x_pos = random.uniform(x_dims[0], x_dims[1])
            y_pos = random.uniform(y_dims[0], y_dims[1])
            weight = 1/self.num_particles
            self.particles.append(Particle(x_pos, y_pos, weight))

        return self.particles

    def resample(self, time, x_dims, y_dims):
        """
        new_particles = []
        if round(time % .3, 1) == 0.:
            for particle in self.particles:
                particle.x = random.uniform(x_dims[0], x_dims[1])
                particle.y = random.uniform(y_dims[0], y_dims[1])
                new_particles.append(particle)
            self.particles = new_particles
        """
        pass
