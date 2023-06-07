import pygame
import sys
import time
from Text import Word, Words
from input import Input
from ui import Ui
from test_data import Database
from statistics import Statisticsui

pygame.init()

dependent_puncuations = {';': ':',',': '"', '[': '{', ']': '}', 
'/': '?', '.': '>', ',': '<', '1': '!', '2': '@', '3': '#', '4': '$',
'5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_',
'=': '+', '\\': '|'}

main_punctuations = list(dependent_puncuations.keys())
punctuation = main_punctuations + list(dependent_puncuations.values())

class App:

    def __init__(self):
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, 0, 32)
        self.input = Input()
        self.text = ''
        self.words = Words()
        self.file_data = open('text_data.txt', 'r')
        self.text_data = []
        self.load_words('text_data.txt')
        self.base_position = [(self.screen_size[0] - self.get_firstline_len()) * 0.5, 60]
        self.create_word_objects(self.text_data[:3])
        self.time = 0
        self.initial_frame = time.time()
        self.ui = Ui()

        self.words_to_remove = []
        self.sixty_seconds = 60

        self.database = Database()
        self.database.create_table()
        self.result_stored = False

        self.statsui = Statisticsui(self.screen)

        self.state = "main"
        self.states = ["main", "statistics"]

        self.statistics_main_toggle = False
    
    def toggle(self):
        rect = pygame.Rect(50, 100, 20, 20)
        pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)
        
        mouse_rect = pygame.Rect(*self.mouse_pos, 3, 3)
        if mouse_rect.colliderect(rect) and self.input.get_event() == 1:
            self.input._event = None
            if self.state == self.states[0]:
                self.state = self.states[1]
            else:
                self.state = self.states[0]
    
    def new_session(self):
        if self.input.get_event() == 1 and self.ui.restart_pressed:
            self.__init__()

    def get_firstline_len(self):
        l = 0
        for word in self.text_data[0].split(' '):
            surf = self.font_type.render(word, True, (255, 255, 255))
            l += (surf.get_width() + 6)
        return l
    
    @property
    def font_type(self):

        font = pygame.font.SysFont('arial', 24)
        return font
    
    def parse_text(self, text):
        text_components = []
        if (text[0] not in punctuation and text[-1] not in punctuation) or text in punctuation:
            text_components.append(text)
        else:
            if text[0] in punctuation and text[-1] in punctuation:
                text_components.append(text[0])
                text_components.append(text[1:-1])
                text_components.append(text[-1])
            else:
                if text[0] in punctuation:
                    text_components.append(text[0])
                    text_components.append(text[1:])
                else:
                    text_components.append(text[:-1])
                    text_components.append(text[-1])
        
        return text_components
    
    def make_word(self, text_components):
        position_displacement = [0, 0]
        len_text_components = len(text_components)
        words = []
        if len_text_components == 1:
            word = Word(text_components[0], self.font_type)
            words.append(word)
        else:
            if len_text_components == 2:
                if text_components[0] in punctuation:
                    punctuation_1 = Word(text_components[0], self.font_type)
                    word = Word(text_components[1], self.font_type)
                    words.append(punctuation_1)
                    words.append(word)
                else:
                    word = Word(text_components[0], self.font_type)
                    punctuation_1 = Word(text_components[-1], self.font_type)
                    words.append(word)
                    words.append(punctuation_1)
            elif len_text_components == 3:
                punctuation_1 = Word(text_components[0], self.font_type)
                word = Word(text_components[1], self.font_type)
                punctuation_2 = Word(text_components[2], self.font_type)
                words.append(punctuation_1)
                words.append(word)
                words.append(punctuation_2)
        return words
    
    def position_word(self, word, position_displacement):
        text_components = self.parse_text(word)
        words = self.make_word(text_components)

        if len(words) == 1:
            word = words[0]
            word.set_position([self.base_position[0] + position_displacement[0],
            self.base_position[1] + position_displacement[1]])
            self.words.add_word(word)
            position_displacement[0] += (word.width + 6)
        elif len(words) == 2:
            word1 = words[0]
            word2 = words[1]
            word1.set_position([self.base_position[0] + position_displacement[0],
            self.base_position[1] + position_displacement[1]])

            word2.set_position(word1.position.copy())
            word2.position[0] += word1.width
            self.words.add_word(word1)
            self.words.add_word(word2)
            position_displacement[0] += (word1.width + word2.width + 6)
        elif len(words) == 3:
            word1 = words[0]
            word2 = words[1]
            word3 = words[2]

            word1.set_position([self.base_position[0] + position_displacement[0],
            self.base_position[1] + position_displacement[1]])

            word2.set_position(word1.position.copy())
            word2.position[0] += word1.width

            word3.set_position(word2.position.copy())
            word3.position[0] += word2.width

            self.words.add_word(word1)
            self.words.add_word(word2)
            self.words.add_word(word3)

            position_displacement[0] += (word1.width + word2.width + word3.width + 6)
        
    
    def load_sentence(self):

        line = self.file_data.readline().strip()

        position_displacement = [0, 0]

        if line != '':
            for x, word in enumerate(line.split(' ')):
                self.position_word(word, position_displacement)
                
            self.words.set_last_sentence_word()
    
    def remove_sentence(self):
        for word in self.words_to_remove:
            self.words.words.remove(word)
        self.words_to_remove = []
        self.words.focus = 0
    
    def add_words_to_remove(self):
        self.words_to_remove.append(self.words.words[self.words.focus])
    
    def create_word_objects(self, lines):

        position_displacement = [0, 0]

        for y, line in enumerate(lines):
            position_displacement[1] = y * self.words.sentence_height
            for x, word in enumerate(line.split(' ')):
                self.position_word(word, position_displacement)

            self.words.set_last_sentence_word()
            position_displacement[0] = 0
        
        self.base_position[1] = (y + 2) * self.words.sentence_height

    
    @property
    def one_sentence_up(self):
        return self.words.words[self.words.focus - 1].last_sentence_word
    
    def move_1_sentence_up(self):
        for word in self.words.words:
            word.position[1] -= self.words.sentence_height

    
    def render_text(self):
        self.screen.fill((0, 0, 0))
        self.words.render_words(self.screen)

    
    def load_words(self, path):

        for i in range(3):
            line = self.file_data.readline().strip()
            if line == '':
                break
            else:
                self.text_data.append(line)

    def construct_word(self):
        
        if self.input.trigger_event:
            self.input.trigger_event = False

            if self.input.get_event() > 32 and self.input.get_event() <= 126:
                character = chr(self.input.get_event())
                
                if self.input.event_queue:
                    if self.input.event_queue[0] in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        if character in main_punctuations:
                            character = dependent_puncuations[character]
                        character = character.upper()
                        self.input.event_queue = []

                self.text += character
            else:
                pass

            if self.input.get_event() == pygame.K_SPACE:
                self.add_words_to_remove()
                self.compare()
                self.move_to_next_word()
                if self.one_sentence_up:
                    self.move_1_sentence_up()
                    self.load_sentence()
                    self.remove_sentence()
            elif self.input.get_event() == pygame.K_BACKSPACE:
                self.erase()
    
    def compare(self):
        if self.text == self.words.focus_word.text:
            self.words.number_of_correctly_typed_words += 1
            self.words.focus_word.typed_correctly = True
            self.words.focus_word.color = (0, 255, 0)
            self.text = ''
        else:
            self.words.focus_word.color = (255, 0, 0)
            self.text = ''
    
    def focus_against_typed(self):
        if self.text:
            if self.text != self.words.focus_word.text[:len(self.text)]:
                self.words.focus_word.background_color = (255, 0, 0)
            else:
                self.words.focus_word.background_color = (0, 0, 0)

        if self.text == self.words.focus_word.text[:len(self.text)]:
            self.words.focus_word.background_color = (0, 0, 0)
    
    def calculate_time(self):
        dt = time.time() - self.initial_frame
        self.initial_frame = time.time()
        self.time += dt
    
    @property
    def time_up(self):
        return self.time >= self.sixty_seconds
    
    @property
    def speed(self):
        return self.words.number_of_correctly_typed_words / (int(self.time) / 60)
    
    @property
    def typing_finished(self):
        if self.words.focus >= len(self.words.words):
            return True
        return False

    
    def erase(self):
        if self.input.event_queue:
            if self.input.event_queue[0] in [pygame.K_RCTRL, pygame.K_LCTRL]:
                self.text = ''
                self.input.event_queue = []
        else:
            self.text = self.text[:-1]
    
    def move_to_next_word(self):
        self.words.focus += 1
    
    @property
    def preview_word(self):
        return Word(self.text, self.font_type)
    
    @property
    def mouse_pos(self):
        return pygame.mouse.get_pos()
    
    def store(self):
        if self.time_up and not self.result_stored:
            self.result_stored = True
            data = time.asctime().split(" ")
            if "" in data:
                data.remove('')
            self.database.insert_row(*data, str(round(self.speed)))

    def update(self):
        while True:

            self.input.update()
            if self.input.quit:
                pygame.quit()
                sys.exit()
            
            if self.state == "main":
                self.render_text()
                if not self.time_up:
                    self.construct_word()
                    self.calculate_time()
                    self.focus_against_typed()

                    # will probably remove later if I remember
                    if self.words.words[self.words.focus - 1].background_color == (255, 0, 0):
                        self.words.words[self.words.focus - 1].background_color = (0, 0, 0)

                self.ui.update(self.screen, [self.screen.get_width() / 2, 
                (self.screen.get_height() / 2) + 40], 
                self.words.focus_word.position, self.sixty_seconds - self.time,
                self.words.focus_word.width, self.words.sentence_height, 
                self.preview_word, self.mouse_pos, 0, 0)
        
                self.store()
                if self.time_up:
                    self.ui.declare_speed(self.speed, self.screen)

                self.new_session()
            elif self.state == self.states[1]:
                self.screen.fill((0, 0, 0))
                self.statsui.update()
                self.state = "main"
                self.statsui.break_from_loop = False
                self.statsui.state = "statistics"
            self.toggle()
            pygame.display.update()

app = App()
app.update()
