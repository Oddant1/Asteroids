from proj import *
from bullet import *
from ship import *
from asteroid import *
from vec2 import *
from mat2 import *
from drawn_object import *

def main():

    # Initialize turtle parameters
    tracer(0)
    bgcolor('BLACK')

    # Create our player, bullet list, and asteroid list
    player, bullets, asteroids, fragments, hud = initialize()

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
        hud.draw_object()

        # Check for bullet collision with asteroids then move and draw bullets
        for i in reversed(range(len(bullets))):
            # See if the bullet has traveled max distance
            bullets[i].decrement_timer()
            if bullets[i].timer <= 0:
                del bullets[i]
                continue
            # See if bullet collided with an asteroid
            collided, asteroid_index = bullets[i].continuous_collision_check(asteroids)
            # Check for a collision
            if collided:
                # Split the asteroid
                asteroids[asteroid_index].split(asteroids, fragments)
                # Clean up our asteroid and bullet
                del asteroids[asteroid_index]
                del bullets[i]
                continue
            bullets[i].move_object()
            bullets[i].draw_object()

        # Move and draw all asteroids
        for i in reversed(range(len(asteroids))):
            # Move the asteroids
            asteroids[i].move_object()
            # If the player isn't respawning check collision
            if not player.respawning:
                if asteroids[i].collision_testing(player, False):
                    # Kill the player and split the asteroid they hit
                    player.respawn(hud)
                    asteroids[i].split(asteroids, fragments)
                    del asteroids[i]
                    continue
            # Draw the asteroid if it wasn't hit
            asteroids[i].draw_object()

        # Move and draw all fragmentsS
        for i in reversed(range(len(fragments))):
            fragments[i].decrement_timer()
            # Kill fragments if they run out of time
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
    # Create the initial hud
    hud = HUD(player)
    # Create a list to contain the bullets
    bullets = []
    # Creates a list to contain asteroid fragments
    fragments = []
    # Create the initial four asteroids
    asteroids = []
    for i in range(4):
        asteroids.append(Asteroid())

    # Return a list of the player the bullet list, the asteroid list, and the fragment list
    return player, bullets, asteroids, fragments, hud


# Get user input
def get_input(player, bullets):

    # Move the ship forward
    if is_pressed('w'):
        player.accelerate_object()
    elif player.velocity.get_magnitude() > 0:
        player.decelerate_object()
    # Rotate the ship right
    if is_pressed('d'):
        player.rotate_object('d')
    # Rotate the ship left
    elif is_pressed('a'):
        player.rotate_object('a')
    # Fire a bullet
    if player.queued_shots == 0:
        if is_pressed(' '):
            player.shoot(bullets)
            player.shot_last_frame = True
        else:
            player.shot_last_frame = False
    else:
        player.shoot(bullets)


main()
win.exitonclick()
