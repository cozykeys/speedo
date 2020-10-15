#!/usr/bin/env python3

import json
import os
import math

from .common import Corner
from .util import get_speedo_repo_dir
from .geometry import Polygon2D, Vector2D


class SwitchData:
    def __init__(self):
        self.switch_data = None

        path = os.path.join(get_speedo_repo_dir(), "data", "switches.json")

        with open(path, "r") as f:
            self.switch_data = json.loads(f.read())

        self.id_lookup = [
            # fmt: off
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),                         (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),         (2, 7),         (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),         (3, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),         (3, 6),         (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),         (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13),
            # fmt: on
        ]

    def get_switch_count(self):
        """Get the number of switches"""
        return len(self.id_lookup)

    def get_switches(self):
        """Find all the switches"""
        switches = []
        for (row, col) in self.id_lookup:
            switches.append(self.get_switch_by_coord(row, col))
        return switches

    def get_switch_by_ref(self, ref):
        """Find the switch by either the switch or diode reference (I.E. 'D00')"""
        switch_index = int(ref.replace("SW", "").replace("D", "")) - 1
        (row, col) = self.id_lookup[switch_index]
        return self.get_switch_by_coord(row, col)

    def get_switch_by_coord(self, row, col):
        """Find the switch by its row and column"""
        for s in self.switch_data:
            if s["row"] == row and s["column"] == col:
                return s
        return None

    def get_corner(self, coord, corner):
        """TODO"""
        d = 9.525
        s = self.get_switch_by_coord(coord[0], coord[1])
        p = Polygon2D(
            [
                Vector2D(s["x"] - d, s["y"] - d),
                Vector2D(s["x"] + d, s["y"] - d),
                Vector2D(s["x"] + d, s["y"] + d),
                Vector2D(s["x"] - d, s["y"] + d),
            ]
        ).rotated_around(math.radians(s["rotation"]), Vector2D(s["x"], s["y"]))

        if corner == Corner.TOP_LEFT:
            return (round(p.vertices[0].x, 3), round(p.vertices[0].y, 3))
        elif corner == Corner.TOP_RIGHT:
            return (round(p.vertices[1].x, 3), round(p.vertices[1].y, 3))
        elif corner == Corner.BOTTOM_RIGHT:
            return (round(p.vertices[2].x, 3), round(p.vertices[2].y, 3))
        elif corner == Corner.BOTTOM_LEFT:
            return (round(p.vertices[3].x, 3), round(p.vertices[3].y, 3))

    def get_midpoint(self, s1_coord, s2_coord):
        """TODO"""
        s1 = self.get_switch_by_coord(s1_coord[0], s1_coord[1])
        s2 = self.get_switch_by_coord(s2_coord[0], s2_coord[1])

        x = round(s1["x"] + ((s2["x"] - s1["x"]) / 2.0), 3)
        y = round(s1["y"] + ((s2["y"] - s1["y"]) / 2.0), 3)

        return (x, y)
