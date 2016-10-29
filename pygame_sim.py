import pygame as pg
import numpy as np

CONTROL_ACC = set(['FWD', 'BACK'])
CONTROL_ANG = set(['LEFT', 'RIGHT'])

def update_vel(vel, heading, force, mass, drag=0.1):
    """
    Returns a new velocity vector...
    """
    acc = force/mass
    new_vel = np.array(vel)
    new_vel[0] = vel[0] + acc*np.cos(heading) - drag*vel[0]
    # use -sin because in pygame, positive y is down
    new_vel[1] = vel[1] + acc*-np.sin(heading) - drag*vel[1]
    return new_vel

def update_pos(pos, heading, vel):
    """
    Returns a new position vector...
    """
    new_pos = np.array(pos)
    new_pos[0] = pos[0] + vel[0]
    new_pos[1] = pos[1] + vel[1]
    return new_pos

class Vehicle(object):

    def __init__(self, mass = 10.0, force=1.0, ang=0.01,
            init_pos = np.array([0.0, 0.0]),
            noise = 0.0, drag=0.3):
        """
        Defines a new vehicle.
        noise is the variance of the noise distribution.
        drag is some drag coefficient... (not actually a physical parameter)
        """
        self.mass = mass
        self.force = force
        # ang = angular velocity
        self.ang = ang
        self.pos = init_pos
        # angle heading in radians (?)
        self.heading = 0.0
        self.vel = np.array([0.0, 0.0])
        # angular velocity
        self.max_vel = 10.0
        self.noise = noise
        self.drag = drag

    def state(self):
        """
        Returns the state of the vehicle:
            x-position, y-position, heading, x-velocity, y-velocity,
            angular velocity
        """
        return np.array([self.pos[0], self.pos[1], self.heading, self.vel[0],
                self.vel[1]])

    def update(self, control):
        """
        Updates the vehicle state
        """
        if 'FWD' in control:
            self.vel = update_vel(self.vel, self.heading, self.force,
                    self.mass, self.drag)
        elif 'BACK' in control:
            self.vel = update_vel(self.vel, self.heading, -self.force,
                    self.mass, self.drag)
        else:
            self.vel = update_vel(self.vel, self.heading, 0.0,
                    self.mass, self.drag)

        if 'LEFT' in control:
            self.heading += self.ang
        elif 'RIGHT' in control:
            self.heading -= self.ang
        self.pos = update_pos(self.pos, self.heading, self.vel)

def main():
    vehicle1 = Vehicle()
    vehicle1.pos = np.array([250.0,250.0])
    screen = pg.display.set_mode((500,500))
    vehicle1_surface = pg.Surface((30, 30))
    pg.draw.ellipse(vehicle1_surface, (255,255,255),(0,0,30,30))
    pg.draw.line(vehicle1_surface, (0,0,255),(15,15),(30,15))
    while 1:
        control = []
        pg.event.pump()
        keys = pg.key.get_pressed()
        #print [i for i in keys if i>0]
        if keys[pg.K_UP]:
            control.append('FWD')
        # flip left and right because ???
        if keys[pg.K_LEFT]:
            control.append('LEFT')
        if keys[pg.K_DOWN]:
            control.append('BACK')
        if keys[pg.K_RIGHT]:
            control.append('RIGHT')
        vehicle1.update(control)
        #print control
        #print vehicle1.state()
        screen.fill((0,0,0))
        angle = np.degrees(vehicle1.heading)
        print angle
        s1 = pg.transform.rotate(vehicle1_surface, angle)
        screen.blit(s1, vehicle1.pos)
        pg.display.flip()

if __name__ == '__main__':
    main()
