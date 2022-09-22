
if __name__ == "__main__":

    min_fold_change=sys.argv[1]
    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_10_upload_to_db/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_10_upload_to_db/dummy.txt')