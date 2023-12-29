
from PIL import ImageChops, Image, ImageGrab
from mcf_data import (
    ALL_CHAMPIONS_IDs,
    SCREENSHOT_FILE_PATH,
)

class RecognizedCharacters:
    def __init__(self, team_color: str, calibration_index: int = 0) -> None:
        """
            Team color should be 'blue' or 'red'
            Calibration index shoult be 0, 1 or 2

        """
        self.characters = []
        self.__team_color = team_color
        self.__calibration = calibration_index
    
    def screenshot(self):
        screen = ImageGrab.grab()
        screen.save(SCREENSHOT_FILE_PATH)

    def get_pixels_diff(self, main_, secondary_, team):

        char_from_screen = Image.open(f"images_lib\\chars\\{team}\\char_{secondary_}.png")
        char_from_base = Image.open(f"images_lib\\chars\\origin\\{team}\\{main_}.png")
        diff_between_pixels = ImageChops.difference(char_from_screen, char_from_base).getdata()
        
        return diff_between_pixels

    def cut_from_screenshot(self):

        y = [160, 263, 366, 469, 572, 194, 297, 400, 503, 606]
        x = [45, 58, 1858, 1873]
        
        if self.__calibration == 1:
            for i in range(10): y[i] = y[i] - 1
        elif self.__calibration == 2:
            for i in range(2): x[i] = x[i] + 1
            for i in range(2, 4): x[i] = x[i] - 1
        
        im = Image.open(SCREENSHOT_FILE_PATH)
        
        if im.size != (1920, 1080):
            im = im.resize((1920, 1080))
        
        crops = (
            im.crop((x[0], y[0], x[1], y[5])), 
            im.crop((x[0], y[1], x[1], y[6])),
            im.crop((x[0], y[2], x[1], y[7])), 
            im.crop((x[0], y[3], x[1], y[8])),
            im.crop((x[0], y[4], x[1], y[9])),

            im.crop((x[2], y[0], x[3], y[5])), 
            im.crop((x[2], y[1], x[3], y[6])),
            im.crop((x[2], y[2], x[3], y[7])), 
            im.crop((x[2], y[3], x[3], y[8])),
            im.crop((x[2], y[4], x[3], y[9]))
        )

        for a, b in tuple(zip(range(0,5), range(5, 10))):
            crops[a].save(f'images_lib\\chars\\blue\\char_{a}.png')
            crops[b].save(f'images_lib\\chars\\red\\char_{a}.png')
    
    def compare_shorts(self):
        champions_list = tuple(i.title() for i in ALL_CHAMPIONS_IDs.values() if i.title() != 'Monkeyking')
        
        selection = {}
        for i in range(0, 5):
            for char in champions_list:
                colors =  self.get_pixels_diff(char, i, self.__team_color)
                # numpy_colors = numpy.array(colors)
                final_value = sum((sum(i) for i in colors))
                
                if final_value < 37000:
                    if char == 'Kayn_b': char = 'Kayn'
                    selection[char] = final_value
                    
        while len(selection) > 5:
            key_del = max(selection, key=lambda k: selection[k])
            del selection[key_del]
        # print(f'{self.__team_color.capitalize()}: {selection}')
        self.characters = list(selection)
        
    def run(self):
        self.screenshot()
        self.cut_from_screenshot()
        self.compare_shorts()
    
   
    

