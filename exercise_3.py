# Задание 3 - Калькулятор расширенный и обычный функционал

import PySimpleGUI as sg

from MainHandler import MainHandler
from SimpleModOutput import SimpleModOutput
from AdvancedModOutput import AdvancedModOutput
import graphicPack
import helper


# Выбор темы оформления 
sg.theme("DarkAmber")

# генерирует необходимую информацию для запуска расширенного режима
def startInfoSimpleMode(memory_cells_count=1, max_row_size=9):
    start_info = dict()
    # формирования обработчика вывода, для него необходимо окно вывода
    outputWindow = graphicPack.generateSimpleModeOutput()
    output = SimpleModOutput(outputWindow[0][0])
    # формирование графического интерфейса
    layout = (outputWindow
            + graphicPack.generateControlButtons()
            + graphicPack.memoryWindowGenerator(memory_cells_count) 
            + graphicPack.generateCommonButtons())

    # заполняем объект необходимой информацией
    start_info["mode"] = "simple"
    start_info["window"] = sg.Window('Калькулятор - обычный режим', layout, element_padding=(4, 3))
    start_info["main_handler"] = MainHandler(output, max_row_size, memory_cells_count)
    return start_info

# генерирует необходимую информацию для запуска расширенного режима
def startInfoAdvancedMode(user_id = 70153452, max_row_size=9):
    # вычисление количества строк и количество ячеек памяти из ID пользователя
    sum_num_id = helper.value_sum(int(user_id))
    memory_cells_count = helper.value_sum(int(str(user_id)[-3:]))
    advanced_mod_row_count = 10 if sum_num_id == 1 else sum_num_id
    start_info = dict()
    # формирования обработчика вывода, для него необходимо окно вывода
    outputWindow = graphicPack.generateAdvancedModeOutput(advanced_mod_row_count)
    output = AdvancedModOutput(outputWindow[0][0], advanced_mod_row_count)
    # формирование графического интерфейса
    layout = (graphicPack.generateAdvancedModeUserWindow(user_id)
                        + outputWindow 
                        + graphicPack.generateControlButtons() 
                        + graphicPack.generateAdvancedCommonButtons()
                        + graphicPack.generateCommonButtons()
                        + graphicPack.memoryWindowGenerator(memory_cells_count))

    # заполняем объект необходимой информацией
    start_info["mode"] = "advanced"
    start_info["window"] = sg.Window('Калькулятор - расширенный режим', layout, element_padding=(4, 3))
    start_info["main_handler"] = MainHandler(output, max_row_size, memory_cells_count)
    return start_info

# изначально калькулятор запускается в обычном режиме
start_info = startInfoSimpleMode()

while True:  # The Event Loop
    event, values = start_info["window"].read()
    print(event, values)  # debug
    # закрытие окна
    if event in (None, 'Exit', 'Cancel'):
        break
    # смена режима с расширенного на обычный и обратно
    if event == 'mode':
        if start_info['mode'] == 'simple':
            start_info["window"].close()
            start_info = startInfoAdvancedMode()
        elif start_info['mode'] == 'advanced':
            start_info["window"].close()
            start_info = startInfoSimpleMode()
    # перерасчет данных исходя из ID
    elif event == '<>':
        if values["id"].isdigit():
            start_info["window"].close()
            start_info = startInfoAdvancedMode(values["id"])
        else:
            start_info["window"].Element('message').update('Поле ID должно содержать только цифры 0 - 9')
    # любое другое событие передает выполнение в главный обработчик
    else:
        start_info["main_handler"].input(event)





    