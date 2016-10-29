from pygame_sim import Vehicle
from vehicle_controller import VehicleController
import pygame
import numpy as np

if __name__ == '__main__':
    # set time to 15ms/tick
    vehicle1 = Vehicle(mass=1., ang=0.1)
    vehicle1_surface = vehicle1.create_display_surface()
    vehicle2 = Vehicle(mass=5., ang=0.1)
    vehicle2_surface = vehicle2.create_display_surface()
    controller = VehicleController(vehicle2)
    vehicle1.pos = np.array([100.0,100.0])
    vehicle2.pos = np.array([600.0, 600.0])
    screen = pygame.display.set_mode((1000,1000))
    while 1:
        current_time = pygame.time.get_ticks()
        # update vehicle1 control (user)
        control = []
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        #print [i for i in keys if i>0]
        if keys[pygame.K_UP]:
                        control.append('FWD')
        if keys[pygame.K_LEFT]:
                        control.append('LEFT')
        if keys[pygame.K_DOWN]:
                        control.append('BACK')
        if keys[pygame.K_RIGHT]:
                        control.append('RIGHT')
        vehicle1.update(control)
        # update vehicle2 control (auto)
        v2_control = controller.next_action()
        vehicle2.update(v2_control)
        #print control
        #print vehicle1.state()
        # display vehicle1
        screen.fill((0,0,0))
        vehicle1.draw(screen)
        vehicle2.draw(screen)
        pygame.display.flip()
        pygame.time.delay(15 - (pygame.time.get_ticks()-current_time))


