from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
key_position = [100, 40, 1500]
key_collected = False
shards = []
is_raining = False
rain_drops = []
MAX_RAIN_DROPS = 50000
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GRID_LENGTH = 300
player_pos = [0, 0,-280]
player_angle = 0
camera_pos = [0, 500, 500]
bombs = []
coins=[]
coin_score=0
life = 5
game_score = 5
missed_bullets = 0
cheat_mode = False
game_over = False
game_win=False
bullets = []
enemies = []
time_tick = 0
MAX_ENEMIES = 25
first_person_mode = False

def radians(deg):
    return deg * math.pi / 180
def random_enemy_pos():
    room = random.choice([1, 2, 3])
    if room == 1:
        z_range = (-GRID_LENGTH, GRID_LENGTH)
    elif room == 2:
        z_range = (GRID_LENGTH + 40, int(GRID_LENGTH * 3.2 - 40))
    else:  # Room 3
        z_range = (int(GRID_LENGTH * 3.3), int(GRID_LENGTH * 5.5))
    return [
        random.randint(-GRID_LENGTH + 20, GRID_LENGTH - 20),
        25,
        random.randint(*z_range)
    ]
def draw_key():
    global key_collected, coin_score
    if coin_score >= 6 and not key_collected:
        glPushMatrix()
        glColor3f(1.0, 1.0, 0.0)  # Yellow color
        glTranslatef(key_position[0], key_position[1], key_position[2])
        glRotatef(90, 1, 0, 0)
        glutSolidSphere(10, 20, 20)
        gluCylinder(gluNewQuadric(),5, 5, 25, 10, 10)# Key shape
        glPopMatrix()
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glColor3f(1, 1, 1)
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glEnable(GL_DEPTH_TEST)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 1, 0)
    #head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 65, 0)
    glutSolidSphere(10, 20, 20)
    glPopMatrix()
    #body
    glColor3f(0.4, 0.8, 0.4)
    glPushMatrix()
    glTranslatef(0, 44, 0)
    glutSolidCube(22)
    glPopMatrix()
    #arms
    glColor3f(1, 0.8, 0.6)
    arm = gluNewQuadric()
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 10, 55, 0)
        gluCylinder(arm, 6, 2.5, 25, 10, 10)

        glPopMatrix()
    #legs
    glColor3f(0.2, 0.2, 1)
    leg = gluNewQuadric()
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 7, 0, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(leg, 3, 7, 30, 10, 10)
        glPopMatrix()
    #gun
    glColor3f(1, 1, 0)
    glPushMatrix()
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 8, 2, 30, 10, 10)
    glPopMatrix()
    glPopMatrix()
def draw_enemy(pos):
    glPushMatrix()
    glTranslatef(*pos)
    scale = 1 + 0.1 * math.sin(time_tick + pos[0])
    glScalef(scale, scale, scale)
    glColor3f(1, 0, 0)
    glTranslate(0,30,0)
    glutSolidSphere(20, 20, 20)
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 10, 26, 0)
        glColor3f(1, 1, 1)
        glutSolidSphere(6, 20, 20)
        glPopMatrix()
    glPopMatrix()
def draw_shards():
    glColor3f(1, 0, 1)
    for shard in shards:
        glPushMatrix()
        glTranslatef(*shard)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 6, 0.5, 15, 10, 10)
        glPopMatrix()
def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(*bullet['pos'])
    glColor3f(0, 1, 0)
    glutSolidCube(5)
    glPopMatrix()
def draw_bombs():
    glColor3f(0.5, 0.0, 0.0)
    for bomb in bombs:
        glPushMatrix()
        glTranslatef(bomb[0], bomb[1], bomb[2])
        glutSolidCube(50)
        glPopMatrix()
def draw_walls():
    wall_height = 50
    wall_thickness = 5
    glColor3f(0.4, 0.5, 0.6)
    # Back wall
    glPushMatrix()
    glTranslatef(0, wall_height / 2, -GRID_LENGTH)
    glScalef(GRID_LENGTH * 2, wall_height, wall_thickness)
    glutSolidCube(1)
    glPopMatrix()
    #2nd wall
    glPushMatrix()
    glTranslatef(0, wall_height / 2, GRID_LENGTH)
    glScalef(GRID_LENGTH * 2, wall_height, wall_thickness)
    glutSolidCube(1)
    glPopMatrix()
    #3rdwall
    glPushMatrix()
    glTranslatef(0, wall_height / 2, GRID_LENGTH*3.23)
    glScalef(GRID_LENGTH * 2, wall_height, wall_thickness)
    glutSolidCube(1)
    glPopMatrix()
    #4thwall
    glPushMatrix()
    glTranslatef(0, wall_height / 2, GRID_LENGTH * 5.6)
    glScalef(GRID_LENGTH * 2, wall_height, wall_thickness)
    glutSolidCube(1)
    glPopMatrix()

def draw_rain():
    glColor3f(0.5, 0.5, 1.0)
    for drop in rain_drops:
        glPushMatrix()
        glTranslatef(*drop)
        gluSphere(gluNewQuadric(), 2, 6, 6)
        glPopMatrix()

def draw_coins():
    glColor3f(1, 1, 0)  # Yellow color for coins
    for coin in coins:
        glPushMatrix()
        glTranslatef(*coin)
        glutSolidSphere(5, 10, 10)  # Draw a sphere as the coin
        glPopMatrix()
def draw_grid():
    square_size = 40
    num_rows = 50  # Extended for three rooms
    num_cols = 15
    start_x = -GRID_LENGTH
    start_z = -GRID_LENGTH
    for i in range(num_rows):
        for j in range(num_cols):
            x = start_x + j * square_size
            z = start_z + i * square_size

            # Color differently in each room
            if z > GRID_LENGTH *3.2:
                glColor3f(1.0, 1.0, 1.0) if (i + j) % 2 == 0 else glColor3f(0.2, 0.4, 0.9)
            elif z > GRID_LENGTH:
                glColor3f(0.9, 1.0, 1.0) if (i + j) % 2 == 0 else glColor3f(0.8, 0.4, 0.9)
            else:
                glColor3f(1.0, 1.0, 1.0) if (i + j) % 2 == 0 else glColor3f(0.7, 0.6, 1.0)
            glBegin(GL_QUADS)
            glVertex3f(x, 0, z)
            glVertex3f(x + square_size, 0, z)
            glVertex3f(x + square_size, 0, z + square_size)
            glVertex3f(x, 0, z + square_size)
            glEnd()
def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, WINDOW_WIDTH / WINDOW_HEIGHT, 1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if first_person_mode:
        rad = math.radians(player_angle)
        eye_height = 50
        eye_x = player_pos[0]
        eye_y = player_pos[1] + eye_height
        eye_z = player_pos[2]
        center_x = eye_x + math.sin(rad)
        center_y = eye_y
        center_z = eye_z + math.cos(rad)
        gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, 0, 1, 0)
    else:
        cam_distance = 150
        cam_height = 80

        rad = math.radians(player_angle)

        cam_x = player_pos[0] - cam_distance * math.sin(rad)
        cam_y = player_pos[1] + cam_height
        cam_z = player_pos[2] - cam_distance * math.cos(rad)

        center_x = player_pos[0] + 30 * math.sin(rad)
        center_y = player_pos[1] + 20
        center_z = player_pos[2] + 30 * math.cos(rad)

        gluLookAt(cam_x, cam_y, cam_z,
                  center_x, center_y, center_z,
                  0, 1, 0)


def update_shards():
    global life
    if random.random() < 0.01:
        z = random.randint(int(GRID_LENGTH * 3.3), int(GRID_LENGTH * 5.5))
        x = random.randint(-GRID_LENGTH + 40, GRID_LENGTH - 40)
        shards.append([x, 30, z])
    for shard in shards[:]:
        dx = abs(shard[0] - player_pos[0])
        dz = abs(shard[2] - player_pos[2])

        if dx < 10 and dz < 10:
            life -= 1
            shards.remove(shard)
            print(f"Shard passed! Life: {life}")
def check_key_collection():
    global key_collected, game_win, enemies, bullets, bombs, shards

    if key_collected or game_win:
        return
    dx = abs(key_position[0] - player_pos[0])
    dy = abs(key_position[1] - player_pos[1])
    dz = abs(key_position[2] - player_pos[2])

    if dx < 20 and dy < 50 and dz < 20:
        key_collected = True
        game_win = not game_win
        enemies.clear()
        bullets.clear()
        bombs.clear()
        shards.clear()
        print(" Key collected! You won the game.")
def update_enemies():
    global life, game_over,game_win
    if game_over:
        return
    if game_win:
        return
    for enemy in enemies:
        direction = [player_pos[i] - enemy[i] for i in range(3)]
        dist = math.sqrt(sum([d**2 for d in direction]))
        if dist > 1:
            direction = [d / dist * 0.2 for d in direction]
            for i in range(3):
                enemy[i] += direction[i]
        enemy[1] = 25
        if dist < 30:
            life -= 1
            enemies.clear()
            break

    if life <= 0:
        game_over = True
        enemies.clear()

def update_coins():
    global coin_score,game_score
    for coin in coins[:]:
        dx = abs(coin[0] - player_pos[0])
        dz = abs(coin[2] - player_pos[2])
        if dx < 10 and dz < 10:
            coins.remove(coin)
            coin_score += 1
            print(f"Coin collected! coin: {coin_score}")
            break

def update_bullets():
    global missed_bullets, game_score
    for bullet in bullets[:]:
        for i in range(3):
            bullet['pos'][i] += bullet['dir'][i] * 10
        for enemy in enemies:
            dist = math.sqrt(sum((bullet['pos'][i] - enemy[i]) ** 2 for i in range(3)))
            if dist < 25:
                game_score += 1
                print("bullet is fired")
                enemies[enemies.index(enemy)] = random_enemy_pos()
                bullets.remove(bullet)
                break
        else:
            if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][2]) > GRID_LENGTH:
                missed_bullets += 1
                print(f" bullet missed{missed_bullets} ")
                bullets.remove(bullet)
def spawn_bombs():
    if GRID_LENGTH < player_pos[2] <= int(GRID_LENGTH * 3.5):
        if random.random() < 0.03:
            x = random.randint(-GRID_LENGTH + 40, GRID_LENGTH - 40)
            z = random.randint(GRID_LENGTH + 40, int(GRID_LENGTH * 3.5 - 40))
            bombs.append([x, 200, z])

def update_bombs():
    global life
    for bomb in bombs[:]:
        bomb[1] -= 0.5
        if bomb[1] <= 10:
            dx = abs(bomb[0] - player_pos[0])
            dz = abs(bomb[2] - player_pos[2])
            if dx < 50 and dz < 50:
                life -= 1
            bombs.remove(bomb)
def spawn_coins():
    if random.random() < 0.01:
        x = random.randint(-GRID_LENGTH + 40, GRID_LENGTH - 40)
        z = random.randint(-GRID_LENGTH + 40, GRID_LENGTH * 5 - 40)
        coins.append([x, 50, z])

def update_rain():
    global rain_drops
    if is_raining:
        if random.random() < 0.2:
            x = random.randint(-GRID_LENGTH+40, GRID_LENGTH - 40)
            z = random.randint(-GRID_LENGTH+40, GRID_LENGTH * 7 - 40)
            rain_drops.append([x, 200, z])

    for drop in rain_drops[:]:
        drop[1] -= 1.0

        if drop[1] < 0:
            rain_drops.remove(drop)
def keyboard(key, x, y):
    global player_angle, cheat_mode, life, game_score, missed_bullets, game_over,first_person_mode,is_raining,game_win
    if key == b'a':  # Rotate left
        player_angle += 5
    elif key == b'd':  # Rotate right
        player_angle -= 5
    elif key == b'c':
        cheat_mode = not cheat_mode
    elif key == b'v':
        if cheat_mode:
            first_person_mode = not first_person_mode
    elif key == b'r' or game_over or game_win:
        life = 5
        missed_bullets = 0
        game_score = 0
        coin_score=0
        game_over = False
        game_win= False
        key_position=[1000,40,-1000]
        player_pos[:] = [0, 0, 0]  # Reset player position
        enemies.clear()
        for _ in range(MAX_ENEMIES):
            enemies.append(random_enemy_pos())
    if key == b'm':
        is_raining = True
    elif key == b'n':
        is_raining = False

def special_keys(key, x, y):
    global player_angle, first_person_mode
    movement_x = 0
    movement_z = 0
    if key == GLUT_KEY_LEFT:
        movement_x = 10 * math.cos(math.radians(player_angle))
        movement_z = -10 * math.sin(math.radians(player_angle))
    elif key == GLUT_KEY_RIGHT:
        movement_x = -10 * math.cos(math.radians(player_angle))
        movement_z = 10 *  math.sin(math.radians(player_angle))
    elif key == GLUT_KEY_UP:
        movement_x = 10 * math.sin(math.radians(player_angle))
        movement_z = 10 * math.cos(math.radians(player_angle))
    elif key == GLUT_KEY_DOWN:
        movement_x = -10 * math.sin(math.radians(player_angle))
        movement_z = -10 * math.cos(math.radians(player_angle))
    new_x = player_pos[0] + movement_x
    new_z = player_pos[2] + movement_z
    if abs(new_x) > GRID_LENGTH - 10:
        return

    if new_z < -GRID_LENGTH + 10:
        return
    if new_z > GRID_LENGTH and coin_score < 3:
        new_z = GRID_LENGTH
    elif new_z > GRID_LENGTH * 3.2 and coin_score <5 :
        new_z = GRID_LENGTH*3.2
    elif new_z > GRID_LENGTH * 5.5:
        new_z = GRID_LENGTH * 5.5
    player_pos[0] = new_x
    player_pos[2] = new_z

def mouse(button, state, x, y):
    global first_person_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rad = math.radians(player_angle)
        dir = [math.sin(rad), 0, math.cos(rad)]
        bullet_start = [player_pos[0] + dir[0] * 30, 43, player_pos[2] + dir[2] * 30]
        bullets.append({'pos': bullet_start, 'dir': dir})
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode

def display():
    global player_angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setup_camera()
    if cheat_mode:
        player_angle +=2.5
        rad = math.radians(player_angle)
        dir = [math.sin(rad), 0, math.cos(rad)]
        bullet_start = [player_pos[0] + dir[0] * 30, 43, player_pos[2] + dir[2] * 30]
        bullets.append({'pos': bullet_start, 'dir': dir})
    draw_grid()
    draw_walls()
    if not first_person_mode:
        draw_player()

    for enemy in enemies:
        draw_enemy(enemy)
    for bullet in bullets:
        draw_bullet(bullet)
    for bomb in bombs:
        draw_bombs()
    for rain in rain_drops:
        draw_rain()
    for coin in coins:
        draw_coins()
    for shard in shards:
        draw_shards()
    draw_key()

    draw_text(10, 760, f"Player Life Remaining: {life}")
    draw_text(10, 740, f"Game Score: {game_score}")
    draw_text(10, 720, f"Player Bullet Missed: {missed_bullets}")
    draw_text(10,705,f"Coins Collected: {coin_score}")
    if game_over:
        draw_text(400, 400, "GAME OVER - Press R to Restart")
    if game_win:
        draw_text(400, 400, "You GOT THE KEY TO ESCAPE THE MAZE")
    glutSwapBuffers()

def idle():
    global time_tick
    time_tick += 0.05
    if not game_over and not game_win:
        update_enemies()
        update_bullets()
        spawn_bombs()
        update_bombs()
        update_rain()
        spawn_coins()
        update_coins()
        update_shards()
        check_key_collection()
        current_max = min(10, MAX_ENEMIES + game_score // 5)
        while len(enemies) < current_max:
            enemies.append(random_enemy_pos())


    glutPostRedisplay()

# --- Init ---
def init():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    for _ in range(MAX_ENEMIES):
        enemies.append(random_enemy_pos())

# --- Main Loop ---
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D OpenGL Intro")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)
    glutMainLoop()
if __name__ == "__main__":
    main()