#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Самостоятельно изучите работу с пакетом click для построения
# интерфейса командной строки (CLI). Для своего варианта лабораторной
# работы 2.16 необходимо реализовать интерфейс командной строки с
# использованием пакета click
# Вариант 29


import click
import json
import os.path


@click.group()
def commands():
    pass


@commands.command("add")
@click.argument("filename")
@click.option("--start", help="Start station")
@click.option("--end", help="End station")
@click.option("--number", type=int, help="Number of route")
def add_route(filename, start, end, number):
    '''
    Добавить маршрут
    '''

    routes = load_routes(filename)
    route = {
        'name_start': start,
        'name_end': end,
        'number': number
    }
    routes.append(route)
    save_routes(filename, routes)


def list(routes):
    '''
    Вывести список маршрутов
    '''
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 8
        )
        print(line)

        print('| {:^4} | {:^30} | {:^30} | {:^8} |'.format(
            "№",
            "Начальный пункт",
            "Конечный пункт",
            "Номер"
        )
        )
        print(line)

        for idx, route in enumerate(routes, 1):
            print('| {:>4} | {:<30} | {:<30} | {:>8} |'.format(
                idx,
                route.get('name_start', ''),
                route.get('name_end', ''),
                route.get('number', 0)
            )
            )
            print(line)
    else:
        print("Список маршрутов пуст.")


def save_routes(file_name, staff):
    """
    Сохранить все маршруты в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузка маршрутов из файла JSON
    """
    if os.path.isfile(file_name):
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    return []


@commands.command("display")
@click.argument("filename")
def display_routes(filename):
    """
    Отобразить список маршрутов.
    """
    routes = load_routes(filename)
    list(routes)


@commands.command("select")
@click.argument("filename")
@click.option("--station", help="Start or end station")
def select_routes(filename, station):
    '''
    Вывести выбранные маршруты
    '''
    st = station
    routes = load_routes(filename)
    count = 0
    result = []
    for route in routes:
        if (st.lower() == route["name_start"].lower() or
                st == route["name_end"].lower()):
            result.append(route)
            count += 1

    if count == 0:
        print("Маршрут не найден.")
    else:
        list(result)


def main():
    '''
    Основная функция
    '''
    commands()


if __name__ == '__main__':
    main()
