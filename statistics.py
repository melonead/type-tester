import time
import pygame
import sys
import math
from test_data import Database
from input import Input

class Statistics(Database):

    def __init__(self):
        Database.__init__(self)
        self.last_speed = 0
    
    def today_results(self, day=None, month=None, month_date=None, tim=None, year=None):
        
        if not (day and month and month_date and year):
            x = time.asctime().split(" ")
            if "" in x:
                x.remove("")
            day, month, month_date, tim, year = x
        return self.db_cursor.execute("""
        SELECT * FROM results 
        WHERE day = ? AND month = ? AND month_date = ?
        AND year = ?
        
        """, (day, month, month_date, year))
    
    @property
    def best_speed(self):
        res = self.db_cursor.execute("""
        SELECT MAX(speed) FROM results
        """)
        best = int(list(res)[0][0])
        return best
    
    @property
    def last_score(self):
        return self.last_speed
    
    
    @property
    def today_average(self):
        summation = sum([x[-1] for x in self.today_results()])
        if summation:
            return  summation / len(list(self.today_results()))
        else:
            return 0
    
    def average_result(self, data):
        summation = sum([x[-1] for x in data])
        if summation:
            return summation / len(data)
        else:
            return 0
               

class Statisticsui():

    def __init__(self, screen):
        self.statistics = Statistics()
        self.screen = screen

        self.days = dict(enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))

        self.month_days = {'Jan': (31, 'Dec'), 'Feb': (30, 'Jan'), 'Mar': (31, 'Feb'), 
        'Apr': (30, 'Mar'), 'May': (31, 'Apr'), 'Jun': (30, 'May'), 'Jul': (31, 'Jun'), 
        'Aug': (31, 'Jul'), 'Sep': (30, 'Aug'), 'Oct': (31, 'Sep'), 'Nov': (30, 'Oct'), 
        'Dec': (31, 'Nov')}

        self.origin = [60, self.screen.get_height() - 30]
        self.current_bar_position = self.origin.copy()
        self.bar_data = []
        self._bar_data()
        self.line_data = self._line_data()

        self.input = Input()

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 16)

        self.state = "statistics"

        self.break_from_loop = False
    
    def toggle(self):
        rect = pygame.Rect(50, 100, 20, 20)
        pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)
        
        mouse_rect = pygame.Rect(*pygame.mouse.get_pos(), 3, 3)
        if mouse_rect.colliderect(rect) and self.input.get_event() == 1:
            if self.state == "statistics":
                self.break_from_loop = True
    
    def check_escape(self, trigger):
        if trigger:
            return True
    
    def days_key(self, day):
        for key in self.days:
            if day == self.days[key]:
                return key
        

    def past_x_days(self, x):
        # infor needed = day, month, month_date, year
        relevant_data = list(time.asctime().split(" "))
        if "" in relevant_data:
            relevant_data.remove("")
        relevant_data = relevant_data[:3] + relevant_data[4:]
        day_index = int(self.days_key(relevant_data[0]))
        month_date = int(relevant_data[2])
        results = []
        for i in range(x):
            
            results.append(list(self.statistics.today_results(
                day=relevant_data[0], month=relevant_data[1], 
                month_date=relevant_data[2], tim=None, year=relevant_data[3]
                )))

            day_index -= 1
                
            if month_date > 1:
                month_date -= 1
            else:
                if relevant_data[1] == 'Jan':
                    relevant_data[-1] = str(int(relevant_data[-1]) - 1)
                month_date = self.month_days[relevant_data[1]][0]
                relevant_data[1] = self.month_days[relevant_data[1]][1]
                relevant_data[2] = month_date
                
            
            # print(relevant_data)
            
            if day_index >= 7:
                day_index = 0
            if day_index <= -1:
                day_index = 6
            
            if relevant_data:
                relevant_data[0] = self.days[day_index]
                relevant_data[2] = str(month_date)

        try:
            self.statistics.last_speed = results[0][0][-1]
        except IndexError:
            print(results)
            pass
        return results
    
    def process_results(self):
        results = self.past_x_days(7)
        averages = {}
        for day_res in results:
            if day_res:
                averages[day_res[0]] = self.statistics.average_result(day_res) 
            # averages.append(self.statistics.average_result(day_res))
        
        return averages
    
    def _bar_data(self):
        averages = self.process_results()
        for i, key in enumerate(averages):
            average_height = averages[key]
            if average_height:
                x = self.origin[0] + i * 50
                y = self.origin[1] - average_height * 6
                self.bar_data.append([x, y, average_height, key[0]])
    
    def _line_data(self):
        dat = []
        fin_dat = []
        averages = self.process_results()
        for i, key in enumerate(averages):
            average_height = averages[key]
            if average_height:
                x = self.origin[0] + i * 50
                y = self.origin[1] - average_height * 6
                dat.append([x, y - 300, average_height, key])
        
        for i, d in enumerate(dat):
            if i < len(dat) - 1:
                fin_dat.append([dat[i], dat[i + 1], d[-1][0]])
        
        return fin_dat
    
    def draw_bars(self):

        scale = 6
        for i, point_data in enumerate(self.bar_data):
            rect = pygame.Rect(point_data[:2][0] + 5 * i, 
            point_data[:2][1], 50, point_data[2] * scale
            )
            pygame.draw.rect(self.screen, (0, 255, 255), rect)

            tag = self.font.render(point_data[-1], True, (255, 255, 255))
            self.screen.blit(tag, (rect.x, rect.bottom + 10))

        v_1 = [self.bar_data[0][0], self.bar_data[0][1] - 50]
        v_2 = [self.bar_data[0][0], self.bar_data[0][1] + self.bar_data[0][2] * 6]
        pygame.draw.line(self.screen, (150, 150, 150), v_1, v_2, 3)

        pygame.draw.line(self.screen, (150, 150, 150), 
        [self.bar_data[0][0], self.bar_data[0][1] + self.bar_data[0][2] * 6], 
        [self.bar_data[0][0] + len(self.bar_data) * 55, self.bar_data[0][1] + self.bar_data[0][2] * 6], 3)

        x = v_2[0] - 30
        speed = 0
        for j, i in enumerate(list(range(0, int(v_2[1] - v_1[1]), scale))):
            
            y = v_2[1] - j * scale
            speed_tag = self.font.render(str(int(speed)), True, (255, 255, 255))
            
            if int(speed) % 6 == 0 or int(speed) == 0:
                self.screen.blit(speed_tag, (x, y - speed_tag.get_height() / 2))

            speed += 1
        
        heading_text = "Past Seven Days, From Left (Today or most recent) to Right"
        heading = self.font.render(heading_text, True, (255, 255, 255))
        self.screen.blit(heading, (self.origin[0], self.origin[1] - (v_2[1] - v_1[1] + 30)))
        pygame.draw.line(self.screen, (255, 255, 255), 
        (self.origin[0], self.origin[1] - (v_2[1] - v_1[1] + 10)),
        (self.origin[0] + 420, self.origin[1] - (v_2[1] - v_1[1] + 10))
        )
        

    def draw_line(self):
        for points_data in self.line_data:
            point1 = points_data[0][:2]
            point2 = points_data[1][:2]
            pygame.draw.line(self.screen, (0, 255, 0), point1, point2)

    
    def update(self):

        while True:

            if self.break_from_loop:
                break
            
            self.input.update()
            if self.input.quit:
                pygame.quit()
                sys.exit()

            self.toggle()
            self.draw_bars()
            self.draw_line()
            pygame.display.update()
        
if __name__ == "__main__":
    '''
    stats = Statistics()
    # print(stats.best_speed)

    statsui = Statisticsui()
    statsui.update()
    '''
    pass
