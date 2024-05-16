import numpy as np
import pandas as pd
import os


def make_file_list():
    file_list = []
    for root, dirs, files in os.walk('data/'):  # 工作目录, 子目录, 文件
        for json_name in files:
            file_list.append('data/' + json_name)
    return file_list


def DataRead_xls(dataMat_name):
    dataMat = pd.read_excel(dataMat_name, sheet_name='RR间期', header=7,
                            index_col=None)  # "header:指定列名行，0取第一行，数据为列名行以下；index_col:指定列为索引列"
    dataMat = np.array(dataMat)
    return dataMat


def step2():
    files_list = make_file_list()
    for xlxs_name in files_list:
        data_mat = DataRead_xls(xlxs_name)
        temp_num = None
        for i in range(len(data_mat) - 4):  # 滑动步长为5
            if data_mat[i, -1] != 0:
                if temp_num is None and 0 in data_mat[i: i + 5, -1]:
                    data_mat[i: i + 5, -1] = 0
                    continue
                elif temp_num is not None:
                    if temp_num > 5:
                        temp_num = None
                    else:
                        temp_num += 1
                temp_num = 1
        write_str = ['', '', '']
        now_work_index = [data_mat[0, 0].to_pydatetime().strftime('%Y-%m-%d %H:%M'),
                          data_mat[0, 0].to_pydatetime().strftime('%Y-%m-%d %H:%M'),
                          data_mat[0, 0].to_pydatetime().strftime('%Y-%m-%d %H:%M')]
        for data_line in data_mat:
            work_num = data_line[-1]
            if data_line[0].to_pydatetime().strftime('%Y-%m-%d %H:%M') != now_work_index[work_num]:
                write_str[work_num] += '\n'
                now_work_index[work_num] = data_line[0].to_pydatetime().strftime('%Y-%m-%d %H:%M')
            write_str[work_num] += str(data_line[0]) + ',' + str(data_line[1]) + ','
        if not os.path.exists('OSA RRi'):
            os.makedirs('OSA RRi')
        if not os.path.exists('step2 folder'):
            os.makedirs('step2 folder')
        for worker_id, worker in enumerate(write_str):
            with open('step2 folder\\' + xlxs_name[6: -5] + '_' + str(worker_id) + '.csv', 'w') as file_out:
                file_out.write(worker)
    print('step2 done')