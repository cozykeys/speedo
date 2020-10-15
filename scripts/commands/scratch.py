#!/usr/bin/env python3

import json
import os
import argparse
import math
from typing import List, Dict, Tuple
from lib import (
    SvgStyle,
    SvgWriter,
    Vector2D,
    Segment2D,
    Polygon2D,
    get_speedo_repo_dir,
    SwitchData,
    Corner,
)


class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(round(self.x, 3), round(self.y, 3))


def project_from_point(x, y, magnitude, theta):
    return Vec2(x + magnitude * math.cos(theta), y + magnitude * math.sin(theta))


def add_scratch_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "scratch", help="Scratchpad, dumping ground for temporary code"
    )
    parser.set_defaults(func=scratch)


def scratch(args: argparse.Namespace) -> int:
    # Case Perimeter
    points = [
        # x, y, d, theta
        (-138.252, -56.626, 10.0, 135.0 - 10),
        (-80.581, -54.580, 5.0, 90.0 - 10),
        (-60.786, -51.090, 5.0, 90.0 - 10),
        (-25.175, -33.641, 10.0, 45.0 - 10),
        (25.175, -33.641, 10.0, 135.0 + 10),
        (60.786, -51.090, 5.0, 90.0 + 10),
        (80.581, -54.580, 5.0, 90.0 + 10),
        (138.252, -56.626, 10.0, 45.0 + 10),
        (154.974, 38.211, 10.0, -45.0 + 10),
        (23.137, 64.504, 5.0, 280),
        (-23.137, 64.504, 5.0, 260),
        (-154.974, 38.211, 10.0, 225.0 - 10),
        (-138.252, -56.626, 10.0, 135.0 - 10),
    ]

    # PCB Perimeter
    points = [
        # x, y, d, theta
        (-137.441, -55.467, 0.0, 0.0),
        (-79.770, -53.422, 0.0, 0.0),
        (-61.945, -50.279, 0.0, 0.0),
        (-26.334, -32.830, 0.0, 0.0),
        (26.334, -32.830, 0.0, 0.0),
        (61.945, -50.279, 0.0, 0.0),
        (79.770, -53.422, 0.0, 0.0),
        (137.441, -55.467, 0.0, 0.0),
        (153.816, 37.400, 0.0, 0.0),
        (117.230, 43.851, 0.0, 0.0),
        (60.534, 56.895, 0.0, 0.0),
        (23.948, 63.346, 0.0, 0.0),
        (23.948, 63.346, 5.0, 145.0),
        (-23.948, 63.346, 5.0, 35.0),
        (-23.948, 63.346, 0.0, 0.0),
        (-60.534, 56.895, 0.0, 0.0),
        (-117.230, 43.851, 0.0, 0.0),
        (-153.816, 37.400, 0.0, 0.0),
        (-137.441, -55.467, 0.0, 0.0),
    ]

    i = 0
    for p in points:
        dp = project_from_point(p[0], -p[1], p[2], math.radians(p[3]))

        if i == 0:
            print(
                '<AbsoluteMoveTo> <EndPoint X="{}" Y="{}" /> </AbsoluteMoveTo>'.format(
                    round(dp.x, 3), round(-dp.y, 3)
                )
            )
            i = 1
        else:
            print(
                '<AbsoluteLineTo> <EndPoint X="{}" Y="{}" /> </AbsoluteLineTo>'.format(
                    round(dp.x, 3), round(-dp.y, 3)
                )
            )

    return 0
