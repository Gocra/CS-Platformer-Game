import pygame
import json
from os import walk

# l = lower bound, v = variable, u = upper bound
def clamp(l, v, u):
    return l if l >= v else u if u <= v else v

def get_file_contents(filename):
    try:
        file = open(filename)
        contents = file.read()
        return contents
    except:
        raise Exception("Failed to open file")

def get_json_from_file(filename):
    contents = get_file_contents(filename)
    try:
        json_data = json.loads(contents)
        return json_data
    except:
        raise Exception("Invalid JSON Format")

def draw_text(screen, text, font, pos, color = (255,255,255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, dest=pos)

def update_json_file(filename, settings):
    data = get_json_from_file(filename)

    data["settings"]["volume"]["music"] = settings.get("volume").get("music")
    data["settings"]["volume"]["sfx"] = settings.get("volume").get("sfx")

    with open(filename, "w") as file:
        json.dump(data, file)

def getFilenamesInFolder(dir):
    filenames = next(walk(dir), (None, None, []))[2]  # [] if no file
    return filenames