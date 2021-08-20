import multiprocessing

def do_something(temp_list):
    print('hi')
    return [i**2 for i in temp_list]


def multi_wrapper(temp_list):

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    test_result=pool.map(do_something,temp_list)
    print(test_result)

if __name__ == "__main__":

    #temp=[i for i in range(0,100)]
    temp=[[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18]]
    multi_wrapper(temp)
