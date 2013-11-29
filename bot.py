#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import random
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class TfwBot(object):
    # Some basic variables used to configure the bot
    server = "irc.freenode.net" # Server
    port = 6667
    channel = "##middach"
    botnick = "YumBotto"

    restaurants = [
        'Weserhaus',
        'Scharfrichter',
        'Mekong Delta',
        'Koreahaus',
        'Maribondo',
        'Döner',
        'Kabuki Sushi Bar',
        'Bolero',
        'Bäcker',
        'Prima Pasta',
        'Pizza Hut'
    ]

    def _send(self, command):
        log.debug(command)
        self.ircsock.send(command)


    def ping(self):
        self._send("PONG :pingis\n")

    def sendmsg(self, chan, msg):
        self._send("PRIVMSG " + chan + " :" + msg + "\n")

    def joinchan(self, chan):
        self._send("JOIN " + chan + "\n")

    def hello(self):
        self._send("PRIVMSG " + self.channel + " :Hello!\n")

    def error(self):
        self._send("PRIVMSG " + self.channel + " :Nö!\n")

    def weserhaus(self):
        """
        Weserhaus Menu
        """
        url = 'http://dashboard.tfw.ag:8888/api/weserhaus'
        data = requests.get(url).content

        menuString = data.replace("undefined(", "")
        menuString = menuString.replace(")", "")
        # to list
        menuString = json.loads(menuString)

        try:
            self.sendmsg(self.channel, 'Im Weserhaus gibt es heute:')
            for item in menuString:
                msg = item['name'] + ' fuer ' + item['price']
                self.sendmsg(self.channel, msg.encode('utf-8'))
        except Exception, e:
            self.error()
            log.exception("Error:")

    # random restaurant
    def randomRestaurant(self):
        msg = 'Wie wär\'s mit ' + random.choice(self.restaurants) + '?'
        try:
            self.sendmsg(self.channel, msg)
        except Exception, e:
            self.error()
            print "Error:", e

    # random xkcd comic
    def randomXkcd(self):
        req = requests.get("http://dynamic.xkcd.com/random/comic/")
        data = req.text
        soup = BeautifulSoup(data)
        img = soup.select("#comic img")[0]['src']
        try:
            self.sendmsg(self.channel, img)
        except Exception, e:
            self.error()
            print "Error:", e

    # magic 8 ball
    def magic8ball(self):
        answers = ['Es ist sicher', 'Es ist eindeutig', 'Zweifelsfrei', \
            'Ja - Absolut!', 'Du kannst dich darauf verlassen', 'So wie ich es sehe ja',\
            'Höchstwahrscheinlich', 'Sieht gut aus', 'Die Zeichen stehen gut', 'Ja', \
            'Antwort verschwommen, versuch\'s noch mal', 'Frag\' später noch mal', 'Ich sollte es dir besser nicht sagen', \
            'Das lässt sich jetzt nicht voraussehen', 'Konzentrier\' dich und frag mich noch mal', 'Ich würde nicht darauf zählen', \
            'Meine Antwort ist Nein', 'Meine Quellen sagen Nein', 'Die Aussichten sind nicht so gut', \
            'Zweifelhaft'
        ]
        sendmsg(channel, random.choice(answers))

    # random restaurant
    def showHelp(self):
        self.sendmsg(self.channel, 'Es gibt zur Zeit folgende Commands:')
        self.sendmsg(self.channel, '!middach')
        self.sendmsg(self.channel, '!weserhaus')
        self.sendmsg(self.channel, '!xkcd')
        self.sendmsg(self.channel, '!8ball')
        self.sendmsg(self.channel, '!help')

    def __init__(self):
        # connect to server
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((self.server, self.port))
        # identify
        self._send("USER %s %s bla :%s\r\n" % (self.botnick, self.server, self.botnick))
        self._send("NICK %s\r\n" % self.botnick)
        #  and join channel
        self.joinchan(self.channel)

    def __call__(self):
        while True:
            # receive data from the server
            ircmsg = self.ircsock.recv(2048)
            # remove any unnecessary linebreaks.
            ircmsg = ircmsg.strip('\n\r')
            log.debug(ircmsg)
            # print what's coming from the server

            if ircmsg.lower().find(
                ":Hallo " + self.botnick) != -1:
                self.hello()

            if ircmsg.find("PING :") != -1:
                self.ping()

            if ircmsg.lower().find("!weserhaus") != -1:
                self.weserhaus()

            if ircmsg.lower().find("!middach") != -1:
                self.randomRestaurant()

            if ircmsg.lower().find("!xkcd") != -1:
                self.randomXkcd()

            if ircmsg.lower().find("!8ball") != -1:
                magic8ball()

            if ircmsg.lower().find("!help") != -1:
                self.showHelp()


if __name__ == '__main__':
    TfwBot()()
