COLORS = {
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "gray": "#C0C0C0",
    "pink": "#FF99CC",
    "butter": "#FFFF99",
    "blue": "#3366FF",
    "sky_blue": "#99CCFF",
    "orange": "#FF9900",
    "green": "#A7DE03",
    "sky_green": "#CCFFCC"
}


class Format:
    def __init__(self, workbook):
        self.workbook = workbook

    def test(self):
        return self.workbook.add_format({"bold": True, "font_color": "red"})

    @staticmethod
    def set_color_by_adj(adj):
        adj = adj.lower()
        if "native" in adj:
            return COLORS["butter"]
        elif "system" in adj or "persistent" in adj:
            return COLORS["yellow"]
        elif "foreground" in adj:
            return COLORS["pink"]
        elif "service" in adj:
            return COLORS["sky_green"]
        elif "visible" in adj or "perceptible" in adj:
            return COLORS["green"]
        elif "previous" in adj or "archived" in adj or "picked" in adj:
            return COLORS["sky_blue"]
        elif "cached" in adj:
            return COLORS["gray"]
        else:
            return COLORS["blue"]

    def set_title(self):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": COLORS["blue"],
            "font_color": COLORS["white"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_merge_left(self):
        return self.workbook.add_format({
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 0
        })

    def set_merge_right(self):
        return self.workbook.add_format({
            "top": 2,
            "bottom": 2,
            "left": 0,
            "right": 2
        })

    def set_default_left(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "left",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_default_center(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_default_right(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_default_right_mb(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "MB"'
        })

    def set_default_center_mb(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "MB"'
        })

    def set_default_center_kb(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "KB"'
        })

    def set_default_right_kb(self):
        return self.workbook.add_format({
            "bg_color": COLORS["white"],
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "KB"'
        })

    def set_point_center_mb(self):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": COLORS["white"],
            "font_color": COLORS["orange"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "MB"'
        })

    def set_point_center_ratio(self):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": COLORS["white"],
            "font_color": COLORS["orange"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '0.00 "%"'
        })

    def set_point_center(self):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": COLORS["white"],
            "font_color": COLORS["orange"],
            "align": "center",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_point_left(self):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": COLORS["white"],
            "font_color": COLORS["orange"],
            "align": "left",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_adj_left(self, adj):
        return self.workbook.add_format({
            "bold": True,
            "bg_color": self.set_color_by_adj(adj),
            "font_color": COLORS["black"],
            "align": "left",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_adj_right(self, adj):
        return self.workbook.add_format({
            "bold": False,
            "bg_color": self.set_color_by_adj(adj),
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2
        })

    def set_adj_right_mb(self, adj):
        return self.workbook.add_format({
            "bold": False,
            "bg_color": self.set_color_by_adj(adj),
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "MB"'
        })

    def set_adj_right_kb(self, adj):
        return self.workbook.add_format({
            "bold": False,
            "bg_color": self.set_color_by_adj(adj),
            "font_color": COLORS["black"],
            "align": "right",
            "top": 2,
            "bottom": 2,
            "left": 2,
            "right": 2,
            "num_format": '#,##0 "KB"'
        })
