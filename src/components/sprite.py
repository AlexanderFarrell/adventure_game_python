import pygame
from core.camera import camera

image_path = "content/images"

loaded = {}

class Sprite:
    def __init__(self, image, is_ui=False):
        from core.engine import engine
        global sprites
        self.is_ui = is_ui

        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if is_ui:
            engine.ui_drawables.append(self)
        else:
            engine.drawables.append(self)

    def set_image(self, image):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image_path + "/" + image)
            loaded[image] = self.image

    def rotate(self, amo):
        self.image = pygame.transform.rotate(self.image, amo)

    def scale(self, x_scale, y_scale):
        self.image = pygame.transform.scale(self.image, (x_scale, y_scale))

    def breakdown(self):
        from core.engine import engine
        if self.is_ui:
            engine.ui_drawables.remove(self)
        else:
            engine.drawables.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else \
                (self.entity.x, self.entity.y)
        if pos[0] < camera.width and \
            pos[1] < camera.height and \
            pos[0] + self.width > 0 and \
            pos[1] + self.height > 0:
            screen.blit(self.image, pos)



# Loads an image with several sub-images inside of it.
# 
# Instead of having 16 different images 😬
# We can just have one image with a table of all 16 sub-images.
# 🌲🌲🌲
# 🌲🌲🌲
# 🌲🌲🌲
class Atlas(Sprite):

    # image       - The filename to load. 
    # cell_width  - Size of sub-images in pixels left and right
    # cell_height - Size of sub-images in pixels up and down
    # start_x     - Which sub-images to use. 0 would give you an image to the very left.
    # start_y     - Which sub-images to use. 0 would give you an image on the very top.
    def __init__(self, image, cell_width, cell_height, start_x, start_y,  is_ui=False):
        # Will ensure the image is loaded, and the draw function is called.
        super().__init__(image, is_ui=is_ui)

        # We will then take Sprite's image to get a sub-image.
        self.base_image = self.image

        self.cell_width = cell_width
        self.cell_height = cell_height
        self.start_x = start_x
        self.start_y = start_y

        # Create a surface to render each sub-image into
        from pygame.surface import Surface
        self.image = Surface((cell_width, cell_height), pygame.SRCALPHA)

        # Recycle our code, and just use switch_to to pick the image for us.
        self.switch_to(self.start_x, self.start_y)
        

    # Chooses a sub-image given two coordinates in the sprite atlas.
    #
    # cell_x - Which variant to use. 0 would give you an image to the very left.
    # cell_y - Which variant to use. 0 would give you an image on the very top.
    def switch_to(self, cell_x, cell_y):
        self.cell_x = cell_x
        self.cell_y = cell_y
        # Coordinates in pixels
        pixel_x = cell_x * self.cell_width
        pixel_y = cell_y * self.cell_height
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.base_image, (0, 0), pygame.Rect(pixel_x, pixel_y, self.cell_width, self.cell_height))

    # Override the set_image to not do the base functionality of Sprite
    def set_image(self, image):
        if not image in loaded:
            loaded[image] = pygame.image.load(image_path + "/" + image)
            self.base_image = loaded[image]
        
        self.switch_to(self.cell_x, self.cell_y)


# Cycles through select images to create an animation
class Animation(Atlas):

    # image            - The filename to load. 
    # cell_width       - Size of sub-images in pixels left and right
    # cell_height      - Size of sub-images in pixels up and down
    # frame_coords     - A list of coordinates for each frame. Make a list, then put a tuple of two numbers for each
    #                    frame. For example [(0, 0), (0, 1)] will start with the top-left sub-image, then go one image 
    #                    to the right of that one, then go back to the top-left image.
    # frames_per_image - How many frames before switching images. 
    def __init__(self, image, cell_width, cell_height, frame_coords=[(0, 0)], frames_per_image=10, is_ui=False):
        
        # Frame coords must have at least one thing. If it doesn't, let's throw a helpful error
        if len(frame_coords) == 0:
            raise Exception("""Frame coords needs at least one coordinate. For example, [(0, 0), (0, 1), (0, 2)] will be an 
                            animation of 3 sub-images.""")
        
        # Get the starting sub-image from the first coordinate.
        start_x = frame_coords[0][0]
        start_y = frame_coords[0][1]
        self.frame_coords = frame_coords

        super().__init__(image, cell_width, cell_height, start_x, start_y, is_ui)

        self.frames_per_image = frames_per_image
        self.current_image = 0
        self.ticks = 0

        # To update the animation, we tell the engine to call our update function.
        from core.engine import engine
        engine.active_objs.append(self)

    # Switches to a different sequences of images to animate on
    # Allows for different animations on the same sprite sheet.
    def set_frame_coords(self, frame_coords):
        # Just reset everything to the first image in the new frame coords list
        self.frame_coords = frame_coords
        self.ticks = 0
        self.current_image = 0
        cell_x = frame_coords[0][0]
        cell_y = frame_coords[0][1]
        self.switch_to(cell_x, cell_y)


    def update(self):
        self.ticks += 1

        # If enough ticks have gone by to switch the image
        if self.ticks >= self.frames_per_image:
            # Reset the ticks
            self.ticks = 0
            self.current_image += 1
            # If we are passed the last image, then just set it back to the first image
            if len(self.frame_coords) <= self.current_image:
                self.current_image = 0

            # Set the position of the next image
            cell_x = self.frame_coords[self.current_image][0]
            cell_y = self.frame_coords[self.current_image][1]
            self.switch_to(cell_x, cell_y)
            