

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
ANGLE_VEL_INCREMENT = 0.1
MAX_ROCKS = 12
score = 0
lives = 0
time = 0
started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    #for sprite in group:
    #    sprite.update()
    #    sprite.draw(canvas)
    expired_objects = set([])
    for sprite in group:
        if sprite.update():
            expired_objects.add(sprite)
            group.difference_update(expired_objects)
        else:
            sprite.draw(canvas)
            
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0.0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def reset(self):
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.vel = [0,0]
        self.angle_vel = 0.0
        
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius   

    def draw(self,canvas):

        if my_ship.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + 90 , self.image_center[1]],  self.image_size, self.pos, self.image_size, self.angle)

    def shoot(self):

        nose = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * nose[0],self.pos[1] + self.radius * nose[1]]

        missile_group.add(Sprite(missile_pos, #pos
                          [my_ship.vel[0] + 7 * nose[0],my_ship.vel[1] + 7 * nose[1]],  #vel
                          0,
                          0,
                          missile_image,
                          missile_info,
                          missile_sound))
        missile_sound.play()
        #print "Pew!"
        #print my_ship.pos[0]



    def update(self):
        if self.thrust == True:
            ship_thrust_sound.play()
            #print angle_to_vector(self.angle)
            self.vel[0] +=  angle_to_vector(self.angle)[0] * 0.5
            self.vel[1] +=  angle_to_vector(self.angle)[1] * 0.5
        else:
            ship_thrust_sound.rewind()


            #   
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.vel[0] *= 0.97
        self.vel[1] *= 0.97

        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.spin_direction = random.randint(0,1)
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        if self.spin_direction == 0:
            self.spin_direction = -1

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += 0.05 * self.spin_direction
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False


        #print self.angle_vel

    def collide(self, other_object):
        distance_between_centers = dist(self.get_position(), other_object.get_position())
        if distance_between_centers <= self.get_radius() + other_object.get_radius():
            explosion_sound.play()
            return True
        else:
            return False
        
    def group_collide(group, other_sprite):
        for object in list(group):
            if object.collide(other_sprite):
                group.discard(object)
                return True
        else:
            return False        

    def group_group_collide(rock_group, missile_group):
        collisions = 0
        for missile in list(missile_group):
            if Sprite.group_collide(rock_group, missile):
                collisions += 1
                missile_group.discard(missile)
        return collisions        
                
def click(pos):
    global started, score, lives
    if started == False:
        started = True
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        lives = 3
        score = 0
        soundtrack.play()
        
def keydown(key):
    global started
    if started:
        if simplegui.KEY_MAP["left"] == key:
            my_ship.angle_vel -= ANGLE_VEL_INCREMENT
            #print my_ship.angle
        if simplegui.KEY_MAP["right"] == key:
            my_ship.angle_vel += ANGLE_VEL_INCREMENT
            #print my_ship.angle
        if simplegui.KEY_MAP["up"] == key:
            my_ship.thrust = True
        if simplegui.KEY_MAP["space"] == key:
            my_ship.shoot()       

def keyup(key):
        if simplegui.KEY_MAP["left"] == key or simplegui.KEY_MAP["right"] == key:
            my_ship.angle_vel = 0
        if simplegui.KEY_MAP["up"] == key:
            my_ship.thrust = False
            
            

def draw(canvas):
    global time, score, lives, started
    # animiate background
    if lives <= 0:
        lives = 0
        started = False
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Score: " + str(score),(WIDTH * 0.1 , HEIGHT * 0.05), 12, "White" )
    canvas.draw_text("Lives: " + str(lives),(WIDTH * 0.85, HEIGHT * 0.05), 12,  "White" )
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    # update ship and sprites
    my_ship.update()
    if Sprite.group_collide(rock_group, my_ship):
        lives -= 1
    if Sprite.group_group_collide(rock_group, missile_group) > 0:
        score += 10
    if not started:
        my_ship.reset()
        soundtrack.rewind()
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), (WIDTH / 2, HEIGHT / 2))
        

# timer handler that spawns a rock   
def rock_spawner():
    global rock_group, started
    spawn_position = [random.randint(1, WIDTH), random.randint(1, HEIGHT)]
    
    if len(rock_group) < MAX_ROCKS and started and dist(my_ship.get_position(),spawn_position) > 100:
        rock_group.add(Sprite(spawn_position, #position
                    [(random.randint(-150, 150))/100, (random.randint(-150, 150))/100], #vel
                    (random.randint(-900, 900))/100,  #ang_vel
                    0,
                    asteroid_image,
                    asteroid_info))
    elif not started:
        rock_group = set([])

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

rock_group = set([])
missile_group = set([])


#a_rock = Sprite([WIDTH / 2, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
# get things rolling
timer.start()
frame.start()
