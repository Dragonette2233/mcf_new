from PIL import Image, ImageGrab
import numpy as np
from skimage.metrics import structural_similarity as ssim
from mcf_build import MCFWindow
from mcf_data import SCREENSHOT_FILE_PATH
import os


# SCREENSHOT_FILE_PATH = os.path.join('.',
#                                     'images_lib',
#                                     'chars',
#                                     'testfield',
#                                     'screenshotPIL.png')

app_blueprint = MCFWindow()
class RecognizedCharacters:
    def __init__(self, team_color: str) -> None:
        """
            Team color should be 'blue' or 'red'
            Calibration index shoult be 0, 1 or 2

        """
        self.characters = []
        self.team_color = team_color
                                
    def screenshot(self):
        screen = ImageGrab.grab()
        screen.save(SCREENSHOT_FILE_PATH)

    def cut_from_screenshot(self):

        y = [160, 263, 366, 469, 572, 194, 297, 400, 503, 606]
        x = [45, 58, 1858, 1873]
        
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
            crops[a].save(app_blueprint.blue_path.format(indx=a))
            crops[b].save(app_blueprint.red_path.format(indx=a))
    
    def compare_shorts(self):

        main_images = [os.path.join('.', 
                                'images_lib', 
                                'chars', 
                                self.team_color, 
                                f'char_{i}.png') for i in range(5)] # Путь к основному изображению (35x35)
        main_images_converted = [Image.open(img).convert('L') for img in main_images]

        # Подготовка массива основного изображения для последующего сравнения
        main_images_arr = [np.array(img) for img in main_images_converted]

        best_similarity = 0  # Переменная для хранения наилучшего сходства
        best_character = None

        # simul_team = []

        if self.team_color == 'blue':
            arr_images_compare = app_blueprint.bluearr_images_compare
        else:
            arr_images_compare = app_blueprint.redarr_images_compare

        for main_img_arr in main_images_arr:

            for char, arr in arr_images_compare.items():
                similarity_index = ssim(main_img_arr, arr)

                # Если найдено более высокое сходство, сохраняем его и путь к изображению
                if similarity_index > best_similarity:
                    best_similarity = similarity_index
                    best_character = char

            if best_similarity > 0.5:
                self.characters.append(best_character)
            
            best_similarity = 0  # Переменная для хранения наилучшего сходства
            best_character = None
        
        # self.characters = simul_team
        
    def run(self):
        self.screenshot()
        self.cut_from_screenshot()
        self.compare_shorts()
        # return recognized_list

        
