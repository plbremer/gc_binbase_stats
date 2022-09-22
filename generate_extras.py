import sys
import os

if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_9_generate_extras_for_db_and_api/dummy.txt')