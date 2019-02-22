#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
import rospy
from sensor_msgs.msg import Joy

# XBox360 mapping
ButtonGreen  = 0
ButtonRed    = 1
ButtonBlue   = 2
ButtonYellow = 3
ButtonLB     = 4
ButtonRB     = 5
ButtonBack   = 6
ButtonStart  = 7

lastButtonData = None
controller = None


def joyChanged(data):
    global lastButtonData

    if lastButtonData:
        if data.buttons[ButtonRed] == 1 and lastButtonData.buttons[ButtonRed] == 0:
            emergency()
        if data.buttons[ButtonStart] == 1 and lastButtonData.buttons[ButtonStart] == 0:
            takeoff()
        if data.buttons[ButtonBack] == 1 and lastButtonData.buttons[ButtonBack] == 0:
            land()
        if data.buttons[ButtonGreen] == 1 and lastButtonData.buttons[ButtonGreen] == 0:
            switchController()
    lastButtonData = data


def emergency():
    allcfs.emergency()


def takeoff():
    allcfs.takeoff(targetHeight=1.0, duration=3.0)
    timeHelper.sleep(3.0)
    for cf in allcfs.crazyflies:
        # pos = np.array(cf.initialPosition) + np.array([0, 0, 1.0])
        pos = np.array([0, 0, 1.0])
        cf.goTo(pos, 0, 2.0)


def land():
    allcfs.land(targetHeight=0.02, duration=3.5)


def switchController():
    global controller

    if controller == 2:
        controller = 3
    else:
        controller = 2

    try:
        allcfs.crazyflies[0].setParam("stabilizer/controller", controller)
        rospy.loginfo("Controller set to: " + str(controller))
    except:
        rospy.logwarn("Couldn't update controller!")


if __name__ == "__main__":
    swarm = Crazyswarm(parse_args = False)
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    rospy.Subscriber("joy", Joy, joyChanged)

    controller = allcfs.crazyflies[0].getParam("stabilizer/controller")
    rospy.loginfo("Controller set to: " + str(controller))

    rospy.spin()

    # allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    # timeHelper.sleep(1.5+Z)
    # for cf in allcfs.crazyflies:
    #     pos = np.array(cf.initialPosition) + np.array([0, 0, Z])
    #     cf.goTo(pos, 0, 1.0)

    # print("press button to continue...")
    # swarm.input.waitUntilButtonPressed()

    # allcfs.land(targetHeight=0.02, duration=1.0+Z)
    # timeHelper.sleep(1.0+Z)
