import os
import matplotlib.pyplot as plt
import numpy as np
from get_results import *
from draw_para import *

print('Using results from run_single_core_gaze_analysis.py and run_single_core_main.py')

# -------------------------- prefetchers list --------------------------
prefetchers = [
    'no',
    '1offset', '2offset', '3offset', '4offset',
    'gaze_analysis_pht', 'gaze_analysis_pht4ss', 'gaze_analysis_sm4ss',
    'gaze', 'gaze_dynamic_dc_sm4ss'
]
prefixes = {p: 'v00' for p in prefetchers}

# -------------------------- get results --------------------------
ipc, cycles, llc_load_miss, l1_pf_late, l1_pf_useful, l1_pf_useless, l2_pf_useful, l2_pf_useless, workloads_simplified = get_raw_results(
    1, prefetchers, prefixes, workload_spec_single)

metrics = {
    'IPC': ipc,
    'Cycles': cycles,
    'LLC Load Misses': llc_load_miss,
    'L1 Prefetch Late': l1_pf_late,
    'L1 Prefetch Useful': l1_pf_useful,
    'L1 Prefetch Useless': l1_pf_useless,
    'L2 Prefetch Useful': l2_pf_useful,
    'L2 Prefetch Useless': l2_pf_useless
}

# -------------------------- select one trace --------------------------
trace_name = workloads_simplified[0]  # first trace
print(f"Plotting metrics for trace: {trace_name}")

# -------------------------- labels & colors --------------------------
prefetcher_dict.update({
    'no': 'No Prefetching',
    '1offset': '1-Offset',
    '2offset': '2-Offset',
    '3offset': '3-Offset',
    '4offset': '4-Offset',
    'gaze_analysis_pht': 'Gaze-PHT',
    'gaze_analysis_pht4ss': 'Gaze-PHT4SS',
    'gaze_analysis_sm4ss': 'Gaze-SM4SS',
    'gaze': 'Full Gaze',
    'gaze_dynamic_dc_sm4ss': 'Gaze-DynDCSM-4SS'
})
linecolor_dict.update({
    'no': '#aaaaaa',
    '1offset': '#86b5a1',
    '2offset': '#6aa98c',
    '3offset': '#529377',
    '4offset': '#3a7d62',
    'gaze_analysis_pht': '#ac667e',
    'gaze_analysis_pht4ss': '#b87c90',
    'gaze_analysis_sm4ss': '#c692a2',
    'gaze': '#e47159',
    'gaze_dynamic_dc_sm4ss': '#d83f3f'
})

# -------------------------- plot setup --------------------------
os.makedirs('fig', exist_ok=True)

def plot_bar(metric_name, values, ylabel, filename_suffix, highlight='gaze_dynamic_dc_sm4ss'):
    """Generic bar plot generator"""
    labels = [prefetcher_dict[p] for p in prefetchers]
    colors = [linecolor_dict[p] for p in prefetchers]
    x = np.arange(len(prefetchers))
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(x, values, color=colors, width=0.5, edgecolor='black', linewidth=0.25)
    
    for i, v in enumerate(values):
        ax.text(x[i], v + 0.01 * max(values), f"{v:.2f}", ha='center', va='bottom', fontsize=6,
                fontweight='bold' if prefetchers[i] == highlight else 'normal')
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6, rotation=25, ha='right')
    ax.set_ylabel(ylabel, fontsize=7)
    ax.set_title(f"{metric_name} for {trace_name}", fontsize=8, fontweight='bold', pad=4)
    ax.grid(axis='y', linestyle='--', linewidth=0.3, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig(f'fig/{trace_name}_{filename_suffix}.pdf', dpi=600, bbox_inches='tight')
    plt.show()


# -------------------------- plot each raw metric --------------------------
for metric_name, metric_dict in metrics.items():
    eliminate_invalid_values(metric_dict, prefetchers, workloads_simplified)
    values = [metric_dict[p][trace_name][0] for p in prefetchers]
    plot_bar(metric_name, values, metric_name, metric_name.replace(" ", "_"))


# -------------------------- additional metric 1: IPC Speedup --------------------------
eliminate_invalid_values(ipc, prefetchers, workloads_simplified)
ipc_speedup = [ipc[p][trace_name][0] / ipc['no'][trace_name][0] for p in prefetchers]
plot_bar('IPC Speedup', ipc_speedup, 'Speedup over No Prefetching', 'IPC_Speedup')


# -------------------------- additional metric 2: L2 Prefetch Accuracy --------------------------
eliminate_invalid_values(l2_pf_useful, prefetchers, workloads_simplified)
eliminate_invalid_values(l2_pf_useless, prefetchers, workloads_simplified)

l2_accuracy = []
for p in prefetchers:
    useful = l2_pf_useful[p][trace_name][0]
    useless = l2_pf_useless[p][trace_name][0]
    acc = useful / (useful + useless) if (useful + useless) > 0 else 0
    l2_accuracy.append(acc)

plot_bar('L2 Prefetch Accuracy', l2_accuracy, 'Accuracy (Useful / Total)', 'L2_Prefetch_Accuracy')
