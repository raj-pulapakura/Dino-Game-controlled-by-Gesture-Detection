import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, walking_sprite_paths, jumping_sprite_path, walking_speed, jump_velocity, jump_height, jump_gravity):
        super().__init__()
        self.is_walking = False
        self.is_jumping = False
        self.walking_speed = walking_speed
        self.jump_velocity = jump_velocity
        self.jump_height = jump_height
        self.jump_gravity = jump_gravity
        self.walking_sprites = [pygame.transform.scale_by(pygame.image.load(p).convert_alpha(), 1.6) for p in walking_sprite_paths]
        self.jumping_sprite = pygame.transform.scale_by(pygame.image.load(jumping_sprite_path).convert_alpha(), 1.6)
        
        self.current_walking_sprite = 0
        self.image = self.walking_sprites[self.current_walking_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)

    def start_walking(self):
        self.is_walking = True

    def start_jumping(self):
        self.is_jumping = True

    def end_walking(self):
        self.is_walking = False

    def end_jumping(self):
        self.is_jumping = False

    def update(self):
        if self.is_walking:
            self.current_walking_sprite += self.walking_speed
            if self.current_walking_sprite >= len(self.walking_sprites):
                self.current_walking_sprite = 0
            self.image = self.walking_sprites[int(self.current_walking_sprite)]
        if self.is_jumping:
            self.image = self.jumping_sprite
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.jump_gravity
            if self.jump_velocity < -self.jump_height:
                self.is_jumping = False
                self.jump_velocity = self.jump_height
                self.image = self.walking_sprites[int(self.current_walking_sprite)]
