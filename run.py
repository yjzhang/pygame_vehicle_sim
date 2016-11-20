from pygame_sim import Vehicle
from vehicle_controller import VehicleController, UserController,\
        BasicEvasionController, DaggerPursuitController
import dagger
import pygame
import numpy as np
import random

def reset_sim():
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([100.0+random.randint(-400, 400), 
        100.0+random.randint(-400, 400)])
    v1_controller.train()
    if random.random()<0.5:
        print 'policy'
        v1_controller.control='policy'
    else:
        print 'random'
        v1_controller.control='user'

if __name__ == '__main__':
    # set time to 15ms/tick
    pursuit_model = dagger.LinearDaggerModel()
    vehicle1 = Vehicle(mass=1., ang=0.1, main=True)
    vehicle2 = Vehicle(mass=5., ang=0.1)
    v1_controller = DaggerPursuitController(vehicle1, model=pursuit_model)
    v2_controller = BasicEvasionController(vehicle2)
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([100.0+random.randint(-400, 400), 
        100.0+random.randint(-400, 400)])
    screen = pygame.display.set_mode((1000,1000))
    steps = 0
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
            print 'collision'
            reset_sim()
            steps = 0
        if steps>=500:
            reset_sim()
            steps = 0
        steps += 1
        pygame.time.delay(15 - (pygame.time.get_ticks()-current_time))


