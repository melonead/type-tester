from pygame import (font, draw, Rect)
from misc_funcs import load_image

# images
replay_button_im = load_image("images/replay.png")

class Ui:

    def __init__(self):
        self.font = font.SysFont('arial', 30)
        self.restart_pressed = False
    
    def show_time(self, time, surface, position):
        color = (0, 255, 0)
        time_suface = self.font.render(str(int(time)), True, color)
        surface.blit(time_suface, position)
    

    def highlight_current_word(self, surface, position, width, height):
        draw.rect(surface, (255, 255, 255),
        Rect(*position, width, height - 3), 1
        )
    
    def typing_preview(self, surface, preview_word):
        x_displacement = preview_word.width * 0.5
        position = [(surface.get_width() * 0.5) - x_displacement, 200]
        preview_surface = self.font.render(preview_word.text, True, (255, 255, 255))
        surface.blit(preview_surface, position)
        draw.rect(surface, (255, 255, 255), Rect(*position, preview_surface.get_width(), 30), 1)
    
    def declare_speed(self, speed, surface):
    
        position = [(surface.get_width() * 0.5), 250]
        speed_surface = self.font.render(str(round(speed)), True, (0, 255, 0))
        surface.blit(speed_surface, position)
    
    def score_data_declarations(self, surface, last_speed=0, best_speed=0):
        last_score_surface = self.font.render(f"last score: {str(last_speed)}", True, (255, 255, 255))
        best_speed_surface = self.font.render(f"best speed: {str(best_speed)}", True, (255, 255, 255))

        surface.blit(last_score_surface, (70, 200))
        surface.blit(best_speed_surface, (70, 240))
    
    def restart_button(self, surface, mouse_pos):
        restart_rect = Rect(40, 40, 35, 31)
        mouse_rect = Rect(*mouse_pos, 3, 3)
        if mouse_rect.colliderect(restart_rect):
            draw.rect(surface, (0, 255, 0), restart_rect)
            self.restart_pressed = True
        else:
            draw.rect(surface, (0, 255, 0), restart_rect, 1)
        
        surface.blit(replay_button_im, (restart_rect.x, restart_rect.y))


    def update(self, surface, time_position, current_word_position, 
                time, width, height, preveiw_word, mouse_pos, best_speed, last_speed):

        self.show_time(time, surface, time_position)
        self.highlight_current_word(surface, current_word_position, width, height)
        self.typing_preview(surface, preveiw_word)
        self.restart_button(surface, mouse_pos)
        self.score_data_declarations(surface, best_speed=best_speed, last_speed=last_speed)