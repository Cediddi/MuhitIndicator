#!/usr/bin/python
#  -*- coding: utf-8 -*-

import os
from os import path
import webbrowser
import appdirs
import requests
import sys
import time
try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
except ImportError:
    print "\n".join((
        "PyQt4 is missing.",
        "  For linux, you should be able to install python-qt4 package.",
        "  For mac, you can install py-pyqt4 package with macports.",
        "  For windows, you can install from the official website of PyQt4",
        "    http://www.riverbankcomputing.com/software/pyqt/download"))
    exit(1)
import res_rc

last_beep = 0
app = QtGui.QApplication(sys.argv)

UPDATE_INTERVAL = 11000

ICONS = [
    QtGui.QIcon(":/muhit.png"),
    QtGui.QIcon(":/muhit_b.png")
]

CONFDIR = appdirs.user_config_dir("muhit_indicator")

if not path.exists(CONFDIR):
    if path.exists(CONFDIR):
        os.remove(CONFDIR)
    os.mkdir(CONFDIR)


class MuhitIndicator(QtGui.QSystemTrayIcon):
    def __init__(self, *__args):
        super(MuhitIndicator, self).__init__(*__args)
        self.icon_index = self.get_icon_index()
        self.setIcon(ICONS[self.icon_index])
        self.set_menu()
        QtCore.QTimer.singleShot(300, self.update_menu)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_menu)
        self.timer.start(UPDATE_INTERVAL)

    def set_menu(self):
        self.menu = QtGui.QMenu()

        separator = self.menu.addAction("-"*20)
        separator.setDisabled(True)
        update_item = self.menu.addAction("Update Now")
        icon_item = self.menu.addAction("Change Icon")
        quit_item = self.menu.addAction("Quit")

        update_item.triggered.connect(self.update_menu)
        icon_item.triggered.connect(self.inverse_icon)
        quit_item.triggered.connect(self.quit_app)

        self.setContextMenu(self.menu)

    def quit_app(self):
        self.timer.stop()
        QtCore.QCoreApplication.instance().quit()

    def inverse_icon(self):
        self.set_icon_index((self.icon_index+1) % 2)
        self.setIcon(ICONS[self.icon_index])

    @staticmethod
    def get_muhits():
        """Requests latest posts from muhit.geekyapar.com"""
        response = requests.get("http://muhit.geekyapar.com/latest.json")
        return response.json()

    def update_menu(self):
        global last_beep
        print "beep" + str(last_beep-time.time())
        last_beep = time.time()
        from functools import partial
        _open_web = lambda slug: webbrowser.open("http://muhit.geekyapar.com/t/"+slug)

        for item in self.menu.actions()[:-4]:
            self.menu.removeAction(item)

        muhits = self.get_muhits()["topic_list"]["topics"]
        actions = []
        for muhit in muhits:
            if len(actions) == 10:
                break

            if muhit["id"] == 8:
                continue

            item = self.menu.addAction(u"{title} //{uname}".format(
                title=muhit["title"], uname=muhit["last_poster_username"]))
            item.triggered.connect(partial(_open_web, muhit["slug"]))
            actions.append(item)

        self.menu.insertActions(self.menu.actions()[0], actions)

    def get_icon_index(self):
        """Reads icon index from config file"""
        if not path.exists(path.join(CONFDIR, "icon_index")):
            self.set_icon_index(0)
        with open(path.join(CONFDIR, "icon_index")) as f:
            output = f.read()
        if output.isdigit():
            return int(output)
        return 0

    def set_icon_index(self, index):
        """Saves icon index to config file"""
        with open(path.join(CONFDIR, "icon_index"), "wb") as f:
            f.write(str(index))
        self.icon_index = self.get_icon_index()


def main():
    muhit_indicator = MuhitIndicator()
    muhit_indicator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()