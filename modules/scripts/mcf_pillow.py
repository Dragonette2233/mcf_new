from PIL import Image, ImageChops, ImageGrab
from mcf_data import MCFStorage
import os

def convert_to_greyshade(img):
    return Image.open(img).convert('L')

def is_league_stream_active():

    stream_image = ImageGrab.grab()
    compare_slice_main = Image.open(os.path.join('.', 'images_lib', 'build_compare.png'))
    compare_slice_active = stream_image.crop((1675, 839, 1764, 887))
    compare_slice_active = compare_slice_active.convert(compare_slice_main.mode)
    diff_between_pixels = ImageChops.difference(compare_slice_main, compare_slice_active).getdata()
    diff_int = sum((sum(i) for i in diff_between_pixels))
    if diff_int == 0:
        return True
    
def generate_scoreboard():
    from modules.scripts.ssim_recognition import ScoreRecognition
    screen = ImageGrab.grab()
    score = screen.crop((681, 7, 1261, 99))
    scoredata = ScoreRecognition.screen_score_recognition(image=score)
    MCFStorage.save_score(score=scoredata)
    
    items_build = screen.crop((602, 850, 1334, 1078))
    items_build.save(os.path.join('images_lib', 'buildcrop.png'))
    return scoredata