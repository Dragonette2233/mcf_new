from mcf_build import MCFWindow

app_blueprint = MCFWindow()


def disable_button_while_running(object_, buttons: tuple[str]):
    """
    This decortator accepts tuple of buttons in str representation
    object_ parameter accepts "obj_gamechecker", "obj_aram", "obj_featured" only
    
    """
    # objects_ - variable name of MCF object (canvas.obj_aram, canvas.obj_featured, canvas.obj_match_c)
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            [app_blueprint.__getattribute__(object_)
             .__getattribute__(button).configure(state='disabled') for button in buttons]
            
            func(self, *args, **kwargs)
            
            [app_blueprint.__getattribute__(object_)
             .__getattribute__(button).configure(state='normal') for button in buttons]

        return wrapper
    return decorator