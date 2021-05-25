import pygame as pg
from math import sqrt

G = 4.30091e-3

if __name__ == "__main__":
    bodiesX = [400, 450]
    bodiesY = [300, 350]
    bodiesVX = [0, 0]
    bodiesVY = [0, -0.02]
    bodiesMass = [10, 1]

    pg.init()
    screen = pg.display.set_mode((800, 600))

    dt = 0.5

    stop = False
    while not stop:
        # SIMULATE

        bodiesAX = [0 for i in range(len(bodiesX))]
        bodiesAY = [0 for i in range(len(bodiesX))]

        for i in range(len(bodiesX)):
            for j in range(len(bodiesX)):
                if i == j:
                    continue

                diffX = bodiesX[j] - bodiesX[i]
                diffY = bodiesY[j] - bodiesY[i]

                sqrnorm = diffX * diffX + diffY * diffY
                norm = sqrt(sqrnorm)

                unitX = diffX / norm
                unitY = diffY / norm

                bodiesAX[i] += unitX * G * bodiesMass[i] * \
                    bodiesMass[j] / (norm * norm)
                bodiesAY[i] += unitY * G * bodiesMass[i] * \
                    bodiesMass[j] / (norm * norm)

        for i in range(len(bodiesX)):
            bodiesAX[i] /= bodiesMass[i]
            bodiesAX[j] /= bodiesMass[j]

        for i in range(len(bodiesX)):
            bodiesX[i] += dt * bodiesVX[i]
            bodiesY[i] += dt * bodiesVY[i]
            bodiesVX[i] += dt * bodiesAX[i]
            bodiesVY[i] += dt * bodiesAY[i]

        # DRAW
        screen.fill((0, 0, 0))

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                stop = True

        for i in range(len(bodiesX)):
            pg.draw.circle(screen, (255, 255, 255),
                           (bodiesX[i], bodiesY[i]), 10, 0)

        pg.display.update()

    pg.display.quit()
