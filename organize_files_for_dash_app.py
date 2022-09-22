
if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_11_organize_files_for_dash_app/dummy.txt')