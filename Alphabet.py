
class Alphabet:
    def __init__(self, color=(255,255,255), scale = 1.0):
        # pen color & size
        self.color = color
        self.scale = scale

        #  alphabets cvs
        self.characters = {}
        self.characters["1"] = ((-5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["2"] = ((-5, 10),(5, 10),(5, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["3"] = ((-5, 10),(5, 10),(5, 0), (0, 0), (5, 0), (5,-10), (-5, -10))
        self.characters["4"] = ((-5, 10), (-5, 0), (5, 0), (2,0), (2, 5), (2, -10))
        self.characters["5"] = ((5, 10), (-5, 10), (-5, 0), (5,0), (5,-10), (-5, -10))
        self.characters["6"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters["7"] = ((-5, 10), (5, 10), (0, -10))
        self.characters["8"] = ((-5, 0), (5, 0), (5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0))
        self.characters["9"] = ((5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters["0"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))

        self.characters["A"] = ((-5, -10), (-5, 10), (5, 10), (5, -10), (5, 0), (-5, 0))
        self.characters["B"] = ((-5, -10), (-5, 10), (3, 10), (3, 0), (-5, 0), (5,0), (5, -10), (-5, -10))
        self.characters["C"] = ((5, 10), (-5, 10), (-5, -10), (5, -10))
        self.characters["D"] = ((-5, 10), (-5, -10), (5, -8), (5, 8), (-5, 10))
        self.characters["E"] = ((5, 10), (-5, 10), (-5, 0), (0, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["F"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (-5, 0), (-5, -10))
        self.characters["G"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (0, 0))
        self.characters["H"] = ((-5, 10), (-5, -10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters["I"] = ((-5, 10), (5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["J"] = ((5, 10), (5, -10), (-5, -10), (-5, 0))   
        self.characters["K"] = ((-5, 10), (-5, -10), (-5, 0), (5, 10), (-5, 0), (5, -10))
        self.characters["L"] = ((-5, 10), (-5, -10), (5, -10))
        self.characters["M"] = ((-5, -10), (-3, 10), (0, 0), (3, 10), (5, -10))
        self.characters["N"] = ((-5, -10), (-5, 10), (5, -10), (5, 10))
        self.characters["O"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))
        self.characters["P"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0))
        self.characters["Q"] = ((5, -10), (-5, -10), (-5, 10), (5, 10), (5, -10), (2, -7), (6, -11))
        self.characters["R"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0), (5, -10))
        self.characters["S"] = ((5, 8), (5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10), (-5, -8))
        self.characters["T"] = ((-5, 10), (5, 10), (0, 10), (0, -10)) 
        self.characters["V"] = ((-5, 10), (0, -10), (5, 10)) 
        self.characters["U"] = ((-5, 10), (-5, -10), (5, -10), (5, 10)) 
        self.characters["W"] = ((-5, 10), (-3, -10), (0, 0), (3, -10), (5, 10))   
        self.characters["X"] = ((-5, 10), (5, -10), (0, 0), (-5, -10), (5, 10))   
        self.characters["Y"] = ((-5, 10), (0, 0), (5, 10), (0,0), (0, -10))   
        self.characters["Z"] = ((-5, 10), (5, 10), (-5, -10), (5, -10))   
        
        self.characters["-"] = ((-3, 0), (3, 0))
        self.characters["."] = ((-3, -9), (0, -6))

    # draw whole sentence
    def draw_string(self, pen, str, x, y):
        pen.width(2)
        pen.color(self.color)

        x -= 15 * self.scale * ((len(str)-1) / 2)
        for character in str:
            self.draw_alphabet(pen, character, x, y)
            x += 15 * self.scale

    # draw single alphabet
    def draw_alphabet(self, pen, character, x, y):
        scale = self.scale
        
        if character in "abcdefghijklmnopqrstuvwxyz":
            scale *= 0.8
        
        character = character.upper()
        
        if character in self.characters:
            pen.penup()
            xy = self.characters[character][0]
            pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.pendown()
            for i in range(1, len(self.characters[character])):
                xy = self.characters[character][i]
                pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.penup()

    # intro screen
    def draw_splash(pen, chars, screen):
        chars.scale = 3.0
        chars.draw_string(pen, "DODINGS", 220, 200)

        chars.scale = 2.5
        pen.color((255,255,255))
        chars.draw_string(pen, "BALL", 245, 135)
        pen.color((255,0,0))
        chars.draw_alphabet(pen, "S", 335, 135)

        chars.scale = 1.0
        pen.goto(-400, 220)
        pen.pendown()
        pen.goto(-400, -220)
        pen.penup()
        pen.color((255,255,255))
        chars.draw_string(pen, "PRESS Q TO CONFIRM", -205, 200)

        chars.draw_string(pen, "PRESS W TO", -265, 150)
        chars.draw_string(pen, "MOVE FORWARD", -252, 120)

        chars.draw_string(pen, "PRESS A or D TO", -228, 70)
        chars.draw_string(pen, "TURN LEFT or RIGHT", -210, 40)

        chars.draw_string(pen, "PRESS S TO", -265, -10)
        chars.draw_string(pen, "SLOW DOWN", -272, -40)

        chars.draw_string(pen, "PRESS SPACEBAR TO", -212, -90)
        chars.draw_string(pen, "SHOOT", -303, -120)

        chars.draw_string(pen, "PRESS R TO", -265, -170)
        chars.draw_string(pen, "CHANGE MODES", -252, -200)

        chars.scale = 0.6
        chars.draw_string(pen, "VERSION BETA 1.0", 300, -285)

        screen.tracer(1)
        chars.scale = 1.0
        chars.draw_string(pen, "START", 200, 20)

        screen.tracer(0)
            

    #  gameover sceen
    def draw_gameover(pen, char, ply):
        pen.clear()
        
        char.scale = 3.0
        char.draw_string(pen, "GAME OVER", 0, 140)
        char.scale = 1.0
        char.draw_string(pen, "YOUR SCORE IS {}".format(ply.score), 0, 25)
        char.draw_string(pen, "HIGHEST SCORE IS {}".format(ply.hi_score), 0, -5)
        char.draw_string(pen, "PRESS Q TO", 0, -80)
        char.draw_string(pen, "GO BACK TO MAINMENU", 0, -120)


    def draw_stamp(pen):
        pen.color((255,255,255))
        pen.shape("triangle")
        pen.goto(100, 20)
        pen.goto(100, -30)
        pen.stamp()


    def draw_intro(pen, choice):
        pen.color((255,255,255))
        pen.shape("triangle")
        if choice == "start":
            pen.goto(100, 20)
        elif choice == "exit":
            pen.goto(100, -30)
        pen.stamp()