import pygame as pg

class Timer:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.secs, self.mins, self.text = -1, 0, '00:00'.rjust(5)
        self.time = pg.time
        self.font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 35)
        

    def update_timer(self):
        
        self.secs += 1
            
        if self.secs // 60 != 0:
            self.mins += 1
            self.secs = 0
        if self.secs < 10:   
            self.text = ("0"+str(self.mins)+":0" + str(self.secs)).rjust(5) 
        else:
            self.text = ("0"+str(self.mins)+":"+str(self.secs)).rjust(5)
    
    def reset_timer(self):
        self.secs, self.mins, self.text = -1, 0, '00:00'.rjust(5)

    def total_secs(self):
        return self.secs + self.mins * 60
    
    def on_off_timer(self,bool):
        if bool:
            self.time.set_timer(pg.USEREVENT, 1000)
        else:
            self.time.set_timer(pg.USEREVENT, 0)
        
    def display_timer(self):
        self.display_surface.blit(self.font.render(self.text, True, 'white'), (275, 10))
        

    
    
   
    