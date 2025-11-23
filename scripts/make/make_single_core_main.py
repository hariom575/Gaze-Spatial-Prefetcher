import os
import json
from make_functions import *
    
def main():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir + '/../../ChampSim')
    
    print('Making prefetchers used to generate the results of fig. 1, 6, 7, 8, 11, 12')
    
    for prefetcher in ['gaze','no','1offset','gaze_analysis_pht4ss','gaze_analysis_pht','gaze_dynamic_dc_sm4ss']:
        make_1core(prefetcher)
    
    print('Done.')


if __name__ == '__main__':
    main()
