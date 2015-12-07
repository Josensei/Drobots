#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
import time
from math import atan2, degrees, sqrt
from random import randint

Ice.loadSlice('Drobots.ice')
import drobots


class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("PlayerAdapter")
        adapter.activate()
        servant = PlayerI(broker, adapter)

        player_prx = adapter.add(servant, broker.stringToIdentity("player1"))
        print(str(player_prx))
        player = drobots.PlayerPrx.uncheckedCast(player_prx)

        game_prx = broker.stringToProxy(argv[1])
        print(str(game_prx))
        game = drobots.GamePrx.uncheckedCast(game_prx)

        nick = "josen" + str(randint(100, 999))

        if not game:
            raise RuntimeError('Invalid proxy')
        while 1:
            try:
                game.login(player, nick)
                break
            except drobots.GameInProgress:
                print("\n Lo están usando tron, espera un poco")
                time.sleep(2)
            except drobots.InvalidProxy:
                print("Proxy invalido")
            except drobots.InvalidName:
                print("No vale ese nombre jefe")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 1


class PlayerI(drobots.Player):
    def __init__(self, broker, adapter):
        self.broker = broker
        self.adapter = adapter

    def makeController(self, robot, current=None):
        print("make Controller")
        rb_servant = RobotController(robot)
        rb_proxy = self.adapter.add(rb_servant, self.broker.stringToIdentity("robotcontroller"))
        robot_controller = drobots.RobotControllerPrx.uncheckedCast(rb_proxy)

        return robot_controller

    def win(self, current=None):
            print("DiooooH, Hemoh Ganao")

    def lose(self, current=None):
            print("Foh, otra derrota")


class RobotController(drobots.RobotController):

    def __init__(self, robot):
        self.robot = robot

    def turn(self, current=None):

        SCAN = 1
        MOVE = 2
        ATTACK = 3
        action = None
        sAngle = 0

        if action.equals(None):

            action = MOVE


        if action == MOVE:

            position = self.robot.location()
            print(position.y, position.x)
            deltax = 500 - position.x
            deltay = 500 - position.y
            hip = sqrt(deltax**2 + deltay**2)

            angle = int(degrees(atan2(deltay, deltax)))
            if hip >= 100:
                speed = 100
            else:
                speed = 0
                action = SCAN

            self.robot.drive(angle, speed)

        if action == SCAN:
            wide = 18

            while 1:
                print(self.robot.scan(sAngle, wide))

                if (self.robot.scan(sAngle, wide)) == 1:

                    action = ATTACK
                    break
                else:
                    sAngle += wide

        if action == ATTACK:
            self.robot.cannon(sAngle, 90)







client = Client()
sys.exit(client.main(sys.argv))
