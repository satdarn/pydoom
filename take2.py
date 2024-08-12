import pygame
import math

pygame.init()

WIDTH = 500
HEIGHT = 500

PLAYER_SPEED = 5
PLAYER_ROT_SPEED = 5

FOV_CONST = 300

BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player:
    def __init__(self, x,y,z, pitch, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
    def get_yaw_rad(self):
        return math.radians(self.yaw)
    def get_pitch_rad(self):
        return math.radians(self.pitch)
    

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return (self.x, self.y, self.z)


def handle_inputs(keys, player):
    
    if keys[pygame.K_w]:
        player.y += PLAYER_SPEED
    if keys[pygame.K_s]:
        player.y -=PLAYER_SPEED
    if keys[pygame.K_a]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_d]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_COMMA]:
        player.yaw += PLAYER_ROT_SPEED
    if keys[pygame.K_PERIOD]:
        player.yaw -= PLAYER_ROT_SPEED

def draw_face_3d(screen, player, points, color):
    screen_points = []
    # offset points by player
    player_cos = math.cos(player.get_yaw_rad())
    player_sin = math.sin(player.get_yaw_rad())
    for point in points:
        offset_x =point.x - player.x
        offset_y =point.y - player.y
        # rotate points around player 
        world_x = offset_x * player_cos - offset_y * player_sin
        world_y = offset_y * player_cos + offset_x * player_sin
        world_z = point.z 
        try:
            screen_x = world_x * FOV_CONST / world_y + WIDTH/2
            screen_y = world_z * FOV_CONST / world_y + HEIGHT/2
            screen_points.append((screen_x, screen_y))
            
        except:
            pass
    if len(screen_points) > 2:
        pygame.draw.polygon(screen, color, (screen_points))


clock = pygame.time.Clock()

player = Player(0,0,0, 0, 0)

face1 = [ 
        Point(30, 100, -50),
        Point(30, 100, 40),
        Point(-30, 100, 40),
        Point(-30, 100, -50)        
          ]
face2 = [ 
        Point(30, 90, -50),
        Point(30, 90, 40),
        Point(-30, 90, 40),
        Point(-30, 90, -50)        
          ]
while True:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        

    
    keys = pygame.key.get_pressed()
    handle_inputs(keys, player)
    draw_face_3d(screen, player, face1, (238, 193, 112))
    draw_face_3d(screen, player, face2, (245, 133, 73))


    clock.tick(30)
    pygame.display.update()