import numpy as np

WIDTH = 800
HEIGHT = 600

ship = Actor('tship')
ship.pos = 400, 300
ship.direction = 1
ship.velocity = 1
ship.angle = 0

bullets = []
asteroids = []


def reset():
    global asteroids
    asteroids = []
    global bullets
    bullets = []
    ship.pos = 400, 300


def draw():
    screen.fill((0, 0, 0))
    # Draw our main game objects: the ship, bullets, and asteroid
    ship.draw()
    for a in asteroids:
        if a.draw_me:
            a.draw()
    for b in bullets:
        b.draw()


def on_key_down(key):
    if key == keys.LEFT:  # Turn
        ship.angle += 10
    elif key == keys.RIGHT:  # Turn
        ship.angle -= 10
    elif key == keys.UP:  # Thruster
        if ship.velocity < 1000:
            ship.velocity += 10

    elif key == keys.SPACE:  # Fire!
        bullet = Actor('tbullet')
        bullet.angle = ship.angle
        bullet.pos = ship.pos
        bullet.velocity = ship.velocity + 500
        bullets.append(bullet)
    elif key == keys.ESCAPE:  # Reset Game State
        reset()


def add_asteroid():
    asteroid = Actor('asteroid')
    asteroid.pos = (400, 300)
    asteroid.angle = np.random.randint(180)
    asteroid.velocity = 500
    asteroid.draw_me = True
    asteroids.append(asteroid)


def update_position(obj):
    obj.x -= obj.velocity * np.sin(np.deg2rad(obj.angle)) / (2 * np.pi)
    obj.y -= obj.velocity * np.cos(np.deg2rad(obj.angle)) / (2 * np.pi)


timer = TIMEOUT = 10


def update():
    # Update Ship Positions
    update_position(ship)
    # Update Bullet Positions
    for b in bullets:
        update_position(b)
    for a in asteroids:
        update_position(a)

    # Detect bullet-asteroid collisions
    for b in bullets:
        for a in asteroids:
            if b.colliderect(a):
                a.draw_me = False

    # Ship Wrap-Around
    if ship.left > WIDTH:
        ship.right = 0
    elif ship.right < 0:
        ship.right = WIDTH

    elif ship.bottom < 0:
        ship.top = HEIGHT
    elif ship.top > HEIGHT:
        ship.bottom = 0

    # Dispatch a new asteroid
    global timer
    timer -= 1
    if timer == 0:
        timer = TIMEOUT
        add_asteroid()

    # "Frictional" Slow-Down
    if ship.velocity > 0:
        ship.velocity -= 1

    # TODO: retire off-screen stuff!
