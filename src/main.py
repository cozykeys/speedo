#!/usr/bin/env python

from speedo import Point, Square, Circle, Keycap


def generate_thumb_cluster():
    circle = Circle()

    # This magic number doesn't come from anywhere special; I found through
    # trial and error that it was a decent value for generating the thumb keys
    circle.radius = 82

    angles = [80, 65, 50, 35]
    thumb_keys = []

    for angle in angles:
        point = circle.get_point(angle)

        square = Square()
        square.angle = angle
        square.radius = Keycap.DIAMETER_MM / 2
        square.position = point

        adjusted_square = square.get_adjusted()
        print(adjusted_square.to_string())

        thumb_keys.append(adjusted_square)

    return thumb_keys


def main():
    thumb_keys = generate_thumb_cluster()


if __name__ == "__main__":
    main()
