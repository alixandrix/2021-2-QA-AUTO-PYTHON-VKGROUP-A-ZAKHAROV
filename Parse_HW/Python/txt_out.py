from Python.functions import *


def txt_output(input, output):
    with open(input, 'r') as f:
        with open(output, 'w', encoding='UTF-8') as ans_file:
            ans_file.write('Общее количество запросов\n')
            my_dict = line_count(f)
            for k in my_dict.keys():
                ans_file.write(str(k) + ' : ' + str(my_dict[k]) + '\n')
            ans_file.write('\nОбщее количество запросов по типу\n')
            my_dict = count_response(f)
            for k in my_dict.keys():
                ans_file.write(str(k) + ' : ' + str(my_dict[k]) + '\n')
            ans_file.write('\nТоп 10 самых частых запросов\n')
            my_dict = popular_url(f)
            for k in my_dict.keys():
                ans_file.write(str(k) + ' : ' + str(my_dict[k]) + '\n')
            ans_file.write('\nТоп 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой\n')
            my_dict = client_error(f)
            for k in my_dict.keys():
                ans_file.write(str(k) + ' : ' + str(my_dict[k])[1:-1] + '\n')
            ans_file.write('\nТоп 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой\n')
            my_dict = server_error(f)
            for k in my_dict.keys():
                ans_file.write(str(k) + ' : ' + str(my_dict[k]) + '\n')