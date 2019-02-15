#!/usr/bin/env python

import numpy as np
import random
from pycrazyswarm import *

def randomWaypoints():
    waypoints = []
    for i in range(50):
        waypoints.append([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(0.45, 0.55)])
        waypoints.append([0.0, 0.0, 0.5])

    return waypoints

if __name__ == "__main__":

    # generate waypoints randomly
    waypoints = randomWaypoints()
    # execute waypoints
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    height = 1.0

    allcfs.takeoff(targetHeight=1.0, duration=2.0)
    timeHelper.sleep(2.0)
    lastTime = 0.0
    counter = 0
    for waypoint in waypoints:
        for cf in allcfs.crazyflies:
            print "Going to " + str(counter) +": " + str(waypoint)
            cf.goTo(waypoint, 0, 0.3)
            timeHelper.sleep(0.3)
        counter += 1    

    allcfs.land(targetHeight=0.06, duration=2.0)
    timeHelper.sleep(3.0)