import pygame
from math import ceil

map_folder_location = "content/maps"
image_path = "content/images"
tile_size = 32

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(image_path + "/" + image)
        self.is_solid = is_solid

class Map:
    def __init__(self, data, tile_kinds, legacy_data=False):
        from core.engine import engine
        engine.background_drawables.append(self)

        # Keep a list of different kinds of files (grass, sand, water, etc.)
        self.tile_kinds = tile_kinds

        if legacy_data:
            # Set up the tiles from loaded data
            self.tiles = []
            for line in data.split('\n'):
                row = []
                for tile_number in line:
                    row.append(int(tile_number))
                self.tiles.append(row)
            print(self.tiles)
        else:
            self.tiles = data

        # How big in pixels are the tiles?
        self.tile_size = tile_size

    def is_point_solid(self, x, y):
        x_tile = int(x/self.tile_size)
        y_tile = int(y/self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return True
        tile = self.tiles[y_tile][x_tile]
        return self.tile_kinds[tile].is_solid
    
    
    def set_tile(self, x, y, index):
        x_tile = int(x/self.tile_size)
        y_tile = int(y/self.tile_size)
        if x_tile < 0 or \
            y_tile < 0 or \
            y_tile >= len(self.tiles) or \
            x_tile >= len(self.tiles[y_tile]):
            return
        print("Setting tile to", y_tile, x_tile, index)
        self.tiles[y_tile][x_tile] = index


    def is_rect_solid(self, x, y, width, height):
        # Check the top left and middle (if bigger than tile size)
        x_checks = int(ceil(width/self.tile_size))
        y_checks = int(ceil(height/self.tile_size))
        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi*self.tile_size + x
                y = yi*self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        if self.is_point_solid(x + width, y):
            return True
        if self.is_point_solid(x, y + height):
            return True
        if self.is_point_solid(x + width, y + height):
            return True
        return False
    
    def save_to_file(self, file):
        import struct
        # Save the width and height
        for row in self.tiles:
            for n in row:
                packed = struct.pack('H', n)
                file.write(packed)


    def draw(self, screen):
        # Go row by row
        from core.camera import camera
        for y, row in enumerate(self.tiles):
            # Within the current row, go through each tile
            for x, tile in enumerate(row):
                location = (x * self.tile_size - camera.x, y * self.tile_size - camera.y)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)