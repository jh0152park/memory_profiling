import os
import miner
import datetime
import xlsxwriter
import report_generator

log_files = []
file_list = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]

date = str(datetime.datetime.now()).split()[0]
report_name = "_vs_".join(file.split(".")[0] for file in file_list)
report_name += "_" + date + ".xlsx"

workbook = xlsxwriter.Workbook(report_name)

for file in file_list:
    log_files.append({
        "name": file,
        "file": open(file, "r").readlines()
    })
    log_files[-1]["miner"] = miner.Miner(log_files[-1]["file"])
    log_files[-1]["miner"].read_proc_meminfo()
    log_files[-1]["miner"].read_dumpsys_meminfo()
    log_files[-1]["miner"].read_properties()
    log_files[-1]["miner"].read_reserved_memory_info()

summary = report_generator.Summary(workbook, workbook.add_worksheet("summary"), log_files)
reserved = report_generator.Summary(workbook, workbook.add_worksheet("reserved"), log_files)
summary.write_summary_sheet()
reserved.write_reserved_sheet()
workbook.close()
