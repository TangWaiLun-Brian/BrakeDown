import pygame

def check_collison(obstacle, ball, previous, current, rng):
    '''
    We implement the check collison code with reference to
    https://youtu.be/1_H7InPMjaY
    '''

    # For each of the case, the ball is judged to be collided with obstacle when
    # the distance two adjacent sides are within a certain tolerance
    # Also We check the ball speed direction to avoid double counting the same collision
    flag = -1
    tolerance = 10
    x_sign = 1 if ball.speed[0] >= 0 else -1
    y_sign = 1 if ball.speed[1] >= 0 else -1
    if obstacle.rect.colliderect(ball.rect):
        if abs(obstacle.rect.top - ball.rect.bottom) < tolerance and ball.speed[1] > 0:
            ball.speed[1] += -0.02
            ball.speed[1] *= -1.02
            ball.speed[0] += x_sign * rng.uniform(0.05, 0.2)
            flag = current
        elif abs(obstacle.rect.bottom - ball.rect.top) < tolerance and ball.speed[1] < 0:
            ball.speed[1] -= 0.02
            ball.speed[1] *= -1.02
            ball.speed[0] += x_sign * rng.uniform(0.05, 0.2)
            flag = current + 1
        if abs(obstacle.rect.left - ball.rect.right) < tolerance and ball.speed[0] > 0:
            ball.speed[0] += 0.02
            ball.speed[0] *= -1.02
            ball.speed[1] += y_sign * rng.uniform(0.05, 0.2)
            flag = current + 2
        elif abs(obstacle.rect.right - ball.rect.left) < tolerance and ball.speed[0] < 0:
            ball.speed[0] -= 0.02
            ball.speed[0] *= -1.02
            ball.speed[1] += y_sign * rng.uniform(0.05, 0.2)
            flag = current + 3


    return flag


def ball_collide_with_obstacles(ball, obstacles, previous_collison, rng):
    '''
    This function checks if any obstacle collides with ball.
    Counting one of valid collisions only (obstacles can overlap each other, such action avoid double counting)
    '''
    tmp_pre = -1
    for i, obstacle in enumerate(obstacles):
        collide = check_collison(obstacle, ball, previous_collison, i * 4, rng)
        if collide >= 0:
            tmp_pre = collide
            break
    previous_collison = tmp_pre
    return previous_collison
