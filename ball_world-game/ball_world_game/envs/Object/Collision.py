
def check_collison(obstacle, ball, previous, current, rng):
    """flag = -1
    if obstacle.rect.left <= ball.rect.right and obstacle.rect.right >= ball.rect.left and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(-1, 1)
        flag = current
    elif obstacle.rect.right >= ball.rect.left and obstacle.rect.left <= ball.rect.right and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current+1:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(-1, 1)
        flag = current+1
    if obstacle.rect.top <= ball.rect.bottom and obstacle.rect.bottom >= ball.rect.top and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current+2:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(-1, 1)
        flag = current+2
    elif obstacle.rect.bottom >= ball.rect.top and obstacle.rect.top <= ball.rect.bottom and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current+3:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(-1, 1)
        flag = current+3
    return flag"""
    
    flag = -1
    tolerance = 10
    if obstacle.rect.colliderect(ball.rect):
        if abs(obstacle.rect.top - ball.rect.bottom) < tolerance and ball.speed[1] > 0:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(0.1, 0.2) * (rng.integers(0, 2) * 2 - 1)
            flag = current
        elif abs(obstacle.rect.bottom - ball.rect.top) < tolerance and ball.speed[1] < 0:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(0.1, 0.2) * (rng.integers(0, 2) * 2 - 1)
            flag = current + 1
        if abs(obstacle.rect.left - ball.rect.right) < tolerance and ball.speed[0] > 0:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(0.1, 0.2) * (rng.integers(0, 2) * 2 - 1)
            flag = current + 2
        elif abs(obstacle.rect.right - ball.rect.left) < tolerance and ball.speed[0] < 0:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(0.1, 0.2) * (rng.integers(0, 2) * 2 - 1)
            flag = current + 3

    """flag = -1
    # if min(abs(obstacle.rect.left - ball.rect.centerx), abs(obstacle.rect.right - ball.rect.centerx)) <= min(abs(obstacle.rect.top - ball.rect.centery), abs(obstacle.rect.bottom - ball.rect.centery)):
    if obstacle.rect.left <= ball.rect.right and obstacle.rect.right >= ball.rect.left and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(-1, 1)
        flag = current
    elif obstacle.rect.right >= ball.rect.left and obstacle.rect.left <= ball.rect.right and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current + 1:
            ball.speed[0] *= -1
            ball.speed[1] += rng.uniform(-1, 1)
        flag = current + 1
    # else
    if obstacle.rect.top <= ball.rect.bottom and obstacle.rect.bottom >= ball.rect.top and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current + 2:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(-1, 1)
        flag = current + 2
    elif obstacle.rect.bottom >= ball.rect.top and obstacle.rect.top <= ball.rect.bottom and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current + 3:
            ball.speed[1] *= -1
            ball.speed[0] += rng.uniform(-1, 1)
        flag = current + 3"""
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