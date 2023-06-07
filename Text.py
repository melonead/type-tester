from pygame import font

class Word:

    def __init__(self, text, font):
        self.color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.font = None
        self.text = text
        self.font = font
        self.typed_correctly = False
        self.last_sentence_word = False
    
    @property
    def width(self):
        return self._font_surface().get_width()

    def set_position(self, position):
        self.position = position
    
    def _font_surface(self):
        return self.font.render(self.text, True, self.color, self.background_color)
    
    def write(self, surface, position):
        surface.blit(self._font_surface(), self.position)

class Words:

    def __init__(self):
        self.words = []
        self.focus = 0
        self.sentence_height = 30
        self.next_line_position = [0, 0]
        self.number_of_correctly_typed_words = 0
    
    def add_word(self, word):
        self.words.append(word)
    
    def render_words(self, surface):
        for word in self.words:
            word.write(surface, word.position)

    def set_last_sentence_word(self):
        self.words[-1].last_sentence_word = True
    
    @property
    def focus_word(self):
        if self.focus >= len(self.words):
            return self.words[-1]
        return self.words[self.focus]
    
    @property
    def correctly_typed_words(self):
        return [word for word in self.words if word.typed_correctly == True]