import random
import time
import threading
import pygame
import sys

# Signal Timer Values
greenTimer = {0: 10, 1: 10, 2: 10, 3: 10}
redTimer = 150
yellowTimer = 5

# Pedestrian Signal Timer
pedestrianGreenTimer = {0: 10, 1: 10, 2: 10, 3: 10}
pedestrianRedTimer = 150

trafficSignals = []
noOfTrafficSignals = 2
presentGreen = 0  # Denotes Current Green Signal
# Shows which signal is going to turn green in next stage
nextSignalGreen = (presentGreen + 1) % noOfTrafficSignals
presentYellow = 0  # Denotes State of Yellow Signal


pedestrianSignals = []
noOfPedestrianSignals = 4
# Denoted current green pedestrian signal
presentPedestrianGreen = 0
# Shows which pedestrian signal is going to turn green in next stage
nextPedestrianGreenSignal = (
    presentPedestrianGreen + 1) % noOfPedestrianSignals

#  movingSpeed of 2 vehicles and pedestrians
movingSpeed = {'car': 1.8, 'truck': 1.8, 'pedestrian1': 0.2}

# Coordinates for vehicle and pedestrina spawn locations

x_coord = {'right': [1, 0, 1], 'down': [615, 635, 576], 'left': [1400, 1400, 1400], 'up': [790, 750, 709],
           'pedestrian_right': [1, 2, 0], 'pedestrian_down': [890, 830, 809], 'pedestrian_left': [1400, 1400, 1400], 'pedestrian_up': [485, 500, 526]}
y_coord = {'right': [446, 517, 476], 'down': [1, 0, 1], 'left': [323, 358, 399], 'up': [801, 803, 802],
           'pedestrian_right': [223, 258, 269], 'pedestrian_down': [0, 1, 0], 'pedestrian_left': [546, 567, 586], 'pedestrian_up': [800, 800, 800]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
typesOfVehicles = {0: 'car', 1: 'truck'}

pedestrians = {'pedestrian_right': {0: [], 1: [], 2: [], 'crossed': 0}, 'pedestrian_down': {0: [], 1: [], 2: [], 'crossed': 0},
               'pedestrian_left': {0: [], 1: [], 2: [], 'crossed': 0}, 'pedestrian_up': {0: [], 1: [], 2: [], 'crossed': 0}}
typesOfPedestrians = {0: 'pedestrian1'}

directionNum = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

pedestrianDirectionNumbers = {
    0: 'pedestrian_right', 1: 'pedestrian_down', 2: 'pedestrian_left', 3: 'pedestrian_up'}

# Coordinates of signal image, timer, and vehicle count
coordinatesForSignals = [(455, 500), (515, 140), (865, 200), (800, 530)]
coordinatesForSignalTimers = [(465, 563), (527, 205), (873, 265), (810, 595)]

# Coordinates of signal image, timer, and pedestrian count
pedestrianSignalCoords = [(460, 200), (850, 210), (860, 630), (455, 630)]

# Coordinates for stop lines
coordsStopLines = {'right': 450, 'down': 230, 'left': 900, 'up': 635}
defaultStop = {'right': 440, 'down': 220, 'left': 910, 'up': 650}

# Coordinates for pedestrian stop lines
pedestrianStopCoords = {'pedestrian_right': 560, 'pedestrian_down': 340,
                        'pedestrian_left': 810, 'pedestrian_up': 575}
defStopPedestrians = {'pedestrian_right': 550, 'pedestrian_down': 330,
                      'pedestrian_left': 820, 'pedestrian_up': 590}

# Gap between vehicles
vehiclesStopGap = 20  # stop gap
vehiclesMoveGap = 20  # moving gap

# Gap between pedestrians
pedestriansStpGap = 7  # stop gap
pedestriansMoveGap = 7  # moving gap

allowedVehicles = {'car': True, 'truck': True}
allowedVehiclesList = []
turnedVehicles = {'right': {1: [], 2: []}, 'down': {
    1: [], 2: []}, 'left': {1: [], 2: []}, 'up': {1: [], 2: []}}
notTurnedVehicles = {'right': {1: [], 2: []}, 'down': {
    1: [], 2: []}, 'left': {1: [], 2: []}, 'up': {1: [], 2: []}}
turnAngle = 3
middle = {'right': {'x_coord': 705, 'y_coord': 445}, 'down': {'x_coord': 695, 'y_coord': 450},
          'left': {'x_coord': 695, 'y_coord': 425}, 'up': {'x_coord': 695, 'y_coord': 400}}
randGSignTimers = True
randGSignTimersRange = [10, 20]

pygame.init()
simulate = pygame.sprite.Group()


class TrafficSignals:
    def __init__(self, redSignal, yellowSignal, greenSignal):
        self.redSignal = redSignal
        self.yellowSignal = yellowSignal
        self.greenSignal = greenSignal
        self.signalText = ""


class PedestrianSignals:
    def __init__(self, redSignal, greenSignal):
        self.redSignal = redSignal
        self.greenSignal = greenSignal
        self.signalText = ""


class Automobile(pygame.sprite.Sprite):
    def __init__(self, lane, automobileClass, direction_number, direction, goingto_turn):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.automobileClass = automobileClass
        self.speed = movingSpeed[automobileClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x_coord = x_coord[direction][lane]
        self.y_coord = y_coord[direction][lane]
        self.turned = 0
        vehicles[direction][lane].append(self)
        self.crossed = 0
        self.willTurn = goingto_turn
        self.index = len(vehicles[direction][lane]) - 1
        self.crossedIndex = 0
        self.rotateAngle = 0
        path = "images/" + direction + "/" + automobileClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.image = pygame.image.load(path)

        if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][
                self.index - 1].crossed == 0):
            # stop line
            if direction == 'right':
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index -
                                                                                                       1].image.get_rect().width - vehiclesStopGap  # setting stop coordinate as: stop

            elif direction == 'left':
                self.stop = vehicles[direction][lane][self.index - 1].stop + \
                    vehicles[direction][lane][self.index -
                                              1].image.get_rect().width + vehiclesStopGap
            elif direction == 'down':
                self.stop = vehicles[direction][lane][self.index - 1].stop - \
                    vehicles[direction][lane][self.index -
                                              1].image.get_rect().height - vehiclesStopGap
            elif direction == 'up':
                self.stop = vehicles[direction][lane][self.index - 1].stop + \
                    vehicles[direction][lane][self.index -
                                              1].image.get_rect().height + vehiclesStopGap

        else:
            self.stop = defaultStop[direction]

        # Define new start and stop coordinates
        if direction == 'right':
            aux = self.image.get_rect().width + vehiclesStopGap
            x_coord[direction][lane] -= aux
        elif direction == 'left':
            aux = self.image.get_rect().width + vehiclesStopGap
            x_coord[direction][lane] += aux
        elif direction == 'down':
            aux = self.image.get_rect().height + vehiclesStopGap
            y_coord[direction][lane] -= aux
        elif direction == 'up':
            aux = self.image.get_rect().height + vehiclesStopGap
            y_coord[direction][lane] += aux
        simulate.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x_coord, self.y_coord))

    def moveResources(self):
        global canTurnRight
        canTurnRight = False

        if self.direction == 'right':
            if self.crossed == 0 and self.x_coord + self.image.get_rect().width > coordsStopLines[self.direction]:
                self.crossed = 1

                vehicles[self.direction]['crossed'] += 1
                if self.willTurn == 0:
                    notTurnedVehicles[self.direction][self.lane].append(self)
                    self.crossedIndex = len(
                        notTurnedVehicles[self.direction][self.lane]) - 1
            # print('presentGreen', presentPedestrianGreen)
            if self.willTurn == 1:
                if self.lane == 2 and presentPedestrianGreen != 0 and canTurnRight:
                    if self.crossed == 0 or self.x_coord + self.image.get_rect().width < middle[self.direction]['x_coord'] + 10:

                        if ((self.x_coord + self.image.get_rect().width <= self.stop or (
                                presentGreen == 0 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.x_coord + self.image.get_rect().width < (
                                vehicles[self.direction][self.lane][self.index - 1].x_coord - vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x_coord += self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x_coord += 2.4
                            self.y_coord -= 2.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.y_coord > (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord +
                                    turnedVehicles[self.direction][self.lane][
                                        self.crossedIndex - 1].image.get_rect().height + vehiclesMoveGap))):
                                self.y_coord -= self.speed
                elif self.lane == 1 and presentPedestrianGreen != 2:
                    if self.crossed == 0 or self.x_coord + self.image.get_rect().width < coordsStopLines[self.direction] + 150:
                        if ((self.x_coord + self.image.get_rect().width <= self.stop or (
                                presentGreen == 0 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.x_coord + self.image.get_rect().width < (
                                vehicles[self.direction][self.lane][self.index - 1].x_coord - vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x_coord += self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x_coord += 2
                            self.y_coord += 1.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or ((self.y_coord + self.image.get_rect().height) < (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord - vehiclesMoveGap))):
                                self.y_coord += self.speed
            else:
                if self.crossed == 0:
                    if ((self.x_coord + self.image.get_rect().width <= self.stop or (
                            presentGreen == 0 and presentYellow == 0)) and (
                            self.index == 0 or self.x_coord + self.image.get_rect().width < (
                            vehicles[self.direction][self.lane][self.index - 1].x_coord - vehiclesMoveGap))):
                        self.x_coord += self.speed
                else:
                    if ((self.crossedIndex == 0) or (self.x_coord + self.image.get_rect().width < (
                            notTurnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord - vehiclesMoveGap))):
                        self.x_coord += self.speed
        elif self.direction == 'down':
            if self.crossed == 0 and self.y_coord + self.image.get_rect().height > coordsStopLines[self.direction]:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if self.willTurn == 0:
                    notTurnedVehicles[self.direction][self.lane].append(self)
                    self.crossedIndex = len(
                        notTurnedVehicles[self.direction][self.lane]) - 1
            if self.willTurn == 1:
                if self.lane == 1 and presentPedestrianGreen != 1 and canTurnRight:
                    if self.crossed == 0 or self.y_coord + self.image.get_rect().height < middle[self.direction]['y_coord'] + 50:

                        if ((self.y_coord + self.image.get_rect().height <= self.stop or (
                                presentGreen == 1 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.y_coord + self.image.get_rect().height < (
                                vehicles[self.direction][self.lane][self.index - 1].y_coord - vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y_coord += self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x_coord += 1.2
                            self.y_coord += 1.8
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or ((self.x_coord + self.image.get_rect().width) < (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord - vehiclesMoveGap))):
                                self.x_coord += self.speed
                elif self.lane == 2 and presentPedestrianGreen != 3:
                    if self.crossed == 0 or self.y_coord + self.image.get_rect().height < coordsStopLines[self.direction] + 150:

                        if ((self.y_coord + self.image.get_rect().height <= self.stop or (
                                presentGreen == 1 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.y_coord + self.image.get_rect().height < (
                                vehicles[self.direction][self.lane][self.index - 1].y_coord - vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y_coord += self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, -self.rotateAngle)
                            self.x_coord -= 2.5
                            self.y_coord += 2
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.x_coord > (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord +
                                    turnedVehicles[self.direction][self.lane][
                                        self.crossedIndex - 1].image.get_rect().width + vehiclesMoveGap))):
                                self.x_coord -= self.speed
            else:
                if self.crossed == 0:
                    if ((self.y_coord + self.image.get_rect().height <= self.stop or (
                            presentGreen == 1 and presentYellow == 0)) and (
                            self.index == 0 or self.y_coord + self.image.get_rect().height < (
                            vehicles[self.direction][self.lane][self.index - 1].y_coord - vehiclesMoveGap))):
                        self.y_coord += self.speed
                else:
                    if ((self.crossedIndex == 0) or (self.y_coord + self.image.get_rect().height < (
                            notTurnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord - vehiclesMoveGap))):
                        self.y_coord += self.speed
        elif self.direction == 'left':
            if self.crossed == 0 and self.x_coord < coordsStopLines[self.direction]:

                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if self.willTurn == 0:
                    notTurnedVehicles[self.direction][self.lane].append(self)
                    self.crossedIndex = len(
                        notTurnedVehicles[self.direction][self.lane]) - 1
            if self.willTurn == 1:
                if self.lane == 2 and presentPedestrianGreen != 2 and canTurnRight:
                    if self.crossed == 0 or self.x_coord > middle[self.direction]['x_coord'] - 40:

                        if ((self.x_coord >= self.stop or (
                                presentGreen == 0 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.x_coord > (vehicles[self.direction][self.lane][self.index - 1].x_coord +
                                                                   vehicles[self.direction][self.lane][
                                    self.index - 1].image.get_rect().width + vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x_coord -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x_coord -= 1
                            self.y_coord += 1.2
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or ((self.y_coord + self.image.get_rect().height) < (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord - vehiclesMoveGap))):
                                self.y_coord += self.speed
                elif self.lane == 1 and presentPedestrianGreen != 0:
                    if self.crossed == 0 or self.x_coord > coordsStopLines[self.direction] - 130:
                        if ((self.x_coord >= self.stop or (
                                presentGreen == 0 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.x_coord > (vehicles[self.direction][self.lane][self.index - 1].x_coord +
                                                                   vehicles[self.direction][self.lane][
                                    self.index - 1].image.get_rect().width + vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.x_coord -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, -self.rotateAngle)
                            self.x_coord -= 1.8
                            self.y_coord -= 2.5
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.y_coord > (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord +
                                    turnedVehicles[self.direction][self.lane][
                                        self.crossedIndex - 1].image.get_rect().height + vehiclesMoveGap))):
                                self.y_coord -= self.speed
            else:
                if self.crossed == 0:
                    if ((self.x_coord >= self.stop or (presentGreen == 0 and presentYellow == 0)) and (
                            self.index == 0 or self.x_coord > (
                            vehicles[self.direction][self.lane][self.index - 1].x_coord + vehicles[self.direction][self.lane][
                                self.index - 1].image.get_rect().width + vehiclesMoveGap))):
                        self.x_coord -= self.speed
                else:
                    if ((self.crossedIndex == 0) or (self.x_coord > (
                            notTurnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord +
                            notTurnedVehicles[self.direction][self.lane][
                                self.crossedIndex - 1].image.get_rect().width + vehiclesMoveGap))):
                        self.x_coord -= self.speed
        elif self.direction == 'up':
            if self.crossed == 0 and self.y_coord < coordsStopLines[self.direction] and presentPedestrianGreen != 2 and presentPedestrianGreen != 0:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if self.willTurn == 0:
                    notTurnedVehicles[self.direction][self.lane].append(self)
                    self.crossedIndex = len(
                        notTurnedVehicles[self.direction][self.lane]) - 1
            if self.willTurn == 1:
                if self.lane == 2 and presentPedestrianGreen != 3 and canTurnRight:
                    # if self.crossed == 0 or self.y_coord > coordsStopLines[self.direction] - 60:
                    if self.crossed == 0 or self.y_coord > middle[self.direction]['y_coord'] - 20:

                        if ((self.y_coord >= self.stop or (
                                presentGreen == 1 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.y_coord > (vehicles[self.direction][self.lane][self.index - 1].y_coord +
                                                                   vehicles[self.direction][self.lane][
                                    self.index - 1].image.get_rect().height + vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y_coord -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x_coord -= 2
                            self.y_coord -= 1.2
                            if self.rotateAngle == 90:
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.x_coord > (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord +
                                    turnedVehicles[self.direction][self.lane][
                                        self.crossedIndex - 1].image.get_rect().width + vehiclesMoveGap))):
                                self.x_coord -= self.speed
                elif self.lane == 1 and presentPedestrianGreen != 1:
                    # if self.crossed == 0 or self.y_coord > middle[self.direction]['y_coord']:
                    if self.crossed == 0 or self.y_coord > coordsStopLines[self.direction] - 100:
                        if ((self.y_coord >= self.stop or (
                                presentGreen == 1 and presentYellow == 0) or self.crossed == 1) and (
                                self.index == 0 or self.y_coord > (vehicles[self.direction][self.lane][self.index - 1].y_coord +
                                                                   vehicles[self.direction][self.lane][
                                    self.index - 1].image.get_rect().height + vehiclesMoveGap) or
                                vehicles[self.direction][self.lane][self.index - 1].turned == 1)):
                            self.y_coord -= self.speed
                    else:
                        if self.turned == 0:
                            self.rotateAngle += turnAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, -self.rotateAngle)
                            self.x_coord += 1
                            self.y_coord -= 1
                            if (self.rotateAngle == 90):
                                self.turned = 1
                                turnedVehicles[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    turnedVehicles[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.x_coord < (
                                    turnedVehicles[self.direction][self.lane][self.crossedIndex - 1].x_coord -
                                    turnedVehicles[self.direction][self.lane][
                                        self.crossedIndex - 1].image.get_rect().width - vehiclesMoveGap))):
                                self.x_coord += self.speed
            else:
                if self.crossed == 0:
                    if ((self.y_coord >= self.stop or (presentGreen == 1 and presentYellow == 0)) and (
                            self.index == 0 or self.y_coord > (
                            vehicles[self.direction][self.lane][self.index - 1].y_coord + vehicles[self.direction][self.lane][
                                self.index - 1].image.get_rect().height + vehiclesMoveGap))):
                        self.y_coord -= self.speed
                else:
                    if ((self.crossedIndex == 0) or (self.y_coord > (
                            notTurnedVehicles[self.direction][self.lane][self.crossedIndex - 1].y_coord +
                            notTurnedVehicles[self.direction][self.lane][
                                self.crossedIndex - 1].image.get_rect().height + vehiclesMoveGap))):
                        self.y_coord -= self.speed

        return self.y_coord, self.x_coord


class Pedestrian(pygame.sprite.Sprite):
    def __init__(self, lane, pedestrianClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.pedestrianClass = pedestrianClass
        self.speed = movingSpeed[pedestrianClass]
        self.direction_number = direction_number
        self.direction = direction
        self.crossed = 0
        self.x_coord = x_coord[direction][lane]
        self.y_coord = y_coord[direction][lane]
        pedestrians[direction][lane].append(self)
        self.index = len(pedestrians[direction][lane]) - 1
        path = "images/" + "Pdirection/" + direction + "/" + pedestrianClass + ".png"
        self.image = pygame.image.load(path)

        if len(pedestrians[direction][lane]) > 1 and pedestrians[direction][lane][self.index - 1].crossed == 0:
            # if more than 1 pedestrians are present already at crossing line
            if direction == 'pedestrian_right':
                self.stop = pedestrians[direction][lane][self.index - 1].stop - pedestrians[direction][lane][
                    self.index - 1].image.get_rect().width - pedestriansStpGap

            elif direction == 'pedestrian_left':
                self.stop = pedestrians[direction][lane][self.index - 1].stop + pedestrians[direction][lane][
                    self.index - 1].image.get_rect().width + pedestriansStpGap

            elif direction == 'pedestrian_down':
                self.stop = pedestrians[direction][lane][self.index - 1].stop - pedestrians[direction][lane][
                    self.index - 1].image.get_rect().height - pedestriansStpGap

            elif direction == 'pedestrian_up':
                self.stop = pedestrians[direction][lane][self.index - 1].stop + pedestrians[direction][lane][
                    self.index - 1].image.get_rect().height + pedestriansStpGap

        else:
            self.stop = defStopPedestrians[direction]

        # Populate new stop and start times
        if direction == 'pedestrian_right':
            aux = self.image.get_rect().width + pedestriansStpGap
            x_coord[direction][lane] -= aux
        elif direction == 'pedestrian_left':
            aux = self.image.get_rect().width + pedestriansStpGap
            x_coord[direction][lane] += aux
        elif direction == 'pedestrian_down':
            aux = self.image.get_rect().height + pedestriansStpGap
            y_coord[direction][lane] -= aux
        elif direction == 'pedestrian_up':
            aux = self.image.get_rect().height + pedestriansStpGap
            y_coord[direction][lane] += aux
        simulate.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x_coord, self.y_coord))

    def moveResources(self):
        if self.direction == 'pedestrian_right':

            if self.crossed == 0 and self.x_coord + self.image.get_rect().width > pedestrianStopCoords[self.direction]:
                self.crossed = 1

            if ((self.x_coord + self.image.get_rect().width <= self.stop or self.crossed == 1 or (presentPedestrianGreen == 0)) and (
                    self.index == 0 or self.x_coord + self.image.get_rect().width < (
                    pedestrians[self.direction][self.lane][self.index - 1].x_coord - pedestriansMoveGap))):
                self.x_coord += self.speed
        elif self.direction == 'pedestrian_down':
            if self.crossed == 0 and self.y_coord + self.image.get_rect().height > pedestrianStopCoords[self.direction]:
                self.crossed = 1
            if ((self.y_coord + self.image.get_rect().height <= self.stop or self.crossed == 1 or (presentPedestrianGreen == 1)) and (
                    self.index == 0 or self.y_coord + self.image.get_rect().height < (
                    pedestrians[self.direction][self.lane][self.index - 1].y_coord - pedestriansMoveGap))):
                self.y_coord += self.speed
        elif self.direction == 'pedestrian_left':
            if self.crossed == 0 and self.x_coord < pedestrianStopCoords[self.direction]:
                self.crossed = 1
            if ((self.x_coord >= self.stop or self.crossed == 1 or (presentPedestrianGreen == 2)) and (self.index == 0 or self.x_coord > (
                    pedestrians[self.direction][self.lane][self.index - 1].x_coord + pedestrians[self.direction][self.lane][
                        self.index - 1].image.get_rect().width + pedestriansMoveGap))):
                self.x_coord -= self.speed
        elif self.direction == 'pedestrian_up':
            if self.crossed == 0 and self.y_coord < pedestrianStopCoords[self.direction]:
                self.crossed = 1
            if ((self.y_coord >= self.stop or self.crossed == 1 or (presentPedestrianGreen == 3)) and
                    (self.index == 0 or self.y_coord > (pedestrians[self.direction][self.lane][self.index - 1].y_coord +
                                                        pedestrians[self.direction][self.lane][
                        self.index - 1].image.get_rect().height + pedestriansMoveGap))):
                self.y_coord -= self.speed
        return self.y_coord, self.x_coord


def moveResources():
    p = Pedestrian
    a = Automobile
    if (p.direction == 'pedestrian_right') and (a.direction == 'up'):

        if p.crossed == 0 and p.x_coord + p.image.get_rect().width > pedestrianStopCoords[p.direction]:
            p.crossed = 1
        if ((p.x_coord + p.image.get_rect().width <= p.stop or p.crossed == 1 or (presentPedestrianGreen == 0)) and (
                p.index == 0 or p.x_coord + p.image.get_rect().width < (
                pedestrians[p.direction][p.lane][p.index - 1].x_coord - pedestriansMoveGap))):
            p.x_coord += p.speed

        # if signal is green and vehicle lane is up
        if presentGreen == 1:
            p.x_coord += p.stop

    elif (p.direction == 'pedestrian_down') and (a.direction == 'right'):
        if p.crossed == 0 and p.y_coord + p.image.get_rect().height > pedestrianStopCoords[p.direction]:
            p.crossed = 1
        if ((p.y_coord + p.image.get_rect().height <= p.stop or p.crossed == 1 or (presentPedestrianGreen == 1)) and (
                p.index == 0 or p.y_coord + p.image.get_rect().height < (
                pedestrians[p.direction][p.lane][p.index - 1].y_coord - pedestriansMoveGap))):
            p.y_coord += p.speed
        # # if signal is green and vehicle lane is right
        if presentGreen == 0:
            p.x_coord += p.stop
    elif (p.direction == 'pedestrian_left') and (a.direction == 'down'):
        if p.crossed == 0 and p.x_coord < pedestrianStopCoords[p.direction]:
            p.crossed = 1
        if ((p.x_coord >= p.stop or p.crossed == 1 or (presentPedestrianGreen == 2)) and (p.index == 0 or p.x_coord > (
                pedestrians[p.direction][p.lane][p.index - 1].x_coord + pedestrians[p.direction][p.lane][
                    p.index - 1].image.get_rect().width + pedestriansMoveGap))):
            p.x_coord -= p.speed
            # # if signal is green and vehicle lane is down
        if presentGreen == 1:
            p.x_coord += p.stop
    elif (p.direction == 'pedestrian_up') and (a.direction == 'left'):
        if p.crossed == 0 and p.y_coord < pedestrianStopCoords[p.direction]:
            p.crossed = 1
        if ((p.y_coord >= p.stop or p.crossed == 1 or (presentPedestrianGreen == 3)) and
                (p.index == 0 or p.y_coord > (pedestrians[p.direction][p.lane][p.index - 1].y_coord +
                                              pedestrians[p.direction][p.lane][
                    p.index - 1].image.get_rect().height + pedestriansMoveGap))):
            p.y_coord -= p.speed
        # # if signal is green and vehicle lane is left
        if presentGreen == 0:
            p.x_coord += p.stop


def start():
    minT = randGSignTimersRange[0]
    maxT = randGSignTimersRange[1]
    if randGSignTimers:
        tSignal1 = TrafficSignals(
            0, yellowTimer, random.randint(minT, maxT))
        trafficSignals.append(tSignal1)
        tSignal2 = TrafficSignals(tSignal1.yellowSignal + tSignal1.greenSignal,
                                  yellowTimer, random.randint(minT, maxT))
        trafficSignals.append(tSignal2)
        tSignal3 = TrafficSignals(
            0, yellowTimer, random.randint(minT, maxT))
        trafficSignals.append(tSignal3)
        tSignal4 = TrafficSignals(redTimer, yellowTimer,
                                  random.randint(minT, maxT))
        trafficSignals.append(tSignal4)
    else:
        tSignal1 = TrafficSignals(0, yellowTimer, greenTimer[0])
        trafficSignals.append(tSignal1)
        tSignal2 = TrafficSignals(tSignal1.yellowSignal + tSignal1.greenSignal,
                                  yellowTimer, greenTimer[1])
        trafficSignals.append(tSignal2)
        tSignal3 = TrafficSignals(0, yellowTimer, greenTimer[2])
        trafficSignals.append(tSignal3)
        tSignal4 = TrafficSignals(redTimer, yellowTimer, greenTimer[3])
        trafficSignals.append(tSignal4)

    pSignal1 = PedestrianSignals(0, pedestrianGreenTimer[0])
    pedestrianSignals.append(pSignal1)
    pSignal2 = PedestrianSignals(
        pSignal1.redSignal + pSignal1.greenSignal, pedestrianGreenTimer[1])
    pedestrianSignals.append(pSignal2)
    pSignal3 = PedestrianSignals(0, pedestrianGreenTimer[2])
    pedestrianSignals.append(pSignal3)
    pSignal4 = PedestrianSignals(pedestrianRedTimer, pedestrianGreenTimer[3])
    pedestrianSignals.append(pSignal4)
    repeatLoop()


def repeatLoop():
    global presentGreen, presentYellow, nextSignalGreen, presentPedestrianGreen, nextPedestrianGreenSignal
    # Considered only Vehicle Traffic Signals
    while trafficSignals[presentGreen].greenSignal > 0:
        changeTimerValues()
        time.sleep(1)

    presentYellow = 1
    for i in range(0, 3):
        for vehicle in vehicles[directionNum[presentGreen]][i]:
            vehicle.stop = defaultStop[directionNum[presentGreen]]
    while trafficSignals[presentGreen].yellowSignal > 0:
        changeTimerValues()
        time.sleep(1)
    presentYellow = 0

    # Change to next Green Signal
    setNextGreenSignalForVehicles()

    # Change Pedestrian traffic Signals based on Vehicle Traffic Signals
    changePedestrianSignals()

    repeatLoop()


def setNextGreenSignalForVehicles():
    global presentGreen, nextSignalGreen
    minT = randGSignTimersRange[0]
    maxT = randGSignTimersRange[1]
    if randGSignTimers:
        trafficSignals[presentGreen].greenSignal = random.randint(
            minT, maxT)
    else:
        trafficSignals[presentGreen].greenSignal = greenTimer[presentGreen]
    trafficSignals[presentGreen].yellowSignal = yellowTimer
    trafficSignals[presentGreen].redSignal = redTimer
    presentGreen = nextSignalGreen
    nextSignalGreen = (presentGreen + 1) % noOfTrafficSignals
    trafficSignals[nextSignalGreen].redSignal = trafficSignals[presentGreen].yellowSignal + \
        trafficSignals[presentGreen].greenSignal


def changePedestrianSignals():
    global presentPedestrianGreen, nextPedestrianGreenSignal
    # When vehicles are moving from north to south or vice versa we change the east and west pedestrian signals to red
    if presentGreen in [1, 3]:
        # 0 corresponds to pedestrian red signal
        pedestrianSignals[0].greenSignal = 0
        # 2 represents left pedestrian signal
        pedestrianSignals[2].greenSignal = 0
        pedestrianSignals[0].redSignal = trafficSignals[presentGreen].greenSignal + \
            trafficSignals[presentGreen].yellowSignal  # Sync with vehicle signal timer
        pedestrianSignals[2].redSignal = trafficSignals[presentGreen].greenSignal + \
            trafficSignals[presentGreen].yellowSignal

        # Change pedestrian signal back to green after vehicle signal changes to red
        pedestrianSignals[1].greenSignal = pedestrianGreenTimer[1]
        pedestrianSignals[3].greenSignal = pedestrianGreenTimer[3]
        pedestrianSignals[1].redSignal = 0
        pedestrianSignals[3].redSignal = 0

    # next pedestrian signal is set to green
    presentPedestrianGreen = nextPedestrianGreenSignal
    nextPedestrianGreenSignal = (
        presentPedestrianGreen + 1) % noOfPedestrianSignals


# Change signal timer values after every second
def changeTimerValues():
    for i in range(0, noOfTrafficSignals):
        if i == presentGreen:
            if presentYellow == 0:
                trafficSignals[i].greenSignal -= 1
            else:
                trafficSignals[i].yellowSignal -= 1
        else:
            trafficSignals[i].redSignal -= 1

    for i in range(0, noOfPedestrianSignals):
        if i == presentPedestrianGreen:
            pedestrianSignals[i].greenSignal -= 1
        else:
            pedestrianSignals[i].redSignal -= 1


# Creating vehicles in the simulation
def createVehicles():
    while True:
        type_vehicle = random.choice(allowedVehiclesList)
        number_lane = random.randint(1, 2)
        goingto_turn = 0
        if number_lane == 1:
            aux = random.randint(0, 99)
            if aux < 40:
                goingto_turn = 1
        elif number_lane == 2:
            aux = random.randint(0, 99)
            if aux < 40:
                goingto_turn = 1
        aux = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if aux < dist[0]:
            direction_number = 0
        elif aux < dist[1]:
            direction_number = 1
        elif aux < dist[2]:
            direction_number = 2
        elif aux < dist[3]:
            direction_number = 3
        Automobile(number_lane, typesOfVehicles[type_vehicle], direction_number, directionNum[direction_number],
                   goingto_turn)
        time.sleep(2)


# Creating vehicles in the simulation
def createPedestrians():
    while (True):
        type_pedestrian = 0
        number_lane = random.randint(1, 2)
        aux = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if aux < dist[0]:
            direction_number = 0
        elif aux < dist[1]:
            direction_number = 1
        elif aux < dist[2]:
            direction_number = 2
        elif aux < dist[3]:
            direction_number = 3
        Pedestrian(number_lane, typesOfPedestrians[type_pedestrian],
                   direction_number, pedestrianDirectionNumbers[direction_number])
        time.sleep(10)


class Main:
    global allowedVehiclesList
    i = 0
    for vehicleType in allowedVehicles:
        if (allowedVehicles[vehicleType]):
            allowedVehiclesList.append(i)
        i += 1
    thread1 = threading.Thread(
        name="start", target=start, args=())  # initialization
    thread1.daemon = True
    thread1.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1300
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Loading Image for intersection
    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Load images for signals
    redSignal = pygame.image.load('images/trafficSignals/red.png')
    yellowSignal = pygame.image.load('images/trafficSignals/yellow.png')
    greenSignal = pygame.image.load('images/trafficSignals/green.png')
    PredSignal = pygame.image.load('images/trafficSignals/Pred.png')
    PgreenSignal = pygame.image.load('images/trafficSignals/Pgreen.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(
        name="createVehicles", target=createVehicles, args=())  # Creating Vehicles
    thread2.daemon = True
    thread2.start()

    thread3 = threading.Thread(name="createPedestrians", target=createPedestrians,
                               args=())  # Creating pedestrians
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (-260, -50))

        # Show pedestrian signals
        for i in range(0, noOfPedestrianSignals):
            # greenSignal or redSignal
            if i == presentPedestrianGreen:
                pedestrianSignals[i].signalText = pedestrianSignals[i].greenSignal
                screen.blit(PgreenSignal, pedestrianSignalCoords[i])
            else:
                if pedestrianSignals[i].redSignal <= 10:
                    pedestrianSignals[i].signalText = pedestrianSignals[i].redSignal
                else:
                    pedestrianSignals[i].signalText = "---"
                screen.blit(PredSignal, pedestrianSignalCoords[i])
        psignalTexts = ["", "", "", ""]

        # Show signal and display timer according to the timer of the signals
        for i in range(0, noOfTrafficSignals):
            if i == presentGreen:
                if presentYellow == 1:
                    trafficSignals[i].signalText = trafficSignals[i].yellowSignal
                    screen.blit(yellowSignal, coordinatesForSignals[i])

                else:
                    trafficSignals[i].signalText = trafficSignals[i].greenSignal
                    screen.blit(greenSignal, coordinatesForSignals[i])

            else:
                if trafficSignals[i].redSignal <= 10:
                    trafficSignals[i].signalText = trafficSignals[i].redSignal

                else:
                    trafficSignals[i].signalText = "---"
                screen.blit(redSignal, coordinatesForSignals[i])

        signalTexts = ["", "", "", ""]

        # Show Traffic Signal Timer
        for i in range(0, noOfTrafficSignals):
            signalTexts[i] = font.render(
                str(trafficSignals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], coordinatesForSignalTimers[i])

        # Show the vehicles
        for vehicle in simulate:
            screen.blit(vehicle.image, [vehicle.x_coord, vehicle.y_coord])
            vehicle.moveResources()

        # Show pedestrians
        for pedestrian in simulate:
            screen.blit(pedestrian.image, [
                        pedestrian.x_coord, pedestrian.y_coord])
            pedestrian.moveResources()

        pygame.display.update()


Main()
