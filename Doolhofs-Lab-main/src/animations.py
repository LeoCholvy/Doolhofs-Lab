import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name, path, group):
        super().__init__(group)
        self.sprite_sheet = pygame.image.load(path)
        self.size = 16
        self.clock = 0
        self.animation_speed = 0.3
        self.path = path
        self.dict_animation = {
            'player':{'up' : self.get_images(72),
            'down': self.get_images(0),
            'left': self.get_images(106),
            'right':self.get_images(36)} 
        }
        self.images = self.dict_animation[name]
        self.animation_index = 0

    def change_animation(self, name):
        
        self.image  = self.images[name][self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((0,0,0))
        self.clock = self.clock + self.animation_speed

        if self.clock >= 100:
            self.animation_index += 1
            if self.animation_index > len(self.images[name]) -1 :
                self.animation_index = 0
            self.clock = 0 
    
    
    
    def get_images(self, y):
        images = []
        for i in range(3):
            x = i*36
            image = self.get_image(x,y)
            images.append(image)
        return images
    
    
    
    def get_image(self, x, y):
        image = pygame.Surface([36,36])
        image.blit(self.sprite_sheet, (0,0), (x, y, 36, 36))
        return image