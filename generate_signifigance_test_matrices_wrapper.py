from subprocess import Popen
import os
import sys
from pprint import pprint

def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def build_one_command(temp_file_name):
    command_string=f'python3 ./code/generate_signifigance_test_matrices.py 0 1 {temp_file_name}\n'
    return command_string

if __name__=="__main__":

    min_fold_change=sys.argv[1]
    cores_available=int(sys.argv[2])


    os.system('mkdir -p ../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/')
    os.system('touch ../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/dummy.txt')


    full_file_list=os.listdir('../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/')
    full_file_list.remove('dummy.txt')

    full_file_list_list=list(divide_chunks(full_file_list,cores_available))

    full_command_list_list=list()
    for i in range(len(full_file_list_list)):
        full_command_list_list.append(list())
        for j in range(len(full_file_list_list[i])):
            full_command_list_list[i].append(
                build_one_command(full_file_list_list[i][j])
            )
    # full_command_list=list()
    # for element in full_file_list:
    #     full_command_list.append(
    #         build_one_command(element)
    #     )
    # full_Popen_list_list=list()
    # for i in range(len(full_command_list_list)):
    #     full_Popen_list_list.append(list())
    #     for j in range(len(full_command_list_list[i])):
    #         full_Popen_list_list[i].append(
    #             Popen(full_command_list_list[i][j], shell=True)
    #        )

    for i in range(len(full_command_list_list)):
        temp_Popen_list=[Popen(element,shell=True) for element in full_command_list_list[i]]
        for command in temp_Popen_list:
            command.wait()

    # commands_reformatted_list=list()
    # for element in full_command_list_list:
    #     commands_reformatted_list.append(
    #         ''.join(element)
    #     )
    #print(commands_reformatted_list)
    # for element in commands_reformatted_list:
    #     print(element)

    # print('---------------------------')
    # print(full_command_list_list)
    # full_Popen_list=list()
    # for i in range(len(commands_reformatted_list)):
    #     full_Popen_list.append(
    #         Popen(full_command_list_list[i], shell=True)
    #     )

    # for i in range(len(full_command_list_list)):
    #     #full_Popen_list.append(
    #     print(full_command_list_list[i])#, shell=True)
    #     #)

    # for element in full_Popen_list:
    #     element.wait()


    # for j in range(max(int(len(full_command_list)/cores_available), 1)):
    #     #procs = [Popen(i, shell=True) for i in full_command_list[j*cores_available: min((j+1)*cores_available, len(full_command_list))] ]
    #     procs = [i for i in full_command_list[j*cores_available: min((j+1)*cores_available, len(full_command_list))] ]
    #     #for p in procs:
    #     #    p.wait()

    #print(procs)
    #pprint(procs)
    # print(full_file_list_list)
    # print(full_command_list_list)
    #print(list(full_file_list_list))
    #    for i in rang

    # input_panda_address='../results/'+str(min_fold_change)+'/step_6_generate_fold_matrices/'+input_panda_file
    # #output_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/binvestigate_with_signifigance_matrices.bin'
    # output_panda_address='../results/'+str(min_fold_change)+'/step_6_b_generate_signifigance_test_matrices/'+\
    # 'binvestigate_with_signifigance_matrices'+str(temp_file_numbers[0])+'_'+str(temp_file_numbers[1])+'.bin'