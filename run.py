from pygame_sim import Vehicle
from vehicle_controller import VehicleController, UserController,\
        BasicEvasionController, DaggerPursuitController
import dagger
import dagger_nn
import pygame
import numpy as np
import random

# TODO: compare different learning algorithms/systems
# types: dagger, expert, deepq
run_type = 'dagger_lookback'
epsilon=0.5

def reset_sim():
    print iterations
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([100.0+random.randint(-400, 400),
        100.0+random.randint(-400, 400)])
    v1_controller.train()
    v1_controller.model.save(file_prefix='nn_'+run_type)
    if 'dagger' in run_type:
        if random.random()<epsilon:
            print 'policy control (learning)'
            v1_controller.control='policy_learn'
        else:
            print 'user control'
            v1_controller.control='user'
    elif run_type=='expert':
        v1_controller.control='user'

if __name__ == '__main__':
    # set time to 15ms/tick
    pursuit_model = dagger_nn.NNDaggerLookbackModel()
    #pursuit_model.load()
    vehicle1 = Vehicle(mass=1., ang=0.1, main=True)
    vehicle2 = Vehicle(mass=5., ang=0.1)
    v1_controller = DaggerPursuitController(vehicle1, model=pursuit_model)
    v2_controller = BasicEvasionController(vehicle2)
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([100.0+random.randint(-400, 400),
        100.0+random.randint(-400, 400)])
    screen = pygame.display.set_mode((1000,1000))
    iterations = 0
    steps = 0
    total_steps = 0
    # results: 1 for success, 0 for failure
    results = []
    while 1:
        current_time = pygame.time.get_ticks()
        # update vehicle1 control (user)
        state = (vehicle1.state(), vehicle2.state())
        v1_control = v1_controller.next_action(state)
        vehicle1.update(v1_control)
        # update vehicle2 control (auto)
        state = (vehicle2.state(), vehicle1.state())
        v2_control = v2_controller.next_action(state)
        vehicle2.update(v2_control)
        #print control
        #print vehicle1.state()
        # display vehicle1
        screen.fill((0,0,0))
        vehicle1.draw(screen, main_pos=vehicle1.pos)
        vehicle2.draw(screen, main_pos=vehicle1.pos)
        pygame.display.flip()
        if vehicle1.detect_collision(vehicle2):
            iterations += 1
            if v1_controller.control=='policy' \
                    or v1_controller.control=='policy_learn':
                results.append(1)
            print 'collision'
            reset_sim()
            total_steps += steps
            steps = 0
        if steps>=500:
            iterations += 1
            if v1_controller.control=='policy' \
                    or v1_controller.control=='policy_learn':
                results.append(0)
            reset_sim()
            total_steps += steps
            steps = 0
            print 'failed'
        steps += 1
        pygame.time.delay(30 - (pygame.time.get_ticks()-current_time))
        with open(run_type + '_notes.txt', 'w') as f:
            f.write('iterations: ' + str(iterations) + '\n')
            f.write('steps: ' + str(total_steps) + '\n')


