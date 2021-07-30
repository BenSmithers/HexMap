from enum import Enum 
from collections import deque

from MultiHex.objects import Mobile, Entity 
from MultiHex.clock import Clock, Time
from MultiHex.core import Hexmap, Hex

from MultiHex.logger import Logger

from pandas import DataFrame, read_csv
from copy import copy
import os
import sys

"""
Notes for future Ben! All hexmap edits need to be done through these actions
Tools will construct an action object and pass it through the action manager
The clicker control will have the action manager
The action manager needs a "do now" feature

None of these do any drawing of a map! They EXCLUSIVELY edit things ON the map
"""


def get_base_dir():
    # set up the save directory
    if sys.platform=='linux':
        basedir = os.path.join(os.path.expandvars('$HOME'),'.local','MultiHex')
    elif sys.platform=='darwin': #macOS
        basedir = os.path.join(os.path.expandvars('$HOME'),'MultiHex')
    elif sys.platform=='win32' or sys.platform=='cygwin': # Windows and/or cygwin. Not actually sure if this works on cygwin
        basedir = os.path.join(os.path.expandvars('%AppData%'),'MultiHex')
    else:
        Logger.Fatal("{} is not a supported OS".format(sys.platform), NotImplementedError)

    return(basedir)

class mapActionItem(Enum):
    move = 1

class actionDrawTypes(Enum):
    hex = 1
    region = 2
    entity = 3
    path = 4

class MapEvent:
    def __init__(self,recurring=None, **kwargs):
        """
        An event used by the Action Manager. 

        recurring - a Time object. Represents how frequently the event happens. 'None' for one-time events. When this kind of event is triggered, a new one is auto-queued 
        kwargs - arguments specific to this kind of event. Varies 
        """

        if recurring is not None:
            if not isinstance(recurring, Time):
                Logger.Fatal("If recurring, arg must be {}, not {}".format(Time, type(recurring)), TypeError)
        self.recurring = recurring

        self.brief_desc = "" # will be used on the event list
        self.long_desc = ""

        # whether or not the event should appear in the Event List
        self._show = True

        self.needed = []
        self.verify(kwargs)
    
    def verify(self,kwargs):
        """
        This function verifies we received all the arguments
        """
        for entry in self.needed:
            if entry not in kwargs:
                Logger.Fatal("Missing entry {} in kwargs".format(entry), ValueError)

    @property
    def show(self):
        return(self._show)

class MapAction(MapEvent):
    """
    These are MapEvents that actually effect the map. We call these when they come up. 

    We have a drawtype entry to specify whether or not this Action has an associated redraw command 
    """
    def __init__(self, recurring=None, **kwargs):
        self._drawtype = False
        MapEvent.__init__(self,recurring=None, **kwargs)

    
    @property
    def drawtype(self)->bool:
        return self._drawtype

    def draw(self)->tuple:
        """
        This will return a tuple describing 
        """
        if not self.drawtype:
            raise NotImplementedError("Must override base implementation")

    def __call__(self, map, actionskip=False):
        """
        This function is accessed through the `action(map)` syntax

        This then does the action defined by this object, and returns the inverse of the action.
        The actionskip argument tells the action to not do, and just return the inverse 
        """
        raise NotImplementedError("Must override base implementation!")

class NullAction(MapAction):
    """
    An action used to do nothing 
    """
    def __init__(self, **kwargs):
        MapAction.__init__(self, recurring=None, **kwargs)
    def __call__(self, map, actionskip=False):
        pass

class Add_Remove_Hex(MapAction):
    def __init__(self, **kwargs):
        """
        This action addds hexes to the map where there was either 
            1. a hex already there 
            2. no hex already there 
        """
        MapAction.__init__(self, recurring=None,**kwargs)

        self.needed = ["hexID","hex"]
        self.verify(kwargs)
        self.newHex = kwargs["hex"]
        self.hexID = kwargs["hexID"]
        if not isinstance(self.newHex, Hex) and (self.newHex is not None):
            Logger.Fatal("AddHex actions require {} or {}, not {}".format(Hex, None, type(self.newHex)), TypeError)

        self._drawtype = True
    
    def draw(self):
        return(actionDrawTypes.hex, "", self.hexID)

    def __call__(self, map, actionskip=False):
        if (self.hexID not in map.catalog) and (self.newHex is None):
            Logger.Fatal("Tried removing hex from tile that doesn't exist.", ValueError)
        
        # we set aside what was already there (if anything), and tell the map to get rid of it. 
        # then we register the new hex and make the inverter function 
        if self.hexID in map.catalog:
            old_hex = map.catalog[self.hexID]
            if not actionskip:
                map.remove_hex(self.hexID)
        else:
            old_hex = None

    
        if isinstance(self.newHex, Hex) and (not actionskip):
            map.register_hex(self.newHex, self.hexID)
        
        return Add_Remove_Hex(hex=old_hex, hexID=self.hexID)

class AdjustExistingHex(MapAction):
    def __init__(self, **kwargs):
        """
        This action changes an existing hex to have the given set of parameters
        """
        MapAction.__init__(self, recurring=None,**kwargs)

        self.needed = ["hexID","params"]
        self.verify(kwargs)
        self.hexID = kwargs["hexID"]
        self.params = kwargs["params"]
        if not isinstance(self.params, dict):
            Logger.Fatal("Adjust hex actions require {}, not {}".format(dict, type(self.params)))

        self._drawtype = True
    
    def draw(self):
        return(actionDrawTypes.hex, "", self.hexID)

    def __call__(self, map, actionskip=False):
        if self.hexID not in map.catalog:
            Logger.Fatal("Tried adjusting hex that doesn't exist.", ValueError)
        
        # we set aside what was already there (if anything), and tell the map to get rid of it. 
        # then we register the new hex and make the inverter function 
        old_params = {}
        for key in self.params:
            old_params[key] = copy(getattr(map.catalog[self.hexID], key))
            if not actionskip:
                setattr(map.catalog[self.hexID], key, self.params[key])
        
        return AdjustExistingHex(params=old_params, hexID=self.hexID)

class Add_Remove_Entity(MapAction):
    def __init__(self, **kwargs):
        """
        This action adds entities to the map where there was either 
            1. a Hex already there or 
            2. there was no hex already there 
        """
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed = ["eID", "entity"]
        self.verify(kwargs)

class EditEntity(MapAction):
    """
    Edits one entity parameter 
    """
    def __init__(self, **kwargs):
        """
        This action edits an entity 
        """
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed = ["eID", "parameter", "new_value"]
        self.verify(kwargs)
        self.eID = kwargs["eID"]
        self.parameter = kwargs["parameter"]
        self.new_value = kwargs["new_value"]

    def __call__(self, map:Hexmap, actionskip=False):
        if not self.eID in map.eid_catalog:
            Logger.Warn("Action Failed! {} not in catalog".format(self.eID))
            return
        else:
            entity = map.eid_catalog[self.eID]
            inverse = EditEntity(eID=self.eID, parameter=self.parameter, new_value=getattr(entity, self.parameter))
            if not actionskip:
                setattr(entity, self.parameter, self.new_value)
            return inverse 



class MetaAction(MapAction):
    """
    A combination of actions treated as one. 

    This would be useful when working with large brushes 
    """
    def __init__(self, *args,**kwargs):
        MapAction.__init__(self,**kwargs)
        for arg in args:
            if not isinstance(arg, MapAction):
                Logger.Fatal("Cannot make MetaAction with object of type {}".format(type(arg)), TypeError)
        if len(args)==0:
            Logger.Fatal("Cannot make a meta action of no actions {}".format(len(args)))
        
        self._actions = [arg for arg in args]

    def add_to(self, action:MapAction):
        if action is None:
            return
        
        if not isinstance(action, NullAction):
            if isinstance(action, MetaAction):
                self._actions += action._actions
            else:
                self._actions.append(action)

    @property
    def actions(self):
        return self._actions

    def __call__(self, map:Hexmap, actionskip=True):
        """
        The actions are already done, so just make the inverses and return them in inverse-order 
        """
        inverses = [action(map, actionskip) for action in self.actions][::-1]
        return MetaAction(*inverses)

class MapMove(MapAction):
    def __init__(self, **kwargs):
        """
        Move an entity from one place to another. 

        Required 
            - eID (entity ID)
            - to   (hexID for where we're moving the entity)
        """
        MapAction.__init__(self, recurring=None, **kwargs)
        self.needed =["eID", "to"]
        self.verify(kwargs)
        
        self.eid = kwargs["eID"]
        self.to = kwargs["to"]

    def __call__(self, map, actionskip=False):
        if not isinstance(map, Hexmap):
            Logger.Fatal("Can only act on {}, not {}".format(Hexmap, type(map)), ValueError)

        inverse = MapMove(eID = self.eid, to=map.eid_catalog[self.eid].location)
        if not actionskip:
            map.eid_catalog[self.eid].set_location(self.to)

        return(inverse)


class ActionManager:
    """
    This keeps track of upcoming events (and actions) and the time.
    It allows you to add new events and 

    This is made before on launch before the map is loaded, so it doesn't do anything until the map is loaded. 
    """
    def __init__(self, parent_map=None):
        self._queue = []

        self.clock = Clock()
        self._configured = False
        if parent_map is not None:
            self.configure_with_map(parent_map)

        self.database_dir = get_base_dir()
        self.database_filename = "event_database.csv"

        # we keep a list of Actions' inverses we've done, so we can always go back through
        self.n_history_max = 50 
        self.redo_history = deque()
        self.undo_history = deque()

        self._making_meta = False
        self._meta_inverses = []

    def configure_with_map(self, parent_map:Hexmap):
        self._configured = True
        self._parent = parent_map

    def add_to_meta(self, action:MapAction):
        """
        For these special meta actions, we do the things as they are sent. Once we do something non-meta related (or call the finish meta function), 
        we bundle these up in a single MetaAction that can be reversed as one. 

        This is important for doing sweeping brush strokes! 
        """
        self._making_meta = True
        if not isinstance(action, NullAction):
            inverse = action(self.parent)
            self._meta_inverses.append(inverse)


    def finish_meta(self):
        """
        Use the inverses we've collected to make a new MetaEvent, then manually pop that on our undo queue

        return the draw thingy from the meta action 
        """
        this_meta = MetaAction(*self._meta_inverses[::-1])
            
        self.undo_history.appendleft(this_meta)
        while len(self.undo_history)>self.n_history_max:
            self.undo_history.pop()

            if len(self.redo_history)!=0:
                self.redo_history=deque()

        self._meta_inverses=[]
        self._meta = None
        self._making_meta = False

    def do_now(self, event: MapAction, ignore_history = False, action_skip=False):
        """
        Tells the action manager to do an action
            - ignore history, bypass the undo/redo functionality. Useful with MetaActions. We can do those actions as we build up the MetaAction
                    then pass the MetaAction through here again and use it with the undo/redo
            - action skip, adds this to the undo/redo queues without actually doing anything. Used with the above! 
        """
        if not self._configured:
            return

        if self._making_meta:
            self.finish_meta()


        inverse = event(self.parent, action_skip)
        if not ignore_history:
            self.undo_history.appendleft(inverse)
            while len(self.undo_history)>self.n_history_max:
                self.undo_history.pop()
            
            if len(self.redo_history)!=0:
                self.redo_history = deque()

        return inverse
    
    def _generic_do(self, list1, list2):
        """
        This handles the undo and redo functions

        When you do something in a deque, you call the 0th entry, invert the action, and append it at the start of other deque.
        This is done to give undo/redo functionality.
        """
        if not self._configured:
            return []
        if len(list1)==0:
            return []
        
        #does the action, stores inverse 
        inverse = list1[0](self.parent, False)
        
        # check if we'll need to redraw anything 
        draw = None
        if list1[0].drawtype:
            draw = [list1[0].draw(),]
        if isinstance(list1[0], MetaAction):

            draw = [entry.draw() for entry in filter(lambda ex:ex.drawtype, list1[0].actions)]

        list2.appendleft(inverse)
        while len(list2)>self.n_history_max:
            list2.pop()
        
        list1.popleft()

        # check if the thing we did has a draw command, if it does, pass that up
        return draw

    def undo(self):
        if self._making_meta:
            self.finish_meta()
        
        return self._generic_do(self.undo_history, self.redo_history)
    def redo(self):
        return self._generic_do(self.redo_history, self.undo_history)



    def add_event(self, event, time):
        if not isinstance(event, MapEvent):
            Logger.Fatal("Can only register {} type events, not {}".format(MapEvent, type(event)), TypeError)
        if not isinstance(time, Time):
            Logger.Fatal("Expected {} for time, not {}.".format(Time, type(time)), TypeError)

        if len(self.queue)==0:
            self._queue.append( [time, event] )
        else:
            if time<self.queue[0][0]:
                self._queue.insert(0, [time,event])
            elif time > self.queue[-1][0]:
                self._queue.append([time,event])

            else:
                loc = 0
                while time > self.queue[loc][0]:
                    loc+=1

                self._queue.insert(loc, [time,event])

    def skip_to_next_event(self):
        if len(self.queue)==0:
            return

        data = self.queue[0]

        # If this is an action, do it. Otherwise it's an event, nothing is done. 
        if isinstance(data[1], MapAction):
            data[1].do()
            if data[1].recurring is not None:
                self.add_event(data[1], data[0]+data[1].recurring)

        self.clock.skip_to(data[0])
        self.queue.pop(0)

    def skip_to_time(self, time):
        if len(self.queue)!=0:
            while time<self.queue[0][0]:
                # moves time up to the next event, does the action (if there is one), and pops the event from the queue
                self.skip_to_next_event()

                if len(self.queue)==0:
                    break

        self.clock.skip_to(time)


    @property
    def queue(self):
        return(self._queue)

    @property 
    def parent(self):
        return(self._parent)
