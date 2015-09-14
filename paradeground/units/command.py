class CommandQueue(object):

    def __init__(self):
        self.queue = []
        self.active = None
    
    
    def add(self, command):
        self.queue.append(command)
        
    def clear(self):
        self.queue = []
        
    def update(self, dt):
        if self.active = None:
            if self.queue:  
                self.active = self.queue.pop(0)
        else:
            self.active()