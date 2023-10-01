from pico2d import *
import math

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)
r = 10

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

def handle_events():
    global running, hand_coord, hand_cnt, value
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == 1 and hand_cnt < 5:
            hand_coord[hand_cnt] = (event.x, TUK_HEIGHT - 1 - event.y)
            hand_cnt += 1
            if hand_cnt == 1:
                angle = math.atan2(hand_coord[0][1] - character_coord[1], hand_coord[0][0] - character_coord[0])
                value = (math.cos(angle) * r, math.sin(angle) * r)
    pass

def change_destination():
    global hand_coord, character_coord, angle, value, hand_cnt
    if hand_cnt > 1:
        angle = math.atan2(hand_coord[1][1] - character_coord[1], hand_coord[1][0] - character_coord[0])
        value = (math.cos(angle) * r, math.sin(angle) * r)
        hand_coord = [hand_coord[1], hand_coord[2], hand_coord[3], hand_coord[4], (0, 0)]
        hand_cnt -= 1
    else:
        value = (0, 0)
        hand_coord = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        hand_cnt = 0

running = True
character_coord, value = (TUK_WIDTH // 2, TUK_HEIGHT // 2), (0, 0)
hand_coord = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
hand_cnt = 0
frame, angle = 0, 0

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    for i in range(0, hand_cnt):
        hand_arrow.draw(hand_coord[i][0] + 25, hand_coord[i][1] - 26)

    if (value[0] >= 0):
        character.clip_draw(frame * 100, 100 * 1, 100, 100, character_coord[0], character_coord[1])
    else:
        character.clip_composite_draw(frame * 100, 100, 100, 100, 0, 'h', character_coord[0], character_coord[1], 100, 100)
    frame = (frame + 1) % 8

    character_coord = (character_coord[0] + value[0], character_coord[1] + value[1])

    if hand_cnt > 0:
        if value[0] > 0 and value[1] > 0 and character_coord[0] >= hand_coord[0][0] and character_coord[1] >= hand_coord[0][1]:
            change_destination()
        elif value[0] <= 0 and value[1] > 0 and character_coord[0] <= hand_coord[0][0] and character_coord[1] >= hand_coord[0][1]:
            change_destination()
        elif value[0] <= 0 and value[1] <= 0 and character_coord[0] <= hand_coord[0][0] and character_coord[1] <= hand_coord[0][1]:
            change_destination()
        elif value[0] > 0 and value[1] <= 0 and character_coord[0] >= hand_coord[0][0] and character_coord[1] <= hand_coord[0][1]:
            change_destination()

    update_canvas()
    handle_events()
    delay(0.05)

close_canvas()




