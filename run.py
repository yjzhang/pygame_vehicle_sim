from pygame_sim import Vehicle
from vehicle_controller import VehicleController, UserController,\
        BasicEvasionController
import pygame
import numpy as np

if __name__ == '__main__':
    # set time to 15ms/tick
    vehicle1 = Vehicle(mass=1., ang=0.1)
    vehicle1_surface = vehicle1.create_display_surface()
    vehicle2 = Vehicle(mass=5., ang=0.1)
    vehicle2_surface = vehicle2.create_display_surface()
    v1_controller = UserController(vehicle1)
    v2_controller = BasicEvasionController(vehicle2)
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([600.0, 600.0])
    screen = pygame.display.set_mode((1000,1000))
    while 1:
        current_time = pygame.time.get_ticks()
        # update vehicle1 control (user)
        v1_control = v1_controller.next_action()
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
        pygame.time.delay(15 - (pygame.time.get_ticks()-current_time))


