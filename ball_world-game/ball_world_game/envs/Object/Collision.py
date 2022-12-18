
def check_collison(obstacle, ball, previous, current, rng):
    
    flag = -1
    tolerance = 10
    x_sign = 1 if ball.speed[0] >= 0 else -1
    y_sign = 1 if ball.speed[1] >= 0 else -1
    if obstacle.rect.colliderect(ball.rect):
        if abs(obstacle.rect.top - ball.rect.bottom) < tolerance and ball.speed[1] > 0:
            ball.speed[1] *= -1
            #ball.speed[0] += rng.uniform(0.2, 0.3) * (rng.integers(0, 2) * 2 - 1)
            ball.speed[0] += x_sign * rng.uniform(0.05, 0.08)
            flag = current
        elif abs(obstacle.rect.bottom - ball.rect.top) < tolerance and ball.speed[1] < 0:
            ball.speed[1] *= -1
            #ball.speed[0] += rng.uniform(0.2, 0.3) * (rng.integers(0, 2) * 2 - 1)
            ball.speed[0] += x_sign * rng.uniform(0.05, 0.08)
            flag = current + 1
        if abs(obstacle.rect.left - ball.rect.right) < tolerance and ball.speed[0] > 0:
            ball.speed[0] *= -1
            #ball.speed[1] += rng.uniform(0.2, 0.3) * (rng.integers(0, 2) * 2 - 1)
            ball.speed[1] += y_sign * rng.uniform(0.05, 0.08)
            flag = current + 2
        elif abs(obstacle.rect.right - ball.rect.left) < tolerance and ball.speed[0] < 0:
            ball.speed[0] *= -1
            #ball.speed[1] += rng.uniform(0.2, 0.3) * (rng.integers(0, 2) * 2 - 1)
            ball.speed[1] += y_sign * rng.uniform(0.05, 0.08)
            flag = current + 3


    return flag


def ball_collide_with_obstacles(ball, obstacles, previous_collison, rng):
    tmp_pre = -1
    for i, obstacle in enumerate(obstacles):
        collide = check_collison(obstacle, ball, previous_collison, i * 4, rng)
        if collide >= 0:
            tmp_pre = collide
            break
    previous_collison = tmp_pre
    return previous_collison