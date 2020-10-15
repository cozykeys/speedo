import enum
import math
import inspect
import json
import os
import pcbnew
import wx

import sys

scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.append(scripts_dir)
from lib import SwitchData, Logger, get_speedo_repo_dir, Corner, Vector2D

# Useful documentation:
# - https://docs.kicad-pcb.org/doxygen/classMODULE.html
# - https://docs.kicad-pcb.org/doxygen/classBOARD.html

POSITION_SCALE = 1000000.0
ROTATION_SCALE = 10

MID_X = 172.9725

# TODO: These shouldn't need to be hard-coded but this needs to be resolved:
# https://gitlab.com/kicad/code/kicad/-/issues/4308
COZY_FOOTPRINT_LIBRARY_PATH = "/home/pewing/kicad/cozy-parts.pretty"


class Position:
    def __init__(self, x=0.0, y=0.0, r=0.0):
        self.x = x
        self.y = y
        self.r = r


class TextSize:
    def __init__(self, h=1.0, w=1.0, t=0.15):
        self.h = h
        self.w = w
        self.t = t


class Text:
    def __init__(
        self,
        text="",
        position=Position(),
        layer=pcbnew.F_SilkS,
        size=TextSize(),
        justify=pcbnew.GR_TEXT_HJUSTIFY_CENTER,
    ):
        self.text = text
        self.position = position
        self.layer = layer
        self.size = size
        self.justify = justify


class Graphic:
    def __init__(
        self,
        reference="",
        footprint="",
        library="",
        position=Position(),
        layer=pcbnew.F_SilkS,
    ):
        self.reference = reference
        self.footprint = footprint
        self.library = library
        self.position = position
        self.layer = layer


class LogLevel(enum.IntEnum):
    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4


class SpeedoKicadPluginDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Speedo Dialog", style=wx.RESIZE_BORDER)

        self.panel = wx.Panel(self)

        title = wx.StaticText(self.panel, wx.ID_ANY, "Speedo Plugin Log")
        self.log = wx.TextCtrl(
            self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH
        )
        button = wx.Button(self.panel, wx.ID_OK, label="OK")

        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        logSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(title, 0, wx.ALL, 5)
        logSizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        buttonSizer.Add(button, 0, wx.ALL | wx.EXPAND, 5)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(logSizer, 1, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(buttonSizer, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizerAndFit(topSizer)

    def LogClear(self, text):
        self.log.Clear()

    def LogAppend(self, level, text):
        lookup = {
            LogLevel.ERROR: ("ERROR", wx.RED),
            LogLevel.WARN: ("WARN", wx.YELLOW),
            LogLevel.INFO: ("INFO", wx.BLUE),
            LogLevel.DEBUG: ("DEBUG", wx.GREEN),
            LogLevel.TRACE: ("TRACE", wx.LIGHT_GREY),
        }

        (label, color) = lookup[level]

        self.log.SetDefaultStyle(wx.TextAttr(color))
        self.log.AppendText("[{}] {}\n".format(label, text))
        self.log.SetDefaultStyle(wx.TextAttr(wx.BLACK))


class SpeedoKicadPluginAction(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Speedo Plugin"
        self.category = "Modify PCB"
        self.description = "Place Speedo components"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            get_speedo_repo_dir(), "icon", "speedo_32x32.png"
        )
        self.version = "0.0.11"
        self.wx_version = wx.version()
        self.dialog = None
        self.footprints = None
        self.log_level = LogLevel.INFO
        self.local_build = False

    def Run(self):
        self.logger = Logger()
        self.initialize_dialog()
        self.log_info("Running version {}".format(self.version))
        self.log_info("Running wxPython version {}".format(self.wx_version))
        self.log_info("Logging to directory {}".format(self.logger.path))
        self.log_info("Setting icon to {}".format(self.icon_file_name))

        if self.local_build:
            self.initialize_footprint_cache()
        pcb = pcbnew.GetBoard()

        self.log_info("Running Speedo Kicad plugin")

        self.switch_data = SwitchData()

        # Positions & rotations for the RGB LEDs
        self.led_bearings = {
            "L1": (self.switch_data.get_midpoint((0, 8), (1, 8)), 180.0 + 10.0),
            "L2": (self.switch_data.get_midpoint((0, 10), (1, 10)), 180.0 + 10.0),
            "L3": (self.switch_data.get_midpoint((0, 12), (1, 12)), 180.0 + 10.0),
            "L4": (self.switch_data.get_midpoint((3, 12), (4, 12)), 0.0 + 10.0),
            "L5": (self.switch_data.get_midpoint((3, 10), (4, 10)), 0.0 + 10.0),
            "L6": (self.switch_data.get_midpoint((3, 8), (4, 8)), 0.0 + 10.0),
            "L7": (self.switch_data.get_midpoint((3, 5), (4, 5)), 0.0 - 10.0),
            "L8": (self.switch_data.get_midpoint((3, 3), (4, 3)), 0.0 - 10.0),
            "L9": (self.switch_data.get_midpoint((3, 1), (4, 1)), 0.0 - 10.0),
            "L10": (self.switch_data.get_midpoint((0, 1), (1, 1)), 180.0 - 10.0),
            "L11": (self.switch_data.get_midpoint((0, 3), (1, 3)), 180.0 - 10.0),
            "L12": (self.switch_data.get_midpoint((0, 5), (1, 5)), 180.0 - 10.0),
        }

        # Set switch and diode positions
        key_count = self.switch_data.get_switch_count()
        for i in range(0, key_count):
            key_id = "SW{}".format(str(i + 1))
            key = pcb.FindModuleByReference(key_id)
            if key == None:
                raise Exception("No key with id {} found".format(key_id))
            self.set_key_position(key)

            diode_id = "D{}".format(str(i + 1))
            diode = pcb.FindModuleByReference(diode_id)
            if diode == None:
                raise Exception("No diode with id {} found".format(diode_id))
            self.set_diode_position(diode)

        # Set LED and capacitor positions
        for i in range(0, 12):
            led_id = "L{}".format(i + 1)
            led = pcb.FindModuleByReference(led_id)
            if led == None:
                raise Exception("No led with id {} found".format(led_id))
            self.log_info("Found LED {}".format(led_id))
            self.set_led_position(led)

            capacitor_id = "C{}".format(i + 1)
            capacitor = pcb.FindModuleByReference(capacitor_id)
            if capacitor == None:
                self.log_warn("No capacitor with id {} found".format(capacitor_id))
            self.set_capacitor_position(capacitor)

        # Elite-C
        mcu_id = "U1"
        mcu = pcb.FindModuleByReference(mcu_id)
        if mcu == None:
            self.log_warn("No mcu with id {} found".format(mcu_id))
        else:
            self.log_info("Found MCU {}".format(mcu_id))
            self.set_mcu_position(mcu)

        # Remove all existing drawings on the Edge.Cuts line, then add the
        # desired edge cut segments
        for d in pcb.GetDrawings():
            if d.GetLayerName() == "Edge.Cuts":
                self.log_info("Found a drawing on Edge.Cuts layer")
                pcb.Remove(d)
        self.draw_edge_cuts(pcb)

        self.setup_text(pcb)
        self.setup_graphics(pcb)

    def log_error(self, message):
        self.log(LogLevel.ERROR, message)

    def log_warn(self, message):
        self.log(LogLevel.WARN, message)

    def log_info(self, message):
        self.log(LogLevel.INFO, message)

    def log_debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def log_trace(self, message):
        self.log(LogLevel.TRACE, message)

    def log(self, level, message):
        if int(level) > int(self.log_level):
            return
        if self.logger != None:
            self.logger.log(message)
        if self.dialog != None:
            self.dialog.LogAppend(level, message)

    def initialize_dialog(self):
        pcbnew_window = None
        for w in wx.GetTopLevelWindows():
            if w.GetTitle().startswith("Pcbnew"):
                pcbnew_window = w
                self.log_info("Pcbnew window found!")
                break

        self.dialog = None
        for child in w.GetChildren():
            if type(child) == SpeedoKicadPluginDialog:
                self.dialog = child
                self.log_info("Speedo window found!")
                break

        if self.dialog == None:
            self.dialog = SpeedoKicadPluginDialog(pcbnew_window)

        self.dialog.Show()
        self.dialog.SetSize(800, 600)

    def initialize_footprint_cache(self):
        self.footprints = {}
        libraryNames = pcbnew.GetFootprintLibraries()
        self.log_info("Initializing footprint cache:")
        self.log_debug("Footprints:")
        count = 0
        for l in libraryNames:
            self.log_debug("    {}".format(l))
            if not l in self.footprints:
                self.footprints[l] = []
            for f in pcbnew.GetFootprints(l):
                self.log_debug("        {}".format(f))
                self.footprints[l].append(f)
                count += 1
        self.log_info("Footprint cache initialized; {} footprints found".format(count))

    def set_key_position(self, key):
        ref = key.GetReference()
        pos = key.GetPosition()
        s = self.switch_data.get_switch_by_ref(ref)
        pos.x = int(s["x"] * POSITION_SCALE)
        pos.y = int(s["y"] * POSITION_SCALE)
        key.SetPosition(pos)
        key.SetOrientation(-s["rotation"] * ROTATION_SCALE)

    def set_diode_position(self, diode):
        ref = diode.GetReference()
        pos = diode.GetPosition()
        s = self.switch_data.get_switch_by_ref(ref)
        switch_pos = Vector2D(s["x"], s["y"])
        rot = 90 - s["rotation"]
        theta = None
        if s["diode_position"] == "left":
            theta = math.pi
        elif s["diode_position"] == "right":
            theta = 0.0
        elif s["diode_position"] == "top":
            theta = math.pi / 2.0
        elif s["diode_position"] == "bottom":
            theta = 1.5 * math.pi
        else:
            raise Exception("Unsupported diode position {}".format(s["diode_position"]))
        diode_pos = switch_pos.project(8.2625, theta + math.radians(s["rotation"]))
        pos.x = int(diode_pos.x * POSITION_SCALE)
        pos.y = int(diode_pos.y * POSITION_SCALE)
        diode.SetPosition(pos)
        if diode.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping diode {} because layer name {} is not B.Cu".format(
                    ref, diode.GetLayerName()
                )
            )
            diode.Flip(pos)
        diode.SetOrientation(rot * ROTATION_SCALE)

    def set_led_position(self, led):
        ref = led.GetReference()
        pos = led.GetPosition()

        x = self.led_bearings[ref][0][0]
        y = self.led_bearings[ref][0][1]
        rot = self.led_bearings[ref][1]

        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        led.SetPosition(pos)

        led.SetOrientation(rot * ROTATION_SCALE)

        if led.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping led {} because layer name {} is not B.Cu".format(
                    ref, led.GetLayerName()
                )
            )
            led.Flip(pos)

    def set_capacitor_position(self, capacitor):
        lookup_table = {
            "C1": (0.0, 5.0, 0.0),
            "C2": (10.0, 5.0, 0.0),
            "C3": (20.0, 5.0, 0.0),
            "C4": (30.0, 5.0, 0.0),
            "C5": (40.0, 5.0, 0.0),
            "C6": (50.0, 5.0, 0.0),
            "C7": (60.0, 5.0, 0.0),
            "C8": (70.0, 5.0, 0.0),
            "C9": (80.0, 5.0, 0.0),
            "C10": (90.0, 5.0, 0.0),
            "C11": (100.0, 5.0, 0.0),
            "C12": (110.0, 5.0, 0.0),
        }

        ref = capacitor.GetReference()
        pos = capacitor.GetPosition()

        led_id = ref.replace("C", "L")
        led_bearing = self.led_bearings[led_id]
        led_position = Vector2D(led_bearing[0][0], led_bearing[0][1])

        r = None
        theta = None
        if ref in ["C1", "C2", "C3"]:
            r = 10.0
            theta = -math.radians(100)
        elif ref in ["C4", "C5", "C6"]:
            r = 190.0
            theta = -math.radians(100)
        elif ref in ["C7", "C8", "C9"]:
            r = 170.0
            theta = -math.radians(80)
        elif ref in ["C10", "C11", "C12"]:
            r = -10.0
            theta = -math.radians(80)
        else:
            raise Exception("Invalid capacitor ID {}".format(ref))

        cap_position = led_position.project(4.14, theta)

        x = cap_position.x
        y = cap_position.y
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        capacitor.SetPosition(pos)
        capacitor.SetOrientation(r * ROTATION_SCALE)
        if capacitor.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping capacitor {} because layer name {} is not B.Cu".format(
                    ref, capacitor.GetLayerName()
                )
            )
            capacitor.Flip(pos)

    def set_mcu_position(self, mcu):
        ref = mcu.GetReference()
        pos = mcu.GetPosition()
        (x, y, r) = (172.9725, 62.209, 270)
        pos.x = int(x * POSITION_SCALE)
        pos.y = int(y * POSITION_SCALE)
        mcu.SetPosition(pos)
        mcu.SetOrientation(r * ROTATION_SCALE)
        if mcu.GetLayerName() != "B.Cu":
            self.log_info(
                "Flipping mcu {} because layer name {} is not B.Cu".format(
                    ref, mcu.GetLayerName()
                )
            )
            mcu.Flip(pos)

    def draw_edge_cuts(self, pcb):
        vertices = [
            (35.531, 21.792),
            (93.203, 23.837),
            (111.028, 26.98),
            (146.638, 44.429),
            (172.9725 - 6.35, 44.429),
            (172.9725 - 6.35, 44.429 + 30.48),
            (172.9725 + 6.35, 44.429 + 30.48),
            (172.9725 + 6.35, 44.429),
            (199.306, 44.429),
            (234.917, 26.98),
            (252.743, 23.837),
            (310.413, 21.792),
            (326.788, 114.659),
            (290.202, 121.11),
            (233.506, 134.154),
            (196.921, 140.605),
            (192.825, 137.737),
            (153.12, 137.737),
            (149.024, 140.605),
            (112.439, 134.154),
            (55.742, 121.11),
            (19.156, 114.659),
            (35.531, 21.792),
        ]

        l = len(vertices)
        for i in range(0, l):
            start = vertices[i]
            end = vertices[(i + 1) % l]
            segment = pcbnew.DRAWSEGMENT()
            segment.SetStartX(int(start[0] * POSITION_SCALE))
            segment.SetStartY(int(start[1] * POSITION_SCALE))
            segment.SetEndX(int(end[0] * POSITION_SCALE))
            segment.SetEndY(int(end[1] * POSITION_SCALE))
            segment.SetAngle(int(90 * ROTATION_SCALE))
            segment.SetWidth(int(0.3 * POSITION_SCALE))
            segment.SetLayer(pcbnew.Edge_Cuts)
            pcb.Add(segment)

    def setup_text(self, pcb):
        texts = [
            Text(
                text="v3.0",
                position=Position(155.446, 53.34, 0),
                size=TextSize(2.0, 2.0, 0.3),
                layer=pcbnew.F_SilkS,
            ),
            Text(
                text="v3.0",
                position=Position(155.446, 53.34, 0),
                size=TextSize(2.0, 2.0, 0.3),
                layer=pcbnew.B_SilkS,
            ),
        ]

        for d in pcb.GetDrawings():
            if type(d) == pcbnew.TEXTE_PCB:
                pcb.Remove(d)

        for text in texts:
            # The ordering of these operations is very important. Properties
            # like angle/justifcation affect the behavhior of the flip
            # operation. Always set position and flip before adjusting text.
            t = pcbnew.TEXTE_PCB(pcb)
            pos = t.GetPosition()
            pos.x = int(text.position.x * POSITION_SCALE)
            pos.y = int(text.position.y * POSITION_SCALE)
            t.SetPosition(pos)
            t.SetLayer(pcbnew.F_SilkS)
            if text.layer == pcbnew.B_SilkS:
                if self.local_build:
                    t.Flip(pos, False)
                else:
                    t.Flip(pos)
            t.SetText(text.text)
            t.SetTextAngle(text.position.r * ROTATION_SCALE)
            if self.local_build:
                t.SetTextThickness(int(text.size.t * POSITION_SCALE))
            else:
                t.SetThickness(int(text.size.t * POSITION_SCALE))
            t.SetTextWidth(int(text.size.w * POSITION_SCALE))
            t.SetTextHeight(int(text.size.h * POSITION_SCALE))
            t.SetHorizJustify(text.justify)
            pcb.Add(t)

    def setup_graphics(self, pcb):
        graphics = [
            Graphic(
                reference="G1",
                footprint="oshw-logo-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(190.5, 53.34, 0),
                layer=pcbnew.F_SilkS,
            ),
            Graphic(
                reference="G2",
                footprint="oshw-logo-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(190.5, 53.34, 180),
                layer=pcbnew.B_SilkS,
            ),
            Graphic(
                reference="G3",
                footprint="qmk-badge",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 133.35, 0),
                layer=pcbnew.F_SilkS,
            ),
            Graphic(
                reference="G4",
                footprint="qmk-badge",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 133.35, 180),
                layer=pcbnew.B_SilkS,
            ),
            Graphic(
                reference="G5",
                footprint="speedo-attribution-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 125.73, 0),
                layer=pcbnew.F_SilkS,
            ),
            Graphic(
                reference="G6",
                footprint="speedo-attribution-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 125.73, 180),
                layer=pcbnew.B_SilkS,
            ),
            Graphic(
                reference="G7",
                footprint="cozykeys-graphic-speedo",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(88.9, 74.93, 190),
                layer=pcbnew.B_SilkS,
            ),
            Graphic(
                reference="G8",
                footprint="cozykeys-graphic-speedo",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(257.046, 74.93, 170),
                layer=pcbnew.B_SilkS,
            ),
            Graphic(
                reference="G9",
                footprint="dumplings-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 86.0, 0),
                layer=pcbnew.F_SilkS,
            ),
            Graphic(
                reference="G10",
                footprint="dumplings-small",
                library=COZY_FOOTPRINT_LIBRARY_PATH,
                position=Position(172.973, 86.0, 180),
                layer=pcbnew.B_SilkS,
            ),
        ]

        for g in graphics:
            self.log_info("Setting up graphic {}".format(g.reference))
            module = pcb.FindModuleByReference(g.reference)
            if module != None:
                self.log_info("Found existing graphic {}, removing".format(g.reference))
                pcb.Remove(module)
            module = pcbnew.FootprintLoad(g.library, g.footprint)
            if module == None:
                raise Exception("Failed to create graphic {}".format(g.reference))
            module.SetParent(pcb)
            module.SetReference(g.reference)
            pcb.Add(module)
            pos = module.GetPosition()
            pos.x = int(g.position.x * POSITION_SCALE)
            pos.y = int(g.position.y * POSITION_SCALE)
            module.SetPosition(pos)
            module.SetOrientation(g.position.r * ROTATION_SCALE)
            module.SetLayer(pcbnew.F_SilkS)
            if g.layer == pcbnew.B_SilkS:
                module.Flip(pos)


SpeedoKicadPluginAction().register()
