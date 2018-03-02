#!/usr/bin/env python

from speedo import Point, Square, Circle, Keycap, Switch, Column


# TODO: Deserialize this from a json file
def get_switch_data():
    return {
        "columns": [
            Column(0, 3, 80, 5),
            Column(0, 3, 80, 5),
            Column(0, 6, 80, 5),
            Column(0, 11, 80, 5),
            Column(0, 5, 80, 5),
            Column(0, 0, 80, 5)
        ]
    }


def generate_columns():
    columns = get_switch_data()["columns"]

    for i in range(0, len(columns)):
        if i > 0:
            columns[i].x_offset = columns[i - 1].x_offset \
                + Switch.MM_BETWEEN_HORIZONTAL

        columns[i].initialize_switches()

        print('Column:')
        for switch in columns[i].switches:
            print('  {0}'.format(switch.position.to_string()))


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
    generate_columns()


if __name__ == "__main__":
    main()
