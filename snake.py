import turtle
import time
import random
import gc

screen = turtle.getscreen()
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()

snake = turtle.Turtle()
enemy = turtle.Turtle()
border = turtle.Turtle()
score_writer = turtle.Turtle()
enemy_score_writer = turtle.Turtle()
high_score_writer = turtle.Turtle()
game_over_writer = turtle.Turtle()

screen.setup(width=2000, height=2000)
screen.title("Snake Python")
screen.bgcolor("black")
screen.tracer(False)

high_score_writer.hideturtle()
high_score_writer.penup()
high_score_writer.goto(650, 850)
high_score_writer.color("white")
high_score_writer._write('HighScore: ', align='left', font='tahoma')
enemy_score_writer.penup()
enemy_score_writer.hideturtle()
enemy_score_writer.goto(650, 900)
enemy_score_writer.color("white")
enemy_score_writer._write('EnemyScore: 0', align='left', font='tahoma')
score_writer.penup()
score_writer.hideturtle()
score_writer.goto(650, 950)
score_writer.color("white")
score_writer._write('PlayerScore: 0', align='left', font='tahoma')
game_over_writer.hideturtle()
game_over_writer.penup()
game_over_writer.color("white")

border.goto(-1980, -1980)
border.pensize(40)
border.forward(4000)
border.left(90)
border.forward(4000)
border.left(90)
border.forward(4000)
border.left(90)
border.forward(4000)
border.left(90)
border.hideturtle()

snake.penup()
snake.goto(1200, -1200)
snake.setheading(90)
snake.speed(0)
snake.shape("turtle")
snake.color("yellow")
snake_parts = {}
snake_last_positions = {}
snake_last_positions[0] = [snake.xcor(), snake.ycor()]

enemy.penup()
enemy.goto(-900, 900)
enemy.speed(0)
enemy.shape("turtle")
enemy.color("orange")
enemy_parts = {}
enemy_last_positions = {}
enemy_last_positions[0] = [enemy.xcor(), enemy.ycor()]
enemy_next_pos = []
snake_next_pos = []

food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randrange(-980, 981, 20), random.randrange(-980, 981, 20))

delay = 0.005
score = 0
enemy_score = 0
high_score = 0
alive = True
enemy_alive = True
paused = False


def pause():
    global paused
    paused = not paused


def on_close():
    global running
    running = False


def up():
    if(snake.heading() != 270):
        snake.setheading(90)


def down():
    if(snake.heading() != 90):
        snake.setheading(270)


def left():
    if(snake.heading() != 0):
        snake.setheading(180)


def right():
    if(snake.heading() != 180):
        snake.setheading(0)


screen.listen()
screen.onkey(pause, "Escape")
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")

running = True

root.protocol("WM_DELETE_WINDOW", on_close)

while(running):
    while(paused and running):
        screen.update()
        time.sleep(delay)
    screen.update()
    time.sleep(delay)
    snake.forward(20)
    enemy.forward(20)

    # NORMALIZE
    enemy.goto(round(enemy.xcor()), round(enemy.ycor()))
    snake.goto(round(snake.xcor()), round(snake.ycor()))

    # IA
    if(enemy.xcor() < food.xcor()):
        enemy.setheading(0)
        enemy_next_pos = [enemy.xcor() + 20, enemy.ycor()]
    elif(enemy.xcor() > food.xcor()):
        enemy.setheading(180)
        enemy_next_pos = [enemy.xcor() - 20, enemy.ycor()]
    else:
        if(enemy.ycor() < food.ycor()):
            enemy.setheading(90)
            enemy_next_pos = [enemy.xcor(),
                              enemy.ycor() + 20]
        elif(enemy.ycor() > food.ycor()):
            enemy.setheading(270)
            enemy_next_pos = [enemy.xcor(),
                              enemy.ycor() - 20]

    if(snake.xcor() < food.xcor()):
        snake.setheading(0)
        snake_next_pos = [snake.xcor() + 20, snake.ycor()]
    elif(snake.xcor() > food.xcor()):
        snake.setheading(180)
        snake_next_pos = [snake.xcor() - 20, snake.ycor()]
    else:
        if(snake.ycor() < food.ycor()):
            snake.setheading(90)
            snake_next_pos = [snake.xcor(),
                              snake.ycor() + 20]
        elif(snake.ycor() > food.ycor()):
            snake.setheading(270)
            snake_next_pos = [snake.xcor(),
                              snake.ycor() - 20]
    # CHECK IF TARGET IS PART OF HIMSELF

    # TODO CHECK IF NEXT POSITION IS CLOSED (ALL DIECTION RESULT TO DEATH)
    def recursive_path():
        global paused
        global enemy_next_pos
        global snake_next_pos

        for i in enemy_parts.keys():

            if(enemy_last_positions[i][0] == enemy_next_pos[0] and enemy_last_positions[i][1] == enemy_next_pos[1]):

                if(i > 0 and enemy_last_positions[i][0] == enemy.xcor() and enemy_last_positions[i - 1][0] < enemy_last_positions[i][0]):
                    enemy.setheading(0)
                    enemy_next_pos = [enemy.xcor() + 20, enemy.ycor()]
                    recursive_path()

                elif(i > 0 and enemy_last_positions[i][0] == enemy.xcor() and enemy_last_positions[i - 1][0] > enemy_last_positions[i][0]):
                    enemy.setheading(180)
                    enemy_next_pos = [enemy.xcor() - 20, enemy.ycor()]
                    recursive_path()

                elif(i > 0 and enemy_last_positions[i - 1][1] > enemy_last_positions[i][1] and enemy_last_positions[i][1] == enemy.ycor()):
                    enemy.setheading(270)
                    enemy_next_pos = [enemy.xcor(), enemy.ycor() - 20]
                    recursive_path()

                elif(i > 0 and enemy_last_positions[i - 1][1] < enemy_last_positions[i][1] and enemy_last_positions[i][1] == enemy.ycor()):
                    enemy.setheading(90)
                    enemy_next_pos = [enemy.xcor(), enemy.ycor() + 20]
                    recursive_path()

                elif(enemy_last_positions[i][0] == enemy.xcor() and enemy_last_positions[i][1] >= enemy.ycor()):
                    enemy.setheading((0))
                    enemy_next_pos = [enemy.xcor() + 20, enemy.ycor()]
                    recursive_path()

                elif(enemy_last_positions[i][0] == enemy.xcor() and enemy_last_positions[i][1] < enemy.ycor()):
                    enemy.setheading(180)
                    enemy_next_pos = [enemy.xcor() - 20, enemy.ycor()]
                    recursive_path()

                elif(enemy_last_positions[i][0] >= enemy.xcor() and enemy_last_positions[i][1] == enemy.ycor()):
                    enemy.setheading(270)
                    enemy_next_pos = [enemy.xcor(), enemy.ycor() - 20]
                    recursive_path()

                elif(enemy_last_positions[i][0] < enemy.xcor() and enemy_last_positions[i][1] == enemy.ycor()):
                    enemy.setheading(90)
                    enemy_next_pos = [enemy.xcor(), enemy.ycor() + 20]
                    recursive_path()
                break

        for i in snake_parts.keys():

            if(snake_last_positions[i][0] == snake_next_pos[0] and snake_last_positions[i][1] == snake_next_pos[1]):

                if(i > 0 and snake_last_positions[i][0] == snake.xcor() and snake_last_positions[i - 1][0] < snake_last_positions[i][0]):
                    snake.setheading(0)
                    snake_next_pos = [snake.xcor() + 20, snake.ycor()]
                    recursive_path()

                elif(i > 0 and snake_last_positions[i][0] == snake.xcor() and snake_last_positions[i - 1][0] > snake_last_positions[i][0]):
                    snake.setheading(180)
                    snake_next_pos = [snake.xcor() - 20, snake.ycor()]
                    recursive_path()

                elif(i > 0 and snake_last_positions[i - 1][1] > snake_last_positions[i][1] and snake_last_positions[i][1] == snake.ycor()):
                    snake.setheading(270)
                    snake_next_pos = [snake.xcor(), snake.ycor() - 20]
                    recursive_path()

                elif(i > 0 and snake_last_positions[i - 1][1] < snake_last_positions[i][1] and snake_last_positions[i][1] == snake.ycor()):
                    snake.setheading(90)
                    snake_next_pos = [snake.xcor(), snake.ycor() + 20]
                    recursive_path()

                elif(snake_last_positions[i][0] == snake.xcor() and snake_last_positions[i][1] >= snake.ycor()):
                    snake.setheading((0))
                    snake_next_pos = [snake.xcor() + 20, snake.ycor()]
                    recursive_path()

                elif(snake_last_positions[i][0] == snake.xcor() and snake_last_positions[i][1] < snake.ycor()):
                    snake.setheading(180)
                    snake_next_pos = [snake.xcor() - 20, snake.ycor()]
                    recursive_path()

                elif(snake_last_positions[i][0] >= snake.xcor() and snake_last_positions[i][1] == snake.ycor()):
                    snake.setheading(270)
                    snake_next_pos = [snake.xcor(), snake.ycor() - 20]
                    recursive_path()

                elif(snake_last_positions[i][0] < snake.xcor() and snake_last_positions[i][1] == snake.ycor()):
                    snake.setheading(90)
                    snake_next_pos = [snake.xcor(), snake.ycor() + 20]
                    recursive_path()
                break

    for i in snake_parts.keys():
        if(enemy_next_pos[0] == snake_last_positions[i][0] and enemy_next_pos[1] == snake_last_positions[i][1] or enemy_next_pos == snake_next_pos or enemy_next_pos[0] == snake.xcor() and enemy_next_pos[1] == snake.ycor()):
            if(enemy.heading() == 270):
                enemy.setheading(0)
            else:
                enemy.setheading(enemy.heading()+90)
    for i in enemy_parts.keys():
        if(snake_next_pos[0] == enemy_last_positions[i][0] and snake_next_pos[1] == enemy_last_positions[i][1] or snake_next_pos == enemy_next_pos or snake_next_pos[0] == enemy.xcor() and snake_next_pos[1] == enemy.ycor()):
            if(snake.heading() == 270):
                snake.setheading(0)
            else:
                snake.setheading(snake.heading()+90)

    if (enemy.distance(food) < 19):
        food.goto(random.randrange(-980, 981, 20),
                  random.randrange(-980, 981, 20))
        enemy_body_part = turtle.Turtle()
        enemy_body_part.shape("circle")
        enemy_body_part.color("green")
        enemy_body_part.penup()
        enemy_parts[enemy_score] = enemy_body_part
        enemy_score += 1
        enemy_score_writer.clear()
        enemy_score_writer._write('EnemyScore: ' + str(enemy_score),
                                  align='left', font='tahoma')

    if(len(enemy_parts.keys()) >= 1):
        for i in enemy_parts.keys():
            if(round(enemy.xcor()) == round(enemy_last_positions[i][0]) and round(enemy.ycor()) == round(enemy_last_positions[i][1])):
                enemy_alive = False
            if(len(enemy_parts.keys()) >= 2 and len(enemy_parts.keys()) - i-2 >= 0):
                enemy_last_positions[len(
                    enemy_parts.keys())-i-1] = enemy_last_positions[len(enemy_parts.keys())-i-2]
            enemy_parts[i].goto(enemy_last_positions[i])
        enemy_last_positions[0] = [enemy.xcor(), enemy.ycor()]

    # PLAYER

    if(snake.ycor() > 1000 or snake.ycor() < -1000 or snake.xcor() > 1000 or snake.xcor() < -1000):
        alive = False

    if (snake.distance(food) < 19):
        food.goto(random.randrange(-980, 981, 20),
                  random.randrange(-980, 981, 20))
        body_part = turtle.Turtle()
        body_part.speed(0)
        body_part.shape("circle")
        body_part.color("green")
        body_part.penup()
        snake_parts[score] = body_part
        score += 1
        score_writer.clear()
        score_writer._write('PlayerScore: ' + str(score),
                            align='left', font='tahoma')
        if(score > high_score):
            high_score_writer.clear()
            high_score_writer._write(
                'HighScore: ' + str(score), align='left', font='tahoma')

    if(len(snake_parts.keys()) >= 1):
        for i in snake_parts.keys():
            if(round(snake.xcor()) == round(snake_last_positions[i][0]) and round(snake.ycor()) == round(snake_last_positions[i][1])):
                alive = False
            if(len(snake_parts.keys()) >= 2 and len(snake_parts.keys()) - i-2 >= 0):
                snake_last_positions[len(
                    snake_parts.keys())-i-1] = snake_last_positions[len(snake_parts.keys())-i-2]
            snake_parts[i].goto(snake_last_positions[i])
        snake_last_positions[0] = [snake.xcor(), snake.ycor()]

    # COLLISION

    for i in enemy_parts.keys():
        if(round(snake.xcor()) == round(enemy_last_positions[i][0]) and round(snake.ycor()) == round(enemy_last_positions[i][1])):
            alive = False
    for i in snake_parts.keys():
        if(round(enemy.xcor()) == round(snake_last_positions[i][0]) and round(enemy.ycor()) == round(snake_last_positions[i][1])):
            enemy_alive = False
    if(round(snake.xcor()) == round(enemy.xcor()) and round(snake.ycor()) == round(enemy.ycor())):
        alive = False
        enemy_alive = False

    if(not enemy_alive):
        for j in enemy_parts.keys():
            enemy_parts[j].reset()
        enemy_score = 0
        enemy_parts = {}
        enemy_last_positions = {}
        enemy.goto(-900, 900)
        enemy_last_positions[0] = [enemy.xcor(), enemy.ycor()]
        enemy_score_writer.clear()
        enemy_score_writer._write('EnemyScore: ' + str(enemy_score),
                                  align='left', font='tahoma')
        gc.collect()
        enemy_alive = True

    if(not alive):
        # game_over_writer._write('GAME OVER RESTART IN: 3' , align='center', font='tahoma')
        # time.sleep(1)
        # game_over_writer.clear()
        # game_over_writer._write('GAME OVER RESTART IN: 2' , align='center', font='tahoma')
        # time.sleep(1)
        # game_over_writer.clear()
        # game_over_writer._write('GAME OVER RESTART IN: 1' , align='center', font='tahoma')
        # time.sleep(1)
        # game_over_writer.clear()
        for i in snake_parts.keys():
            snake_parts[i].reset()
        food.goto(random.randrange(-980, 981, 20),
                  random.randrange(-980, 981, 20))
        score = 0
        snake_parts = {}
        snake_last_positions = {}
        snake.goto(900, -900)
        snake_last_positions[0] = [snake.xcor(), snake.ycor()]
        score_writer.clear()
        score_writer._write('PlayerScore: ' + str(score),
                            align='left', font='tahoma')
        gc.collect()
        alive = True
    recursive_path()
