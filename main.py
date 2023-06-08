from mcf_build import MCFWindow, MCFCanvas, MCFInfo

if __name__ == '__main__':
    
    app = MCFWindow()
    app_2 = MCFWindow()
    app_canvas = MCFCanvas(app)
    app_info_manager = MCFInfo(app)
    app.mainloop()


