"""
Draw a polygonal cat using Turtle graphics with a dash of randomness.
"""

import random
import turtle

import numpy as np


def draw_polygon(pen, vertices, fill_color):
    """Draw a filled polygon from a list of (x, y) vertices."""
    pen.color("black", fill_color)
    pen.up()
    pen.goto(vertices[0])
    pen.down()
    pen.begin_fill()
    for vertex in vertices[1:]:
        pen.goto(vertex)
    pen.goto(vertices[0])
    pen.end_fill()


def jitter(vertices, amount=5):
    """Add a slight random jitter so each cat looks unique."""
    return [
        (x + random.uniform(-amount, amount), y + random.uniform(-amount, amount))
        for x, y in vertices
    ]


def polygonal_cat(seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    turtle.colormode(255)
    screen = turtle.Screen()
    screen.bgcolor("#f0f0f0")

    pen = turtle.Turtle()
    pen.speed("fastest")
    pen.hideturtle()

    base_palette = np.array(
        [
            [199, 181, 155],
            [168, 142, 122],
            [140, 120, 110],
            [90, 70, 60],
            [230, 200, 170],
        ],
        dtype=float,
    )

    # Slightly tweak palette so each run feels unique but stays cohesive.
    palette = [
        tuple(np.clip(color + np.random.normal(0, 8, size=3), 60, 255).astype(int))
        for color in base_palette
    ]

    body_color = random.choice(palette)
    accent_color = random.choice([c for c in palette if c != body_color])

    body = [
        (-80, -40),
        (80, -40),
        (110, 40),
        (90, 110),
        (-90, 110),
        (-110, 40),
    ]

    head = [
        (-60, 110),
        (60, 110),
        (70, 190),
        (0, 230),
        (-70, 190),
    ]

    ear_left = [(-58, 190), (-95, 255), (-30, 210)]
    ear_right = [(58, 190), (30, 210), (95, 255)]

    eye_left = [(-35, 170), (-15, 170), (-18, 185), (-32, 185)]
    eye_right = [(35, 170), (15, 170), (18, 185), (32, 185)]

    nose = [(-10, 150), (0, 140), (10, 150)]
    muzzle = [(-30, 135), (30, 135), (40, 120), (-40, 120)]

    tail = [(110, 40), (140, 60), (150, 120), (130, 140), (110, 120)]

    shapes = [
        (body, body_color),
        (tail, body_color),
        (head, accent_color),
        (ear_left, accent_color),
        (ear_right, accent_color),
        (muzzle, (255, 248, 240)),
        (nose, (250, 120, 120)),
        (eye_left, (255, 255, 255)),
        (eye_right, (255, 255, 255)),
    ]

    for vertices, color in shapes:
        draw_polygon(pen, jitter(vertices), color)
    print("Just to make a new PR.")
  
    turtle.done()


if __name__ == "__main__":
    polygonal_cat()

