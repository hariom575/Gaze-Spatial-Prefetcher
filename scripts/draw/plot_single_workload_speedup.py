import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gmean
from get_results import *

print('Using results from run_single_core_gaze_analysis.py and run_single_core_main.py')

# -------------------------- Workload and Prefetchers --------------------------
workload = '410_1963'  # short name for bwaves
prefetchers = ['no', '1offset', '2offset', '3offset', '4offset',
               'gaze_analysis_pht', 'gaze_analysis_pht4ss',
               'gaze_analysis_sm4ss', 'gaze_dyanamic_dc_sm4ss']
prefixes = {pf: 'v00-' + workload for pf in prefetchers}

# -------------------------- Get results --------------------------
speedup_detail = get_singlecore_speedup_detail(prefetchers, prefixes, [workload])

# -------------------------- Plotting --------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.0))

# Remove 'no prefetch' since it’s baseline
prefetchers.remove('no')

# Define labels and colors
prefetcher_dict = {
    '1offset': '1-Offset',
    '2offset': '2-Offset',
    '3offset': '3-Offset',
    '4offset': '4-Offset',
    'gaze_analysis_pht': 'Gaze-PHT',
    'gaze_analysis_pht4ss': 'Gaze-4SS',
    'gaze_analysis_sm4ss': 'Static Gaze',
    'gaze_dyanamic_dc_sm4ss': 'Dynamic DC-Gaze'
}

linecolor_dict = {
    '1offset': '#86b5a1',
    '2offset': '#7193c6',
    '3offset': '#9b59b6',
    '4offset': '#e67e22',
    'gaze_analysis_pht': '#ac667e',
    'gaze_analysis_pht4ss': '#c0392b',
    'gaze_analysis_sm4ss': '#e47159',
    'gaze_dyanamic_dc_sm4ss': '#2ecc71'
}

# Get x and y values
x = np.arange(len(prefetchers))
y = [speedup_detail[p][workload] for p in prefetchers]

# Plot bars
bars = ax.bar(x, y, color=[linecolor_dict[p] for p in prefetchers], width=0.6)

# Annotate values on top
for i, val in enumerate(y):
    ax.text(i, val + 0.03, f'{val:.2f}', ha='center', va='bottom', fontsize=6)

# Axis labels
ax.set_xticks(x)
ax.set_xticklabels([prefetcher_dict[p] for p in prefetchers], rotation=30, ha='right', fontsize=6)
ax.set_ylabel('Speedup over No Prefetch', fontsize=7)
ax.set_title(f'Prefetcher Comparison on {workload}', fontsize=8)

# Grid and style
ax.set_ylim(0.8, max(y) + 0.3)
ax.grid(True, axis='y', linestyle='--', alpha=0.4, linewidth=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('fig/single_workload_speedup.pdf', dpi=600, bbox_inches='tight')
plt.show()
