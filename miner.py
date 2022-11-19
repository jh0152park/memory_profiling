class Miner:
    def __init__(self, file):
        self.log = file
        self.adj_sequence = []
        self.proc_meminfo = {}
        self.dumpsys_meminfo = {}
        self.dumpsys_meminfo_by_adj = {}
        self.properties = {}

        self.physical_memory = 0
        self.reserved_memory = 0
        self.reserved_memory_info = {}

    def read_proc_meminfo(self):
        for i in range(self.log.index("------ MEMORY INFO (/proc/meminfo) ------\n") + 1, len(self.log)):
            log = self.log[i][:-1]
            if len(log) <= 2:
                break

            if "kb" in log.lower():
                category = log.split()[0][:-1]
                memory = log.split()[1]
                if category not in self.proc_meminfo.keys():
                    self.proc_meminfo[category] = int(memory)

    def get_proc_meminfo(self):
        return self.proc_meminfo

    def compute_adj(self, log):
        adj = log.split(":")[1].split("(")[0].strip()
        pss = int(log.split()[0][:-2].replace(",", ""))
        # swap = 0 if "swap" not in log else int(log.split()[-3][:-1].replace(",", ""))
        swap = 0 if "swap" not in log else int(log.split("(")[-1].strip().split("K")[0].replace(",", ""))

        if adj not in self.dumpsys_meminfo_by_adj.keys():
            self.dumpsys_meminfo_by_adj[adj] = {
                "pss": 0,
                "swap": 0,
                "cnt": 0
            }
        self.adj_sequence.append(adj)
        self.dumpsys_meminfo_by_adj[adj]["pss"] = pss
        self.dumpsys_meminfo_by_adj[adj]["swap"] = swap
        return adj

    # 242,877K: com.kakao.talk (pid 24522 / activities)                      (  122,424K in swap)
    @staticmethod
    def compute_pss(log) -> int:
        return int(log.split()[0][:-2].replace(",", ""))

    @staticmethod
    def compute_swap(log) -> int:
        return 0 if "swap)" not in log else int(log.split()[-3][:-1].replace(",", ""))

    @staticmethod
    def compute_pid(log) -> str:
        return log.split()[3].replace(")", "")

    @staticmethod
    def compute_process(log) -> str:
        return log.split()[1]

    def read_dumpsys_meminfo(self):
        adj = ""
        for i in range(self.log.index("Total PSS by OOM adjustment:\n") + 1, len(self.log)):
            log = self.log[i][:-1]

            if len(log) <= 2:
                break

            if "(pid" not in log:
                adj = self.compute_adj(log)
                # if adj not in self.dumpsys_meminfo.keys():
                #    self.dumpsys_meminfo[adj] = {}
            else:
                proc = self.compute_process(log)
                if proc not in self.dumpsys_meminfo.keys():
                    self.dumpsys_meminfo[proc] = {
                        "adj": adj,
                        "overlap": 1
                    }
                else:
                    self.dumpsys_meminfo[proc]["overlap"] += 1
                    proc += "_" + str(self.dumpsys_meminfo[proc]["overlap"])
                    self.dumpsys_meminfo[proc] = {"adj": adj}

                self.dumpsys_meminfo_by_adj[adj]["cnt"] += 1
                self.dumpsys_meminfo[proc].update({
                    "pss": self.compute_pss(log),
                    "pid": self.compute_pid(log),
                    "swap": self.compute_swap(log)
                })

    def get_dumpsys_meminfo(self):
        return self.dumpsys_meminfo

    def get_dumpsys_meminfo_by_adj(self):
        return self.dumpsys_meminfo_by_adj

    def print_dumpsys_meminfo_by_adj(self):
        for adj in self.adj_sequence:
            print("{} / {} / {}".format(adj,
                                        self.dumpsys_meminfo_by_adj[adj]["pss"],
                                        self.dumpsys_meminfo_by_adj[adj]["swap"]))

    def print_dumpsys_meminfo(self):
        for adj in self.adj_sequence:
            for proc in self.dumpsys_meminfo[adj].keys():
                print("{} / {} / {} / {} / {}".format(adj,
                                                      proc,
                                                      self.dumpsys_meminfo[adj][proc]["pid"],
                                                      self.dumpsys_meminfo[adj][proc]["pss"],
                                                      self.dumpsys_meminfo[adj][proc]["swap"]))

    def read_properties(self):
        for i in range(self.log.index("------ SYSTEM PROPERTIES (getprop) ------\n") + 1, len(self.log)):
            log = self.log[i][:-1]
            if "as the duration of 'SYSTEM PROPERTIES' ------" in log:
                break

            """
            # Skip below case
            [persist.sys.boot.reason.history]: [reboot,ota,1664249732
            recovery,1664249671
            """
            if log.count("[") != 2 or log.count("]") != 2:
                continue
            prop = log.split()[0][1:-2]
            value = log.split()[1][1:-1]
            if prop not in self.properties.keys():
                self.properties[prop] = value

    def get_properties(self):
        return self.properties

    def read_reserved_memory_info(self):
        for i in range(self.log.index("------ MEMSIZE INFO RESERVED (/proc/memsize/reserved) ------\n") + 2,
                       len(self.log)):
            log = self.log[i][:-1]
            if "------" in log:
                break

            if "KB )" in log:
                size = int(log.split()[3])
                category = log.split()[-1]
                if category not in self.reserved_memory_info.keys():
                    self.reserved_memory_info[category] = size

            if "Reserved " in log:
                self.reserved_memory = int(log.split()[-2])

            if "Total " in log:
                self.physical_memory = int(log.split()[2])

    def get_reserved_memory(self):
        return self.reserved_memory

    def get_reserved_memory_info(self):
        return self.reserved_memory_info

    def get_physical_memory(self):
        return self.physical_memory

    def get_available_memory(self):
        return self.proc_meminfo["MemFree"] + self.proc_meminfo["Cached"]

    def get_available_memory_ratio(self):
        return (self.get_available_memory() / self.physical_memory) * 100.0

    def get_swap_used_memory(self):
        return self.proc_meminfo["SwapTotal"] - self.proc_meminfo["SwapFree"]

    def get_swap_used_memory_ratio(self):
        return (self.get_swap_used_memory() / self.proc_meminfo["SwapTotal"]) * 100.0
