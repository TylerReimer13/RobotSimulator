import numpy as np
from math import sin, cos, atan2
import random

DT = .1


class Robot:
    def __init__(self, pos, vel, acc, heading):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.heading = heading
        self.measured_pos = pos

        self.color = 'r'
        self.icon = 'X'

        self.rotation_matrix = self.rotate(heading)
        self.sensor = Sensor()
        self.laser = LaserScanner()
        self.controller = RobotController()

        self.landmarks_spotted = []

    def rotate(self, theta):
        theta *= .01745
        self.rotation_matrix = np.array((
                                        (cos(theta), -sin(theta)),
                                        (sin(theta), cos(theta) ),
                                        ))
        return self.rotation_matrix

    def update(self, time, landmarks=None):
        _, heading = self.controller.straight_line(time)
        self.rotate(heading)
        #self.vel += self.acc*DT
        self.pos += self.rotation_matrix.dot(self.vel*DT)
        self.measured_pos = self.sensor.GPS(self.pos)
        self.sense(self.pos, landmarks, time)

    @property
    def getPos(self):
        return self.pos.copy()

    @property
    def getVel(self):
        return self.vel.copy()

    @property
    def get_measured_pos(self):
        return self.measured_pos.copy()

    def sense(self, pos, landmarks, time):
        self.laser.scan(pos, landmarks, time)
        self.landmarks_spotted = self.laser.landmarks_detected.copy()


class Sensor:
    def __init__(self):
        pass

    def white_noise(self):
        mean = 0
        std = .2
        num_samples = 1
        noise_sample = np.random.normal(mean, std, size=num_samples)
        noise_array = np.array(noise_sample)

        return noise_array

    def GPS(self, pos):
        rand_angle = random.uniform(0., 2*np.pi)
        noise_mag = self.white_noise()
        noise_vec = np.array([noise_mag*cos(rand_angle), noise_mag*sin(rand_angle)])
        noise_vec.shape = (2, 1)
        return pos + self.white_noise()
    

class LaserScanner:
    def __init__(self):
        self.scan_radius = 3.75
        self.landmarks_detected = []
        self.landmark_dict = {}

    def scan(self, pos, landmarks, time):
        for landmark in landmarks:
            delt_x = (pos[0]-landmark.x)
            delt_y = (pos[1]-landmark.y)
            rng = np.sqrt(delt_x**2 + delt_y**2)
            angle = atan2(-delt_y, -delt_x)
            angle *= 57.296
            landmark.spotted = False

            if landmark.id not in self.landmark_dict.keys():
                self.landmark_dict[landmark.id] = []

            if rng <= self.scan_radius:
                if landmark.id not in self.landmarks_detected:
                    self.landmarks_detected.append(landmark.id)
                """
                landmark.info_dict['time'].append(time)
                landmark.info_dict['angle'].append(angle)
                landmark.info_dict['range'].append(round(float(rng), 3))
                self.landmark_dict[landmark.id] = landmark.info_dict
                """
                info_dict = {
                             'time': time,
                             'angle': round(angle, 3),
                             'range': round(float(rng), 3)
                             }
                self.landmark_dict[landmark.id].append(info_dict)
                landmark.spotted = True


class RobotController:
    def __init__(self):
        self.cmd_inputs = []

    def straight_line(self, time):
        vel = 3.5
        hdg = 0.
        if time >= 1.6:
            hdg = -45.
        if time >= 3.2:
            hdg = 45
        if time >= 4.9:
            hdg = 90.

        info_dict = {
                     'time': time,
                     'velocity': vel,
                     'heading': hdg
                     }
        self.cmd_inputs.append(info_dict)
        return vel, hdg
