import os
import json
from make_functions import *
    
def main():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir + '/../../ChampSim')
    
    print('Making prefetchers used to generate the results of fig. 9, 10')
    
    for prefetcher in ['no']:
        make_1core(prefetcher)
    
    print('Done.')


if __name__ == '__main__':
    main()
