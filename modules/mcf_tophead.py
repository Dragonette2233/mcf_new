from modules import mcf_styles
from tkinter import Event, EventType
from mcf_data import (
    currentGameData, 
    MCFStorage,
    Switches
)
from mcf_build import MCFWindow
from mcf_threads import MCFThread


class MCF_Tophead:
    def __init__(self, master: MCFWindow, canvas) -> None:
        self.parent = master
        self.stats = mcf_styles.Button(display=master.button_images['Stats'],
                                       command=self.get_stats_teams_from_storage)
        self.magic = mcf_styles.Image(display=master.button_images['Magic'])
        self.magic_dropdown = (
                        mcf_styles.Button(display=master.button_images['ARAM'],
                                          command=lambda: MCFThread(func=self.pillow_icons_recognition).start()),
                        mcf_styles.Button(display=master.button_images['Rift'])
        )
        self.ground = mcf_styles.Image(display=master.button_images['Ground'])
        self.ground_dropdown = (
                        mcf_styles.Button(display=master.button_images['Kindred'],
                                          command=lambda: canvas.change_background_image('Kindred')),
                        mcf_styles.Button(display=master.button_images['Vayne'],
                                          command=lambda: canvas.change_background_image('Vayne')),
                        mcf_styles.Button(display=master.button_images['TF'],
                                          command=lambda: canvas.change_background_image('TF')),
                        mcf_styles.Button(display=master.button_images['Leblanc'],
                                          command=lambda: canvas.change_background_image('Leblanc')),
                        mcf_styles.Button(display=master.button_images['Annie'],
                                          command=lambda: canvas.change_background_image('Annie')),
                        mcf_styles.Button(display=master.button_images['Diana'],
                                          command=lambda: canvas.change_background_image('Diana')),
                        mcf_styles.Button(display=master.button_images['Custom'],
                                          command=lambda: canvas.change_background_image('Custom'))
                    )
        self.magic.bind('<Enter>', lambda e: [self.ground.config(bg='#652f87'), self.magic_dropdown_show(e)] )
        self.ground.bind('<Enter>', lambda e: [self.ground.config(bg='#652f87'), self.ground_dropdown_show(e)])
        
        canvas.bind('<Enter>', self.all_dropdown_hide)

        self.stats.place(x=0, y=0)
        self.magic.place(x=62, y=0)
        self.ground.place(x=439, y=0)

    def magic_dropdown_show(self, e: Event):
        for button, y in zip(self.magic_dropdown, range(20, (len(self.ground_dropdown) + 1) * 20, 20)):
            button.place(x=62, y=y)

    def ground_dropdown_show(self, e: Event):
        for button, y in zip(self.ground_dropdown, range(20, (len(self.ground_dropdown) + 1) * 20, 20)):
            button.place(x=439, y=y)

    def all_dropdown_hide(self, e: Event):
        for button in *self.ground_dropdown, *self.magic_dropdown:
            button.place_forget()
    
    def get_stats_teams_from_storage(self):

        teams = MCFStorage.get_selective_data(route=('Stats', ))
        self.parent.obj_aram.refill_characters_entrys(
            blue_chars=' '.join(teams['T1']),
            red_chars=' '.join(teams['T2'])
        )
    
    # def ssim_icons_recognition()

    def pillow_icons_recognition(self, ssim=True):
        # from ..deprecated.pillow_recognition import RecognizedCharacters as PilReco
        from .scripts.ssim_recognition import RecognizedCharacters as SsimReco
        self.parent.info_view.notification('Comparing icons...')

        if ssim:
            blue_team = SsimReco(team_color='blue')
            red_team = SsimReco(team_color='red')
        # else:
        #     blue_team = PilReco(team_color='blue', 
        #                                     calibration_index=Switches.calibration_index)
        #     red_team = PilReco(team_color='red', 
        #                                     calibration_index=Switches.calibration_index)
        blue_team.run()
        red_team.run()

        blue_count, red_count = len(blue_team.characters), len(red_team.characters)

        self.parent.obj_aram.refill_characters_entrys(
            blue_chars=' '.join(blue_team.characters),
            red_chars=' '.join(red_team.characters),
        )

        if any([blue_count < 5, red_count < 5]):
            self.parent.info_view.exception(f'Missing: {5 - blue_count} blue | {5 - red_count} red')
            
        currentGameData.highlight_game = '_'.join(sorted(blue_team.characters))