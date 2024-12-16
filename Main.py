import turtle
import math
import random
import Alphabet as Alp


class Game:
    def __init__(self):
        # window setup
        screen_width = 960
        screen_height = 640
        self.width = 860
        self.height = 520

        self.window = turtle.Screen()
        self.window.setup(screen_width, screen_height)
        self.window.title("Dodging Balls")
        self.window.colormode(255)
        self.window.bgcolor(0, 0, 0)
        self.window.tracer(0)

        self.bg_pen = turtle.Turtle()
        self.bg_pen.speed(0)
        self.bg_pen.shape("square")
        self.bg_pen.color((255, 255, 255))
        self.bg_pen.penup()
        self.bg_pen.hideturtle()

        self.char_pen = Alp.Alphabet((255, 255, 255), 3)

        self.intro_pen = turtle.Turtle()
        self.intro_pen.speed(0)
        self.intro_pen.shape("square")
        self.intro_pen.color((255, 255, 255))
        self.intro_pen.penup()
        self.intro_pen.hideturtle()

        self.entity_list = []
        self.bullet_list = []
        self.powerup_list = []
        self.enemy_bullet_list = []

        # in-game attribute
        self.bullet_num = 10

        self.wave = 1
        self.state = "splash"
        self.load = False
        self.choice = "start"

        self.attemp = 0
        self.score = 0
        self.hi_score = 0
        self.new_record = False

        self.player = Player(0, 0, "triangle", (255, 255, 255))

    def start(self):
        self.entity_list.clear()

        self.entity_list.append(game.player)

        for num in range(self.bullet_num):
            self.bullet_list.append(Bullet(0, 0, "square", (252, 222, 0)))

        for bullet in self.bullet_list:
            self.entity_list.append(bullet)
        
        num_enemy = 3 + (self.wave - 1)

        for num in range(num_enemy):
            x = random.choice([random.uniform(-self.width/2, game.player.x - 25),
                                random.uniform(self.width/2, game.player.x + 25)])
            y = random.choice([random.uniform(-self.height/2, game.player.y - 25),
                                random.uniform(self.height/2, game.player.y + 50)])
            dx = 0
            dy = 0

            self.entity_list.append(Enemy(x, y, "circle", (255, 0, 0)))
            self.entity_list[-1].dx = dx
            self.entity_list[-1].dy = dy

        powerup_num = 2 + math.floor(self.wave / 5)

        for num in range(powerup_num):
            x = random.choice([random.uniform(-self.width/2, game.player.x - 25),
                                random.uniform(self.width/2, game.player.x + 25)])
            y = random.choice([random.uniform(-self.height/2, game.player.y - 25),
                                random.uniform(self.height/2, game.player.y + 25)])
            dx = random.uniform(-0.15, 0.15)
            dy = random.uniform(-0.15, 0.15)

            self.entity_list.append(Powerups(x, y, "square", "blue"))
            self.entity_list[-1].dx = dx
            self.entity_list[-1].dy = dy

    def border_render(self, pen):
        pen.color((255, 255, 255))
        pen.width(3)
        pen.penup()

        left_pos = -self.width / 2
        right_pos = self.width / 2
        top_pos = self.height / 2
        bottom_pos = -self.height / 2

        pen.goto(left_pos, top_pos)
        pen.pendown()
        pen.goto(right_pos, top_pos)
        pen.goto(right_pos, bottom_pos)
        pen.goto(left_pos, bottom_pos)
        pen.goto(left_pos, top_pos)
        pen.penup()

    def render_info(self, pen, score):
        pen.color((255, 255, 255))
        pen.width(3)
        pen.goto(-400, 300)
        pen.pendown()
        pen.goto(400, 300)
        pen.penup()

        pen.color((255, 255, 255))
        game.char_pen.scale = 0.8
        game.char_pen.draw_string(pen, "SCORE {}".format(score), -300, 280)
        game.char_pen.draw_string(pen, "WAVE", -150, 280)
        game.char_pen.draw_string(pen, "{}".format(game.wave), -100, 280)
        game.char_pen.draw_string(pen, "MODES", 40, 280)
        game.char_pen.scale = 0.6
        game.char_pen.draw_string(pen, "{}".format(game.player.boolets_mode), 120, 285)
        
    def launch(self):
        if self.state == "splash":
            self.state = "playing"
            
        elif self.state == "gameover":
            game.player.lives = 1
            game.attemp += 1
            self.state = "splash"
            self.load = False




class Entity:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.shape = shape
        self.color = color
        self.heading = 0
        self.da = 0
        self.speed = 0.0
        self.accel = 0.0004
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"
        self.max_dx = 0.1
        self.max_dy = 0.1

    def health_render(self, pen):
        pen.goto(self.x - 10, self.y + 20)
        pen.width(3)
        pen.pendown()
        pen.setheading(0)

        if self.health/self.max_health < 0.3:
            pen.color((255, 0, 0))
        elif self.health/self.max_health < 0.7:
            pen.color((255, 255, 0))
        else:
            pen.color((0, 255, 0))

        pen.fd(20 * (self.health / self.max_health))

        if self.health != self.max_health:
            pen.color((192, 192, 192))
            pen.fd(20 * ((self.max_health - self.health) / self.max_health))

        pen.penup()

    def is_collision(self, other):
        if self.x < other.x + other.width and\
        self.x + self.width > other.x and\
        self.y < other.y + other.height and\
        self.y + self.height > other.y:
            return True
        else:
            return False
        
    def bounce_off(self, other):
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dy = other.dy

        other.dx = temp_dx
        other.dy = temp_dy

    def border_check(self):
        if self.x > game.width/2.0 - 10 :
            self.x = game.width/2.0 - 10
            self.dx *= -0.8

        if self.x < -game.width/2.0 + 10 :
            self.x = -game.width/2.0 + 10
            self.dx *= -0.8

        if self.y > game.height/2.0 - 10 :
            self.y = game.height/2.0 - 10
            self.dy *= -0.8

        if self.y < -game.height/2.0 + 10 :
            self.y = -game.height/2.0 + 10
            self.dy *= -0.8

    def update(self):

        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.speed
        self.dy += math.sin(math.radians(self.heading)) * self.speed

        self.x += self.dx
        self.y += self.dy

        self.border_check()


    def render(self, pen):
        if self.state == "active":
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            self.health_render(pen)




class Player(Entity):
    def __init__(self, x, y, shape, color):
        Entity.__init__(self, 0, 0, shape, color)
        self.lives = 1
        self.heading = 90
        self.da = 0
        self.damage = 50
        self.boolets_mode = "Single"
        self.max_cooldown = 250
        self.cooldown = 250
        self.on_cooldown = False

    def rotate_left(self):
        self.da = 0.45

    def rotate_right(self):
        self.da = -0.45

    def rotate_stop(self):
        self.da = 0

    def accelerate(self):
        if self.speed >= 0.002:
            self.accel = 0
        if self.speed <= 0.002:
            self.accel = 0.0004
        self.speed += self.accel

    def cleanse(self):
        self.dx *= 0.5
        self.dy *= 0.5


    def deaccelerate(self):
        self.speed = 0.0

    def modes_switch(self):
        cond = True
        if game.state == "splash":
            if game.state == "start" and cond is True:
                game.state = "exit"
                cond = False

            if game.state == "exit" and cond is True:
                game.state = "start"
                cond = False
            
        if game.state == "playing":
            if self.boolets_mode == "Single" and cond is True and\
                self.on_cooldown is False:
                self.boolets_mode = "Spread"
                self.max_cooldown = 800
                self.cooldown = 800
                cond = False

            if self.boolets_mode == "Spread" and cond is True and\
                self.on_cooldown is False:
                self.boolets_mode = "Single"
                self.max_cooldown = 250
                self.cooldown = 250
                cond = False
        
    def fire(self):
        boolets_num = 0
        for bullet in game.bullet_list:
            if bullet.state == "ready":
                boolets_num += 1

        if self.boolets_mode == "Single" and\
            self.on_cooldown is False:
            bullet.fire(self.x, self.y, self.heading,
                        self.dx, self.dy)
            self.on_cooldown = True
            self.cooldown = 0                                     

        if self.boolets_mode == "Spread" and\
            self.on_cooldown is False:
            direction = [-20, -10, 0, 10, 20]
            for bullet in game.bullet_list:
                if bullet.state == "ready" and len(direction) != 0:
                    bullet.fire(self.x, self.y, self.heading + direction.pop(),
                                self.dx, self.dy)
            self.on_cooldown = True
            self.cooldown = 0
                    

    def reload_render(self, pen):
        pen.penup()
        pen.goto(90, 272)
        pen.width(4)
        pen.pendown()
        pen.setheading(0)

        if self.on_cooldown is True or\
            self.cooldown < self.max_cooldown:
            self.cooldown += 1
        if self.cooldown >= self.max_cooldown:
            self.on_cooldown = False

        bar_size = 80
        fill_percent = (self.cooldown / self.max_cooldown)
        unfill_percent = 1 - fill_percent

        if fill_percent/1 < 0.5:
            pen.color((255, 0, 0))
        elif fill_percent/1 < 1:
            pen.color((255, 255, 0))
        else:
            pen.color((0, 255, 0))

        pen.fd(bar_size * fill_percent)

        if self.cooldown != self.max_cooldown:
            pen.color((192, 192, 192))
            pen.fd(bar_size * unfill_percent)


    def update(self):
        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.speed
        self.dy += math.sin(math.radians(self.heading)) * self.speed

        self.x += self.dx
        self.y += self.dy

        self.border_check()


    def render(self, pen):
        pen.shapesize(0.6, 1.0, None)
        pen.goto(self.x, self.y)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        pen.shapesize(1.0, 1.0, None)

        self.health_render(pen)

        if self.health <= 0:
            self.killed()

        if self.lives <= 0:
            game.state = "gameover"

    def killed(self):
        self.x = 0
        self.y = 0
        self.health = self.max_health
        self.dx = 0
        self.dy = 0
        self.lives -= 1




class Bullet(Entity):
    def __init__(self, x, y, shape, color):
        Entity.__init__(self, x, y, shape, color)
        self.state = "ready"
        self.fuel = 250
        self.velocity = 3
        self.height = 6
        self.width = 6

    def fire(self, x, y, heading,
            dx, dy):
        if self.state == "ready":
            self.state = "active"
            self.x = x
            self.y = y
            self.dx = dx
            self.dy = dy
            self.heading = heading

            self.dx += math.cos(math.radians(self.heading)) * self.velocity
            self.dy += math.sin(math.radians(self.heading)) * self.velocity

    def update(self):
        if self.state == "active":
            self.fuel -= 1
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.fuel = 250
        self.dx = 0
        self.dy = 0
        self.state = "ready"

    def render(self, pen):
        if self.state == "active":
            pen.shapesize(0.3, 0.3, None)
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(1.0, 1.0, None)




class Enemy(Entity):
    def __init__(self, x, y, shape, color):
        Entity.__init__(self, x, y, shape, color)
        self.max_health = 50
        self.health = 50
        self.damage = 25
        self.type = Enemy.random_type(self)

        if self.type == "defult":
            self.color = (255, 0, 0)

        elif self.type == "idle":
            self.color = (255, 0, 127)
            self.max_health = 50
            self.health = 50
            self.damage = 50

        elif self.type == "fast" and\
              game.wave >= 3:
            self.color = (255, 128, 0)
            self.max_health = 40
            self.health = 40
            self.damage = 20

        elif self.type == "elite" and\
              game.wave >= 6:
            self.color = (247, 0, 255)
            self.max_health = 120
            self.health = 120
            self.damage = 35

        else:
            self.color = (255, 0, 0)


    def random_type(self):
        random_num = random.randint(1, 100)
        if random_num <= 35:
            return "defult"
        if random_num > 35 and\
            random_num <= 65:
            return "idle"
        if random_num > 65 and\
            random_num <= 82:
            return "fast"
        if random_num > 82 and\
            random_num <= 100:
            return "elite"
        

    def update(self):
        if self.state == "active":
            self.heading += math.atan2(game.player.y - self.y,
                                       game.player.x - self.x)
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.speed
            self.dy += math.sin(math.radians(self.heading)) * self.speed

            self.x += self.dx
            self.y += self.dy

            self.border_check()

            if self.health <= 0:
                self.reset()

            if self.type == "defult":
                if self.x < game.player.x:
                    self.x += 0.08
                else:
                    self.x -= 0.08

                if self.y < game.player.y:
                    self.y += 0.08
                else:
                    self.y -= 0.08

            if self.type == "idle":
                self.dx = 0
                self.dy = 0

            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.dx:
                self.dx = -self.max_dx
            
            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.dy:
                self.dy = -self.max_dy

            if self.type == "fast":
                if self.x < game.player.x:
                    self.x += 0.12
                else:
                    self.x -= 0.12

                if self.y < game.player.y:
                    self.y += 0.12
                else:
                    self.y -= 0.12

            if self.type == "elite":
                if self.x < game.player.x:
                    self.x += 0.09
                else:
                    self.x -= 0.09

                if self.y < game.player.y:
                    self.y += 0.09
                else:
                    self.y -= 0.09

    def reset(self):
        self.state = "inactive"
        game.score += 10




class Powerups(Entity):
    def __init__(self, x, y, shape, color):
        Entity.__init__(self, x, y, shape, color)
        self.state = "ready"
        self.type = "Heal"

        if self.type == "Heal":
            self.color = (0, 255, 0)

    def heal(self, ply):
        self.healing = 20
        missing_hp = ply.player.max_health - ply.player.health
        if missing_hp > self.healing:
            ply.player.health += 20
        else:
            ply.player.health += missing_hp
        self.state = "activated"

    def update(self):
        if self.state == "ready":
            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def render(self, pen):
        if self.state == "ready":
            pen.shapesize(1, 1, None)
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(1.0, 1.0, None)


game = Game()

game.window.listen()
game.window.onkeypress(game.player.rotate_left, "a")
game.window.onkeypress(game.player.rotate_right, "d")

game.window.onkeyrelease(game.player.rotate_stop, "a")
game.window.onkeyrelease(game.player.rotate_stop, "d")


game.window.onkeypress(game.player.accelerate, "w")
game.window.onkeyrelease(game.player.deaccelerate, "w")

game.window.onkeypress(game.player.cleanse, "s")
game.window.onkeyrelease(game.player.cleanse, "s")

game.window.onkeypress(game.player.fire, "space")
game.window.onkeyrelease(game.player.fire, "space")

game.window.onkeypress(game.launch, "q")

game.window.onkeypress(game.player.modes_switch, "r")

while True:
    if game.state == "splash":
        if game.load == False:
            game.score = 0
            game.wave = 1
            game.attemp += 1
            game.player.boolets_mode = "Single"
            game.start()
            game.bg_pen.clear()
            game.intro_pen.clear()
            Alp.Alphabet.draw_splash(game.bg_pen, game.char_pen, game.window)
            game.load = True

        game.intro_pen.penup()
        Alp.Alphabet.draw_intro(game.intro_pen, game.choice)
        game.window.update()
    
    elif game.state == "playing":
        game.bg_pen.clear()
        game.intro_pen.clear()

        for entity in game.entity_list:
            entity.update()

        for entity in game.entity_list:
            if isinstance(entity, Enemy) and\
                entity.state == "active":
                if game.player.is_collision(entity):
                    entity.health -= entity.damage
                    game.player.health -= entity.damage
                    game.player.bounce_off(entity)
                    entity.bounce_off(entity)

                for bullet in game.bullet_list:
                    if bullet.state == "active" and\
                        bullet.is_collision(entity):
                        entity.health -= game.player.damage
                        bullet.reset()

        for entity in game.entity_list:
            if isinstance(entity, Powerups) and\
                entity.state == "ready":
                if game.player.is_collision(entity):
                    if entity.type == "Heal":
                        entity.heal(game)

        for entity in game.entity_list:
            entity.render(game.bg_pen)

        game.border_render(game.bg_pen)
        game.player.reload_render(game.intro_pen)

        wave_end = True
        for entity in game.entity_list:
            if isinstance(entity, Enemy) and\
            entity.state == "active":
                wave_end = False
        if wave_end:
            game.wave += 1
            game.start()

        game.render_info(game.bg_pen, game.score)

        game.window.update()

    elif game.state == "gameover":
        game.bg_pen.clear()
        game.intro_pen.clear()

        if game.score > game.hi_score:
            game.hi_score = game.score

        Alp.Alphabet.draw_gameover(game.bg_pen, game.char_pen, game)

        game.window.update()

