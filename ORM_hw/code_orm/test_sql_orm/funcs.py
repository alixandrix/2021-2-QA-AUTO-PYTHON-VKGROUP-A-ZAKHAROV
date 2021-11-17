import re

patt_method = r'[\+]\d{4}]\s"(.+)\s\/'
patt_url = r'"\w{3,4}\s([\/]\S*)\s'
patt_size = r'"\s4\d\d\s(\d+)\s'
patt_status_4XX = r'HTTP.*"\s(4\d\d)\s'
patt_status_5XX = r'HTTP.*"\s(5\d\d)\s'
patt_ip = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'


def line_count(file):
    with open(file, 'r') as f:
        line_count = 0
        for _ in f:
            line_count += 1
        return int(line_count)


def count_response(file):
    with open(file, 'r') as f:
        sorted_dict = {}
        res = set()
        d = {}
        for i in f:
            resp = re.findall(patt_method, i)
            if len(resp):
                res.add(resp[0])
        for j in res:
            counter = 0
            f.seek(0)
            for w in f:
                resp = re.findall(patt_method, w)
                if len(resp):
                    if resp[0] == j:
                        counter += 1
            d[j] = counter
        sorted_keys = sorted(d, key=d.get, reverse=True)
        for w in sorted_keys:
            sorted_dict[w] = d[w]
        return sorted_dict


def popular_url(file):
    with open(file, 'r') as f:
        dict = {}
        for line in f:
            url = re.findall(patt_url, line)
            if len(url):
                if url[0] not in dict:
                    dict[url[0]] = 1
                else:
                    dict[url[0]] += 1
        sorted_dict = {}
        sorted_keys = sorted(dict, key=dict.get, reverse=True)
        checker = []
        for w in sorted_keys:
            checker.append(w)
            if len(checker) == 11:
                break
            sorted_dict[w] = dict[w]
        return sorted_dict


def client_error(file):
    with open(file, 'r') as f:
        d = {}
        for line in f:
            size = re.findall(patt_size, line)
            if len(size):
                size_resp = int(size[0])
                if size_resp not in d:
                    d[size_resp] = [[re.findall(patt_url, line), re.findall(patt_status_4XX, line), re.findall(patt_ip, line)]]
                else:
                    d[size_resp] += [[re.findall(patt_url, line), re.findall(patt_status_4XX, line), re.findall(patt_ip, line)]]
        i = 0
        new_dict = {}
        for k in sorted(d.keys(), reverse=True):
            for j in range(len(d[k])):
                i += 1
                if i > 5:
                    break
                new_dict[str(d[k][j][0][0])] = [str(d[k][j][1][0]), k, str(d[k][j][2][0])]
        return new_dict


def server_error(file):
    with open(file, 'r') as f:
        d = {}
        for line in f:
            code = re.findall(patt_status_5XX, line)
            if len(code):
                client = re.findall(patt_ip, line)
                if len(client):
                    if client[0] not in d:
                        d[client[0]] = 1
                    else:
                        d[client[0]] += 1
        sorted_dict = {}
        sorted_keys = sorted(d, key=d.get, reverse=True)
        checker = []
        for w in sorted_keys:
            checker.append(w)
            if len(checker) == 6:
                break
            sorted_dict[w] = d[w]
        return sorted_dict