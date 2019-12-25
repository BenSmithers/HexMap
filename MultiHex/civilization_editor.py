## #!/usr/bin/python3.6m

from MultiHex.core import Hexmap, save_map, load_map
from MultiHex.map_types.overland import OHex_Brush
from MultiHex.tools import clicker_control, basic_tool, entity_brush, region_brush

# need these to define all the interfaces between the canvas and the user
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog

from MultiHex.guis.civ_gui import editor_gui_window

import sys # basic command line interface 
import os  # basic file-checking, detecting os
  

class editor_gui(QMainWindow):
    """
    This class creates the gui for the main world editor.
    It imports the gui definitions from the guis folder and plugs buttons, switches, and sliders  in to various functions 

    Some important TOOLS used are 
        clicker control
        hex brush
        selector
    All are defined in the tools folder 

    It also needs a  
        Hexmap
    object which defines the hexmap it shows and edits. 

    """

    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = editor_gui_window()
        self.ui.setupUi(self)
        
        # writes hexes on the screen

        # manages the writer and selector controls. This catches clicky-events on the graphicsView
        self.scene = clicker_control( self.ui.graphicsView, self )
        self.entity_control = entity_brush(self)
        self.writer_control = OHex_Brush(self)
        self.biome_control = region_brush(self, 'biome')

        self.scene._active = self.entity_control

        # Allow the graphics view to follow the mouse when it isn't being clicked, and associate the clicker control with the ui 
        self.ui.graphicsView.setMouseTracking(True)
        self.ui.graphicsView.setScene( self.scene )

        self.ui.actionQuit.triggered.connect( self.go_away )
        self.ui.actionSave.triggered.connect( self.save_map )
        self.ui.actionSave_As.triggered.connect( self.save_as)
        
        #buttons
        self.ui.loc_button_1.clicked.connect( self.new_location_button )
        
        self.file_name = ''
        self.main_map = Hexmap()

    def new_location_button(self):
        self.scene._active = self.entity_control 
        self.entity_control.prep_new(0)

    def go_away(self):
        # show the main menu and disappear 
        self.parent().show()
        # need to clear the canvas too!
        self.hide()
        self.entity_control.clear()
        self.writer_control.clear()
        self.biome_control.clear()

        self.scene._held = None

    def save_map(self):
        save_map( self.main_map, self.file_name)
        self.ui.label_2.setText("Saved!")

    def save_as(self):
        """
        Opens a dialog to accept a filename from the user, then calls the save_map function
        """
        self.file_name = QFileDialog.getSaveFileName(None, 'Save HexMap', './saves', 'HexMaps (*.hexmap)')
        self.save_map()



    def prep_map(self, file_name ):
        """
        Needs to be alled when the map is first loaded. This actually has Qt draw all the hexes in the map's hexmap
        """
        self.scene.clear()
            
        self.ui.graphicsView.update()
        self.main_map = load_map( file_name )
        self.file_name = file_name 
        
        print("redrawing")
        for ID in self.main_map.catalogue: 
            self.writer_control.redraw_hex( ID )

        if 'biome' in self.main_map.rid_catalogue :
            for rid in self.main_map.rid_catalogue['biome']:
                self.biome_control.redraw_region( rid )
            
        self.writer_control.redraw_rivers()
        


