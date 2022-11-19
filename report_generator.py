import report_format

SUMMARY_AGENDA = [
    "Model Name",
    "Version",
    "OS",
    "Physical Memory",
    "Reserved Memory",
    "Available Memory",
    "Available Memory(%)",
    "  - Free Memory",
    "  - Cached Memory",
    "Swap Total",
    "Swap Free",
    "Swap Used",
    "Swap Used(%)",
]

RESERVED_AGENDA = [
    "Model Name",
    "Version",
    "OS",
    "Physical Memory",
    "Reserved Memory",
    "Debug Level",
    "Ship Build"
]


class Summary:
    def __init__(self, workbook, sheet, models):
        self.workbook = workbook
        self.sheet = sheet
        self.models = models
        self.form = report_format.Format(self.workbook)

        # [ro.product.name]: [g0qksx]
        self.product_name_key = "ro.product.name"
        # [ro.product.model]: [SM-S906N]
        self.product_model_key = "ro.product.model"
        # [ro.system.build.version.release]: [12]
        self.os_version_key = "ro.system.build.version.release"
        # [ro.omc.build.version]: [S906NOKR2AVI1]
        self.build_version_key = "ro.omc.build.version"

        self.debug_level = "ro.boot.debug_level"
        self.ship_build = "ro.product_ship"

    def set_cell_width(self, x, y, width):
        self.sheet.set_column(y - 1, x - 1, width)

    def write_string(self, x, y, string, form):
        self.sheet.write_string(y - 1, x - 1, string, form)

    def write_number(self, x, y, number, form):
        self.sheet.write_number(y - 1, x - 1, number, form)

    def merge(self, from_x, from_y, to_x, to_y):
        self.sheet.merge_range(from_y - 1, from_x - 1, to_y - 1, to_x - 1, "")

    def filter(self, from_x, from_y, to_x, to_y):
        self.sheet.autofilter(from_y - 1, from_x - 1, to_y - 1, to_x - 1)

    def write_summary_agenda(self):
        self.set_cell_width(2, 3, 50)
        for i in range(len(SUMMARY_AGENDA)):
            if i == 0:
                self.write_string(2, 3 + i, SUMMARY_AGENDA[i], self.form.set_title())
            else:
                if "Available" in SUMMARY_AGENDA[i] or "Swap Used" in SUMMARY_AGENDA[i]:
                    self.write_string(2, 3 + i, SUMMARY_AGENDA[i], self.form.set_point_left())
                else:
                    self.write_string(2, 3 + i, SUMMARY_AGENDA[i], self.form.set_default_left())

    def merge_summary_agenda_cell(self):
        for i in range(len(self.models)):
            for j in range(len(SUMMARY_AGENDA)):
                self.set_cell_width(3 + (i * 2), 3 + (i * 2), 15)
                self.set_cell_width(4 + (i * 2), 4 + (i * 2), 15)
                self.merge(3 + (i * 2), 3 + j, 4 + (i * 2), 3 + j)
                self.write_string(3 + (i * 2), 3 + j, "", self.form.set_merge_left())
                self.write_string(4 + (i * 2), 3 + j, "", self.form.set_merge_right())

    def compute_proc_meminfo_categories(self):
        categories = []
        for model in self.models:
            for category in model["miner"].get_proc_meminfo().keys():
                if category not in categories:
                    categories.append(category)
        return categories

    def write_proc_meminfo_categories(self):
        categories = self.compute_proc_meminfo_categories()
        for i in range(len(categories)):
            self.write_string(2, 3 + len(SUMMARY_AGENDA) + i, categories[i], self.form.set_default_left())

    def write_summary_contents(self):
        for i in range(len(self.models)):
            y = 3
            x = 3 + (i * 2)

            model = self.models[i]["miner"]
            property = model.get_properties()
            proc_meminfo = model.get_proc_meminfo()

            self.write_string(x, y, self.models[i]["name"], self.form.set_title())
            y += 1  # Model Name

            self.write_string(x, y, property[self.build_version_key][-3:], self.form.set_default_center())
            y += 1  # Version

            self.write_number(x, y, int(property[self.os_version_key]), self.form.set_default_center())
            y += 1  # OS

            self.write_number(x, y, model.get_physical_memory() / 1024, self.form.set_default_center_mb())
            y += 1  # Physical Memory

            self.write_number(x, y, model.get_reserved_memory() / 1024, self.form.set_default_center_mb())
            y += 1  # Reserved Memory

            self.write_number(x, y, model.get_available_memory() / 1024, self.form.set_point_center_mb())
            y += 1  # Available Memory

            self.write_number(x, y, model.get_available_memory_ratio(), self.form.set_point_center_ratio())
            y += 1  # Available Memory(%)

            self.write_number(x, y, proc_meminfo["MemFree"] / 1024, self.form.set_default_center_mb())
            y += 1  # Free Memory

            self.write_number(x, y, proc_meminfo["Cached"] / 1024, self.form.set_default_center_mb())
            y += 1  # Cached Memory

            self.write_number(x, y, proc_meminfo["SwapTotal"] / 1024, self.form.set_default_center_mb())
            y += 1  # Swap Total

            self.write_number(x, y, proc_meminfo["SwapFree"] / 1024, self.form.set_default_center_mb())
            y += 1  # Swap Free

            self.write_number(x, y, model.get_swap_used_memory() / 1024, self.form.set_point_center_mb())
            y += 1  # Swap Used

            self.write_number(x, y, model.get_swap_used_memory_ratio(), self.form.set_point_center_ratio())

    def write_proc_meminfo_contents(self):
        categories = self.compute_proc_meminfo_categories()
        for i in range(len(categories)):
            category = categories[i]
            for j in range(len(self.models)):
                x = 3 + (j * 2)
                y = 3 + len(SUMMARY_AGENDA) + i
                model = self.models[j]["miner"]
                proc_meminfo = model.get_proc_meminfo()

                self.merge(3 + (j * 2), y, 4 + (j * 2), y)
                self.write_string(3 + (j * 2), y, "", self.form.set_merge_left())
                self.write_string(4 + (j * 2), y, "", self.form.set_merge_right())
                self.write_number(x, y, 0 if category not in proc_meminfo.keys() else proc_meminfo[category],
                                  self.form.set_default_right_kb())
                self.sheet.set_row(y - 1, None, None, {"hidden": True, "level": 1})

    def write_dumpsys_meminfo_adj_title(self):
        y = 3 + len(SUMMARY_AGENDA) + len(self.compute_proc_meminfo_categories())
        self.write_string(2, y, "Size of PSS by ADJ", self.form.set_title())
        for i in range(len(self.models)):
            self.write_string(3 + (i * 2), y, "PSS", self.form.set_title())
            self.write_string(4 + (i * 2), y, "CNT", self.form.set_title())

    def compute_dumpsys_meminfo_categories(self):
        adjs = []
        for model in self.models:
            for adj in model["miner"].get_dumpsys_meminfo_by_adj().keys():
                if adj not in adjs:
                    adjs.append(adj)
        return adjs

    def write_dumpsys_meminfo_adj_categories(self):
        adjs = self.compute_dumpsys_meminfo_categories()
        x = 2
        y = 4 + len(SUMMARY_AGENDA) + len(self.compute_proc_meminfo_categories())

        self.write_string(x, y, "Total PSS by ADJ", self.form.set_adj_left("None"))
        for i in range(len(self.models)):
            dumpsys_meminfo_by_adj = self.models[i]["miner"].get_dumpsys_meminfo_by_adj()
            total_pss = [dumpsys_meminfo_by_adj[adj]["pss"] for adj in dumpsys_meminfo_by_adj.keys()]
            total_cnt = [dumpsys_meminfo_by_adj[adj]["cnt"] for adj in dumpsys_meminfo_by_adj.keys()]
            self.write_number(3 + (i * 2), y, sum(total_pss) / 1024, self.form.set_default_right_mb())
            self.write_number(4 + (i * 2), y, sum(total_cnt), self.form.set_default_right())

        for adj in adjs:
            y += 1
            self.write_string(x, y, adj, self.form.set_adj_left(adj))
            for i in range(len(self.models)):
                dumpsys_meminfo_by_adj = self.models[i]["miner"].get_dumpsys_meminfo_by_adj()
                pss = 0 if adj not in dumpsys_meminfo_by_adj.keys() else dumpsys_meminfo_by_adj[adj]["pss"]
                cnt = 0 if adj not in dumpsys_meminfo_by_adj.keys() else dumpsys_meminfo_by_adj[adj]["cnt"]
                self.write_number(3 + (i * 2), y, pss / 1024, self.form.set_default_right_mb())
                self.write_number(4 + (i * 2), y, cnt, self.form.set_default_right())

    def write_dumpsys_meminfo_title(self):
        y = len(self.compute_dumpsys_meminfo_categories())
        y += 5 + len(SUMMARY_AGENDA) + len(self.compute_proc_meminfo_categories())
        self.write_string(2, y, "Process PSS Detail", self.form.set_title())
        for i in range(len(self.models)):
            self.write_string(3 + (i * 2), y, "ADJ", self.form.set_title())
            self.write_string(4 + (i * 2), y, "PSS", self.form.set_title())

    def compute_processes_overlap(self):
        processes = []
        for model in self.models:
            for process in model["miner"].get_dumpsys_meminfo().keys():
                if process not in processes:
                    processes.append(process)
        return processes

    def write_dumpsys_meminfo_detail(self):
        x = 2
        processes = self.compute_processes_overlap()
        y = len(self.compute_dumpsys_meminfo_categories())
        y += 5 + len(SUMMARY_AGENDA) + len(self.compute_proc_meminfo_categories())
        filter_y = y

        for process in processes:
            y += 1
            self.write_string(x, y, process, self.form.set_default_left())
            for i in range(len(self.models)):
                dumpsys_meminfo = self.models[i]["miner"].get_dumpsys_meminfo()
                if process not in dumpsys_meminfo.keys():
                    self.write_string(3 + (i * 2), y, "", self.form.set_default_left())
                    self.write_string(4 + (i * 2), y, "", self.form.set_default_left())
                else:
                    adj = dumpsys_meminfo[process]["adj"]
                    pss = dumpsys_meminfo[process]["pss"]
                    self.write_string(3 + (i * 2), y, adj, self.form.set_adj_right(adj))
                    self.write_number(4 + (i * 2), y, pss, self.form.set_adj_right_kb(adj))
        self.filter(2, filter_y, (len(self.models)*2) + 2, filter_y)

    def write_reserved_agenda(self):
        self.set_cell_width(2, 2, 30)
        for i in range(len(RESERVED_AGENDA)):
            if i == 0:
                self.write_string(2, 3 + i, RESERVED_AGENDA[i], self.form.set_title())
            else:
                if "Reserved" in RESERVED_AGENDA[i]:
                    self.write_string(2, 3 + i, RESERVED_AGENDA[i], self.form.set_point_left())
                else:
                    self.write_string(2, 3 + i, RESERVED_AGENDA[i], self.form.set_default_left())

    def write_reserved_contents(self):
        for i in range(len(self.models)):
            x = 3 + i
            y = 3

            model = self.models[i]["miner"]
            property = model.get_properties()
            reserved_memory_info = model.get_reserved_memory_info()
            self.set_cell_width(x, y, 15)

            self.write_string(x, y, self.models[i]["name"], self.form.set_title())
            y += 1  # Model Name

            self.write_string(x, y, property[self.build_version_key][-3:], self.form.set_default_center())
            y += 1  # Version

            self.write_number(x, y, int(property[self.os_version_key]), self.form.set_default_center())
            y += 1  # OS

            self.write_number(x, y, model.get_physical_memory() / 1024, self.form.set_default_center_mb())
            y += 1  # Physical Memory

            self.write_number(x, y, model.get_reserved_memory() / 1024, self.form.set_point_center_mb())
            y += 1  # Reserved Memory

            self.write_string(x, y, property[self.debug_level], self.form.set_default_center())
            y += 1  # Debug Level

            self.write_string(x, y, property[self.ship_build], self.form.set_default_center())
            y += 1  # Ship Build

    def write_reserved_info_title(self):
        x = 2
        y = 3 + len(RESERVED_AGENDA)

        self.write_string(x, y, "Reserved Category", self.form.set_title())
        for i in range(len(self.models)):
            x += 1
            self.write_string(x, y, "Size", self.form.set_title())

    def compute_reserved_memory_categories(self):
        reserved = []
        for model in self.models:
            for category in model["miner"].get_reserved_memory_info().keys():
                if category not in reserved:
                    reserved.append(category)
        return reserved

    def write_reserved_memory_detail(self):
        y = 3 + len(RESERVED_AGENDA)
        categories = self.compute_reserved_memory_categories()

        for reserved in categories:
            x = 2
            y += 1
            self.write_string(x, y, reserved, self.form.set_default_left())

            for model in self.models:
                x += 1
                reserved_memory_info = model["miner"].get_reserved_memory_info()
                size = 0 if reserved not in reserved_memory_info.keys() else reserved_memory_info[reserved]
                self.write_number(x, y, size, self.form.set_default_right_kb())

    def write_summary_sheet(self):
        self.write_summary_agenda()
        self.merge_summary_agenda_cell()
        self.write_summary_contents()

        self.write_proc_meminfo_categories()
        self.write_proc_meminfo_contents()

        self.write_dumpsys_meminfo_adj_title()
        self.write_dumpsys_meminfo_adj_categories()

        self.write_dumpsys_meminfo_title()
        self.write_dumpsys_meminfo_detail()

    def write_reserved_sheet(self):
        self.write_reserved_agenda()
        self.write_reserved_contents()

        self.write_reserved_info_title()
        self.write_reserved_memory_detail()
