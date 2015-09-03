import event

class Observer(object):
    def on_notify(self, unit, event):
        if event == "Event":
            pass
            
class Watched(object):
    def __init__(self):
        self.observers = []
        
    def add_observer(self, obs):
        self.observers.append(obs)
        
    def remove_observer(self, obs):
        self.observers.remove(obs)
        
    def notify(self, event):
        for obs in self.observers:
            obs.on_notify(event)