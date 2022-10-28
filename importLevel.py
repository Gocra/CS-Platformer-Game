import pygame
import json
import ast
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def getJSONFromFile(filename):
    contents = getFileContents(filename)
    try:
        data = json.loads(contents)
        return data
    except:
        raise Exception("Invalid JSON Format")
    
def getFileContents(filename):
    try:
        file = open(filename)
        contents = file.read()
        return contents
    except:
        raise Exception("Failed to open file")

def importLevel(filename):
    JSONData = getJSONFromFile(filename)

    return JSONData.get('levelMap', []), JSONData.get('playerArray', []), JSONData.get('enemyArray', []), JSONData.get('interactableTilesArray', [])

def convertFromStringImportData(levelMap, playerArray, enemyArray, interactableTilesArray):
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            levelMap[y][x]['rect'] = convertDictToPygameRect(ast.literal_eval(levelMap[y][x]['rect']))
    
    for i in range(len(playerArray)):
        playerArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(playerArray[i]['rect']))

    for i in range(len(enemyArray)):
        enemyArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(enemyArray[i]['rect']))

    for i in range(len(interactableTilesArray)):
        interactableTilesArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(interactableTilesArray[i]['rect']))
    
    return levelMap, playerArray, enemyArray, interactableTilesArray

def convertDictToPygameRect(rect):
    return pygame.Rect(rect.get("x"), rect.get("y"), rect.get("w"), rect.get("h"))

def assignTileByIndex(levelMap):
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            if levelMap[y][x]['tileIndex'] != -1:
                levelMap[y][x]['tile'] = tiles[levelMap[y][x]['tileIndex']]
    
    return levelMap

def convertTileMap2Tiles(tilemap):
    global TILE_SIZE, TILEMAP_TILE_SIZE
    tiles = []
    tilemapWidth, tilemapHeight = tilemap.get_width(), tilemap.get_height()
    
    for y in range(int(tilemapHeight / TILEMAP_TILE_SIZE)):
        for x in range(int(tilemapWidth / TILEMAP_TILE_SIZE)):
            tile = pygame.Surface([TILEMAP_TILE_SIZE, TILEMAP_TILE_SIZE], pygame.SRCALPHA).convert_alpha()
            tile.blit(tilemap, (0,0), (x * TILEMAP_TILE_SIZE, y * TILEMAP_TILE_SIZE, TILEMAP_TILE_SIZE, TILEMAP_TILE_SIZE))
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
            tiles.append(tile)
    
    return tiles

tilemapImage = pygame.image.load("assets/tilemap.png")
tiles = convertTileMap2Tiles(tilemapImage)