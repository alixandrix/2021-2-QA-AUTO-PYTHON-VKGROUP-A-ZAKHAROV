from python.functions import *
import json
def json_output(input, output):
    with open(input, 'r') as f:
        with open(output, 'w', encoding='utf-8') as ans_file:
            data = {}
            data['Общее количество запросов'] = line_count(f)
            data['Общее количество запросов по типу'] = count_response(f)
            data['Топ 10 самых частых запросов'] = popular_url(f)
            data['Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой'] = client_error(f)
            data['Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой'] = server_error(
                f)
            json.dump(data, ans_file, ensure_ascii=False, indent=4)