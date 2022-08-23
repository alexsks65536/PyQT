"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""

import os
import platform
import subprocess
import time
import threading
from ipaddress import ip_address
from pprint import pprint

result = {'Доступные узлы': "", "Недоступные узлы": ""}  # словарь с результатами

DNULL = open(os.devnull, 'w')  # заглушка, чтобы поток не выводился на экран


def read2list(file):
    """
    :param file: имя открываемого файла с перечнем адресов.
    :return: список адресов.
    """
    # открываем файл в режиме чтения utf-8
    file = open(file, 'r', encoding='utf-8')
    # читаем все строки и удаляем переводы строк
    lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    file.close()

    return lines


def check_is_ipaddress(value):
    """
    Проверка является ли введённое значение IP адресом
    :param value: присланные значения,
    :return ipv4: полученный ip адрес из переданного значения
        Exception ошибка при невозможности получения ip адреса из значения
    """
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Доступные узлы"] += f"{ipv4}\n"
        res = f"{ipv4} - Узел доступен"
        if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
            print(res)
        return res
    else:
        result["Недоступные узлы"] += f"{ipv4}\n"
        res = f"{str(ipv4)} - Узел недоступен"
        if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
            print(res)
        return res


def host_ping(hosts_list, get_list=False):
    """
    Проверка доступности хостов
    :param hosts_list: список хостов
    :param get_list: признак нужно ли отдать результат в виде словаря (для задания #3)
    :return словарь результатов проверки, если требуется
    """
    print("Начинаю проверку доступности узлов...")
    threads = []
    for host in hosts_list:  # проверяем, является ли значение ip-адресом
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:  # если требуется вернуть словарь (для задачи №3), то возвращаем
        return result


if __name__ == '__main__':

    hosts_list = read2list('adress.txt')
    start = time.time()
    host_ping(hosts_list)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(result)
