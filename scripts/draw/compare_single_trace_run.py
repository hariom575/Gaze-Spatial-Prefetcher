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
speedup_detail = get_singlecore_speedup_detail(prefetchers, prefixes, workload_spec_single)

# -------------------------- select one trace --------------------------
# Option 1: manually specify (recommended)
# trace_name = 'mcf'
# Option 2: pick automatically (first trace)
trace_name = list(speedup_detail['no'].keys())[0]
print(f"Plotting single trace: {trace_name}")

# -------------------------- labeling & colors --------------------------
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

# Distinct color palette
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
    'gaze_dynamic_dc_sm4ss': '#d83f3f'   # highlight your modified version
})

# -------------------------- collect data --------------------------
ipc_values = [speedup_detail[p][trace_name] for p in prefetchers]
labels = [prefetcher_dict[p] for p in prefetchers]
colors = [linecolor_dict[p] for p in prefetchers]

# -------------------------- plot --------------------------
fig, ax = plt.subplots(figsize=(5.5, 2.5))

x = np.arange(len(prefetchers))
bars = ax.bar(x, ipc_values, color=colors, width=0.5, edgecolor='black', linewidth=0.25)

# Highlight your modified one (bold label)
for i, p in enumerate(prefetchers):
    if p == 'gaze_dynamic_dc_sm4ss':
        bars[i].set_edgecolor('black')
        bars[i].set_linewidth(0.6)
        ax.text(x[i], ipc_values[i] + 0.05, f"{ipc_values[i]:.2f}", 
                ha='center', va='bottom', fontsize=6, color='black', fontweight='bold')
    else:
        ax.text(x[i], ipc_values[i] + 0.03, f"{ipc_values[i]:.2f}",
                ha='center', va='bottom', fontsize=6, color='black')

# Axis & labels
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=6, rotation=25, ha='right')
ax.set_ylabel('Speedup over\nno prefetching', fontsize=7, labelpad=2)
ax.set_title(f'Speedup for {trace_name}', fontsize=8, pad=4, fontweight='bold')

# Grid & reference line
ax.axhline(y=1.0, color='#333333', linestyle='--', linewidth=0.3, alpha=0.7)
ax.set_ylim(0, max(ipc_values)*1.3)
ax.grid(axis='y', linestyle='--', linewidth=0.3, alpha=0.4)

# Save figure
os.makedirs('fig', exist_ok=True)
plt.tight_layout()
plt.savefig('fig/single_trace_speedup_all_prefetchers.pdf', dpi=600, bbox_inches='tight', pad_inches=0.02)
plt.show()
