from .putil import *
from bge import logic as g

dark_blue = {
    "text_color": (1, 1, 1, 1),
    "text_dark": (0, 0, 0, 1),
    "control": (0.5, 0.5, 0.5, 1),
    "control_dark": (0.1, 0.1, 0.1, 1),
    "control_light": (0.9, 0.9, 0.9, 1),
    "control_grey": (0.7, 0.7, 0.7, 1),
    "button_normal": (0.5, 0.5, 0.5, 1),
    "button_hover": (0.5, 0.6, 1.0, 1),
    "button_clicked": (0.3, 0.3, 0.3, 1),
    "text_background": (0.3, 0.3, 0.3, 1)
}

dark_orange = {
    "text_color": (1, 1, 1, 1),
    "text_dark": (0, 0, 0, 1),
    "control": (0.5, 0.5, 0.5, 1),
    "control_dark": (0.1, 0.1, 0.1, 1),
    "control_light": (0.9, 0.9, 0.9, 1),
    "control_grey": (0.7, 0.7, 0.7, 1),
    "button_normal": (0.5, 0.5, 0.5, 1),
    "button_hover": (1.0, 0.6, 0.4, 1),
    "button_clicked": (0.3, 0.3, 0.3, 1),
    "text_background": (0.3, 0.3, 0.3, 1)
}

system = {
    "text_color": (0, 0, 0, 1),
    "text_dark": (1, 1, 1, 1),
    "control": (0.83, 0.815, 0.78, 1),
    "control_dark": (0.5, 0.5, 0.5, 1),
    "control_light": (1, 1, 0.8, 1),
    "control_grey": (0.7, 0.7, 0.7, 1),
    "button_normal": (0.83, 0.815, 0.78, 1),
    "button_hover": (0.2, 0.36, 0.65, 1),
    "button_clicked": (0.65, 0.65, 0.66, 1),
    "text_background": (1.0, 1.0, 1.0, 1.0)
}

hologram = {
    "text_color": (1, 1, 1, 1),
    "text_dark": (0, 0, 0, 1),
    "control": (0.1, 0.4, 0.6, 0.4),
    "control_dark": (0.0, 0.2, 0.4, 0.5),
    "control_light": (1, 1, 0.8, 1),
    "control_grey": (0.7, 0.7, 0.7, 1),
    "button_normal": (0.1, 0.4, 0.6, 0.4),
    "button_hover": (0.2, 0.36, 0.65, 1),
    "button_clicked": (0.65, 0.65, 0.66, 1),
    "text_background": (0.1, 0.4, 0.6, 0.4)
}

default_skin = {
    "PGUI_SKIN": 0,
    "button_normal": {
        "padding": [6, 6, 6, 6],
        "image": "//skins/default/button_normal.png"
    },
    "button_hover": {
        "padding": [6, 6, 6, 6],
        "image": "//skins/default/button_hover.png"
    },
    "button_click": {
        "padding": [6, 6, 6, 6],
        "image": "//skins/default/button_click.png"
    },
    "panel": {
        "padding": [5, 5, 5, 5],
        "image": "//skins/default/panel.png",
        "x_text_margin": 4
    },
    "panel_round": {
        "padding": [17, 13, 17, 13],
        "image": "//skins/default/round_panel.png",
        "x_text_margin": 15
    },
    "panel_dark": {
        "padding": [5, 5, 5, 5],
        "image": "//skins/default/panel_dark.png",
        "x_text_margin": 4
    },
    "panel_down": {
        "padding": [5, 5, 5, 5],
        "image": "//skins/default/panel_down.png",
        "x_text_margin": 4
    },
    "check_normal": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_normal.png"
    },
    "check_click": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_click.png"
    },
    "check_hover": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_hover.png"
    },
    "check_u_normal": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_u_normal.png"
    },
    "check_u_click": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_u_click.png"
    },
    "check_u_hover": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/check_u_hover.png"
    },
    "radio_normal": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_normal.png"
    },
    "radio_click": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_click.png"
    },
    "radio_hover": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_hover.png"
    },
    "radio_u_normal": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_u_normal.png"
    },
    "radio_u_click": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_u_click.png"
    },
    "radio_u_hover": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/radio_u_hover.png"
    },
    "select": {
        "padding": [2, 2, 2, 2],
        "image": "//skins/default/selected.png"
    },
    "track_normal": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/track_normal.png"
    },
    "track_click": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/track_click.png"
    },
    "track_hover": {
        "padding": [0, 0, 0, 0],
        "image": "//skins/default/track_hover.png"
    },
    "bar": {
        "padding": [2, 2, 2, 2],
        "image": "//skins/default/bar.png"
    }
}

default = system
