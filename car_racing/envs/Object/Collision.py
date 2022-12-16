import random
def check_collison(obstacle, ball, ball_speed, previous, current):
    flag = -1
    if obstacle.rect.left <= ball.rect.right and obstacle.rect.right >= ball.rect.left and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current:
            ball_speed[0] *= -1
            ball_speed[1] += random.uniform(-1, 1)
        flag = current
    elif obstacle.rect.right >= ball.rect.left and obstacle.rect.left <= ball.rect.right and obstacle.rect.top <= ball.rect.centery <= obstacle.rect.bottom:
        if previous != current+1:
            ball_speed[0] *= -1
            ball_speed[1] += random.uniform(-1, 1)
        flag = current+1
    if obstacle.rect.top <= ball.rect.bottom and obstacle.rect.bottom >= ball.rect.top and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current+2:
            ball_speed[1] *= -1
            ball_speed[0] += random.uniform(-1, 1)
        flag = current+2
    elif obstacle.rect.bottom >= ball.rect.top and obstacle.rect.top <= ball.rect.bottom and obstacle.rect.left <= ball.rect.centerx <= obstacle.rect.right:
        if previous != current+3:
            ball_speed[1] *= -1
            ball_speed[0] += random.uniform(-1, 1)
        flag = current+3
    return flag