from proj import *
from bullet import *
from ship import *
from asteroid import *
from vec2 import *
from mat2 import *
from drawn_object import *

# Due to the way Python deals with deleting objects (they get garbage collected
# when all references are gone) I can't figure out how to delete the asteroids
# or bullets from within their own class code, so it's done here. I know it looks
# weird but that's why. If anyone can change this then awesome
def main():

    # Get the turtle window
    tracer(0)
    bgcolor('BLACK')

    # Create our player, bullet list, and asteroid list
    player, bullets, asteroids, fragments = initialize()

    # Game loop
    while True:

        # Get the time at the start of this frame
        start_time = clock()
        # Must clear entire previous frame if using single turtle
        Drawn_Object.drawer.clear()

        # Get input from the player
        get_input(player, bullets)
        # Move the player if they have velocity
        if player.velocity.get_magnitude() > 0:
            player.move_object()
        # Draw the player for this frame
        player.draw_object()

        # Keep track of bullets to be deleted
        to_delete = []
        # Keep track of asteroids to split
        to_split = []

        # Move and draw all bullets then check for collision with asteroids
        for i in range(len(bullets)):
            # See if the bullet has traveled max distance
            bullets[i].life -= bullets[i].speed
            if bullets[i].life <= 0:
                to_delete.append(i)
            else:
                # See if bullet collided with an asteroid
                collision_info = bullets[i].check_collision(asteroids)
                if collision_info[0]:
                    to_delete.append(i)
                    to_split.append(collision_info[1])
                else:
                    bullets[i].move_object()
                    bullets[i].draw_object()

        # Delete all marked bullets
        for i in reversed(to_delete):
            del bullets[i]
        # Split all asteroids in the list
        for i in reversed(to_split):
            if asteroids[i].life <= 1:
                fragments += asteroids[i].split(asteroids[i])
            else:
                asteroids[i].split(asteroids)
            del asteroids[i]

        # Move and draw all asteroids
        for i in reversed(range(len(asteroids))):
            asteroids[i].move_object()
            asteroids[i].draw_object()

        # Move and draw all fragmentsS
        for i in reversed(range(len(fragments))):
            fragments[i].timer -= fragments[i].velocity.get_magnitude()
            if fragments[i].timer <= 0:
                del fragments[i]
                continue
            fragments[i].move_object()
            fragments[i].draw_object()

        # Draw the new frame to the screen
        update()

        # Keep the frames
        elapsed_time = clock()
        if (frame - (elapsed_time - start_time)) > 0:
            sleep(frame - (elapsed_time - start_time))
        else:
            print(frame - (elapsed_time - start_time))


def initialize():

    # Create the player's ship
    player = Ship()
    # Create a list to contain the bullets
    bullets = []
    # Creates a list to contain asteroid fragments
    fragments = []

    # Create the initial four asteroids
    asteroids = []
    for i in range(4):
        asteroids.append(Asteroid())

    # Return a list of the player the bullet list, the asteroid list, and the
    # fragment list
    return [player, bullets, asteroids, fragments]


# Get user input
def get_input(player, bullets):

    # Move the ship forward
    if is_pressed('w'):
        player.accelerate_ship()
    elif player.velocity.get_magnitude() > 0:
        player.decelerate_ship()
    # Rotate the ship right
    if is_pressed('d'):
        player.rotate_object('d')
    # Rotate the ship left
    elif is_pressed('a'):
        player.rotate_object('a')
    # Fire a bullet
    if is_pressed(' '):
        if len(bullets) < 4:
            player.shoot(bullets)

main()
win.exitonclick()
