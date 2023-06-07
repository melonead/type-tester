import pygame

class Input:

    def __init__(self):

        self.right_mouse_click = False
        self.left_mouse_click = False
        self.quit = False
        self._event = None
        self.trigger_event = False
        self.event_queue = []

    @property
    def shift(self):
        return self.get_event() in [pygame.K_RSHIFT, pygame.K_LSHIFT]
    
    @property
    def control(self):
        return self.get_event() in [pygame.K_RCTRL, pygame.K_LCTRL]
    
    def add_to_event_queue(self):
        if self.shift or self.control:
            self.event_queue.append(self.get_event())
    
    def get_event(self):
        return self._event
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                self.trigger_event = True
                self._event = event.key
            
            if event.type == pygame.KEYUP:
                if self._event in [pygame.K_RCTRL, pygame.K_LCTRL]:
                    self.event_queue = []
                self.trigger_event = False
                self._event = None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._event = event.button
            
            if event.type == pygame.MOUSEBUTTONUP:
                self._event = None
        
        self.add_to_event_queue()          