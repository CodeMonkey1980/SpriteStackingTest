import sys

import pygame

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Sprite Stacking Test')

WINDOW_SIZE = (300, 200)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((100, 75))  # used as the surface for rendering, which could do things like scaling

# load images
knight_sprite = pygame.image.load('resources/knight/chr_knight.png').convert_alpha()

# prepare variables
key_status = {}
debug = False

angle = 0
render_height = 0

# run gameloop
while True:
    # process events
    for key in [x for x in key_status.keys()]:
        if key_status[key] == 'released':
            del key_status[key]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            key_status[event.key] = 'pressed'

        if event.type == pygame.KEYUP:
            key_status[event.key] = 'released'

    if key_status.get(pygame.K_LEFT) == 'pressed':
        angle += 5

    if key_status.get(pygame.K_RIGHT) == 'pressed':
        angle -= 5

    if key_status.get(pygame.K_UP) == 'released':
        render_height += 1

    if key_status.get(pygame.K_DOWN) == 'released':
        render_height -= 1

    display.fill((215, 215, 215))

    # render image
    # https://stackoverflow.com/questions/10560446/how-do-you-select-a-sprite-image-from-a-sprite-sheet-in-python
    sprite_length = int(knight_sprite.get_height() / 21)
    render_target = render_height
    sprite_canvas = pygame.Surface((100, 75), pygame.SRCALPHA, 32)
    for layer_count in range(0, sprite_length):
        knight_sprite.set_clip(pygame.Rect(0, 21 * (sprite_length - layer_count), 20, 21))
        knight_clip = knight_sprite.get_clip()
        active_sprite = knight_sprite.subsurface(knight_clip)
        active_sprite = pygame.transform.rotate(active_sprite, angle)

        # determine center and calculate back from that.
        x = 50 - int(active_sprite.get_width() / 2)
        y = 32 - int(active_sprite.get_height() / 2)

        sprite_canvas.blit(active_sprite, (x, y - layer_count))

    for offset in [{'x': -1, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': -1}, {'x': 0, 'y': 1}]:
        mask = pygame.mask.from_surface(sprite_canvas)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + offset['x'], point[1] + offset['y'])
            n += 1
        pygame.draw.polygon(display, (0, 0, 0), mask_outline, 1)

    display.blit(sprite_canvas, (0, 0))

    pygame.transform.scale(display, (300, 200), screen)
    pygame.display.update()
    clock.tick(60)
