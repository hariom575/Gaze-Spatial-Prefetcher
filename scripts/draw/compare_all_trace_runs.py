import os
import matplotlib.pyplot as plt
import numpy as np
from get_results import *
from draw_para import *

print('Using results from run_single_core_gaze_analysis.py and run_single_core_main.py')

# -------------------------- prefetchers list --------------------------
prefetchers = [
    'no',
    '1offset',
    'gaze_analysis_pht4ss',
    'gaze_analysis_sm4ss',
    'gaze',
    'gaze_dynamic_dc_sm4ss'
]
prefixes = {p: 'v00' for p in prefetchers}

# -------------------------- get results --------------------------
ipc, cycles, llc_load_miss, l1_pf_late, l1_pf_useful, l1_pf_useless, l2_pf_useful, l2_pf_useless, workloads_simplified = get_raw_results(
    1, prefetchers, prefixes, workload_spec_single)

# -------------------------- labels & colors --------------------------
prefetcher_dict.update({
    'no': 'No Prefetching',
    '1offset': '1-Offset',
    'gaze_analysis_pht4ss': 'Gaze-PHT4SS',
    'gaze_analysis_sm4ss': 'Gaze-SM4SS',
    'gaze': 'Full Gaze',
    'gaze_dynamic_dc_sm4ss': 'Gaze-DynDCSM-4SS'
})
linecolor_dict.update({
    'no': '#aaaaaa',
    '1offset': '#86b5a1',
    'gaze_analysis_pht4ss': '#b87c90',
    'gaze_analysis_sm4ss': '#c692a2',
    'gaze': '#e47159',
    'gaze_dynamic_dc_sm4ss': '#d83f3f'
})

# -------------------------- workload name mapping --------------------------
workloads_name_map = {
    '403_17': 'gcc-17',
    '410_1963': 'bwaves-1963',
    '436_1804': 'cactusADM-1804',
    '437_271': 'leslie3d-271',
    '450_92': 'soplex-92',
    '462_714': 'libquantum-714',
    '654_s523': 'roms_s-523',
    'bc-5': 'BC-5',
    'bfs-14': 'BFS-14',
    'cc-5': 'CC-5',
    'pr-3': 'PR-3',
    'sssp-14': 'SSSP-14'
}

# -------------------------- plot setup --------------------------
os.makedirs('fig', exist_ok=True)

def plot_metric_across_workloads(metric_name, metric_dict, prefetchers):
    """
    Plot a metric across all workloads in a single graph and save as PNG.
    """
    workloads = list(metric_dict['no'].keys())
    num_workloads = len(workloads)
    x = np.arange(num_workloads)
    width = 0.12  # width of each bar

    fig, ax = plt.subplots(figsize=(10, 4))

    for i, p in enumerate(prefetchers):
        values = [metric_dict[p][w][0] for w in workloads]
        ax.bar(x + i*width, values, width=width, label=prefetcher_dict.get(p, p),
               color=linecolor_dict.get(p, '#333333'))

    # x-axis labels
    labels = [workloads_name_map.get(w, w) for w in workloads]
    ax.set_xticks(x + width*(len(prefetchers)-1)/2)
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=8)

    ax.set_ylabel(metric_name)
    ax.set_title(f"{metric_name} Across All Workloads", fontsize=10, fontweight='bold')
    ax.grid(axis='y', linestyle='--', linewidth=0.3, alpha=0.4)
    ax.legend(fontsize=6, ncol=2)

    plt.tight_layout()
    plt.savefig(f'fig/{metric_name.replace(" ", "_")}_all_workloads.png', dpi=600)
    plt.show()

# -------------------------- IPC Speedup --------------------------
eliminate_invalid_values(ipc, prefetchers, workloads_simplified)
ipc_speedup = {p: {} for p in prefetchers}
for p in prefetchers:
    for w in workloads_simplified:
        ipc_speedup[p][w] = [ipc[p][w][0] / ipc['no'][w][0]]

plot_metric_across_workloads('IPC Speedup', ipc_speedup, prefetchers)

# -------------------------- L2 Prefetch Accuracy --------------------------
eliminate_invalid_values(l2_pf_useful, prefetchers, workloads_simplified)
eliminate_invalid_values(l2_pf_useless, prefetchers, workloads_simplified)

l2_accuracy = {p: {} for p in prefetchers}
for p in prefetchers:
    for w in workloads_simplified:
        useful = l2_pf_useful[p][w][0]
        useless = l2_pf_useless[p][w][0]
        acc = useful / (useful + useless) if (useful + useless) > 0 else 0
        l2_accuracy[p][w] = [acc]

plot_metric_across_workloads('L2 Prefetch Accuracy', l2_accuracy, prefetchers)
