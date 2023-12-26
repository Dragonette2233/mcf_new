from PIL import Image, ImageChops, ImageGrab
import numpy as np
from skimage.metrics import structural_similarity as ssim
import mcf_data
import os

SCREENSHOT_FILE_PATH = os.path.join('.',
                                    'images_lib',
                                    'chars',
                                    'testfield',
                                    'screenshotPIL.png')

class RecognizedCharacters:
    def __init__(self, team_color: str) -> None:
        """
            Team color should be 'blue' or 'red'
            Calibration index shoult be 0, 1 or 2

        """
        self.characters = []
        self.team_color = team_color
        self.blue_path = os.path.join('.', 
                                'images_lib', 
                                'chars', 
                                'testfield', 
                                'blue', 'char_{indx}')
        self.red_path = os.path.join('.', 
                                'images_lib', 
                                'chars', 
                                'testfield', 
                                'red', 'char_{indx}')

        self.path_images_to_compare = {
            char: os.path.join('.', 
                                    'images_lib', 
                                    'chars', 
                                    'origin', 
                                    self.team_color, f'{char.lower().capitalize()}.png') 
                                    for char in mcf_data.ALL_CHAMPIONS_IDs.values()
            }
        self.grey_shade_compare = {
                    char: Image.open(img).convert('L') for char, img in self.path_images_to_compare.items()
        }
        self.arr_images_compare = {
            char: np.array(img) for char, img in self.grey_shade_compare.items()
        }

                                
    def screenshot(self):
        screen = ImageGrab.grab()
        screen.save(SCREENSHOT_FILE_PATH)

    def cut_from_screenshot(self):

        y = [160, 263, 366, 469, 572, 194, 297, 400, 503, 606]
        x = [45, 58, 1858, 1873]
        
        im = ImageGrab.grab()
        
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
            crops[a].save(self.blue_path.format(indx=a))
            crops[b].save(self.red_path.format(indx=a))
    
    def compare_shorts(self):

        main_images = [os.path.join('.', 
                                'images_lib', 
                                'chars', 
                                'testfield', 
                                self.team_color, 
                                f'char_{i}.png') for i in range(5)] # Путь к основному изображению (35x35)
        main_images_converted = [Image.open(img).convert('L') for img in main_images]

        # Подготовка массива основного изображения для последующего сравнения
        main_images_arr = [np.array(img) for img in main_images_converted]

        best_similarity = 0  # Переменная для хранения наилучшего сходства
        best_character = None

        simul_team = []
        # print(self.arr_images_compare)
        for main_img_arr in main_images_arr:

            for char, arr in self.arr_images_compare.items():
                similarity_index = ssim(main_img_arr, arr)

                # Если найдено более высокое сходство, сохраняем его и путь к изображению
                if similarity_index > best_similarity:
                    best_similarity = similarity_index
                    best_character = char

            if best_similarity > 0.5:
                simul_team.append(best_character)
            
            best_similarity = 0  # Переменная для хранения наилучшего сходства
            best_character = None
        
        return simul_team
        
    def run(self):
        # self.screenshot()
        self.cut_from_screenshot()
        recognized_list = self.compare_shorts()
        return recognized_list
    
   
print('Processing images...')
team_blue = RecognizedCharacters(team_color='blue')
team_red = RecognizedCharacters(team_color='red')
print('Processing done')

while True:
    input('Press any key to get lists')
    charlist_blue = team_blue.run()
    charlist_red = team_red.run()
    print(charlist_blue)
    print(charlist_red)

        
