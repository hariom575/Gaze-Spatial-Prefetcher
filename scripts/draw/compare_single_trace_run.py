import os
import csv
import numpy as np
from get_results import *
from draw_para import *

print("Using results from run_single_core_gaze_analysis.py and run_single_core_main.py")

# -------------------------- Prefetchers --------------------------
prefetchers = [
    'no',
    '1offset',
    'gaze_analysis_pht4ss',
    'gaze_analysis_sm4ss',
    'gaze',
    'gaze_dynamic_dc_sm4ss'
]
prefixes = {p: 'v00' for p in prefetchers}

# -------------------------- Load Raw Results --------------------------
(
    ipc, cycles, llc_load_miss,
    l1_pf_late, l1_pf_useful, l1_pf_useless,
    l2_pf_useful, l2_pf_useless,
    workloads_simplified
) = get_raw_results(1, prefetchers, prefixes, workload_spec_single)

print("\n================ RAW RESULTS LOADED ================\n")

# -------------------------- CSV Output --------------------------
OUTPUT_CSV = "consolidated_metrics.csv"

# Ensure output folder exists
if not os.path.exists("fig"):
    os.makedirs("fig")

# -------------------------- Compute Metrics --------------------------
coverage = {p: {} for p in prefetchers}
pollution = {p: {} for p in prefetchers}
l2_accuracy = {p: {} for p in prefetchers}
ipc_speedup = {p: {} for p in prefetchers}

print("Computing coverage, pollution, accuracy, speedup ...\n")

# Speedup reference
ipc_base = {w: ipc["no"][w][0] for w in workloads_simplified}

for p in prefetchers:
    for w in workloads_simplified:

        # Raw values
        ipc_v = ipc[p][w][0]
        cyc_v = cycles[p][w][0]
        llc_v = llc_load_miss[p][w][0]

        l1_u = l1_pf_useful[p][w][0]
        l1_uu = l1_pf_useless[p][w][0]
        l2_u = l2_pf_useful[p][w][0]
        l2_uu = l2_pf_useless[p][w][0]

        useful = l1_u + l2_u
        useless = l1_uu + l2_uu

        # -------- Coverage --------
        cov = useful / llc_v if llc_v > 0 else 0
        coverage[p][w] = cov

        # -------- Pollution --------
        pol = useless / (useful + useless) if (useful + useless) > 0 else 0
        pollution[p][w] = pol

        # -------- L2 Accuracy --------
        acc = l2_u / (l2_u + l2_uu) if (l2_u + l2_uu) > 0 else 0
        l2_accuracy[p][w] = acc

        # -------- IPC Speedup --------
        spd = ipc_v / ipc_base[w] if ipc_base[w] > 0 else 0
        ipc_speedup[p][w] = spd


# -------------------------- Write CSV --------------------------
print(f"\nWriting consolidated CSV → {OUTPUT_CSV}")

with open(OUTPUT_CSV, mode='w', newline='') as f:
    writer = csv.writer(f)

    # Header
    writer.writerow([
        "prefetcher", "workload",
        "ipc", "cycles", "llc_load_miss",
        "l1_pf_useful", "l1_pf_useless",
        "l2_pf_useful", "l2_pf_useless",
        "coverage", "pollution", "l2_accuracy",
        "ipc_speedup"
    ])

    # Rows
    for p in prefetchers:
        for w in workloads_simplified:

            writer.writerow([
                p, w,
                ipc[p][w][0],
                cycles[p][w][0],
                llc_load_miss[p][w][0],
                l1_pf_useful[p][w][0],
                l1_pf_useless[p][w][0],
                l2_pf_useful[p][w][0],
                l2_pf_useless[p][w][0],
                coverage[p][w],
                pollution[p][w],
                l2_accuracy[p][w],
                ipc_speedup[p][w],
            ])

print("\n✅ CSV generation complete!")
print(f"Location: {OUTPUT_CSV}\n")

