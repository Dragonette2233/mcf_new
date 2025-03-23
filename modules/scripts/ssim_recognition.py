from PIL import Image, ImageGrab
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
from mcf_build import MCFWindow
from mcf_data import (
    SCREENSHOT_FILE_PATH,
    GTIME_DATA_PATH,
    BLUE_SCORE_PATH,
    RED_SCORE_PATH,
    BLUE_TOWER_PATH,
    RED_TOWER_PATH
)

app_blueprint = MCFWindow()
class RecognizedCharacters:
    def __init__(self, team_color: str) -> None:
        """
            Team color should be 'blue' or 'red'

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

        best_similarity = 0
        best_character = None

        if self.team_color == 'blue':
            arr_images_compare = app_blueprint.bluearr_images_compare
        else:
            arr_images_compare = app_blueprint.redarr_images_compare

        for main_img_arr in main_images_arr:

            for char, arr in arr_images_compare.items():
                similarity_index = ssim(main_img_arr, arr)

                if similarity_index > best_similarity:
                    best_similarity = similarity_index
                    best_character = char

            # if best_similarity > 0.65:
            self.characters.append(best_character)
            
            best_similarity = 0 
            best_character = None
        
        # self.characters = simul_team
        
    def run(self):
        self.screenshot()
        self.cut_from_screenshot()
        self.compare_shorts()
        # return recognized_list

        
class ScoreRecognition:
    
    gold_shift = 1
    
    @classmethod
    def extract_digit(cls, filename):
        return filename.split('_')[1].split('.')[0]
    
    @classmethod
    def get_compare(cls, cut_image, type, position, team=None):

        match type, position, team:
            case 'tw_access', pos, None:
                main_image_arr = np.array(Image.open(os.path.join('.', 'ssim_score_data', 'tw_health', 'access.png')))
                similarity_index = ssim(main_image_arr, cut_image)
                if similarity_index > 0.75:
                    return True
                else:
                    return False
            case 'thp', pos, team:
                main_images = [Image.open(os.path.join('.', 'ssim_score_data', 'tw_health_n', f'{pos}', f'{i}.png')) for i in range(10)]
            case 'gold', pos, None:
                main_images = [Image.open(os.path.join('.', 'ssim_score_data', 'gold', 'red', f'{i}.png')) for i in range(10)]
                # print(cut_image.width)
            
            case 'gtime', 0, None:
                # images = {}
                for filename in os.listdir(GTIME_DATA_PATH):
                    if filename.endswith(".png"):
                        # Открываем изображение из каталога и конвертируем в градации серого
                        img_path = os.path.join(GTIME_DATA_PATH, filename)
                        img = Image.open(img_path).convert('L')
                        img_np = np.array(img)

                        # Рассчитываем SSIM
                        similarity_index = ssim(img_np, cut_image, win_size=3)

                        # Если SSIM больше 0.75, выводим результат и завершаем скрипт
                        if similarity_index > 0.75:
                            return cls.extract_digit(filename)
                else:
                    return ''
                            
                # main_images = [Image.open(, f'{i}.png')) for i in range(10)]
            
            # case 'gtime', 0, None:
            #     main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(3)]
            #     print([img.size for img in main_images])
            # case 'gtime', 1 | 3, None:
            #     main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(10)]
            # case 'gtime', 2, None:
            #     main_images = [Image.open(os.path.join(GTIME_DATA_PATH, f'{position}', f'{i}.png')) for i in range(6)]
            case 'score', pos, 'blue':
                main_images = [Image.open(os.path.join(BLUE_SCORE_PATH.format(pos=pos), f'{i}.png')) for i in range(10)]
            case 'score', pos, 'red':
                main_images = [Image.open(os.path.join(RED_SCORE_PATH.format(pos=pos), f'{i}.png')) for i in range(10)]
            case 'towers', pos, 'blue':
                main_images = [Image.open(os.path.join(BLUE_TOWER_PATH, f'{i}.png')) for i in range(5)]
            case 'towers', pos, 'red':
                main_images = [Image.open(os.path.join(RED_TOWER_PATH, f'{i}.png')) for i in range(5)]
            case _:
                print(type, team, position)
                raise ValueError('Undefined value in get_compare()') 
                # return
        
        main_images_arr = [np.array(img) for img in main_images]
        
        # np.array()

        for idx, compare_img in enumerate(main_images_arr):
            # print(compare_img.size)
            # print(cut_image.size)
            # print(cut_image, compare_img)
            similarity_index = ssim(compare_img, cut_image, win_size=3)

            # Если найдено более высокое сходство, сохраняем его и путь к изображению
            if similarity_index > 0.75:
                return idx
            # else:
            #     print(idx, similarity_index)
            
        else:
            # print(similarity_index)
            return ''
    
    @classmethod
    def towers_healh_recognition(cls, image):
        # 20, 850, 59, 902
        if not cls.get_compare(np.array(image.crop((20, 850, 59, 902)).convert('L')), 'tw_access', 0):
            return False

        # NEW: 3 pixels left of X
        t1_health = [
            cls.get_compare(np.array(image.crop((101, 857, 105, 864)).convert('L')), 'thp', 0),
            cls.get_compare(np.array(image.crop((105, 857, 109, 864)).convert('L')), 'thp', 1),
            cls.get_compare(np.array(image.crop((112, 857, 116, 864)).convert('L')), 'thp', 2)
        ]
        
        # OLD DEPRECATED
        # t1_health = [
        #     cls.get_compare(np.array(image.crop((104, 857, 108, 864)).convert('L')), 'thp', 0),
        #     cls.get_compare(np.array(image.crop((110, 857, 114, 864)).convert('L')), 'thp', 1),
        #     cls.get_compare(np.array(image.crop((115, 857, 119, 864)).convert('L')), 'thp', 2)
        # ]

        print(t1_health)
        

        round_value = 295
        
        if t1_health[0] == '':
            round_value = 2950
       
        t1 = ''.join([str(i) for i in t1_health])

        t1_res = int(t1) if t1 !='' else 0

        f_result = int((t1_res / round_value) * 100)
        if f_result > 100:
            return int(f_result / 10)
        return f_result
        # return int((t1_res / round_value) * 100)
    
    @classmethod
    def gold_recognition(cls, image):
        
        print(cls.gold_shift)
        
        blue_gold = (
            cls.get_compare(np.array(image.crop((126 - cls.gold_shift, 12, 134 - cls.gold_shift, 28)).convert('L')), 'gold', 0),
            cls.get_compare(np.array(image.crop((136 - cls.gold_shift, 12, 144 - cls.gold_shift, 28)).convert('L')), 'gold', 1),
            cls.get_compare(np.array(image.crop((151 - cls.gold_shift, 12, 159 - cls.gold_shift, 28)).convert('L')), 'gold', 2),
        )
        red_gold = (
            cls.get_compare(np.array(image.crop((430 - cls.gold_shift, 12, 438 - cls.gold_shift, 28)).convert('L')), 'gold', 0),
            cls.get_compare(np.array(image.crop((440 - cls.gold_shift, 12, 448 - cls.gold_shift, 28)).convert('L')), 'gold', 1),
            cls.get_compare(np.array(image.crop((455 - cls.gold_shift, 12, 463 - cls.gold_shift, 28)).convert('L')), 'gold', 2),
        )
        
        
        return (blue_gold, red_gold)
    
    @classmethod
    def screen_score_recognition(cls, image=None) -> dict[str, int]:

        screen = ImageGrab.grab()
        if not image:
            # screen.width
            image = screen.crop((681, 7, 1261, 99))
        
        # old before 28.08.2024
        # final_time = [
        #     cls.get_compare(np.array(image.crop((264, 72, 271, 85)).convert('L')), 'gtime', 0),
        #     cls.get_compare(np.array(image.crop((273, 72, 280, 85)).convert('L')), 'gtime', 1),
        #     cls.get_compare(np.array(image.crop((287, 72, 294, 85)).convert('L')), 'gtime', 2),
        #     cls.get_compare(np.array(image.crop((296, 72, 304, 85)).convert('L')), 'gtime', 3)
        # ]
        # final_time = [
        #     cls.get_compare(np.array(image.crop((266, 72, 272, 84)).convert('L')), 'gtime', 0),
        #     cls.get_compare(np.array(image.crop((275, 72, 281, 84)).convert('L')), 'gtime', 0),
        #     cls.get_compare(np.array(image.crop((288, 72, 294, 84)).convert('L')), 'gtime', 0),
        #     cls.get_compare(np.array(image.crop((297, 72, 303, 84)).convert('L')), 'gtime', 0)
        # ]
        
        # print(final_time)
        
        # for i, val in enumerate(final_time):
        #     if val == '':
        #         final_time[i] = 0

        blue_gold, red_gold = cls.gold_recognition(image=image)
        
        if '' in blue_gold or '' in red_gold:
            cls.gold_shift = 1
            blue_gold, red_gold = cls.gold_recognition(image=image)
        else:
            cls.gold_shift = 0
        
        print(blue_gold, red_gold)
        
        blue_golds = ''.join([str(i) for i in blue_gold[0:2]]) + ',' + str(blue_gold[2]) if '' not in blue_gold else "< 10k"
        red_golds = ''.join([str(i) for i in red_gold[0:2]]) + ',' + str(red_gold[2]) if '' not in red_gold else "< 10k"
        
        # print(cls.gold_shift)
        
        # blue_score = [
        #     cls.get_compare(np.array(image.crop((225, 18, 242, 41)).convert('L')), 'score', 0, 'blue'),
        #     cls.get_compare(np.array(image.crop((243, 18, 260, 41)).convert('L')), 'score', 1, 'blue')
        # ]

        # red_score = [
        #     cls.get_compare(np.array(image.crop((309, 18, 328, 41)).convert('L')), 'score', 0, 'red'),
        #     cls.get_compare(np.array(image.crop((329, 18, 347, 41)).convert('L')), 'score', 1, 'red')
        # ]

        blue_towers = cls.get_compare(np.array(image.crop((60, 13, 75, 29)).convert('L')), 'towers', 0, 'blue')
        red_towers = cls.get_compare(np.array(image.crop((498, 13, 514, 29)).convert('L')), 'towers', 0, 'red')

        # image.crop((87, 853, 94, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '2.png')) # work
            #image.crop((95, 853, 102, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '9.png')) # work
            # image.crop((103, 853, 110, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '3.png')) # work

        # blue_t1_health = [
        #     cls.get_compare(np.array(image.crop((87, 853, 94, 866)).convert('L')), 'thp', 0, 'blue'),
        #     cls.get_compare(np.array(image.crop((95, 853, 102, 866)).convert('L')), 'thp', 1, 'blue'),
        #     cls.get_compare(np.array(image.crop((103, 853, 110, 866)).convert('L')), 'thp', 2, 'blue')
        # ]
        # red_t1_health = [
        #     cls.get_compare(np.array(image.crop((87, 853, 94, 866)).convert('L')), 'thp', 0, 'red'),
        #     cls.get_compare(np.array(image.crop((95, 853, 102, 866)).convert('L')), 'thp', 1, 'red'),
        #     cls.get_compare(np.array(image.crop((103, 853, 110, 866)).convert('L')), 'thp', 2, 'red')
        # ]


        # print(len(blue_gold))
        # print(len(red_gold))     
        

        # str_final_time = f'{final_time[0]}{final_time[1]}:{final_time[2]}{final_time[3]}' # XX:XX
        # minutes, seconds = map(int, str_final_time.split(':'))
        # blue_kills = ''.join([str(i) for i in blue_score])
        # red_kills = ''.join([str(i) for i in red_score])


        # total_seconds = minutes * 60 + seconds

        # if blue_score[0] == 0:
        #     blue_score.remove(0)
        
        gamedata = {
            'blue_towers': blue_towers,
            'red_towers': red_towers,
            'blue_gold': blue_golds,
            'red_gold': red_golds,
            'is_active': True
        }

        cls.gold_shift = 0
        return gamedata

    @classmethod
    def collecting_ssim_data(cls, **kwargs):

        image = ImageGrab.grab()
        image = image.crop((681, 7, 1261, 99))
        # image.save('.\\susu.png')

        if 'bl_gl_0' in kwargs:
            image.crop((126, 12, 134, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', f'{kwargs["bl_gl_0"]}.png'))
            # print('saved')
        if 'bl_gl_1' in kwargs:
            image.crop((136, 12, 144, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', '1', f'{kwargs["bl_gl_1"]}.png'))
        if 'bl_gl_2' in kwargs:
            image.crop((151, 12, 159, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', '2', f'{kwargs["bl_gl_2"]}.png'))

        if 'rd_gl_0' in kwargs:
            image.crop((430, 12, 438, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', f'{kwargs["rd_gl_0"]}.png'))
        if 'rd_gl_1' in kwargs:
            image.crop((440, 12, 448, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', '1', f'{kwargs["rd_gl_1"]}.png'))
        if 'rd_gl_2' in kwargs:
            image.crop((455, 12, 463, 28)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', '2', f'{kwargs["rd_gl_2"]}.png'))
        # if 'bl_gl_0' in kwargs:
        #     image.crop((807, 19, 815, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', f'{kwargs["bl_gl_0"]}.png'))
        #     # print('saved')
        # if 'bl_gl_1' in kwargs:
        #     image.crop((817, 19, 825, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', '1', f'{kwargs["bl_gl_1"]}.png'))
        # if 'bl_gl_2' in kwargs:
        #     image.crop((832, 19, 840, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'blue', '2', f'{kwargs["bl_gl_2"]}.png'))

        # if 'rd_gl_0' in kwargs:
        #     image.crop((1111, 19, 1119, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', f'{kwargs["rd_gl_0"]}.png'))
        # if 'rd_gl_1' in kwargs:
        #     image.crop((1121, 19, 1129, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', '1', f'{kwargs["rd_gl_1"]}.png'))
        # if 'rd_gl_2' in kwargs:
        #     image.crop((1136, 19, 1144, 35)).convert('L').save(os.path.join('.', 'ssim_score_data', 'gold', 'red', '2', f'{kwargs["rd_gl_2"]}.png'))
        if 'tw_alt_hp' in kwargs:
            ...
            print('THIS IS')
            # image.crop((91, 853, 98, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_3.png')) # work
            # image.crop((99, 853, 106, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_5.png')) # work
            # image.crop((107, 853, 114, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_55.png')) # work
            image.crop((104, 857, 108, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_9.png')) # new work
            image.crop((110, 857, 114, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_8.png')) # new work
            image.crop((115, 857, 119, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'alt_4.png')) # new work
            # image.crop((111, 853, 118, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '5.png')) # work
        if 'tw_access' in kwargs:
            # 20, 850, 59, 902
            image.crop((20, 850, 59, 902)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', 'access.png'))
        if 'tw_hp' in kwargs:
            ...
            # image.crop((104, 857, 108, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health_n', '0', f'{kwargs["tw_hp"]}.png')) # new work
            image.crop((110, 857, 114, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health_n', '1', f'{kwargs["tw_hp"]}.png')) # new work
            image.crop((115, 857, 119, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health_n', '2', f'{kwargs["tw_hp"]}.png')) # new work
            image.crop((121, 857, 125, 864)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health_n', '4.png')) # new work

            # image.crop((87, 853, 94, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '2.png')) # work
            #image.crop((95, 853, 102, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '9.png')) # work
            # image.crop((103, 853, 110, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '3.png')) # work
            # image.crop((111, 853, 118, 866)).convert('L').save(os.path.join('.', 'ssim_score_data', 'tw_health', '5.png')) # work
        if 'tw_icon_0' in kwargs:
            ...
        if 'tw_icon_1' in kwargs:
            ...

        if 'bl_tw' in kwargs:
            image.crop((60, 13, 75, 29)).convert('L').save(os.path.join(BLUE_TOWER_PATH, f'{kwargs["bl_tw"]}.png')) # work
        if 'rd_tw' in kwargs:
            image.crop((498, 13, 514, 29)).convert('L').save(os.path.join(RED_TOWER_PATH, f'{kwargs["rd_tw"]}.png')) # work

        if 'bl_sc_0' in kwargs:
            image.crop((225, 18, 242, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_blue', 'score_0', f'{kwargs["bl_sc_0"]}.png')) # work
        if 'bl_sc_1' in kwargs:
            image.crop((243, 18, 260, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_blue', 'score_1', f'{kwargs["bl_sc_1"]}.png')) # work

        if 'rd_sc_0' in kwargs:
            image.crop((309, 18, 328, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_red', 'score_0', f'{kwargs["rd_sc_0"]}.png')) # work
        if 'rd_sc_1' in kwargs:
            image.crop((329, 18, 347, 41)).convert('L').save(os.path.join('.', 'ssim_score_data', 'team_red', 'score_1', f'{kwargs["rd_sc_1"]}.png')) # work

        if 'g_0' in kwargs:
            image.crop((266, 72, 272, 84)).convert('L').save(os.path.join(GTIME_DATA_PATH, f'{kwargs["g_0"]}.png')) # # 6x13
        if 'g_1' in kwargs:
            image.crop((275, 72, 281, 84)).convert('L').save(os.path.join(GTIME_DATA_PATH, f'{kwargs["g_1"]}.png'))
        if 'g_2' in kwargs:
            image.crop((288, 72, 294, 84)).convert('L').save(os.path.join(GTIME_DATA_PATH, f'{kwargs["g_2"]}.png'))
        if 'g_3' in kwargs:
            image.crop((297, 72, 303, 84)).convert('L').save(os.path.join(GTIME_DATA_PATH, f'{kwargs["g_3"]}.png'))