import matplotlib.pyplot as plt
from math import sin, cos
import numpy as np
from robot import Robot
from Environment import Landmark, ParticleFilter
from avi_playback import generate_avi


def write_dict_to_txt(input_dict):
    output = open(log_path + 'laser_info.txt', 'w')
    for key, value in input_dict.items():
        output.write('LANDMARK ' + str(key) + ': ')
        output.write(str(value))
        output.write("\n")
        output.write("\n")
    output.close()


def write_list_to_txt(input_list):
    output = open(log_path + 'input_info.txt', 'w')
    for info in input_list:
        output.write('[')
        output.write(str(info))
        output.write('], ')
    output.close()


def plot_at_end(counter):
    if counter >= SIM_END:
        plt.plot(x_hist, y_hist, scalex=True, scaley=True, color=my_robot.color, marker=my_robot.icon)
        plt.plot(x_meas, y_meas, scalex=True, scaley=True, color='b', marker='x')  # noisy position
        plt.plot(lm1.x, lm1.y, scalex=True, scaley=True, color=lm1.color, marker=lm1.icon)
        plt.show()
        return True


def plot_in_line(counter, image_counter, pos):
    cur_time = round(counter * .1, 3)
    plt.axis([x_dims[0], x_dims[1], y_dims[0], y_dims[1]])
    plt.text(20., 9.5, 'TIME: ' + str(cur_time))
    P_Filter.resample(time, x_dims, y_dims)
    if counter <= 2:
        plt.plot(x_hist[:], y_hist[:], color=my_robot.color, marker=my_robot.icon)

    else:
        plt.plot(x_hist[-5:-1], y_hist[-5:-1], color=my_robot.color, marker=my_robot.icon)

    for lm in landmarks:
        plt.plot(lm.x, lm.y, scalex=True, scaley=True, color=lm.color, marker=lm.icon)
        if lm.spotted:
            plt.plot([lm.x, pos[0]], [lm.y, pos[1]], color='g')

    for particle in particles:
        plt.plot(particle.x, particle.y, color=particle.color, marker=particle.icon)

    circle = plt.Circle((x_hist[-1], y_hist[-1]), my_robot.laser.scan_radius, color='b', fill=False)
    circle_hist.append(circle)

    fig = plt.gcf()
    ax = fig.gca()
    ax.add_artist(circle_hist[-1])

    plt.savefig(fname=image_path + 'IMAGE' + str(image_counter))
    ax.remove()
    # plt.show()

    if counter >= SIM_END:
        write_dict_to_txt(my_robot.laser.landmark_dict)
        write_list_to_txt(my_robot.controller.cmd_inputs)
        generate_avi(image_path, video_path)
        print('LANDMARK 1 DICT: ', my_robot.laser.landmark_dict[1])
        print('LANDMARK 2 DICT: ', my_robot.laser.landmark_dict[2])
        print('LANDMARK 3 DICT: ', my_robot.laser.landmark_dict[3])
        print('KILLING SIM')
        return True


if __name__ == '__main__':
    image_path = '/home/tyler/Pictures/'
    video_path = '/home/tyler/Videos/Robot_sim.avi'
    log_path = '/home/tyler/Documents/Robotics/'

    # ---------------- Robot Initial Values -------------------- #
    i_pos = np.zeros(2)
    i_pos.shape = (2, 1)

    i_vel = np.zeros(2)
    i_vel.shape = (2, 1)
    i_vel[0] = 3.5

    i_acc = np.zeros(2)
    i_acc.shape = (2, 1)

    DIR = 0.

    my_robot = Robot(i_pos, i_vel, i_acc, DIR)
    # --------------------------------------------------------- #

    # ------------------ Map Initial Values ------------------- #
    x_dims = [0., 24.]
    y_dims = [-12., 12.]
    # --------------------------------------------------------- #

    sim_running = True
    sim_counter = 0
    SIM_END = 65
    img_counter = 1

    x_hist = []
    y_hist = []
    x_meas = []
    y_meas = []
    circle_hist = []

    lm1 = Landmark(4., 2., 1)
    lm2 = Landmark(9., -1.5, 2)
    lm3 = Landmark(11.5, 8.5, 3)
    landmarks = [lm1, lm2, lm3]

    end_plot = False

    P_Filter = ParticleFilter(85)
    particles = P_Filter.place_particles(x_dims, y_dims)

    while sim_running:
        time = round(sim_counter * .1, 3)  # .1=DT
        DIR = 1.5 * sim_counter
        my_robot.update(time, landmarks=landmarks)

        x_hist.append(my_robot.getPos[0])
        y_hist.append(my_robot.getPos[1])

        x_meas.append(my_robot.get_measured_pos[0])
        y_meas.append(my_robot.get_measured_pos[1])

        if not end_plot and plot_in_line(sim_counter, img_counter, my_robot.getPos):
            break

        if end_plot and plot_at_end(sim_counter):
            break

        sim_counter += 1
        img_counter += 1
