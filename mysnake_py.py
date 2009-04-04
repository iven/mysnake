#!/usr/bin/python
#
# main.py
# Copyright (C) Iven Day 2008 <iven@gmail.com>
# 
# main.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
try:
    import pygtk
    pygtk.require ("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit (1)
from Model import SnakeModel
from Consts import *
    
class MySnake:
    def __init__ (self):
        # general init and connect
        self.gladefile = "mysnake.glade"
        self.wTree = gtk.glade.XML (self.gladefile)
        self.callback_dict = {"on_New_activate" : self.on_New_activate,
                    "on_Pause_activate" : self.on_Pause_activate,
                    "on_Stop_activate" : self.on_Stop_activate,
                    "on_About_activate" : self.on_About_activate,
                    "key_press_event" : self.key_press_event,
                    "gtk_main_quit" : gtk.main_quit}
        self.wTree.signal_autoconnect (self.callback_dict)
        self.MainWindow = self.wTree.get_widget ("MainWindow")
        self.AboutDialog = self.wTree.get_widget ("AboutDialog")
        self.GameArea = self.wTree.get_widget ("GameArea")
        self.ScoreLabel = self.wTree.get_widget ("ScoreLabel")
        self.CountLabel = self.wTree.get_widget ("CountLabel")
        # main loop
        gtk.main ()
        
    # callbacks
    def on_New_activate (self, widget, data = None):
        self.model = SnakeModel (self, 20, 30)
        self.model.start ()

    def on_Pause_activate (self, widget, data = None):
        self.model.pause ()

    def on_Stop_activate (self, widget, data = None):
        self.model.stop ()

    def on_About_activate (self, widget, data = None):
        self.AboutDialog.run ()
        self.AboutDialog.hide ()

    # keybindings
    def key_press_event (self, widget, event, data = None):
        keydict = {
                UP : "changedirection",
                DOWN : "changedirection",
                LEFT : "changedirection",
                RIGHT : "changedirection",
                PGUP : "changespeed",
                PGDOWN : "changespeed",
                SPACE : "pause"}
        key = event.keyval
        if key in keydict.keys() and hasattr (self, "model"):
            getattr (self.model, keydict [key]) (key)

    def game_over (self):
        "show game over dialog"
        GameOverDialog = gtk.MessageDialog (self.MainWindow,
                gtk.DIALOG_MODAL,
                gtk.MESSAGE_INFO,
                gtk.BUTTONS_CLOSE,
                "Your score is " + str (self.model.score))
        GameOverDialog.set_modal (True)
        GameOverDialog.show ()
        GameOverDialog.connect ("response", self.hide_dialog)

    def hide_dialog (self, widget, data = None):
        "hide game over dialog when closing"
        widget.hide ()

    def updatescore (self):
        "update ScoreLabel and CountLabel when repaint"
        self.ScoreLabel.set_text ("Score : " + str (self.model.score))
        self.CountLabel.set_text ("MoveCount : " + str (self.model.countMove))
        
    def repaint (self):
        # get ready for painting
        canvas = self.GameArea.window
        gc = self.GameArea.get_style ().fg_gc [gtk.STATE_NORMAL]
        cmap = self.GameArea.get_colormap ()
        # allocate a color
        color = cmap.alloc_color ("white")
        # set it as foreground color
        gc.set_foreground (color)
        # draw a rectangle (as background)
        canvas.draw_rectangle (gc, True, 0, 0, 200, 300)
        # draw food
        color = cmap.alloc_color ("red")
        gc.set_foreground (color)
        x, y = self.model.food
        canvas.draw_rectangle (gc, True,  x * 10, y * 10, 10, 10)
        # draw snake
        color = cmap.alloc_color ("black")
        gc.set_foreground (color)
        for (x, y) in self.model.nodes:
            canvas.draw_rectangle (gc, True, x * 10, y * 10, 10, 10)
        # update score
        self.updatescore ()
    
if __name__ == "__main__":
    #gtk.gdk.threads_init()
    snake = MySnake ()
