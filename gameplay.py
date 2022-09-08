import sys
import random
import pathlib
from pathlib import Path
import os.path

from Game_window import *
from Merchant_window_176 import Ui_MainWindow2
from Merchant_window_448 import Ui_MainWindow3
from Question_window_464 import Ui_MainWindow4
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from units import *


class My_window(QMainWindow):
    def __init__(self):
        super(My_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # объект класса Player из units.py
        self.player1 = Player()

        # сигнал на нажатие кнопки Button1
        self.ui.pushButton.clicked.connect(self.click_next_button)

        # bool-список для одноразового открытия окон битв, изображений, сообщений, аудио и т.д. (индекс равен номеру параграфа)
        self.button_click_on_page = [False] * 750        

        # посещение параграфа 187 (две березы), если True, то уже посещен
        self.page_187_visited = False

        # проверка нажатой кнопки в Merchant_window_176
        self.button1_from_merchant_176_click = 0

        # список товаров у крестьянина п.448
        self.item_list_448 = ["Ананас", "Банан", "Кусочек дерева", "Фигурный ключ", "Попона", "Кусок металла", "Золотая устрица", "Серебр. браслет"]
        # индикатор окончания торговли на п.448
        self.buying448_is_over = False

        # индикатор закрытия окна п.464
        self.window464_is_closed = True
        self.spell_is_selected_464 = 0

        # индикатор заклинаний Силы и Слабости
        self.weakness = False
        self.increase_strength = False

        # переменная показа картинки в параграфах с указанным номером (чтобы показать ее только 1 раз)
        self.picture_page_84 = 0

        # номер предыдущей страницы для некоторых случаев
        self.previous_page = 319

        # переменная для битвы, чтобы не включалась повторно
        self.battle_page_16 = 0
        self.battle_page_93 = 0
        self.battle_page_102 = 0

        # размер шрифта для всплывающих сообщений
        self.font_for_messageboxes = QFont()
        self.font_for_messageboxes.setPointSize(10)

        # переменные аудио-файлов
        self.page1_audio = QMediaPlayer()
        self.page277_audio = QMediaPlayer()

        # использование исцеляющих предметов
        self.ui.tableWidget.cellClicked.connect(self.tableWidget_using_item)
        # использование заклинания исцеления
        self.ui.tableWidget_2.cellClicked.connect(self.tableWidget2_using_spell)

        # номер вступительной страницы
        self.intro_number = 1

        # номер страницы основной игры
        self.page_number = 1                                                                # проверка параграфа

        # начальные надписи на кнопке и метке №2
        self.ui.pushButton.setText("Начать Игру")
        self.ui.label_2.setText("")

    # вступление и установка параметров игрока
    def play_intro(self):
        """
           Вступление, описание правил игры и установка параметров игрока

        """
        # отображение файлов вступления (intro) в textEdit
        self.ui.textEdit.clear()
        self.file_name_to_str = "GameText\Intro" + str(self.intro_number) + ".txt"
        self.intro_file = open(self.file_name_to_str, "r")
        text_from_intro_files = self.intro_file.read()
        self.ui.textEdit.append(text_from_intro_files)
        del text_from_intro_files
        self.intro_file.close

        # Intro1.txt (дополнение)
        if self.intro_number == 1:
            self.ui.pushButton.setText("Далее")
            self.ui.label_2.setText("Введите номер следующего параграфа")

        # Intro2.txt (дополнение)
        if self.intro_number == 2:
            # рисунок листка путешественника на бумаге (выводится во всплывающем окне), прикладывается к файлу Intro2.txt
            message_intro2 = QMessageBox(self)
            message_intro2.setWindowTitle("Листок путешественника")
            message_intro2.setIconPixmap(QPixmap("GameText\Intro2.png"))
            message_intro2.show()

        # Intro3.txt (дополнение)
        elif self.intro_number == 3:
            # рисунок для записи битв на бумаге (выводится во всплывающем окне), прикладывается к файлу Intro3.txt
            message_intro3 = QMessageBox(self)
            message_intro3.setWindowTitle("Мастерство и выносливость")
            message_intro3.setIconPixmap(QPixmap("GameText\Intro3.png"))
            message_intro3.show()

        # Intro4.txt (дополнение)
        elif self.intro_number == 4:
            # определение мастерства, выносливости и удачи (описание в файле Intro4.txt)
            message_intro4 = QMessageBox(self)
            message_intro4.setWindowTitle("Параметры героя")
            message_intro4.resize(200, 200)
            message_intro4.setFont(self.font_for_messageboxes)
            # имитация бросания кубиков для определения мастерства, выносливости и удачи 
            # (на самом деле значения определены заранее в конструкторе класса Player)
            text_information_strength_stamina_luck = ("Первый бросок кубика: выпало " + str(self.player1.strength - 6) + "." +
                                                      "\nВаше Мастерство = " + str(self.player1.strength) + "." +
                                                      "\nВторой бросок кубика: выпало " + str(self.player1.luck - 6) + "." + 
                                                      "\nВаша Удача = " + str(self.player1.luck) + "." +
                                                      "\nБросок двух кубиков: выпало " + str(self.player1.life_points - 12) + "." +
                                                      "\nВаша Выносливость = " + str(self.player1.life_points)) + "."
            message_intro4.setText(text_information_strength_stamina_luck)
            message_intro4.show()
            # del text_information_strength_stamina_luck
            # запись значений мастерства, выносливости и удачи в метки(QLabel) № 5, 6 и 7
            self.strength_stamina_luck_information()
            

        # Intro9.txt (дополнение)
        elif self.intro_number == 9:
            # добавляем 2 строки
            self.ui.tableWidget.insertRow(0)
            self.ui.tableWidget.insertRow(1)
            self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
            # добавляем 2 столбца
            self.ui.tableWidget.insertColumn(0)
            self.ui.tableWidget.insertColumn(1)
            # редактируем титульные ячейки
            self.ui.tableWidget.setHorizontalHeaderLabels(['ПРЕДМЕТЫ', 'ЗНАЧЕНИЕ'])
            # растягиваем ячейки по размеру окна таблицы
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            # устанавливаем текст в ячейки [0, 0] и [0, 1]
            self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("ЗОЛОТО"))
            self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.player1.gold)))
            self.ui.tableWidget.setItem(1, 0, QTableWidgetItem("ЕДА"))
            self.ui.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.player1.food)))
            self.ui.tableWidget.setItem(2, 0, QTableWidgetItem("ВОДА"))
            self.ui.tableWidget.setItem(2, 1, QTableWidgetItem(str(self.player1.water)))
            # золотой цвет для надписей "ЗОЛОТО" и "15"
            # красный цвет для меток "ЕДА" и "2"
            # синий цвет для меток "ВОДА" и "2"
            self.ui.tableWidget.item(0, 0).setForeground(QBrush(QColor("#c58916")))
            self.ui.tableWidget.item(0, 1).setForeground(QBrush(QColor("#c58916")))
            self.ui.tableWidget.item(1, 0).setForeground(QBrush(QColor("red")))
            self.ui.tableWidget.item(1, 1).setForeground(QBrush(QColor("red")))
            self.ui.tableWidget.item(2, 0).setForeground(QBrush(QColor("blue")))
            self.ui.tableWidget.item(2, 1).setForeground(QBrush(QColor("blue")))
            # выравнивание текста по центру в таблице 1 (во всех ячейках)
            self.Cell_alignment_1()


        # Intro13.txt (дополнение)
        elif self.intro_number == 13:
            # обновление информации о мастерстве, выносливости и удаче
            self.strength_stamina_luck_information()
            # выделяем 10 столбцов для начальных заклинаний
            [self.ui.tableWidget_2.insertRow(self.ui.tableWidget_2.rowCount()) for i in range(0, 10, 1)]
            # добавляем столбец
            self.ui.tableWidget_2.insertColumn(0)
            # редактируем титульные ячейки
            self.ui.tableWidget_2.setHorizontalHeaderLabels([""])
            # растягиваем ячейки по размеру окна таблицы
            self.ui.tableWidget_2.horizontalHeader().setStretchLastSection(True)
            # вставляем начальный список заклинаний в tableWidget_2
            [self.ui.tableWidget_2.setItem(k, 0, QTableWidgetItem(str(self.player1.spells[k]))) for k in range(0, 10, 1)]
            # выравниваем надписи по центру
            self.Cell_alignment_2()


    # основная игра
    def play_page(self):
        """
        Основной алгоритм игры
        """

        while True:

            # --------------------------------параграф 1------------------------------------
            if self.page_number == 1:
                self.ui.label_2.setText("Введите номер следующего параграфа")
                self.ui.pushButton.setText("Следующий параграф")
                self.read_page_text()
                self.PlayAudioFile(self.page1_audio, "GameText\Page1.mp3")
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page1 = QMessageBox(self)
                    message_page1.setWindowTitle("Сказочный лес")
                    message_page1.setIconPixmap(QPixmap("GameText\Page1.png"))
                    message_page1.show()
                if self.ui.lineEdit.text() == '86' or self.ui.lineEdit.text() == '110':
                    self.StopAudio(self.page1_audio)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number 


            #------------------------- параграф 2  -----------------------------------          
            elif self.page_number == 2:
                self.read_page_text()
                if self.ui.lineEdit.text() == '97' or self.ui.lineEdit.text() == '175':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number 


            # --------------------------------параграф 3------------------------------------
            elif self.page_number == 3:
                self.read_page_text()
                if self.ui.lineEdit.text() == '211':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number 


            # ----------------------------параграф 4---------------------------------
            elif self.page_number == 4:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)

                elif self.ui.lineEdit.text() == '103':
                    # проверка наличия заклинания левитации у игрока
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")                       
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
 
                elif self.ui.lineEdit.text() == '311' or self.ui.lineEdit.text() == '372':
                    # проверка наличия заклинания плавания у игрока
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # -------------------------параграф 5------------------------------
            elif self.page_number == 5:
                self.read_page_text()
                if self.ui.lineEdit.text() == '216' or self.ui.lineEdit.text() == '517':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # ---------------параграф 6-------------------
            elif self.page_number == 6:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    print("Сражение с двумя дровосеками")
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page6 = QMessageBox()
                        message1_page6.setWindowTitle("Параграф 6")
                        font_page6 = QFont()
                        font_page6.setPointSize(14)
                        message1_page6.setFont(font_page6)
                        message1_page6.setText("Хотите использовать заклинание копии?")
                        message1_page6.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m6 = message1_page6.exec_()
                        if m6 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_two_copy_spell("Первый дровосек", 5, 4, "Второй дровосек", 6, 7)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_two("Первый дровосек", 5, 4, "Второй дровосек", 6, 7)
                            self.strength_stamina_luck_information()
                            print("Игрок победил дровосеков")
                    else:                       
                        self.player1.battleground_two("Первый дровосек", 5, 4, "Второй дровосек", 6, 7)
                        self.strength_stamina_luck_information()
                        print("Игрок победил дровосеков")

                    print("Игрок победил дровосеков")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '420':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    # 1 золотой в кармане одного из дровосеков
                    self.player1.gold += 1
                    self.gold_food_water_information()
                    # -1 к удаче
                    self.player1.luck -= 1
                    # обновление информации о мастерстве, выносливости и удаче
                    self.strength_stamina_luck_information()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # --------------------------параграф 7-----------------------------
            elif self.page_number == 7:
                self.read_page_text()
                # применение залинания СИЛА
                if self.ui.lineEdit.text() == '36':
                    # проверка наличия заклинания плавания у игрока
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # потеря 2 ед. ВЫНОСЛИВОСТИ
                        self.player1.life_points -= 2
                        print("Выносливость - 2, Мастерство + 2")
                        #self.player1.strength += 2                                                 # мастерство увеличено на 2 до окончания битвы
                        self.strength_stamina_luck_information()
                        self.checking_game_over()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        # индикатор применения заклинания силы на параграфе 36               Warning! Индикатор применения заклинания (сила), после битвы вернуть параметр на место
                        self.player1.strength_36 = True
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error() 
                        return self.page_number

                # применение заклинания СЛАБОСТЬ
                elif self.ui.lineEdit.text() == '314':
                    # применение заклинания СЛАБОСТЬ
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # потеря 2 ед. ВЫНОСЛИВОСТИ
                        self.player1.life_points -= 2
                        #self.player1.strength -= 2                                              # мастерство уменьшено на 2 (по сценарию, нестандартный случай) до окончания битвы
                        self.strength_stamina_luck_information()
                        self.checking_game_over()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        # индикатор применения заклинания слабости на параграфе 314         Warning! Индикатор применения заклинания (слабость), после боя вернуть параметр на место
                        self.player1.weakness_314 = True
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()  
                        return self.page_number

                # применение заклинания ОГОНЬ
                elif self.ui.lineEdit.text() == '112':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # потеря 2 ед. ВЫНОСЛИВОСТИ
                        self.player1.life_points -= 2
                        self.strength_stamina_luck_information()
                        self.checking_game_over()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()    
                        return self.page_number

                # обычное стражение с мечом
                elif self.ui.lineEdit.text() == '183':
                    # потеря 2 ед. ВЫНОСЛИВОСТИ
                    self.player1.life_points -= 2
                    self.strength_stamina_luck_information()
                    self.checking_game_over()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # ---------------------------------------параграф 8-------------------------------------------
            elif self.page_number == 8:
                self.read_page_text()
                if self.ui.lineEdit.text() == '118':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    self.add_item_and_print_console(bronze_whistle)
                    self.add_item_to_table_widget(bronze_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number

            # ------------------------------параграф 9--------------------------------
            elif self.page_number == 9:
                self.read_page_text()
                if self.ui.lineEdit.text() == '222':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number 


            # ------------------------------параграф 10--------------------------------
            elif self.page_number == 10:
                self.read_page_text()
                if self.ui.lineEdit.text() == '399' or self.ui.lineEdit.text() == '325':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '459':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # ------------------------------параграф 11--------------------------------
            elif self.page_number == 11:
                self.read_page_text()
                if self.ui.lineEdit.text() == '234':
                    
                    two_birch_trees = Item("'Две берёзы'", "+140")
                    self.add_item_and_print_console(two_birch_trees)
                    self.add_item_to_table_widget(two_birch_trees)

                    self.player1.water -= 2
                    print("Water -2")
                    self.gold_food_water_information()

                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number            


            # ------------------------------параграф 12--------------------------------
            elif self.page_number == 12:
                self.read_page_text()
                if self.ui.lineEdit.text() == '312' :
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '201':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number     
                elif self.ui.lineEdit.text() == '425':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.ui.lineEdit.clear()
                        self.using_spell_error()       
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number      

            
            # --------------------------------параграф 13------------------------------------
            if self.page_number == 13:
                self.read_page_text()
                if self.ui.lineEdit.text() == '360' or self.ui.lineEdit.text() == '184' or self.ui.lineEdit.text() == '235':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Enter number of page")
                        return self.page_number       


            # -----------------------------------параграф 14--------------------------------------
            if self.page_number == 14:
                self.read_page_text()
                QMessageBox.information(self, "Удача", "Проверьте свою удачу")
                if self.player1.checking_luck():                                          # Warning  MessageBox с проверкой удачи - мелкий шрифт
                    self.page_number = 338
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    QMessageBox.information(self, "Переход", "Переход к параграфу 338")
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_number = 404
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    QMessageBox.information(self, "Переход", "Переход к параграфу 404")
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)


            # --------------------------------параграф 15------------------------------------
            if self.page_number == 15:
                self.read_page_text()

                if self.ui.lineEdit.text() == '417':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.strength_stamina_luck_information()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()   
                        print(self.player1.spells)

                elif self.ui.lineEdit.text() == '228':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()   
                        print(self.player1.spells)

                elif self.ui.lineEdit.text() == '521':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()    
                        print(self.player1.spells) 

                elif self.ui.lineEdit.text() == '326':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Enter number of page")
                        return self.page_number 


            # --------------------------------параграф 16------------------------------------
            if self.page_number == 16:
                self.read_page_text()
                if self.ui.lineEdit.text() == '557':
                    # проверка наличия заклинания огня у игрока
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # -1 к выносливости
                        self.losing_life_points(1)
                        print("-1 к выносливости")
                        self.strength_stamina_luck_information()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()    
                        print(self.player1.spells)
                        return self.page_number
                # ввели дополнительный параграф 700 (текст такой же, как и в 16)        
                elif self.ui.lineEdit.text() == '700':
                    # -1 к выносливости
                    self.losing_life_points(1)
                    print("-1 к выносливости")
                    self.strength_stamina_luck_information()
                    self.battle_page_16 += 1
                    if self.battle_page_16 == 1:
                        self.player1.round_number = 0

                        print("Сражение с летучими мышами")
                        self.player1.battleground_16_3()
                        print("Игрок победил летучих мышей")
                        self.strength_stamina_luck_information()

                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующий параграф = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number 
                    else:
                        print("Введите номер страницы")
                        return self.page_number      

            # дополнение к параграфу 16
            if self.page_number == 700:
                self.read_page_text()
                if self.ui.lineEdit.text() == '120' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 17-----------------------------------
            elif self.page_number == 17:
                self.read_page_text()  
                if self.ui.lineEdit.text() == '426' or self.ui.lineEdit.text() == '109' or self.ui.lineEdit.text() == '339':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 18-----------------------------------
            elif self.page_number == 18:
                self.read_page_text()  
                if self.ui.lineEdit.text() == '327':
                    if self.player1.gold >= 7:
                        self.player1.gold -= 7
                        self.gold_food_water_information()
                        print("Отдаете торговцу 7 золотых")
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет столько золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number
                elif self.ui.lineEdit.text() == '217' or self.ui.lineEdit.text() == '106' or self.ui.lineEdit.text() == '518':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()  
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number            


            # --------------------------------параграф 19-----------------------------------
            elif self.page_number == 19:
                self.read_page_text()
                if self.ui.lineEdit.text() == '176' or self.ui.lineEdit.text() == '185':
                    self.page_number = int(self.ui.lineEdit.text())
                    print("Следующий параграф = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # --------------------------------параграф 20-----------------------------------
            elif self.page_number == 20:
                self.read_page_text()
                if self.ui.lineEdit.text() == '340' or self.ui.lineEdit.text() == '442':
                    self.page_number = int(self.ui.lineEdit.text())
                    print("Следующий параграф = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # --------------------------------параграф 21-----------------------------------
            elif self.page_number == 21:
                self.read_page_text()
                if self.ui.lineEdit.text() == '186' or self.ui.lineEdit.text() == '202' or self.ui.lineEdit.text() == '229':
                    self.player1.life_points += 2
                    if self.player1.life_points > self.player1.max_life_points:
                        self.player1.life_points = self.player1.max_life_points
                    print("Восстановили 2 выносливости")    
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующий параграф = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number


            # --------------------------------параграф 22-----------------------------------
            elif self.page_number == 22:
                self.read_page_text() 
                if (self.ui.lineEdit.text() == '427' or self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206'
                          or self.ui.lineEdit.text() == '350'): 
                    white_arrow = Item("Белая стрела", "-")
                    self.add_item_and_print_console(white_arrow)
                    self.add_item_to_table_widget(white_arrow)      
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующий параграф = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер параграфа")
                        return self.page_number

             
            # --------------------------------параграф 23-----------------------------------
            elif self.page_number == 23:
                self.read_page_text() 
                if self.ui.lineEdit.text() == '327':
                    if self.player1.gold >= 7:
                        self.player1.gold -= 7
                        self.gold_food_water_information()
                        print("Отдаете торговцу 7 золотых")
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет столько золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number    
                elif self.ui.lineEdit.text() == '217' or self.ui.lineEdit.text() == '106' or self.ui.lineEdit.text() == '518':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()  
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 24-----------------------------------
            elif self.page_number == 24:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page24 = QMessageBox(self)
                    message_page24.resize(1000, 1000)
                    message_page24.setWindowTitle("Параграф " + str(self.page_number))
                    font24 = QFont()
                    font24.setPointSize(14)
                    message_page24.setFont(self.font_for_messageboxes)
                    name_of_opening_file_24 = "Page" + str(self.page_number) + ".txt"
                    str_to_file_name_24 = Path("GameText", name_of_opening_file_24)
                    page_file_24 = open(str_to_file_name_24, "r")
                    message_page24.setText(page_file_24.read())
                    message_page24.exec_()
                select_spell = random.randint(0, 1)
                if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ") and self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                    if select_spell == 1:                     
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        message2_page24 = QMessageBox(self)
                        message2_page24.resize(1000, 1000)
                        message2_page24.setWindowTitle("-------->>")
                        message2_page24.setFont(font24)
                        message2_page24.setText("Вы применяете заклинание Левитации")
                        message2_page24.exec_()
                        message3_page24 = QMessageBox(self)
                        message3_page24.resize(1000, 1000)
                        message3_page24.setWindowTitle("-------->>")
                        message3_page24.setFont(font24)
                        message3_page24.setText("Переход к параграфу 238")
                        message3_page24.exec_()
                        self.page_number = 238
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        message4_page24 = QMessageBox(self)
                        message4_page24.resize(1000, 1000)
                        message4_page24.setWindowTitle("-------->>")
                        message4_page24.setFont(font24)
                        message4_page24.setText("Вы применяете заклинание Плавания")
                        message4_page24.exec_()
                        message5_page24 = QMessageBox(self)
                        message5_page24.resize(1000, 1000)
                        message5_page24.setWindowTitle("-------->>")
                        message5_page24.setFont(font24)
                        message5_page24.setText("Переход к параграфу 238")
                        message5_page24.exec_()
                        self.page_number = 238
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                elif self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ") and self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ") == False:
                    # если заклинание есть в списке, оно удаляется (1 штука)
                    self.player1.spells.remove("ЛЕВИТАЦИЯ")
                    # обновим список заклинаний на экране в таблице
                    self.output_spells()
                    message6_page24 = QMessageBox(self)
                    message6_page24.resize(1000, 1000)
                    message6_page24.setWindowTitle("-------->>")
                    message6_page24.setFont(font24)
                    message6_page24.setText("Вы применяете заклинание Левитации")
                    message6_page24.exec_()
                    message7_page24 = QMessageBox(self)
                    message7_page24.resize(1000, 1000)
                    message7_page24.setWindowTitle("-------->>")
                    message7_page24.setFont(font24)
                    message7_page24.setText("Переход к параграфу 238")
                    message7_page24.exec_()
                    self.page_number = 238
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ") == False and self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                    # если заклинание есть в списке, оно удаляется (1 штука)
                    self.player1.spells.remove("ПЛАВАНИЕ")
                    # обновим список заклинаний на экране в таблице
                    self.output_spells()
                    message8_page24 = QMessageBox(self)
                    message8_page24.resize(1000, 1000)
                    message8_page24.setWindowTitle("-------->>")
                    message8_page24.setFont(font24)
                    message8_page24.setText("Вы применяете заклинание Плавания")
                    message8_page24.exec_()
                    message9_page24 = QMessageBox(self)
                    message9_page24.resize(1000, 1000)
                    message9_page24.setWindowTitle("-------->>")
                    message9_page24.setFont(font24)
                    message9_page24.setText("Переход к параграфу 238")
                    message9_page24.exec_()
                    self.page_number = 238
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                                      
                else:
                    message10_page24 = QMessageBox(self)
                    message10_page24.resize(1000, 1000)
                    message10_page24.setWindowTitle(":-(")
                    message10_page24.setFont(font24)
                    message10_page24.setText("У вас нет заклинаний Плавания и Левитации :-(")
                    message10_page24.exec_()
                    message11_page24 = QMessageBox(self)
                    message11_page24.resize(1000, 1000)
                    message11_page24.setWindowTitle(":-(")
                    message11_page24.setFont(font24)
                    message11_page24.setText("Вы проиграли\nИгра окончена")
                    message11_page24.exec_()
                    sys.exit("Game over")

                    
            # --------------------------------параграф 25-----------------------------------
            elif self.page_number == 25:
                self.read_page_text()
                if (self.ui.lineEdit.text() == '427' or self.ui.lineEdit.text() == '398' or 
                           self.ui.lineEdit.text() == '206' or self.ui.lineEdit.text() == '350'):
                    # +6 к выносливости
                    self.life_points_recovery(6)                          
                    self.strength_stamina_luck_information()         
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 26-----------------------------------
            elif self.page_number == 26:
                self.read_page_text()
                if self.ui.lineEdit.text() == '341':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 27-----------------------------------
            elif self.page_number == 27:
                self.read_page_text()
                if self.ui.lineEdit.text() == '137' or self.ui.lineEdit.text() == '522':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 28-----------------------------------
            elif self.page_number == 28:
                self.read_page_text()
                if self.ui.lineEdit.text() == '443':
                    diamond = Item("Бриллиант", "-")
                    # удалить бриллиант из инвентаря
                    self.delete_item(diamond)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 29-----------------------------------
            elif self.page_number == 29:
                self.read_page_text()
                if self.ui.lineEdit.text() == '235' or self.ui.lineEdit.text() == '184':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 30-----------------------------------
            elif self.page_number == 30:
                self.read_page_text()
                if self.ui.lineEdit.text() == '10':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 31-----------------------------------
            elif self.page_number == 31:
                self.read_page_text()
                if self.ui.lineEdit.text() == '48':
                    fox_fur = Item("Шкура лисы", "-")
                    # проверка есть ли в мешке шкура лисы (fox fur)
                    if self.checking_bag_item(fox_fur):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет данного предмета")
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number

                elif self.ui.lineEdit.text() == '428':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 32-----------------------------------
            elif self.page_number == 32:
                self.read_page_text()
                if self.ui.lineEdit.text() == '207':
                    # -1 мастерство (игрок выпил плохое вино)
                    self.player1.strength -= 1
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number    


            # --------------------------------параграф 33-----------------------------------
            elif self.page_number == 33:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page33 = QMessageBox()
                    message_page33.setWindowTitle("Параграф 33")
                    font_page33 = QFont()
                    font_page33.setPointSize(14)
                    message_page33.setFont(self.font_for_messageboxes)
                    text_page33 = "Вы входите внутрь и понимаете, что попали на Заставу, поставленную здесь специально для того, чтобы не пропускать таких, как вы. "
                    text_page33 += "Орк-часовой бросается на вас так стремительно, что вы не успеваете применить заклятия, и вам приходится драться с ним."
                    message_page33.setText(text_page33)
                    message_page33.exec_()

                    message1_page33 = QMessageBox()
                    message1_page33.setWindowTitle("Параграф 33")
                    message1_page33.setFont(font_page33)
                    message_page33.setText("Вы можете попытаться убежать.")
                    message_page33.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m33 = message_page33.exec_()
                    if m33 == QMessageBox.Yes:
                        self.strength_stamina_luck_information()
                        self.page_number = 143
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                        continue
                    else:
                        self.player1.round_number = 0
                        print("Битва с орком")
                        self.player1.battleground_one("Орк", 6, 8)
                        print("Игрок победил орка")
                        self.strength_stamina_luck_information()

                        message2_page33 = QMessageBox()
                        message2_page33.setWindowTitle("Параграф 33")
                        message2_page33.setFont(font_page33)
                        text2_page33 = "Если вы убили его, то сделали это как раз вовремя: из погреба с бутылкой вина поднимается Гоблин. "
                        text2_page33 += "Увидев вас, он бросает бутылку и хватается за боевой топор."
                        message2_page33.setText(text2_page33)
                        message2_page33.exec_()

                        self.player1.round_number = 0
                        print("Битва с гоблином")
                        self.player1.battleground_one("Гоблин", 7, 5)
                        print("Игрок победил гоблина")
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '239':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 34-----------------------------------
            elif self.page_number == 34:
                self.read_page_text()
                if self.ui.lineEdit.text() == '3':
                    pocket_mirror = Item("Зеркальце", "-")
                    self.add_item_and_print_console(pocket_mirror)
                    self.add_item_to_table_widget(pocket_mirror)
                    gold_whistle = Item("Золотой свисток", "-")
                    self.add_item_and_print_console(gold_whistle)
                    self.add_item_to_table_widget(gold_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 35-----------------------------------
            elif self.page_number == 35:
                self.read_page_text()
                if self.ui.lineEdit.text() == '204' or self.ui.lineEdit.text() == '342':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 36-----------------------------------
            elif self.page_number == 36:
                self.read_page_text()
                if self.ui.lineEdit.text() == '183':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 37-----------------------------------
            elif self.page_number == 37:
                self.read_page_text()
                if self.ui.lineEdit.text() == '451':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()    
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '701':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к параграфу 37 (№ 701)
            elif self.page_number == 701:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    print("Битва с драконом")
                    print("-2 к выносливости")
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    message1_page701 = QMessageBox()
                    message1_page701.setWindowTitle("!!!")
                    message1_page701.setText("Оставшаяся голова дышит на вас огнем (потеряйте 2 выносливости)")
                    font1_page701 = QFont()
                    font1_page701.setPointSize(14)
                    message1_page701.setFont(self.font_for_messageboxes)
                    message1_page701.exec_()
                    self.player1.battle_text = ""
                    self.player1.battleground_one("Дракон", 9, 4)
                    print("Игрок победил дракона")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '454':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 38-----------------------------------
            elif self.page_number == 38:
                self.read_page_text()
                if self.ui.lineEdit.text() == '221' or self.ui.lineEdit.text() == '55':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 39-----------------------------------
            elif self.page_number == 39:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    picture_page_39 = QMessageBox(self)
                    picture_page_39.setWindowTitle("Комната")
                    picture_page_39.setIconPixmap(QPixmap("GameText\Page39.png"))
                    picture_page_39.show()
                if (self.ui.lineEdit.text() == '138' or self.ui.lineEdit.text() == '523' or 
                        self.ui.lineEdit.text() == '452' or self.ui.lineEdit.text() == '70' or self.ui.lineEdit.text() == '205'):
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 40-----------------------------------
            elif self.page_number == 40:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page40 = QMessageBox()
                        message1_page40.setWindowTitle("Параграф 40")
                        font_page40 = QFont()
                        font_page40.setPointSize(14)
                        message1_page40.setFont(font_page40)
                        message1_page40.setText("Хотите использовать заклинание копии?")
                        message1_page40.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m40 = message1_page40.exec_()
                        if m40 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_two_copy_spell("Первый гоблин", 6, 9, "Второй гоблин", 7, 5)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_two("Первый гоблин", 6, 9, "Второй гоблин", 7, 5)
                            self.strength_stamina_luck_information()
                            print("Игрок победил дровосеков")
                    else:                       
                        self.player1.battleground_two("Первый гоблин", 6, 9, "Второй гоблин", 7, 5)
                        self.strength_stamina_luck_information()
                        print("Игрок победил дровосеков")

                if self.ui.lineEdit.text() == '118':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    self.add_item_and_print_console(bronze_whistle)
                    self.add_item_to_table_widget(bronze_whistle)
                    copper_key = Item("Медный ключик", "-")
                    self.add_item_and_print_console(copper_key)
                    self.add_item_to_table_widget(copper_key)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number   


            # --------------------------------параграф 41-----------------------------------
            elif self.page_number == 41:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    self.player1.round_number = 0
                    print("Битва с драконом")
                    self.player1.battleground_one("Дракон", 9, 4)                                            # Warning битва с драконом
                    print("Игрок победил дракона")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '454':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 42-----------------------------------
            elif self.page_number == 42:
                self.read_page_text()
                if self.ui.lineEdit.text() == '316':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number   

            # --------------------------------параграф 43-----------------------------------
            elif self.page_number == 43:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(2)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 44-----------------------------------
            elif self.page_number == 44:
                self.read_page_text()
                if self.ui.lineEdit.text() == '431' or self.ui.lineEdit.text() == '240':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 45-----------------------------------
            elif self.page_number == 45:
                self.read_page_text()
                if self.ui.lineEdit.text() == '345' or self.ui.lineEdit.text() == '208' or self.ui.lineEdit.text() == '139':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 46-----------------------------------
            elif self.page_number == 46:
                self.read_page_text()
                if self.ui.lineEdit.text() == '445' or self.ui.lineEdit.text() == '524':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 47-----------------------------------
            elif self.page_number == 47:
                self.read_page_text()
                if self.ui.lineEdit.text() == '101' or self.ui.lineEdit.text() == '262':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '187' and self.page_187_visited == False:
                    two_birch_trees = Item("'Две берёзы'", "+140")
                    if self.checking_bag_item(two_birch_trees) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет этой информации")
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 48-----------------------------------
            elif self.page_number == 48:
                self.read_page_text()
                if self.ui.lineEdit.text() == '308' or self.ui.lineEdit.text() == '218' or self.ui.lineEdit.text() == '116':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 49-----------------------------------
            elif self.page_number == 49:
                self.read_page_text()
                if self.ui.lineEdit.text() == '14' or self.ui.lineEdit.text() == '404':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 50-----------------------------------
            elif self.page_number == 50:
                self.read_page_text()
                if self.ui.lineEdit.text() == '310' or self.ui.lineEdit.text() == '418' or self.ui.lineEdit.text() == '179':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 51-----------------------------------
            elif self.page_number == 51:
                self.read_page_text()
                if self.ui.lineEdit.text() == '21' or self.ui.lineEdit.text() == '400':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '81':
                    clew = Item("Клубочек", "+30")
                    if self.checking_bag_item(clew):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 52-----------------------------------
            elif self.page_number == 52:
                self.read_page_text()
                if self.ui.lineEdit.text() == '373' or self.ui.lineEdit.text() == '121':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 53-----------------------------------
            elif self.page_number == 53:
                self.read_page_text()
                if self.ui.lineEdit.text() == '519' or self.ui.lineEdit.text() == '328':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number



            # --------------------------------параграф 54-----------------------------------
            elif self.page_number == 54:
                self.read_page_text()
                message_checking_luck_54 = QMessageBox()
                message_checking_luck_54.setText("Проверьте свою удачу")
                message_checking_luck_54.setWindowTitle("Удача")
                font_checking_luck_54 = QFont()
                font_checking_luck_54.setPointSize(14)
                message_checking_luck_54.setFont(font_checking_luck_54)
                message_checking_luck_54.exec_()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    if self.player1.checking_luck():
                        self.page_number = 558
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        message_page_54 = QMessageBox()
                        message_page_54.setText("Переход к параграфу 558")
                        message_page_54.setWindowTitle("------>>")
                        font_page_54 = QFont()
                        font_page_54.setPointSize(14)
                        message_page_54.setFont(font_page_54)
                        message_page_54.exec_()
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.page_number = 702
                        print("-1 к удаче")
                        print("-1 к мастерству")
                        self.player1.luck -= 1                       
                        self.strength_stamina_luck_information()
                        message2_page_54 = QMessageBox()
                        message2_page_54.setText("Паук затягивает вас на дерево,\nваша СИЛА УДАРА будет уменьшена на 1")
                        message2_page_54.setWindowTitle("Битва с пауком")
                        font_page_54 = QFont()
                        font_page_54.setPointSize(14)
                        message2_page_54.setFont(self.font_for_messageboxes)
                        message2_page_54.exec_()
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)

            # дополнение к параграфу 54 (Page702)
            elif self.page_number == 702:
                self.read_page_text()
                if self.ui.lineEdit.text() == '410':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.player1.strength_spell = True
                        self.strength_stamina_luck_information()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()   
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '219':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()   
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '703': 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number    

            # второе дополнение к параграфу 54 (п. 703)
            elif self.page_number == 703:
                self.page_number = 702
                self.read_page_text()    
                self.page_number = 703
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0
                    # Мастерство уменьшено на -1, только до окончания битвы (т.к. игрок сражается на дереве)
                    self.player1.strength -= 1

                    if self.player1.strength_spell == True:
                        self.player1.strength += 2
                        self.strength_stamina_luck_information()

                    self.strength_stamina_luck_information()
                    print("Битва с пауком")    
                    self.player1.battleground_one("Паук", 8, 8)
                    print("Игрок победил паука")

                    if self.player1.strength_spell == True:
                        self.player1.strength_spell = False
                        # мастерство возвращается на место (заклинание Силы)
                        self.player1.strength -= 2
                        self.strength_stamina_luck_information()

                    # мастерство было уменьшено на 1, т.к. игрок сражался на дереве (возвращено обратно +1)
                    self.player1.strength += 1
                    self.strength_stamina_luck_information()

                    self.page_number = 704    

            # третье дополнение к параграфу 54 (п. 704)
            elif self.page_number == 704:
                self.read_page_text()
                if self.ui.lineEdit.text() == '189':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number
            # --------------------------------параграф 54 (конец)-----------------------------------------


            # --------------------------------параграф 55-----------------------------------
            elif self.page_number == 55:
                self.read_page_text()
                if self.ui.lineEdit.text() == '121' or self.ui.lineEdit.text() == '188':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 56-----------------------------------
            elif self.page_number == 56:
                self.read_page_text()                
                self.page_you_lost(56)


            # --------------------------------параграф 57-----------------------------------
            elif self.page_number == 57:
                self.read_page_text()
                if self.ui.lineEdit.text() == '181':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 58-----------------------------------
            elif self.page_number == 58:
                self.read_page_text()
                if self.ui.lineEdit.text() == '40':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 59-----------------------------------
            elif self.page_number == 59:
                self.read_page_text()
                if self.ui.lineEdit.text() == '240' or self.ui.lineEdit.text() == '528':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 60-----------------------------------
            elif self.page_number == 60:
                self.read_page_text()
                if self.ui.lineEdit.text() == '181':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 61-----------------------------------
            elif self.page_number == 61:
                self.read_page_text()
                if self.ui.lineEdit.text() == '267':
                    peacock_feather = Item("Перо павлина", "-")
                    if self.checking_bag_item(peacock_feather):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '147':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 62-----------------------------------
            elif self.page_number == 62:
                self.read_page_text()
                # взял амулет с медвежей шерстью (вызывает медведицу, чтобы она сражалась за игрока)
                if self.ui.lineEdit.text() == '457':                 
                    message_page62 = QMessageBox()
                    message_page62.setWindowTitle("Медвежий амулет")
                    font_page62 = QFont()
                    font_page62.setPointSize(14)
                    message_page62.setFont(font_page62)
                    message_page62.setText("Медвежий амулет пока что невозможно использовать в игре. Вскоре мы это устраним. Выберите, пожалуйста, другой предмет :-)")
                    message_page62.exec_()
                    self.page_number = 62
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)

                    # bear_amulet = Item("Медвежий амулет", "-")                              # проработать Медведицу в боях вне замка
                    # self.add_item_and_print_console(bear_amulet)
                    # self.add_item_to_table_widget(bear_amulet)
                    # self.page_number = int(self.ui.lineEdit.text())
                    # self.ui.lineEdit.clear()
                    # print("Следующая страница = ", self.page_number)

                # взял волшебный пояс (вызывает крота, чтобы прорыть подземный ход)    
                elif self.ui.lineEdit.text() == '156':
                    magic_belt = Item("Волшебный пояс", "п.167")
                    self.add_item_and_print_console(magic_belt)
                    self.add_item_to_table_widget(magic_belt)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.player1.luck += 1
                    print("Удача +1")
                    self.strength_stamina_luck_information()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # взял шкуру лисы    
                elif self.ui.lineEdit.text() == '367': 
                    fox_fur = Item("Шкура лисы", "-")
                    self.add_item_and_print_console(fox_fur)
                    self.add_item_to_table_widget(fox_fur)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                # выйти из берлоги и уйти по дороге    
                elif self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number    


            # --------------------------------параграф 63-----------------------------------
            elif self.page_number == 63:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 64-----------------------------------
            elif self.page_number == 64:
                self.read_page_text()
                if self.ui.lineEdit.text() == '340' or self.ui.lineEdit.text() == '442':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 65-----------------------------------
            elif self.page_number == 65:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    page65_part1 = "Начальник стражи не успевает даже открыть рот, как вы накидываетесь на него с мечом. " 
                    page65_part1 += "Но будьте осторожны: ведь Орки в соседней комнате не глухие."
                    message_page_65 = QMessageBox(self)
                    message_page_65.resize(1000, 1000)
                    message_page_65.setWindowTitle("Осторожно!")
                    font_65 = QFont()
                    font_65.setPointSize(14)
                    message_page_65.setFont(self.font_for_messageboxes)
                    message_page_65.setText(page65_part1)
                    message_page_65.exec_()

                    self.player1.round_number = 0
                    print("Битва с начальником стражи")

                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page65 = QMessageBox()
                        message1_page65.setWindowTitle("Параграф 65")
                        font_page65 = QFont()
                        font_page65.setPointSize(14)
                        message1_page65.setFont(font_page65)
                        message1_page65.setText("Хотите использовать заклинание копии?")
                        message1_page65.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m65 = message1_page65.exec_()
                        if m65 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_65_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_65()
                            self.strength_stamina_luck_information()
                            print("Игрок победил начальника стражи")
                    else:                       
                        self.player1.battleground_65()
                        self.strength_stamina_luck_information()
                        print("Игрок победил начальника стражи")

                    print("Игрок победил начальника стражи")
                    self.page_number = self.player1.page_number_65_next_page
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                    continue

            # дополнение к параграфу 65
            elif self.page_number == 705:
                self.read_page_text()
                if self.ui.lineEdit.text() == '468':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # второе дополнение к п.65
            elif self.page_number == 726:
                self.read_page_text() 
                self.page_you_lost(726)



            # --------------------------------параграф 66-----------------------------------
            elif self.page_number == 66:
                self.read_page_text()
                if self.ui.lineEdit.text() == '46':
                    stork_feather = Item("Перо аиста", "-")
                    self.add_item_and_print_console(stork_feather)
                    self.add_item_to_table_widget(stork_feather)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 67-----------------------------------
            elif self.page_number == 67:
                self.read_page_text()
                # загадка от домика идёт от параграфа 149 (отгадка пароль - п.95 ("Дракон"))
                if self.ui.lineEdit.text() == '98':
                    dragon_claw = Item("Коготь дракона", "-")
                    self.add_item_and_print_console(dragon_claw)
                    self.add_item_to_table_widget(dragon_claw)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '95':
                    dragon_claw = Item("Коготь дракона", "-")
                    self.add_item_and_print_console(dragon_claw)
                    self.add_item_to_table_widget(dragon_claw)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 68-----------------------------------
            elif self.page_number == 68:
                self.read_page_text()
                if self.ui.lineEdit.text() == '160':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 69-----------------------------------
            elif self.page_number == 69:
                self.read_page_text()
                self.page_you_lost(69)


            # --------------------------------параграф 70-----------------------------------
            elif self.page_number == 70:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '273':
                    # проверка наличия заклинания левитации у игрока
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print("Вы не можете использовать данное заклинание")
                        return self.page_number
                elif self.ui.lineEdit.text() == '609':
                    pegasus = Item("Вызов пегаса", "п.609")
                    if self.checking_bag_item(pegasus) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number
           

            # --------------------------------параграф 71-----------------------------------
            elif self.page_number == 71:
                self.read_page_text()                                                           # использование белой стрелы, выяснить из какого параграфа
                if self.ui.lineEdit.text() == '368' or self.ui.lineEdit.text() == '482' or self.ui.lineEdit.text() == '536':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 72-----------------------------------
            elif self.page_number == 72:
                self.read_page_text()
                if self.ui.lineEdit.text() == '340' or self.ui.lineEdit.text() == '442':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 73-----------------------------------
            elif self.page_number == 73:
                self.read_page_text()
                if self.ui.lineEdit.text() == '286' or self.ui.lineEdit.text() == '470':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

                        
            # --------------------------------параграф 74-----------------------------------
            elif self.page_number == 74:
                self.read_page_text()
                if self.ui.lineEdit.text() == '257':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 75-----------------------------------
            elif self.page_number == 75:
                self.read_page_text()
                if self.ui.lineEdit.text() == '247':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 76-----------------------------------
            elif self.page_number == 76:
                self.read_page_text()
                if self.ui.lineEdit.text() == '379' or self.ui.lineEdit.text() == '486':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 77-----------------------------------
            elif self.page_number == 77:
                self.read_page_text()
                if self.ui.lineEdit.text() == '378':
                    self.losing_life_points(1)
                    print("-1 к выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number
                        

            # --------------------------------параграф 78-----------------------------------
            elif self.page_number == 78:
                self.read_page_text()
                if self.ui.lineEdit.text() == '497':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 79-----------------------------------
            elif self.page_number == 79:
                self.read_page_text()
                # 1 золотой вычтен в предыдущем параграфе (п.255)
                if self.ui.lineEdit.text() == '325':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 80-----------------------------------
            elif self.page_number == 80:
                self.read_page_text()
                if self.ui.lineEdit.text() == '322':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 81-----------------------------------
            elif self.page_number == 81:
                self.read_page_text()
                if self.ui.lineEdit.text() == '51':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 82-----------------------------------
            elif self.page_number == 82:
                self.read_page_text()
                if (self.ui.lineEdit.text() == '280' or self.ui.lineEdit.text() == '384'
                          or self.ui.lineEdit.text() == '492' or self.ui.lineEdit.text() == '563'):
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 83-----------------------------------
            elif self.page_number == 83:
                self.read_page_text()
                if self.ui.lineEdit.text() == '247':
                    self.losing_life_points(2)
                    print("-2 к Выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 84-----------------------------------
            elif self.page_number == 84:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    picture_page_84 = QMessageBox(self)
                    picture_page_84.setWindowTitle("Комната")
                    picture_page_84.setIconPixmap(QPixmap("GameText\Page84.png"))
                    picture_page_84.show()
                if self.ui.lineEdit.text() == '547' or self.ui.lineEdit.text() == '501':
                    badge_with_eagle = Item("Бляха с орлом", "-")
                    self.add_item_and_print_console(badge_with_eagle)
                    self.add_item_to_table_widget(badge_with_eagle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 85-----------------------------------
            elif self.page_number == 85:
                self.read_page_text()
                # заклинания Силы вычеркнуто в п.428
                if self.ui.lineEdit.text() == '569':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 86-----------------------------------
            elif self.page_number == 86:
                self.read_page_text()
                if self.ui.lineEdit.text() == '263' or self.ui.lineEdit.text() == '403':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 87-----------------------------------
            elif self.page_number == 87:
                self.read_page_text()
                # заклинание Левитации вычеркнуто в п.236
                if self.ui.lineEdit.text() == '331':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 88-----------------------------------
            elif self.page_number == 88:
                self.read_page_text()
                if self.ui.lineEdit.text() == '177' or self.ui.lineEdit.text() == '212':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 89-----------------------------------
            elif self.page_number == 89:
                self.read_page_text()
                if self.ui.lineEdit.text() == '419' or self.ui.lineEdit.text() == '374':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '104':
                    if self.player1.food >= 1:
                        self.player1.food = 0
                        print("Отдали всю еду")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        message_89 = QMessageBox()
                        message_89.setWindowTitle("Нет еды")
                        message_89.setText("У вас нет еды")
                        font_89 = QFont()
                        font_89.setPointSize(14)
                        message_89.setFont(font_89)
                        message_89.exec_()   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 90-----------------------------------
            elif self.page_number == 90:
                self.read_page_text()
                if self.ui.lineEdit.text() == '30':
                    green_armor = Item("Зеленые латы", "+60")                       # проверить применение лат зеленого рыцаря в замке (+60)
                                                                                    #    По сценарию:    "Перед каждой дверью вы имеете право решить, 
                                                                                    # хотите надевать латы или нет (если отсутствие врагов вокруг позволяет это). 
                                                                                    # Если решаете, что латы на вас, то прибавьте 60 к тому номеру параграфа, 
                                                                                    # куда будет вести дверь. В том случае, если одежда будет играть какую-нибудь роль, 
                                                                                    # вы почтете, что случится, если вы захотите выдать себя за рыцаря."
                    self.add_item_and_print_console(green_armor)
                    self.add_item_to_table_widget(green_armor)                                                                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 91-----------------------------------
            elif self.page_number == 91:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    page_91_str = "Вы просите накормить вас. Повар соглашается, но требует за это плату — 2 золотых."
                    page_91_str += "Если согласны, то отдайте ему деньги, и он нальет вам тарелку горячих щей."
                    page_91_str += "Восстановите 4 ВЫНОСЛИВОСТИ и уходите — (379)."
                    message_page91 = QMessageBox()
                    message_page91.setWindowTitle("---->>")
                    message_page91.setText("Отдать повару 2 золотых")
                    font_page91 = QFont()
                    font_page91.setPointSize(14)
                    message_page91.setFont(self.font_for_messageboxes)
                    message_page91.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m91 = message_page91.exec_()
                    if m91 == QMessageBox.Yes:
                        self.page_number = 91
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:    
                        self.page_number = 91
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                        return self.page_number
                    if m91 == QMessageBox.Yes:
                        if self.player1.gold >= 2:
                            self.player1.gold -= 2
                            self.gold_food_water_information()
                            print("Золото -2")
                            self.life_points_recovery(4)
                            print("Выносливость +4")
                        else:
                            print("У вас нет столько золота")
                            self.ui.lineEdit.clear()
                            self.not_enough_gold()
                            return self.page_number    
                        if self.ui.lineEdit.text() == '379':
                            self.page_number = int(self.ui.lineEdit.text())
                            self.ui.lineEdit.clear()
                            print("Следующая страница = ", self.page_number)
                        else:
                            if self.ui.lineEdit.text() != "":
                                self.warning_wrong_page_number()
                                self.ui.lineEdit.clear()
                                return self.page_number
                            else:
                                print("Введите номер страницы")
                                return self.page_number
                    elif message_page91 == QMessageBox.No:
                        if self.ui.lineEdit.text() == '379':
                            self.page_number = int(self.ui.lineEdit.text())
                            self.ui.lineEdit.clear()
                            print("Следующая страница = ", self.page_number)
                        else:
                            if self.ui.lineEdit.text() != "":
                                self.warning_wrong_page_number()
                                self.ui.lineEdit.clear()
                                return self.page_number
                            else:
                                print("Введите номер страницы")
                                return self.page_number
                else:
                    if self.ui.lineEdit.text() == '379':
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        if self.ui.lineEdit.text() != "":
                            self.warning_wrong_page_number()
                            self.ui.lineEdit.clear()
                            return self.page_number
                        else:
                            print("Введите номер страницы")
                            return self.page_number


            # --------------------------------параграф 92-----------------------------------
            elif self.page_number == 92:
                self.read_page_text()
                if self.ui.lineEdit.text() == '157' or self.ui.lineEdit.text() == '255':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 93-----------------------------------
            elif self.page_number == 93:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с женщиной-вампиром")
                    self.player1.battleground_one("Женщина-вампир", 11, 14)
                    print("Игрок победил женщину-вампира")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '301':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 94-----------------------------------
            elif self.page_number == 94:
                self.read_page_text()
                if self.ui.lineEdit.text() == '264':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 95-----------------------------------
            elif self.page_number == 95:
                self.read_page_text()
                # правильный ответ на загадку домика - Совесть (п.163)
                if self.ui.lineEdit.text() == '98':
                    password_to_castle = Item("Пароль-122", "п.122")
                    self.add_item_and_print_console(password_to_castle)
                    self.add_item_to_table_widget(password_to_castle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '163':
                    password_to_castle = Item("Пароль-122", "п.122")
                    self.add_item_and_print_console(password_to_castle)
                    self.add_item_to_table_widget(password_to_castle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 96-----------------------------------
            elif self.page_number == 96:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 97-----------------------------------
            elif self.page_number == 97:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_97 = QMessageBox(self)
                    message_page_97.setWindowTitle("Параграф 97")
                    message_page_97.setText("У вас недостаточно золота")
                    font_page97 = QFont()
                    font_page97.setPointSize(14)
                    message_page_97.setFont(font_page97)
                    name_of_opening_file_97 = "Page97.txt"
                    str_to_file_name_97 = Path("GameText", name_of_opening_file_97)
                    page_file_97 = open(str_to_file_name_97, "r")
                    message_page_97.setText(page_file_97.read())
                    message_page_97.exec_()
                    page_file_97.close()    
                    if self.player1.checking_luck() == True:
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        self.page_number = 306
                        self.ui.lineEdit.clear()
                        message_page_97 = QMessageBox(self)
                        message_page_97.setWindowTitle("-------->>")
                        message_page_97.setFont(font_page97)
                        message_page_97.setText("Вам повезло. \nПереход на страницу 306")
                        message_page_97.exec_()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        self.player1.game_over = True
                        self.checking_game_over()
                        return self.page_number


            # --------------------------------параграф 98-----------------------------------
            elif self.page_number == 98:
                self.read_page_text()
                if self.ui.lineEdit.text() == '412':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 99-----------------------------------
            elif self.page_number == 99:
                self.read_page_text()
                self.page_you_lost(99)


            # --------------------------------параграф 100-----------------------------------
            elif self.page_number == 100:
                self.read_page_text()
                if self.ui.lineEdit.text() == '375' or self.ui.lineEdit.text() == '424':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 101-----------------------------------
            elif self.page_number == 101:
                self.read_page_text()
                if self.ui.lineEdit.text() == '261':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '307':
                    self.player1.water = 2
                    print("У вас полная фляга(вода = 2)")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '405':
                    self.player1.life_points = self.player1.max_life_points
                    print("Вы восстановили свою выносливость")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 102-----------------------------------
            elif self.page_number == 102:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с гоблином")
                    message1_page102 = QMessageBox()
                    message1_page102.setWindowTitle("Параграф 102")
                    text_page102 = ""
                    text_page102 += "Перед вами широкая полноводная река с быстрым течением. Дорога пересекает ее по небольшому прочному мосту, но у моста охрана."
                    text_page102 += "Это Гоблин — один из воинов бесчисленной армии Черного замка. Размахивая ятаганом, он приближается к вам."
                    text_page102 += "Вы столкнулись с ним настолько неожиданно, что времени наложить заклятие уже нет и выход лишь один: драться."
                    message1_page102.setText(text_page102)
                    font1_page102 = QFont()
                    font1_page102.setPointSize(14)
                    message1_page102.setFont(self.font_for_messageboxes)
                    message1_page102.exec_()
                    self.player1.battle_text = ""
                    self.player1.battleground_one("Гоблин", 8, 9)
                    self.strength_stamina_luck_information()
                    print("Игрок победил гоблина")

                if self.ui.lineEdit.text() == '8':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 103-----------------------------------
            elif self.page_number == 103:
                self.read_page_text()
                if self.ui.lineEdit.text() == '424':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 104-----------------------------------
            elif self.page_number == 104:
                self.read_page_text()
                if self.ui.lineEdit.text() == '520':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 105-----------------------------------
            elif self.page_number == 105:
                self.read_page_text()
                if self.ui.lineEdit.text() == '413' or self.ui.lineEdit.text() == '425':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 106-----------------------------------
            elif self.page_number == 106:
                self.read_page_text()
                if self.ui.lineEdit.text() == '329' or self.ui.lineEdit.text() == '432' or self.ui.lineEdit.text() == '20':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 107-----------------------------------
            elif self.page_number == 107:
                self.read_page_text()
                # на п.209 покупка рыбы во всплывающем окне
                if self.ui.lineEdit.text() == '332' or self.ui.lineEdit.text() == '209' or self.ui.lineEdit.text() == '376' or self.ui.lineEdit.text() == '15':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 108-----------------------------------
            elif self.page_number == 108:
                self.read_page_text()
                if self.ui.lineEdit.text() == '407':
                    gold_amulet = Item("Золотой амулет", "+217")
                    self.add_item_and_print_console(gold_amulet)
                    self.add_item_to_table_widget(gold_amulet)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 109-----------------------------------
            elif self.page_number == 109:
                self.read_page_text()
                #QMessageBox.information(self, "Удача", "Проверьте свою удачу")
                message_luck109 = QMessageBox()
                message_luck109.setWindowTitle("Удача")
                message_luck109.setText("Проверьте свою удачу")
                font_luck109 = QFont()
                font_luck109.setPointSize(14)
                message_luck109.setFont(font_luck109)
                message_luck109.exec_()
                if self.player1.checking_luck():
                    self.page_number = 453
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message2_luck206 = QMessageBox()
                    message2_luck206.setWindowTitle("------->>")
                    message2_luck206.setText("Переход к параграфу 453")
                    message2_luck206.setFont(font_luck109)
                    message2_luck206.exec_()
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)
                else:
                    self.page_number = 242
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message3_luck206 = QMessageBox()
                    message3_luck206.setWindowTitle("------->>")
                    message3_luck206.setText("Переход к параграфу 242")
                    message3_luck206.setFont(font_luck109)
                    message3_luck206.exec_()
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)
                


            # --------------------------------параграф 110-----------------------------------
            elif self.page_number == 110:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page110 = QMessageBox(self)
                    message_page110.setWindowTitle("Умирающий разбойник")
                    message_page110.setIconPixmap(QPixmap("GameText\Page110.png"))
                    message_page110.show()
                if self.ui.lineEdit.text() == '234' or self.ui.lineEdit.text() == '302':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Enter number of page")
                        return self.page_number


            # --------------------------------параграф 111-----------------------------------
            elif self.page_number == 111:
                self.read_page_text()
                if self.ui.lineEdit.text() == '309':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = 709
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Enter number of page")
                        return self.page_number


            # --------------------------------параграф 112-----------------------------------
            elif self.page_number == 112:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page112 = QMessageBox()
                    message_page112.setWindowTitle("Параграф 112")
                    font_page112 = QFont()
                    font_page112.setPointSize(14)
                    message_page112.setFont(self.font_for_messageboxes)
                    text_page112 = "Вы накладываете заклятие Огня, и мгновенно появившийся в воздухе огненный шар ударяет в грудь "
                    text_page112 += "Первого рыцаря, не ожидавшего от вас такого коварства. Огонь прожигает толстые латы и достигает цели: "
                    text_page112 += "корчась от боли, рыцарь падает с лошади. Теперь перед вами только один противник, а времени на новые заклятия уже нет."
                    message_page112.setText(text_page112)
                    message_page112.exec_()

                    message1_page112 = QMessageBox()
                    message1_page112.setWindowTitle("Параграф 112")
                    message1_page112.setFont(font_page112)                    
                    message1_page112.setText("Проверьте свою удачу.")
                    message1_page112.exec_()

                    if self.player1.checking_luck():
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        message2_page112 = QMessageBox()
                        message2_page112.setWindowTitle("Параграф 112")
                        message2_page112.setFont(font_page112)                       
                        message2_page112.setText("Вам повезло. Вам удается оседлать коня Первого рыцаря, и ваша СИЛА УДАРА не изменяется")
                        message2_page112.exec_()
                        print("Битва с зеленым рыцарем")
                        self.player1.battleground_one("Зеленый рыцарь", 10, 10)
                        print("Игрок победил зеленого рыцаря")
                        self.strength_stamina_luck_information()
                    else:
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        message2_page112 = QMessageBox()
                        message2_page112.setWindowTitle("Параграф 112")
                        message2_page112.setFont(font_page112)                       
                        message2_page112.setText("Вам не повезло. Вы не смогли оседлать коня Первого рыцаря, придется драться, стоя на земле. (-1 к СИЛЕ УДАРА)")
                        message2_page112.exec_()
                        self.player1.strength -= 1
                        print("-1 к мастерству до окончания боя")
                        self.strength_stamina_luck_information()
                        print("Битва с зеленым рыцарем")
                        self.player1.battleground_one("Зеленый рыцарь", 10, 10)
                        print("Игрок победил зеленого рыцаря")
                        self.player1.strength += 1
                        print("+1 к мастерству, бой окончился")
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '414':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 113-----------------------------------
            elif self.page_number == 113:
                self.read_page_text()
                if self.ui.lineEdit.text() == '446' or self.ui.lineEdit.text() == '330' or self.ui.lineEdit.text() == '397':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 114-----------------------------------
            elif self.page_number == 114:
                self.read_page_text()                  
                self.page_you_lost(114)


            # --------------------------------параграф 115-----------------------------------
            elif self.page_number == 115:
                self.read_page_text()
                if self.ui.lineEdit.text() == '424':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 116-----------------------------------
            elif self.page_number == 116:
                self.read_page_text()
                if self.ui.lineEdit.text() == '16' or self.ui.lineEdit.text() == '416' or self.ui.lineEdit.text() == '4':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 117-----------------------------------
            elif self.page_number == 117:
                self.read_page_text()
                if self.ui.lineEdit.text() == '21' or self.ui.lineEdit.text() == '180' or self.ui.lineEdit.text() == '334':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 118-----------------------------------
            elif self.page_number == 118:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page118 = QMessageBox(self)
                    message_page118.setWindowTitle("Черный замок")
                    message_page118.setIconPixmap(QPixmap("GameText\Page118.png"))
                    message_page118.show()
                if self.ui.lineEdit.text() == '190' or self.ui.lineEdit.text() == '236':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '167':
                    magic_belt = Item("Волшебный пояс", "п.167")
                    if self.checking_bag_item(magic_belt) == True:
                        print("Использовать волшебный пояс")
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 119-----------------------------------
            elif self.page_number == 119:
                self.read_page_text()
                if self.ui.lineEdit.text() == '529' or self.ui.lineEdit.text() == '447':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 120-----------------------------------
            elif self.page_number == 120:
                self.read_page_text()
                if self.ui.lineEdit.text() == '433' or self.ui.lineEdit.text() == '227' or self.ui.lineEdit.text() == '416':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 121-----------------------------------
            elif self.page_number == 121:
                self.read_page_text()
                if self.ui.lineEdit.text() == '525' or self.ui.lineEdit.text() == '210':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 122-----------------------------------
            elif self.page_number == 122:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_122 = QMessageBox(self)
                    message_page_122.resize(1000, 1000)
                    message_page_122.setWindowTitle("Параграф 122")
                    name_of_opening_file_122 = "Page122.txt"
                    str_to_file_name_122 = Path("GameText", name_of_opening_file_122)
                    page_file_122 = open(str_to_file_name_122, "r")
                    message_page_122.setText(page_file_122.read())
                    font_message_122 = QFont()
                    font_message_122.setPointSize(14)
                    message_page_122.setFont(self.font_for_messageboxes)
                    message_page_122.exec_()
                    print(page_file_122.read())
                    page_file_122.close()
                if self.previous_page == 319:    
                    self.page_number = 48
                    self.ui.lineEdit.clear()
                    message2_page122 = QMessageBox()
                    message2_page122.setWindowTitle("------->>")
                    message2_page122.setText("Переход к параграфу 48")
                    message2_page122.setFont(font_message_122)
                    message2_page122.exec_()
                    print("Следующая страница = ", self.page_number)
                elif self.previous_page == 190:
                    self.page_number = 100
                    self.ui.lineEdit.clear()
                    print("Вы отправляетесь на параграф 100")
                    message2_page_122 = QMessageBox(self)
                    message2_page_122.resize(1000, 1000)
                    message2_page_122.setWindowTitle("--->")
                    message2_page_122.setText("Вы отправляетесь на параграф 100")
                    font_message2_122 = QFont()
                    font_message2_122.setPointSize(14)
                    message2_page_122.setFont(font_message2_122)
                    message2_page_122.exec_()
                    print("Следующая страница = ", self.page_number)


            # --------------------------------параграф 123-----------------------------------
            elif self.page_number == 123:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page123 = QMessageBox()
                        message1_page123.setWindowTitle("Параграф 123")
                        font_page123 = QFont()
                        font_page123.setPointSize(14)
                        message1_page123.setFont(font_page123)
                        message1_page123.setText("Хотите использовать заклинание копии?")
                        message1_page123.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m123 = message1_page123.exec_()
                        if m123 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ") 
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_123_3_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_123_3("Первый разбойник", 6, 4, "Второй разбойник", 7, 8, "Третий разбойник", 5, 5)
                            self.strength_stamina_luck_information()
                            print("Игрок победил разбойников")
                    else:                       
                        self.player1.battleground_123_3("Первый разбойник", 6, 4, "Второй разбойник", 7, 8, "Третий разбойник", 5, 5)
                        self.strength_stamina_luck_information()
                        print("Игрок победил разбойников")

                    print("Вы победили разбойников")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '46' or self.ui.lineEdit.text() == '335':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 124-----------------------------------
            elif self.page_number == 124:
                self.read_page_text()
                if self.ui.lineEdit.text() == '217' or self.ui.lineEdit.text() == '106' or self.ui.lineEdit.text() == '518':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '327':
                    if self.player1.gold >= 7:
                        self.player1.gold -= 7
                        print("-7 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас недостаточно золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number                       
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 125-----------------------------------
            elif self.page_number == 125:
                self.read_page_text()
                if self.ui.lineEdit.text() == '21' or self.ui.lineEdit.text() == '180' or self.ui.lineEdit.text() == '334':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 126-----------------------------------
            elif self.page_number == 126:
                self.read_page_text()
                if self.ui.lineEdit.text() == '434':
                    green_armor = Item("Зеленые латы", "+60")
                    self.add_item_and_print_console(green_armor)
                    self.add_item_to_table_widget(green_armor)
                    green_sword = Item("Меч зел.рыцаря", "-")
                    self.add_item_and_print_console(green_sword)
                    self.add_item_to_table_widget(green_sword)
                    print("Вы взяли меч зеленого рыцаря, +1 к мастерству")
                    self.player1.strength += 1
                    print("+1 мастерство")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 127-----------------------------------
            elif self.page_number == 127:
                self.read_page_text()
                if self.ui.lineEdit.text() == '225':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 128-----------------------------------
            elif self.page_number == 128:
                self.read_page_text()
                if self.ui.lineEdit.text() == '207':  
                    self.life_points_recovery(4)  
                    print("Восстановили 4 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 129-----------------------------------
            elif self.page_number == 129:
                self.read_page_text()
                if self.ui.lineEdit.text() == '184' or self.ui.lineEdit.text() == '223':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 130-----------------------------------
            elif self.page_number == 130:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 131-----------------------------------
            elif self.page_number == 131:
                self.read_page_text()
                if self.ui.lineEdit.text() == '305': 
                    self.life_points_recovery(6)  
                    self.strength_stamina_luck_information()
                    print("Вы восстановили 6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 132-----------------------------------
            elif self.page_number == 132:
                self.read_page_text()
                if self.ui.lineEdit.text() == '336' or self.ui.lineEdit.text() == '24':
                    self.life_points_recovery(6)
                    self.strength_stamina_luck_information()
                    print("Вы восстановили 6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 133-----------------------------------
            elif self.page_number == 133:
                self.read_page_text()
                if self.ui.lineEdit.text() == '225':    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 134-----------------------------------
            elif self.page_number == 134:
                self.read_page_text()
                if self.ui.lineEdit.text() == '454':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 135-----------------------------------
            elif self.page_number == 135:
                self.read_page_text()
                if self.ui.lineEdit.text() == '422' or self.ui.lineEdit.text() == '435':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 136-----------------------------------
            elif self.page_number == 136:
                self.read_page_text()
                if self.ui.lineEdit.text() == '337':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '397':
                    green_armor = Item("Зеленые латы", "+60")                           # +60 для надевания лат нужно прибавлять в коридоре
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 137-----------------------------------
            elif self.page_number == 137:
                self.read_page_text()
                if self.ui.lineEdit.text() == '458':
                    if self.player1.gold >= 3:
                        self.player1.gold -= 3
                        print("-3 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас недостаточно золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number
                elif self.ui.lineEdit.text() == '369':
                    if self.player1.gold >= 6:
                        self.player1.gold -= 6
                        print("-6 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас недостаточно золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number    
                elif self.ui.lineEdit.text() == '274':
                    if self.player1.gold >= 6:
                        self.player1.gold -= 6
                        print("-8 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас недостаточно золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()   
                        return self.page_number
                elif self.ui.lineEdit.text() == '522':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 138-----------------------------------
            elif self.page_number == 138:
                self.read_page_text()
                if self.ui.lineEdit.text() == '243' or self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 139-----------------------------------
            elif self.page_number == 139:
                self.read_page_text()
                if self.ui.lineEdit.text() == '530' or self.ui.lineEdit.text() == '471' or self.ui.lineEdit.text() == '268' or self.ui.lineEdit.text() == '80':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 140-----------------------------------
            elif self.page_number == 140:
                self.read_page_text()
                if self.ui.lineEdit.text() == '322':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 141-----------------------------------
            elif self.page_number == 141:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    print("-2 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 142-----------------------------------
            elif self.page_number == 142:
                self.read_page_text()
                if self.ui.lineEdit.text() == '443':
                    silver_whistle = Item("Серебряный свисток", "-")
                    if self.checking_bag_item(silver_whistle) == True:
                        if self.player1.gold >= 2:
                            self.player1.gold -= 2
                            self.gold_food_water_information()
                            print("-2 золотых")
                            # вычеркнуть серебряный свисток из списка при переходе на 443
                            self.delete_item(silver_whistle)
                            self.page_number = int(self.ui.lineEdit.text())
                            self.ui.lineEdit.clear()
                            print("Следующая страница = ", self.page_number)
                        else:
                            print("У вас недостаточно золота")
                            self.ui.lineEdit.clear()
                            self.not_enough_gold()
                            return self.page_number
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '106':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 143-----------------------------------
            elif self.page_number == 143:
                self.read_page_text()
                if self.ui.lineEdit.text() == '531':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 144-----------------------------------
            elif self.page_number == 144:
                self.read_page_text()
                if self.ui.lineEdit.text() == '465':
                    mirrors = Item("Секрет зеркал", "-13")
                    self.add_item_and_print_console(mirrors)
                    self.add_item_to_table_widget(mirrors)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 145-----------------------------------
            elif self.page_number == 145:
                self.read_page_text()
                if self.ui.lineEdit.text() == '525' or self.ui.lineEdit.text() == '188':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 146-----------------------------------
            elif self.page_number == 146:
                self.read_page_text()
                if self.ui.lineEdit.text() == '428':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 147-----------------------------------
            elif self.page_number == 147:
                self.read_page_text()
                if self.ui.lineEdit.text() == '348' or self.ui.lineEdit.text() == '537':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '460':
                    silver_whistle = Item("Серебряный свисток", "-")
                    if self.checking_bag_item(silver_whistle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 148-----------------------------------
            elif self.page_number == 148:
                self.read_page_text()
                if self.ui.lineEdit.text() == '464':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 149-----------------------------------
            elif self.page_number == 149:
                self.read_page_text()
                if self.ui.lineEdit.text() == '98':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # разгадка на загадку домика (про дракона)    
                elif self.ui.lineEdit.text() == '67':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 150-----------------------------------
            elif self.page_number == 150:
                self.read_page_text()
                if self.ui.lineEdit.text() == '269' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 151-----------------------------------
            elif self.page_number == 151:
                self.read_page_text()
                # возвращение на опушку сказочного леса, конец игры (всплывает сообщение)
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_151 = QMessageBox(self)
                    message_page_151.resize(1000, 1000)
                    message_page_151.setWindowTitle("Параграф 151")
                    font_151 = QFont()
                    font_151.setPointSize(14)
                    message_page_151.setFont(self.font_for_messageboxes)
                    name_of_opening_file_151 = "Page151.txt"
                    str_to_file_name_151 = Path("GameText", name_of_opening_file_151)
                    page_file_151 = open(str_to_file_name_151, "r")
                    message_page_151.setText(page_file_151.read())
                    message_page_151.exec_()
                    message_page_151.setText("Ну, хотя бы жив остался =))")
                    message_page_151.exec_()
                    print(page_file_151.read())
                    page_file_151.close()
                    self.player1.game_over = True
                    self.checking_game_over()


            # --------------------------------параграф 152-----------------------------------
            elif self.page_number == 152:
                self.read_page_text()
                if self.ui.lineEdit.text() == '472' or self.ui.lineEdit.text() == '275':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 153-----------------------------------
            elif self.page_number == 153:
                self.read_page_text()
                if self.ui.lineEdit.text() == '538':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ") == True:
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '370':
                    if self.player1.check_for_use_necessary_spell("ИЛЛЮЗИЯ") == True:
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ИЛЛЮЗИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 154-----------------------------------
            elif self.page_number == 154:
                self.read_page_text()
                if self.ui.lineEdit.text() == '559' or self.ui.lineEdit.text() == '181' or self.ui.lineEdit.text() == '445':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 155-----------------------------------
            elif self.page_number == 155:
                self.read_page_text()
                if self.ui.lineEdit.text() == '461' or self.ui.lineEdit.text() == '250':
                    self.player1.gold = self.player1.food = self.player1.water = 0
                    self.gold_food_water_information()
                    print("У вас ни золота, ни еды, ни воды")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 156-----------------------------------
            elif self.page_number == 156:
                self.read_page_text()
                if self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 157-----------------------------------
            elif self.page_number == 157:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_157 = QMessageBox(self)
                    message_page_157.resize(1000, 1000)
                    message_page_157.setWindowTitle("Параграф 157")
                    font_157 = QFont()
                    font_157.setPointSize(14)
                    message_page_157.setFont(self.font_for_messageboxes)
                    name_of_opening_file_157 = "Page157.txt"
                    str_to_file_name_157 = Path("GameText", name_of_opening_file_157)
                    page_file_157 = open(str_to_file_name_157, "r")
                    message_page_157.setText(page_file_157.read())
                    message_page_157.exec_()
                    print(page_file_157.read())
                    page_file_157.close()
                    self.player1.game_over = True
                    self.checking_game_over()


            # --------------------------------параграф 158-----------------------------------
            elif self.page_number == 158:
                self.read_page_text()
                if self.ui.lineEdit.text() == '484':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 159-----------------------------------
            elif self.page_number == 159:
                self.read_page_text()
                if self.ui.lineEdit.text() == '540' or self.ui.lineEdit.text() == '380' or self.ui.lineEdit.text() == '39':
                    # сундук ударил по рукам, потеря 1 мастерства и 2 ед. выносливости
                    self.player1.strength -= 1
                    self.losing_life_points(2)
                    print("-1 мастерство и -2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 160-----------------------------------
            elif self.page_number == 160:
                self.read_page_text()
                if self.ui.lineEdit.text() == '371' or self.ui.lineEdit.text() == '276':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # п. 135 появляется, если у игрока есть информация "Трое из Эвенло" (-25), в игре есть несоответствие, которое, возможно, устранено
                # в следующих изданиях: фактически к этому параграфу прийти невозможно, т.к. взяв "Трое из Эвенло", невозможно прийти к этому старику в темницу
                # (изъян в сценарии книги)  
                elif self.ui.lineEdit.text() == '135':
                    three_from_evenlo = Item("'Трое из Эвенло'", "-25")
                    if self.checking_bag_item(three_from_evenlo) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 161-----------------------------------
            elif self.page_number == 161:
                self.read_page_text()
                if self.ui.lineEdit.text() == '316':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 162-----------------------------------
            elif self.page_number == 162:
                self.read_page_text()
                if self.ui.lineEdit.text() == '611' or self.ui.lineEdit.text() == '76':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 163-----------------------------------
            elif self.page_number == 163:
                self.read_page_text()
                # загадка идет с п.95
                if self.ui.lineEdit.text() == '98':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 164-----------------------------------
            elif self.page_number == 164:
                self.read_page_text()
                # заклинание Силы вычеркивается на п.341
                if self.ui.lineEdit.text() == '487':                                         # просмотреть использование Силы на п.487 в битвы с орками
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 165-----------------------------------
            elif self.page_number == 165:
                self.read_page_text()
                if self.ui.lineEdit.text() == '560' or self.ui.lineEdit.text() == '288' or self.ui.lineEdit.text() == '493':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # п.152 появляется, если игроку известен секрет зеркал (-13)    
                elif self.ui.lineEdit.text() == '152':
                    mirrors = Item("Секрет зеркал", "-13")
                    if self.checking_bag_item(mirrors) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 166-----------------------------------
            elif self.page_number == 166:
                self.read_page_text()
                if self.ui.lineEdit.text() == '350':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 167-----------------------------------
            elif self.page_number == 167:
                self.read_page_text()
                if self.ui.lineEdit.text() == '100':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 168-----------------------------------
            elif self.page_number == 168:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 169-----------------------------------
            elif self.page_number == 169:
                self.read_page_text()
                if self.ui.lineEdit.text() == '612' or self.ui.lineEdit.text() == '560' or self.ui.lineEdit.text() == '288' or self.ui.lineEdit.text() == '165':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '617':
                    if self.player1.princess_is_saved == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        print("Принцесса еще не спасена!")
                        message_page_169 = QMessageBox(self)
                        message_page_169.resize(1000, 1000)
                        font_169 = QFont()
                        font_169.setPointSize(14)
                        message_page_169.setFont(font_169)
                        message_page_169.setText("Принцесса еще не разбужена!\nПожалуйста, выберите другой параграф!")
                        message_page_169.exec_()
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 170-----------------------------------
            elif self.page_number == 170:
                self.read_page_text()
                # применение Оберега с п.301
                if self.ui.lineEdit.text() == '594' or self.ui.lineEdit.text() == '599':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 171-----------------------------------
            elif self.page_number == 171:
                self.read_page_text()
                # использование Флакончика ДухОв с п.394
                if self.ui.lineEdit.text() == '301':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 172-----------------------------------
            elif self.page_number == 172:
                self.read_page_text()
                if self.ui.lineEdit.text() == '347':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 173-----------------------------------
            elif self.page_number == 173:
                self.read_page_text()
                if self.ui.lineEdit.text() == '379':
                    self.life_points_recovery(2)
                    print("+2 к выносливости (поели суп из котла)")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 174-----------------------------------
            elif self.page_number == 174:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_174 = QMessageBox(self)
                    message_page_174.resize(1000, 1000)
                    message_page_174.setWindowTitle("Параграф 174")
                    font_174 = QFont()
                    font_174.setPointSize(14)
                    message_page_174.setFont(self.font_for_messageboxes)
                    name_of_opening_file_174 = "Page174.txt"
                    str_to_file_name_174 = Path("GameText", name_of_opening_file_174)
                    page_file_174 = open(str_to_file_name_174, "r")
                    message_page_174.setText(page_file_174.read())
                    message_page_174.exec_()
                    print(page_file_174.read())
                    page_file_174.close()
                    self.player1.game_over = True
                    self.checking_game_over()


            # --------------------------------параграф 175-----------------------------------
            elif self.page_number == 175:
                self.read_page_text()
                if self.ui.lineEdit.text() == '52':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 176-----------------------------------
            elif self.page_number == 176:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.open_window_176()
                if self.ui.lineEdit.text() == '106' or self.ui.lineEdit.text() == '213':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number  


            # --------------------------------параграф 177-----------------------------------
            elif self.page_number == 177:  
                self.read_page_text()
                self.page_you_lost(177)


            # --------------------------------параграф 178-----------------------------------
            elif self.page_number == 178:
                self.read_page_text()
                if self.ui.lineEdit.text() == '406':
                    self.life_points_recovery(6)
                    print("+6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 179-----------------------------------
            elif self.page_number == 179:
                self.read_page_text()
                if self.ui.lineEdit.text() == '99' or self.ui.lineEdit.text() == '377':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 180-----------------------------------
            elif self.page_number == 180:
                self.read_page_text()
                if self.ui.lineEdit.text() == '400':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 181-----------------------------------
            elif self.page_number == 181:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page181 = QMessageBox(self)
                    message_page181.setWindowTitle("Разбойники")
                    message_page181.setIconPixmap(QPixmap("GameText\Page181.png"))
                    message_page181.show()
                if self.ui.lineEdit.text() == '123' or self.ui.lineEdit.text() == '17':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 182-----------------------------------
            elif self.page_number == 182:
                self.read_page_text()
                if (self.ui.lineEdit.text() == '25' or self.ui.lineEdit.text() == '224' or self.ui.lineEdit.text() == '22'
                       or self.ui.lineEdit.text() == '427' or self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206'
                       or self.ui.lineEdit.text() == '350'):
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 183-----------------------------------
            elif self.page_number == 183:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0
                    message_page183 = QMessageBox()
                    message_page183.setWindowTitle("Параграф 183")
                    font_page183 = QFont()
                    font_page183.setPointSize(14)
                    message_page183.setFont(self.font_for_messageboxes)
                    text_page183 = "Вам придется не только драться сразу с обоими Зелеными рыцарями, "
                    text_page183 += "но и вычитать 1 из своей СИЛЫ УДАРА, поскольку вы стоите на земле, а они атакуют вас сверху, с коней."
                    message_page183.setText(text_page183)
                    message_page183.exec_()
            
                    print("Битва с двумя зелеными рыцарями")
                    self.player1.strength -= 1
                    print("-1 к мастерству, игрок стоит на земле, а противники на конях")
                    self.strength_stamina_luck_information()
                    if self.player1.strength_spell == True:
                        self.player1.strength += 2
                        self.strength_stamina_luck_information()
                    self.player1.battleground_two("Первый зеленый рыцарь", 10, 10, "Второй зеленый рыцарь", 10, 10)
                    print("Битва окончена, игрок победил")
                    self.player1.strength += 1
                    print("+1 к мастерству, бой окончен")
                    self.strength_stamina_luck_information()
                    if self.player1.strength_spell == True:
                        self.player1.strength_spell = False
                        self.player1.strength -= 2
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '436':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 184-----------------------------------
            elif self.page_number == 184:
                self.read_page_text()
                if self.ui.lineEdit.text() == '235' or self.ui.lineEdit.text() == '351' or self.ui.lineEdit.text() == '448' or self.ui.lineEdit.text() == '526':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 185-----------------------------------
            elif self.page_number == 185:
                self.read_page_text()
                if self.ui.lineEdit.text() == '329' or self.ui.lineEdit.text() == '432' or self.ui.lineEdit.text() == '20':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 186-----------------------------------
            elif self.page_number == 186:
                self.read_page_text()
                if self.ui.lineEdit.text() == '456':
                    if self.player1.gold >= 2:
                        self.player1.gold -= 2
                        print("-2 зототых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет столько золота")
                        self.ui.lineEdit.clear()
                        self.not_enough_gold()
                        return self.page_number
                elif self.ui.lineEdit.text() == '229':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 187-----------------------------------
            elif self.page_number == 187:
                self.read_page_text()
                if self.ui.lineEdit.text() == '47':
                    two_birch_trees = Item("'Две берёзы'", "+140")
                    # удаляем информацию о кладе
                    self.delete_item(two_birch_trees)
                    self.player1.gold += 10
                    print("+10 золотых")
                    self.gold_food_water_information()
                    silver_ring = Item("Серебряное кольцо", "-")
                    self.add_item_and_print_console(silver_ring)
                    self.add_item_to_table_widget(silver_ring)
                    lamp = Item("Светильник", "+10")
                    self.add_item_and_print_console(lamp)
                    self.add_item_to_table_widget(lamp)
                    self.player1.luck += 1
                    print("+1 к удаче")
                    self.strength_stamina_luck_information()
                    self.page_187_visited = True
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 188-----------------------------------
            elif self.page_number == 188:
                self.read_page_text()
                if self.ui.lineEdit.text() == '184' or self.ui.lineEdit.text() == '235':
                    self.losing_life_points(1)
                    print("-1 к выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 189-----------------------------------
            elif self.page_number == 189:
                self.read_page_text()
                if self.ui.lineEdit.text() == '19':
                    self.player1.gold += 1
                    print("+1 золотой")
                    self.gold_food_water_information()
                    diamond = Item("Бриллиант", "-")
                    self.add_item_and_print_console(diamond)
                    self.add_item_to_table_widget(diamond)
                    gold_whistle = Item("Золотой свисток", "-")
                    self.add_item_and_print_console(gold_whistle)
                    self.add_item_to_table_widget(gold_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 190-----------------------------------
            elif self.page_number == 190:
                self.read_page_text()
                if self.ui.lineEdit.text() == '245' or self.ui.lineEdit.text() == '449' or self.ui.lineEdit.text() == '26' or self.ui.lineEdit.text() == '341':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '122':
                    password_122 = Item("Пароль-122", "п.122")
                    if self.checking_bag_item(password_122) == True:
                        self.previous_page = 190
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("У вас нет данного предмета")
                        message_no_item_in_bag = QMessageBox()
                        message_no_item_in_bag.setWindowTitle(":-(")
                        message_no_item_in_bag.setText("Вы не знаете пароля")
                        font_not_enough_gold = QFont()
                        font_not_enough_gold.setPointSize(14)
                        message_no_item_in_bag.setFont(font_not_enough_gold)
                        message_no_item_in_bag.exec_()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 191-----------------------------------
            elif self.page_number == 191:
                self.read_page_text()
                if self.ui.lineEdit.text() == '532':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '251':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '592':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 192-----------------------------------
            elif self.page_number == 192:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с гоблином")
                    message1_page192 = QMessageBox()
                    message1_page192.setWindowTitle("Параграф 192")
                    text_page192 = ""
                    text_page192 += "Берег охраняется: как только вы достигаете его, из кустов выскакивает Гоблин и, размахивая саблей, бросается на вас."
                    text_page192 += "Воспользоваться заклятиями уже не успеваете."                  
                    message1_page192.setText(text_page192)
                    font1_page192 = QFont()
                    font1_page192.setPointSize(14)
                    message1_page192.setFont(self.font_for_messageboxes)
                    message1_page192.exec_()
                    self.player1.battle_text = ""
                    self.player1.battleground_one("Гоблин", 7, 9)
                    self.strength_stamina_luck_information()
                    print("Игрок победил в бою с гоблином")

                if self.ui.lineEdit.text() == '437':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    self.add_item_and_print_console(bronze_whistle)
                    self.add_item_to_table_widget(bronze_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 193-----------------------------------
            elif self.page_number == 193:
                self.read_page_text()
                if self.ui.lineEdit.text() == '230' or self.ui.lineEdit.text() == '352':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '203':
                    lamp = Item("Светильник", "+10")
                    candle = Item("Свеча", "+10")
                    if self.checking_bag_item(lamp) == True or self.checking_bag_item(candle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()  
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 194-----------------------------------
            elif self.page_number == 194:
                self.read_page_text()              
                if self.ui.lineEdit.text() == '27':
                    peacock_feather = Item("Перо павлина", "-")
                    if self.checking_bag_item(peacock_feather) == True:
                        # удалить перо павлина из инвентаря
                        self.delete_item(peacock_feather)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '270':
                    silver_bracelet = Item("Серебряный браслет", "-")
                    if self.checking_bag_item(silver_bracelet) == True:
                        # удалить серебряный браслет из инвентаря
                        self.delete_item(silver_bracelet)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '533':
                    white_arrow = Item("Белая стрела", "-")
                    if self.checking_bag_item(white_arrow) == True:
                        # удалить белую стрелу из инвентаря
                        self.delete_item(white_arrow)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '137' or self.ui.lineEdit.text() == '522':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 195-----------------------------------
            elif self.page_number == 195:
                self.read_page_text()
                self.page_you_lost(195)


            # --------------------------------параграф 196-----------------------------------
            elif self.page_number == 196:
                self.read_page_text()
                if self.ui.lineEdit.text() == '560' or self.ui.lineEdit.text() == '288' or self.ui.lineEdit.text() == '165':
                    # перстень будет добавлен в инвентарь после ввода одного из параграфов
                    ring_with_ruby = Item("Перстень с рубином", "+49")
                    self.add_item_and_print_console(ring_with_ruby)
                    self.add_item_to_table_widget(ring_with_ruby)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 197-----------------------------------
            elif self.page_number == 197:
                self.read_page_text()
                if self.ui.lineEdit.text() == '434':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 198-----------------------------------
            elif self.page_number == 198:
                self.read_page_text()
                if self.ui.lineEdit.text() == '346':
                    self.losing_life_points(2)
                    print("-2 к выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 199-----------------------------------
            elif self.page_number == 199:
                self.read_page_text()
                if self.ui.lineEdit.text() == '107' or self.ui.lineEdit.text() == '304':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 200-----------------------------------
            elif self.page_number == 200:
                self.read_page_text()
                if self.ui.lineEdit.text() == '318' or self.ui.lineEdit.text() == '193':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 201-----------------------------------
            elif self.page_number == 201:
                self.read_page_text()
                if self.ui.lineEdit.text() == '192':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 202-----------------------------------
            elif self.page_number == 202:
                self.read_page_text()
                if self.ui.lineEdit.text() == '186' or self.ui.lineEdit.text() == '229':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 203-----------------------------------
            elif self.page_number == 203:
                self.read_page_text()
                if self.ui.lineEdit.text() == '440' or self.ui.lineEdit.text() == '140':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 204-----------------------------------
            elif self.page_number == 204:
                self.read_page_text()
                if self.ui.lineEdit.text() == '353':
                    self.life_points_recovery(3)
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 205-----------------------------------
            elif self.page_number == 205:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':
                    self.player1.strength -= 1
                    self.losing_life_points(3)
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 206-----------------------------------
            elif self.page_number == 206:
                self.read_page_text()
                # чтобы выбраться из западни, нужен металлический ключ или кольцо с бриллиантом (-40), всё описано!
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    metal_key = Item("Метал.ключ", "-40")
                    ring_with_diamond = Item("Кольцо с брил.", "-40")
                    if self.checking_bag_item(metal_key) or self.checking_bag_item(ring_with_diamond):
                        message_page206 = QMessageBox()
                        message_page206.setWindowTitle("Параграф 206")
                        message_page206.setText("У вас нет данного предмета")
                        font_page206 = QFont()
                        font_page206.setPointSize(14)
                        name_of_opening_file_206 = "Page" + str(self.page_number) + ".txt"
                        str_to_file_name_206 = Path("GameText", name_of_opening_file_206)
                        page_file_206 = open(str_to_file_name_206, "r")
                        message_page206.setText(page_file_206.read())
                        message_page206.setFont(self.font_for_messageboxes)
                        page_file_206.close()
                        message_page206.exec_()
                        message2_page206 = QMessageBox()
                        message2_page206.setWindowTitle("------->>")
                        message2_page206.setText("Переход к параграфу 166")
                        message2_page206.setFont(font_page206)
                        message2_page206.exec_()
                        self.ui.lineEdit.clear()
                        self.page_number = 166
                        print("Next Page = ", self.page_number)
                    else:
                        self.page_you_lost(206)


            # --------------------------------параграф 207-----------------------------------
            elif self.page_number == 207:
                self.read_page_text()
                if self.ui.lineEdit.text() == '544':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 208-----------------------------------
            elif self.page_number == 208:
                self.read_page_text()
                if self.ui.lineEdit.text() == '141':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 209-----------------------------------
            elif self.page_number == 209:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page209 = QMessageBox()
                    font_page209 = QFont()
                    font_page209.setPointSize(14)
                    message_page209.setFont(font_page209)
                    message_page209.setWindowTitle("Покупка рыбы")
                    message_page209.setText("Хотите купить рыбу?")
                    message_page209.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m209 = message_page209.exec_()
                    if m209 == QMessageBox.Yes:
                        message2_page209 = QMessageBox()
                        message2_page209.setFont(font_page209)
                        message_page209.setWindowTitle("Покупка рыбы")
                        message2_page209.setText("Сколько рыбы вам нужно?\n1 штука = 1 золотой = +2 к выносливости")
                        spinbox_page209 = QSpinBox(message2_page209)
                        spinbox_page209.setRange(0, 10)
                        spinbox_page209.move(150, 80)                   # closeEvent для второго messagebox
                        message2_page209.exec_()
                        if self.player1.gold - spinbox_page209.value() < 0:
                            print("Недостаточно золота")
                            self.not_enough_gold()
                            return self.page_number
                        else:
                            self.player1.gold -= spinbox_page209.value()
                            self.gold_food_water_information()
                            for i in range(0, spinbox_page209.value(), 1):
                                fish = Item("Рыба", "+2 к выносл.")
                                self.add_item_and_print_console(fish)
                                self.add_item_to_table_widget(fish)
                            print("Вы купили " + str(spinbox_page209.value()) + " штук")        
                        if self.ui.lineEdit.text() == '332':
                            self.page_number = int(self.ui.lineEdit.text())
                            self.ui.lineEdit.clear()
                            print("Следующая страница = ", self.page_number)                   
                        else:
                            if self.ui.lineEdit.text() != "":
                                self.warning_wrong_page_number()
                                self.ui.lineEdit.clear()
                                return self.page_number
                            else:
                                print("Введите номер страницы")
                                return self.page_number
                    else:
                        if self.ui.lineEdit.text() == '332':
                            self.page_number = int(self.ui.lineEdit.text())
                            self.ui.lineEdit.clear()
                            print("Следующая страница = ", self.page_number)                   
                        else:
                            if self.ui.lineEdit.text() != "":
                                self.warning_wrong_page_number()
                                self.ui.lineEdit.clear()
                                return self.page_number
                            else:
                                print("Введите номер страницы")
                                return self.page_number
                if self.ui.lineEdit.text() == '332':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 210-----------------------------------
            elif self.page_number == 210:
                self.read_page_text()
                if self.ui.lineEdit.text() == '462':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 211-----------------------------------
            elif self.page_number == 211:
                self.read_page_text()
                if self.ui.lineEdit.text() == '423':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '313':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ") == True:
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '9':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ") == True:
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 212-----------------------------------
            elif self.page_number == 212:
                self.read_page_text()
                if self.ui.lineEdit.text() == '177':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '5':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ") == True:
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '105':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ") == True:
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number            
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 213-----------------------------------
            elif self.page_number == 213:
                self.read_page_text()
                if self.ui.lineEdit.text() == '18' or self.ui.lineEdit.text() == '124' or self.ui.lineEdit.text() == '23' or self.ui.lineEdit.text() == '438':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 214-----------------------------------
            elif self.page_number == 214:
                self.read_page_text()
                if self.ui.lineEdit.text() == '401' or self.ui.lineEdit.text() == '378':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 215-----------------------------------
            elif self.page_number == 215:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с обезьяной")
                    message1_page215 = QMessageBox()
                    message1_page215.setWindowTitle("Параграф 215")
                    text_page215 = ""
                    text_page215 += "Обезьяна угрожающе рычит и надвигается на вас. Вы выбираете бой."                  
                    message1_page215.setText(text_page215)
                    font1_page215 = QFont()
                    font1_page215.setPointSize(14)
                    message1_page215.setFont(font1_page215)
                    message1_page215.exec_()
                    self.player1.battle_text = ""
                    self.player1.battleground_one("Обезьяна", 9, 14)
                    self.strength_stamina_luck_information()
                    print("Игрок победил обезьяну")

                if self.ui.lineEdit.text() == '408':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 216-----------------------------------
            elif self.page_number == 216:
                self.read_page_text()
                if self.ui.lineEdit.text() == '132':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 217-----------------------------------
            elif self.page_number == 217:
                self.read_page_text()
                if self.ui.lineEdit.text() == '106':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '354': 
                    white_arrow = Item("Белая стрела", "-")
                    if self.checking_bag_item(white_arrow) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '28':
                    diamond = Item("Бриллиант", "-")
                    if self.checking_bag_item(diamond) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '142':
                    silver_whistle = Item("Серебряный свисток", "-")
                    if self.checking_bag_item(silver_whistle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 218-----------------------------------
            elif self.page_number == 218:
                self.read_page_text()
                message_luck = QMessageBox()
                message_luck.setWindowTitle("Удача")
                message_luck.setText("Проверьте свою удачу")
                font_luck = QFont()
                font_luck.setPointSize(14)
                message_luck.setFont(font_luck)
                message_luck.exec_()
                self.ui.lineEdit.clear()
                if self.player1.checking_luck() == True:
                    self.page_number = 463
                    self.player1.luck -= 1
                    print("-1 удача")
                    self.strength_stamina_luck_information()
                    message_luck = QMessageBox()
                    message_luck.setWindowTitle("------->>")
                    message_luck.setText("Переход к параграфу 463")
                    font_luck = QFont()
                    font_luck.setPointSize(14)
                    message_luck.setFont(font_luck)
                    message_luck.exec_()
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)
                else:
                    self.page_number = 539
                    self.player1.luck -= 1
                    print("-1 удача")
                    self.strength_stamina_luck_information()
                    message_luck = QMessageBox()
                    message_luck.setWindowTitle("------->>")
                    message_luck.setText("Переход к параграфу 539")
                    font_luck = QFont()
                    font_luck.setPointSize(14)
                    message_luck.setFont(font_luck)
                    message_luck.exec_()
                    self.ui.lineEdit.clear()
                    print("Next Page = ", self.page_number)


            # --------------------------------параграф 219-----------------------------------
            elif self.page_number == 219:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    # -1 к мастреству, т.к. сражение на дереве
                    self.player1.strength -= 1
                    self.strength_stamina_luck_information()

                    print("Битва с пауком")
                    self.player1.battleground_one("Паук", 5, 8)
                    print("Конец битвы с пауком")

                    # возвращаем на место показатель мастерства после боя
                    self.player1.strength += 1
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '189':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 220-----------------------------------
            elif self.page_number == 220:
                self.read_page_text()
                if self.ui.lineEdit.text() == '548' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 221-----------------------------------
            elif self.page_number == 221:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    # рисунок старичка
                    message_page_221 = QMessageBox(self)
                    message_page_221.setWindowTitle("Старый охотник")
                    message_page_221.setIconPixmap(QPixmap("GameText\Page221.png"))
                    message_page_221.show()
                if self.ui.lineEdit.text() == '535' or self.ui.lineEdit.text() == '148' or self.ui.lineEdit.text() == '464' or self.ui.lineEdit.text() == '55':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 222-----------------------------------
            elif self.page_number == 222:
                self.read_page_text()
                if self.ui.lineEdit.text() == '190' or self.ui.lineEdit.text() == '236':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '167':
                    magic_belt = Item("Волшебный пояс", "п.167")
                    if self.checking_bag_item(magic_belt) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 223-----------------------------------
            elif self.page_number == 223:
                self.read_page_text()
                if self.ui.lineEdit.text() == '2' or self.ui.lineEdit.text() == '184' or self.ui.lineEdit.text() == '29':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 224-----------------------------------
            elif self.page_number == 224:
                self.read_page_text()
                if (self.ui.lineEdit.text() == '491' or self.ui.lineEdit.text() == '427' or 
                        self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206' or self.ui.lineEdit.text() == '350'):
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 225-----------------------------------
            elif self.page_number == 225:
                self.read_page_text()
                if self.ui.lineEdit.text() == '465':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '144':
                    deer_skin = Item("Шкура оленя", "-")
                    if self.checking_bag_item(deer_skin) == True:
                        # удалить шкуру оленя из инвентаря
                        self.delete_item(deer_skin)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 226-----------------------------------
            elif self.page_number == 226:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 227-----------------------------------
            elif self.page_number == 227:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '63':
                    copper_key = Item("Медный ключик", "-")
                    if self.checking_bag_item(copper_key) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '150':
                    piece_of_metal = Item("Кусок металла", "-")
                    if self.checking_bag_item(piece_of_metal) == True:
                        # удалить кусок металла из инвентаря
                        self.delete_item(piece_of_metal)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '473':
                    figure_key = Item("Фигурный ключ", "-")
                    if self.checking_bag_item(figure_key) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 228-----------------------------------
            elif self.page_number == 228:
                self.read_page_text()
                if self.ui.lineEdit.text() == '332' or self.ui.lineEdit.text() == '561':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 229-----------------------------------
            elif self.page_number == 229:
                self.read_page_text()
                if self.ui.lineEdit.text() == '180' or self.ui.lineEdit.text() == '334':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 230-----------------------------------
            elif self.page_number == 230:
                self.read_page_text()
                if self.ui.lineEdit.text() == '549' or self.ui.lineEdit.text() == '466':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 231-----------------------------------
            elif self.page_number == 231:
                self.read_page_text()
                if self.ui.lineEdit.text() == '406':
                    self.losing_life_points(1)
                    print("-1 к выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 232-----------------------------------
            elif self.page_number == 232:
                self.read_page_text()
                if self.ui.lineEdit.text() == '319':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # потайная дверца в замок (п.260), секрет дается старым охотником (на п.464)   
                elif self.ui.lineEdit.text() == '260':
                    secret_door = Item("Потайная дверца", "п.260")                   
                    if self.checking_bag_item(secret_door):
                        # удаляем информацию о секретной дверце 
                        self.delete_item(secret_door)          
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 233-----------------------------------
            elif self.page_number == 233:
                self.read_page_text()
                self.page_you_lost(233)


            # --------------------------------параграф 234-----------------------------------
            elif self.page_number == 234:
                self.read_page_text()
                if self.ui.lineEdit.text() == '47' or self.ui.lineEdit.text() == '82':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 235-----------------------------------
            elif self.page_number == 235:
                self.read_page_text()
                if self.ui.lineEdit.text() == '102':
                    self.losing_life_points(1)
                    print("-1 выносливость")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 236-----------------------------------
            elif self.page_number == 236:
                self.read_page_text()
                if self.ui.lineEdit.text() == '331':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif  self.ui.lineEdit.text() == '87': 
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")                    
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 237-----------------------------------
            elif self.page_number == 237:
                self.read_page_text()
                if self.ui.lineEdit.text() == '108' or self.ui.lineEdit.text() == '407':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 238-----------------------------------
            elif self.page_number == 238:
                self.read_page_text()
                if self.ui.lineEdit.text() == '99' or self.ui.lineEdit.text() == '531':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 239-----------------------------------
            elif self.page_number == 239:
                self.read_page_text()
                if self.ui.lineEdit.text() == '531' or self.ui.lineEdit.text() == '64':
                    self.life_points_recovery(3)
                    print("+3 к выносливости")
                    self.strength_stamina_luck_information()
                    self.player1.food += 2
                    print("+2 еды")
                    self.gold_food_water_information()
                    silver_whistle = Item("Серебряный свисток", "-")
                    self.add_item_and_print_console(silver_whistle)
                    self.add_item_to_table_widget(silver_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 240-----------------------------------
            elif self.page_number == 240:
                self.read_page_text()
                if self.ui.lineEdit.text() == '462' or self.ui.lineEdit.text() == '145':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 241-----------------------------------
            elif self.page_number == 241:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_princess_image = QMessageBox(self)
                    message_princess_image.setWindowTitle("Принцесса")
                    message_princess_image.setIconPixmap(QPixmap("GameText\Page241.png"))
                    message_princess_image.show()
                if self.ui.lineEdit.text() == '485':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 242-----------------------------------
            elif self.page_number == 242:
                self.read_page_text()
                if self.ui.lineEdit.text() == '123':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 243-----------------------------------
            elif self.page_number == 243:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с призраком")
                    self.player1.battleground()
                    message1_page243 = QMessageBox()
                    message1_page243.setWindowTitle("Параграф 243")
                    text_page243 = ""
                    text_page243 += "Вы входите в комнату. Как только переступаете порог, одежда на вешалке начинает шевелиться,"  
                    text_page243 += " и через несколько секунд появляется кошмарный Призрак."
                    text_page243 += "Он похож на живого мертвеца: остекленевшие глаза, бессмысленное лицо, рот, из которого вывалились все зубы,"
                    text_page243 += "а синий распухший язык высунут наружу. Он идет на вас безоружный, но его правая рука рассекает воздух как меч."
                    text_page243 += "Придется драться с ним. Заклятия не помогут — Призрак не боится их."
                    message1_page243.setText(text_page243)
                    font1_page243 = QFont()
                    font1_page243.setPointSize(14)
                    message1_page243.setFont(self.font_for_messageboxes)
                    message1_page243.exec_()
                    self.player1.battle_text = ""
                    self.player1.battleground_one("Призрак", 10, 9)
                    self.strength_stamina_luck_information()
                    print("Игрок победил призрака")

                if self.ui.lineEdit.text() == '39' or self.ui.lineEdit.text() == '474' or self.ui.lineEdit.text() == '540' or self.ui.lineEdit.text() == '380':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 244-----------------------------------
            elif self.page_number == 244:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    print("Бой с пауком")
                    message2_page244 = QMessageBox()
                    message2_page244.setWindowTitle("Параграф 244")
                    text_page244 = ""
                    text_page244 += "Решив не доверять подозрительным лесным указателям, вы сворачиваете налево," 
                    text_page244 += "но уже через несколько метров Можете пожалеть о своем выборе. С быстротой молнии откуда-то сверху"
                    text_page244 += "на вас набрасывается гигантский паук. Наложить какое-либо заклятие, кроме заклятия Копии, уже некогда."
                    text_page244 += "Можете, если хотите воспользоваться им — бой предстоит нелегкий."                 
                    message2_page244.setText(text_page244)
                    font1_page244 = QFont()
                    font1_page244.setPointSize(14)
                    message2_page244.setFont(self.font_for_messageboxes)
                    message2_page244.exec_()
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page244 = QMessageBox()
                        message1_page244.setWindowTitle("Параграф 244")
                        font_page244 = QFont()
                        font_page244.setPointSize(14)
                        message1_page244.setFont(font1_page244)
                        message1_page244.setText("Хотите использовать заклинание копии?")
                        message1_page244.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m244 = message1_page244.exec_()
                        if m244 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_one_copy_spell("Паук", 8, 8)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_one("Паук", 8, 8)
                            self.strength_stamina_luck_information()
                            print("Игрок победил паука")
                    else:                       
                        self.player1.battleground_one("Паук", 8, 8)
                        self.strength_stamina_luck_information()
                        print("Игрок победил паука")

                if self.ui.lineEdit.text() == '19':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 245-----------------------------------
            elif self.page_number == 245:
                self.read_page_text()
                if self.ui.lineEdit.text() == '341':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '100':
                    fox_fur = Item("Шкура лисы", "-")
                    if self.checking_bag_item(fox_fur) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 246-----------------------------------
            elif self.page_number == 246:
                self.read_page_text()
                if self.ui.lineEdit.text() == '550' or self.ui.lineEdit.text() == '39':
                    paper_pass = Item("Пропуск", "+20")
                    self.add_item_and_print_console(paper_pass)
                    self.add_item_to_table_widget(paper_pass)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 247-----------------------------------
            elif self.page_number == 247:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page247 = QMessageBox()
                    message_page247.setWindowTitle("Параграф 247")
                    font_page247 = QFont()
                    font_page247.setPointSize(14)
                    message_page247.setFont(font_page247)
                    message_page247.setText("Вы можете попытаться убежать")
                    message_page247.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m247 = message_page247.exec_()
                    if m247 == QMessageBox.Yes:
                        message_page83 = QMessageBox()
                        message_page83.setWindowTitle("Параграф 83")
                        message_page83.setFont(self.font_for_messageboxes)
                        text83 = ""
                        text83 += "Вы пытаетесь отступить назад и захлопнуть дверь, но скелет не дает вам это сделать."
                        text83 += "Несмотря на то, что он только ранил вас, когда вы повернулись к нему спиной (потеряйте 2 ВЫНОСЛИВОСТИ),"
                        text83 += "бегство не удалось. Вам придется вернуться на 247 и сразиться с ним."                       
                        message_page83.setText(text83)
                        message_page83.exec_()
                        self.losing_life_points(2)
                        print("-2 выносливости")
                        self.strength_stamina_luck_information()
                        message2_page83 = QMessageBox()
                        message2_page83.setWindowTitle("-------->>")
                        message2_page83.setFont(font_page247)
                        message_page83.setText("Переход обратно к параграфу 247")
                        message_page83.exec_()
                        print("Бой с духом мертвых")
                        self.player1.battleground_one("Дух мертвых", 10, 12)
                        print("Игрок победил духа мертвых")
                        self.strength_stamina_luck_information()
                    else:
                        print("Бой с духом мертвых")
                        self.player1.battleground_one("Дух мертвых", 10, 12)
                        print("Игрок победил духа мертвых")
                        self.strength_stamina_luck_information()
                if self.ui.lineEdit.text() == '381':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 248-----------------------------------
            elif self.page_number == 248:
                self.read_page_text()
                self.page_you_lost(248)


            #--------------------------------параграф 249-----------------------------------
            elif self.page_number == 249:
                self.read_page_text()
                if self.ui.lineEdit.text() == '562' or self.ui.lineEdit.text() == '315':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 250-----------------------------------
            elif self.page_number == 250:
                self.read_page_text()
                if self.ui.lineEdit.text() == '33':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 251-----------------------------------
            elif self.page_number == 251:
                self.read_page_text()
                if self.ui.lineEdit.text() == '191':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 252-----------------------------------
            elif self.page_number == 252:
                self.read_page_text()
                if self.ui.lineEdit.text() == '494':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '564':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())                      
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear() 
                        return self.page_number
                elif self.ui.lineEdit.text() == '541':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())                      
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear() 
                        return self.page_number
                # параграф, где добывается меч рыцаря ------>> 126 !        
                elif self.ui.lineEdit.text() == '364':
                    green_sword = Item("Меч зел.рыцаря", "-")
                    if self.checking_bag_item(green_sword) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '272':
                    paper_pass = Item("Пропуск", "+20")
                    if self.checking_bag_item(paper_pass) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 253-----------------------------------
            elif self.page_number == 253:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    print("-2 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 254-----------------------------------
            elif self.page_number == 254:
                self.read_page_text()
                if self.ui.lineEdit.text() == '366':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 255-----------------------------------
            elif self.page_number == 255:
                self.read_page_text()
                if self.ui.lineEdit.text() == '551' or self.ui.lineEdit.text() == '198':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '79':
                    if self.player1.gold >= 1:
                        self.player1.gold -= 1
                        print("-1 золотой")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '382':
                    if self.player1.gold >= 4:
                        self.player1.gold -= 4
                        print("-4 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '495':
                    if self.player1.gold >= 6:
                        self.player1.gold -= 6
                        print("-6 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number               
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 256-----------------------------------
            elif self.page_number == 256:
                self.read_page_text()
                if self.ui.lineEdit.text() == '316':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 257-----------------------------------
            elif self.page_number == 257:
                self.read_page_text()
                if self.ui.lineEdit.text() == '565':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '706':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.257
            elif self.page_number == 706:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Сражение со львом")
                    self.player1.battleground_one("Лев", 9, 15)
                    print("Игрок победил льва")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '264':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    del self.button_click_on_page_256
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 258-----------------------------------
            elif self.page_number == 258:
                self.read_page_text()
                if self.ui.lineEdit.text() == '560' or self.ui.lineEdit.text() == '165' or self.ui.lineEdit.text() == '288':
                    ring_with_emerald = Item("Перстень с изумр.", "+169")
                    self.add_item_and_print_console(ring_with_emerald)
                    self.add_item_to_table_widget(ring_with_emerald)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 259-----------------------------------
            elif self.page_number == 259:
                self.read_page_text()
                if self.ui.lineEdit.text() == '48':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 260-----------------------------------
            elif self.page_number == 260:
                self.read_page_text()
                if self.ui.lineEdit.text() == '116' or self.ui.lineEdit.text() == '4' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 261-----------------------------------
            elif self.page_number == 261:
                self.read_page_text()
                if self.ui.lineEdit.text() == '50' or self.ui.lineEdit.text() == '179':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 262-----------------------------------
            elif self.page_number == 262:
                self.read_page_text()
                if self.ui.lineEdit.text() == '117' or self.ui.lineEdit.text() == '303':
                    self.player1.luck -= 1
                    print("-1 удача")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 263-----------------------------------
            elif self.page_number == 263:
                self.read_page_text()
                if self.ui.lineEdit.text() == '54' or self.ui.lineEdit.text() == '19':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 264-----------------------------------
            elif self.page_number == 264:
                self.read_page_text()
                if self.ui.lineEdit.text() == '191' or self.ui.lineEdit.text() == '30' or self.ui.lineEdit.text() == '53' or self.ui.lineEdit.text() == '467':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()                        # во всех параграфах (191, 30, 53, 467) есть варианты входа в зеленых латах (+60) (всё описано ниже)
                    print("Следующая страница = ", self.page_number)    # проверить повторно позже
                elif self.ui.lineEdit.text() == '251' or self.ui.lineEdit.text() == '90' or self.ui.lineEdit.text() == '113' or self.ui.lineEdit.text() == '527':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 265-----------------------------------
            elif self.page_number == 265:          
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с гиеной")
                    self.player1.battleground_one("Гиена", 6, 6)
                    print("Игрок победил гиену")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '125':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 266-----------------------------------
            elif self.page_number == 266:
                self.read_page_text()
                if self.ui.lineEdit.text() == '553':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 267-----------------------------------
            elif self.page_number == 267:
                self.read_page_text()
                if self.ui.lineEdit.text() == '147':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 268-----------------------------------
            elif self.page_number == 268:
                self.read_page_text()
                if self.ui.lineEdit.text() == '80':
                    self.life_points_recovery(4)
                    self.strength_stamina_luck_information()
                    print("+4 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 269-----------------------------------
            elif self.page_number == 269:
                self.read_page_text()
                if self.ui.lineEdit.text() == '264':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 270-----------------------------------
            elif self.page_number == 270:
                self.read_page_text()
                if self.ui.lineEdit.text() == '542' or self.ui.lineEdit.text() == '252':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 271-----------------------------------
            elif self.page_number == 271:
                self.read_page_text()
                if self.ui.lineEdit.text() == '341':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 272-----------------------------------
            elif self.page_number == 272:
                self.read_page_text()
                if self.ui.lineEdit.text() == '480':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 273-----------------------------------
            elif self.page_number == 273:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39' or self.ui.lineEdit.text() == '483' or self.ui.lineEdit.text() == '566':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 274-----------------------------------
            elif self.page_number == 274:
                self.read_page_text()
                if self.ui.lineEdit.text() == '542' or self.ui.lineEdit.text() == '522':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 275-----------------------------------
            elif self.page_number == 275:
                self.read_page_text()
                if self.ui.lineEdit.text() == '279' or self.ui.lineEdit.text() == '385': 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # применение перстня с рубином (+49)  
                elif self.ui.lineEdit.text() == '324':
                    ring_with_ruby = Item("Перстень с рубином", "+49")
                    if self.checking_bag_item(ring_with_ruby) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                # применение перстня с изумрудом (+169) 
                elif self.ui.lineEdit.text() == '444':
                    ring_with_emerald = Item("Перстень с изумрудом", "+169")
                    if self.checking_bag_item(ring_with_emerald) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                # применение Золотого Апельсина (+200) 
                elif self.ui.lineEdit.text() == '475':
                    gold_orange = Item("Золотой апельсин", "+200")
                    if self.checking_bag_item(gold_orange) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 276-----------------------------------
            elif self.page_number == 276:
                self.read_page_text()
                self.page_you_lost(276)


            #--------------------------------параграф 277-----------------------------------
            elif self.page_number == 277:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.PlayAudioFile(self.page277_audio, "GameText\Page277.mp3")
                    message_page_277 = QMessageBox(self)
                    message_page_277.setWindowTitle("Комната со скелетами")
                    message_page_277.setIconPixmap(QPixmap("GameText\Page277.png"))
                    message_page_277.show()
                if self.ui.lineEdit.text() == '572':
                    self.StopAudio(self.page277_audio)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # применение светильника или свечи    
                elif self.ui.lineEdit.text() == '287':
                    self.StopAudio(self.page277_audio)
                    lamp = Item("Светильник", "+10")
                    candle = Item("Свеча", "+10")
                    if self.checking_bag_item(lamp) == True or self.checking_bag_item(candle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number     
                # применение подсвечника    
                elif self.ui.lineEdit.text() == '554':
                    self.StopAudio(self.page277_audio)
                    candlestick = Item("Подсвечник", "-")                   
                    if self.checking_bag_item(candlestick) == True:
                        # удалить подсвечник из инвентаря
                        self.delete_item(candlestick)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                # применение пера павлина    
                elif self.ui.lineEdit.text() == '78':
                    self.StopAudio(self.page277_audio)
                    peacock_feather = Item("Перо павлина", "-")
                    if self.checking_bag_item(peacock_feather) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                # применение серебряного сосуда    
                elif self.ui.lineEdit.text() == '386':
                    self.StopAudio(self.page277_audio)
                    silver_vial = Item("Серебряный сосуд", "-")
                    if self.checking_bag_item(silver_vial) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                # применение золотого ожерелья
                elif self.ui.lineEdit.text() == '429':
                    self.StopAudio(self.page277_audio)
                    gold_necklace = Item("Золотое ожерелье", "-")
                    if self.checking_bag_item(gold_necklace) == True:
                        # удалить золотое ожерелье из инвентаря
                        self.delete_item(gold_necklace)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 278-----------------------------------
            elif self.page_number == 278:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(4)
                    print("-4 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 279-----------------------------------
            elif self.page_number == 279:
                self.read_page_text()
                if self.ui.lineEdit.text() == '502':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '266':
                    mirrors = Item("Секрет зеркал", "-13")
                    if self.checking_bag_item(mirrors) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 280-----------------------------------
            elif self.page_number == 280:
                self.read_page_text()
                if self.ui.lineEdit.text() == '555':                  
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 281-----------------------------------
            elif self.page_number == 281:
                self.read_page_text()
                if self.ui.lineEdit.text() == '547' or self.ui.lineEdit.text() == '501':
                    rosary = Item("Чётки", "-")
                    self.add_item_and_print_console(rosary)
                    self.add_item_to_table_widget(rosary)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 282-----------------------------------
            elif self.page_number == 282:
                self.read_page_text()
                if self.ui.lineEdit.text() == '368' or self.ui.lineEdit.text() == '536':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 283-----------------------------------
            elif self.page_number == 283:
                self.read_page_text()
                if self.ui.lineEdit.text() == '387':
                    pocket_mirror = Item("Зеркальце", "-")
                    if self.checking_bag_item(pocket_mirror):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear() 
                        return self.page_number
                elif self.ui.lineEdit.text() == '69':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    if self.checking_bag_item(bronze_whistle):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear() 
                        return self.page_number
                elif self.ui.lineEdit.text() == '233':
                    gold_ring = Item("Золотое кольцо", "+214")
                    if self.checking_bag_item(gold_ring):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear() 
                        return self.page_number    
                elif self.ui.lineEdit.text() == '567':                  
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                                
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 284-----------------------------------
            elif self.page_number == 284:
                self.read_page_text()
                if self.ui.lineEdit.text() == '474' or self.ui.lineEdit.text() == '380' or self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()                                        # выяснить, с какого параграфа идет применение Фигурного Ключа
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 285-----------------------------------
            elif self.page_number == 285:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page285 = QMessageBox(self)
                    message_page285.setWindowTitle("Подземелье мёртвых")
                    message_page285.setIconPixmap(QPixmap("GameText\Page285.png"))
                    message_page285.show()
                if self.ui.lineEdit.text() == '321':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 286-----------------------------------
            elif self.page_number == 286:
                self.read_page_text()
                if self.ui.lineEdit.text() == '129':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 287-----------------------------------
            elif self.page_number == 287:
                self.read_page_text()
                if self.ui.lineEdit.text() == '497':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 288-----------------------------------
            elif self.page_number == 288:
                self.read_page_text()
                if self.ui.lineEdit.text() == '165' or self.ui.lineEdit.text() == '560' or self.ui.lineEdit.text() == '493':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 289-----------------------------------
            elif self.page_number == 289:
                self.read_page_text()
                if self.ui.lineEdit.text() == '487':
                    #self.player1.strength += 2                                    # мастерство увеличено только на время боя на п.487 (с орками) (заклинание Силы)
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 290-----------------------------------
            elif self.page_number == 290:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с гоблином")
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page290 = QMessageBox()
                        message1_page290.setWindowTitle("Параграф 290")
                        font_page290 = QFont()
                        font_page290.setPointSize(14)
                        message1_page290.setFont(font_page290)
                        message1_page290.setText("Хотите использовать заклинание копии?")
                        message1_page290.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m290 = message1_page290.exec_()
                        if m290 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_one_copy_spell("Гоблин", 6, 9)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_one("Гоблин", 6, 9)
                            self.strength_stamina_luck_information()
                            print("Игрок победил гоблина")
                    else:                       
                        self.player1.battleground_one("Гоблин", 6, 9)
                        self.strength_stamina_luck_information()
                        print("Игрок победил гоблина")

                if self.ui.lineEdit.text() == '118':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    self.add_item_and_print_console(bronze_whistle)
                    self.add_item_to_table_widget(bronze_whistle)
                    copper_key = Item("Медный ключик", "-")
                    self.add_item_and_print_console(copper_key)
                    self.add_item_to_table_widget(copper_key)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 291-----------------------------------
            elif self.page_number == 291:
                self.read_page_text()
                if self.ui.lineEdit.text() == '568' or self.ui.lineEdit.text() == '498' or self.ui.lineEdit.text() == '389' or self.ui.lineEdit.text() == '300':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                    # выяснить, где можно применить меч "Смерть Орков"
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 292-----------------------------------
            elif self.page_number == 292:
                self.read_page_text()
                if self.ui.lineEdit.text() == '503' or self.ui.lineEdit.text() == '265':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 293-----------------------------------
            elif self.page_number == 293:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page293 = QMessageBox()
                    message_page293.setWindowTitle("Параграф 293")
                    font_page293 = QFont()
                    font_page293.setPointSize(14)
                    message_page293.setFont(self.font_for_messageboxes)
                    text293 = ""
                    text293 += "Барлад Дэрт смотрит на ваше оторопевшее лицо, потом начинает хохотать. Это длится довольно долго, и вам начинает надоедать затянувшаяся пауза."
                    text293 += "Неужели ничего нельзя сделать? В отчаянии вы бросаетесь на волшебника с голыми руками."
                    text293 += "Он настолько не ожидает этого, что даже не успевает встать из-за стола, но уже через несколько мгновений как рыба выскальзывает из ваших рук."
                    text293 += "«Ну, что ж, — говорит он задумчиво, — придется тебя проучить. Я буду драться с тобой»."
                    text293 += "«В руках у него оказывается меч, клинок которого светится в полутьме кабинета."
                    message_page293.setText(text293)
                    message_page293.exec_()

                    print("Сражение с Барлад Дэртом")
                    self.player1.battleground_one("Барлад Дэрт", 14, 12)
                    print("Игрок победил Барлад Дэрта")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '169':
                    self.player1.barlad_dart_is_dead = True
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                    self.player1.barlad_dart_is_dead = True                  
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 294-----------------------------------
            elif self.page_number == 294:
                self.read_page_text()
                self.page_you_lost(294)


            #--------------------------------параграф 295-----------------------------------
            elif self.page_number == 295:
                self.read_page_text()
                if self.ui.lineEdit.text() == '379':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 296-----------------------------------
            elif self.page_number == 296:
                self.read_page_text()
                if self.ui.lineEdit.text() == '255' or self.ui.lineEdit.text() == '325':
                    perfume_bottle = Item("Флакончик духов", "-")
                    self.add_item_and_print_console(perfume_bottle)
                    self.add_item_to_table_widget(perfume_bottle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 297-----------------------------------
            elif self.page_number == 297:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':
                    pegasus = Item("Вызов пегаса", "п.609")
                    self.add_item_and_print_console(pegasus)
                    self.add_item_to_table_widget(pegasus)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 298-----------------------------------
            elif self.page_number == 298:
                self.read_page_text()
                if self.ui.lineEdit.text() == '257':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = 707
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.298
            elif self.page_number == 707:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Сражение со львом")
                    self.player1.battleground_one("Лев", 9, 15)
                    print("Игрок победил льва")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '264':
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 299-----------------------------------
            elif self.page_number == 299:
                self.read_page_text()
                if self.ui.lineEdit.text() == '567':
                    self.strength_stamina_luck_information()
                    self.page_number = 718
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 300-----------------------------------
            elif self.page_number == 300:
                self.read_page_text()
                if self.ui.lineEdit.text() == '337' or self.ui.lineEdit.text() == '595':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # +60 для надевания лат нужно прибавлять перед дверью    
                elif self.ui.lineEdit.text() == '397':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 301-----------------------------------
            elif self.page_number == 301:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page_301 = QMessageBox(self)
                    message_page_301.setWindowTitle("Зеленые рыцари")
                    message_page_301.setIconPixmap(QPixmap("GameText\Page301.png"))
                    message_page_301.show()
                # применение Оберега
                if self.ui.lineEdit.text() == '170':
                    talisman = Item("Оберег", "-")
                    if self.checking_bag_item(talisman) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                # применение серебряного сосуда
                elif self.ui.lineEdit.text() == '606':
                    silver_vial = Item("Серебряный сосуд", "-")
                    if self.checking_bag_item(silver_vial) == True:
                        # вычеркнуть серебряный сосуд из инвентаря
                        self.delete_item(silver_vial)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '708':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                            
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.301
            elif self.page_number == 708:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Сражение с зелеными рыцарями и их капитаном")
                    self.player1.battleground_301()               
                    print("Вы победили всех рыцарей")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '594' or self.ui.lineEdit.text() == '599':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 302-----------------------------------
            elif self.page_number == 302:
                self.read_page_text()
                # ! -2 воды уже вычеркнуто в п.11 !
                if self.ui.lineEdit.text() == '11' or self.ui.lineEdit.text() == '234':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 303-----------------------------------
            elif self.page_number == 303:
                self.read_page_text()
                if self.ui.lineEdit.text() == '99' or self.ui.lineEdit.text() == '117':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 304-----------------------------------
            elif self.page_number == 304:
                self.read_page_text()
                if self.ui.lineEdit.text() == '88' or self.ui.lineEdit.text() == '12':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 305-----------------------------------
            elif self.page_number == 305:
                self.read_page_text()
                if self.ui.lineEdit.text() == '412':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 306-----------------------------------
            elif self.page_number == 306:
                self.read_page_text()
                if self.ui.lineEdit.text() == '52':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 307-----------------------------------
            elif self.page_number == 307:
                self.read_page_text()
                if self.ui.lineEdit.text() == '261':
                    self.player1.water = 2
                    print("Вы наполнили флягу")
                    self.gold_food_water_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 308-----------------------------------
            elif self.page_number == 308:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416' or self.ui.lineEdit.text() == '220' or self.ui.lineEdit.text() == '4':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 309-----------------------------------
            elif self.page_number == 309:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image_309 = QMessageBox(self)
                    message_image_309.setWindowTitle("Зелёный рыцарь")
                    message_image_309.setIconPixmap(QPixmap("GameText\Page309.png"))
                    message_image_309.show()
                if self.ui.lineEdit.text() == '111':
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("КОПИЯ")                      
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # -3 выносливости
                        self.losing_life_points(3)
                        print("-3 выносливости")
                        self.strength_stamina_luck_information()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number                
                elif self.ui.lineEdit.text() == '709':
                    # -3 выносливости
                    self.losing_life_points(3)
                    print("-3 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.309
            elif self.page_number == 709:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    self.player1.strength -= 1
                    self.strength_stamina_luck_information()
                    print("Сражение с зеленым рыцарем")
                    self.player1.battleground_one("Зеленый рыцарь", 10, 10)
                    print("Вы победили зеленого рыцаря")
                    self.player1.strength += 1
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '126':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 310-----------------------------------
            elif self.page_number == 310:
                self.read_page_text()
                if self.ui.lineEdit.text() == '179':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 311-----------------------------------
            elif self.page_number == 311:
                self.read_page_text()
                if self.ui.lineEdit.text() == '115':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # -1 выносливость
                        self.losing_life_points(1)
                        print("-1 выносливость")
                        self.strength_stamina_luck_information()
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                elif self.ui.lineEdit.text() == '710':
                    # -1 выносливость
                    self.losing_life_points(1)
                    print("-1 выносливость")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.311            
            elif self.page_number == 710:
                self.read_page_text() 
                self.page_you_lost(710)


            #--------------------------------параграф 312-----------------------------------
            elif self.page_number == 312:
                self.read_page_text()
                if self.ui.lineEdit.text() == '192':   
                    self.losing_life_points(4)
                    print("-4 выносливости")
                    self.strength_stamina_luck_information()                 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 313-----------------------------------
            elif self.page_number == 313:
                self.read_page_text()
                if self.ui.lineEdit.text() == '222':                                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 314-----------------------------------
            elif self.page_number == 314:
                self.read_page_text()
                if self.ui.lineEdit.text() == '183':  
                    #self.player1.strength -= 2                                      # -2 мастерства до окончания битвы с рыцарями (п.183) (проработать)  
                    print("-2 мастерства")
                    self.strength_stamina_luck_information()                             
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 315-----------------------------------
            elif self.page_number == 315:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':  
                    self.losing_life_points(2) 
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()                             
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 316-----------------------------------
            elif self.page_number == 316:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    print("-4 выносливости")
                    self.losing_life_points(4)
                    self.strength_stamina_luck_information()

                    self.player1.round_number = 0
                    print("Сражение с драконом")
                    if self.player1.strength_spell == True:
                        self.player1.strength += 2
                        self.strength_stamina_luck_information()
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page316 = QMessageBox()
                        message1_page316.setWindowTitle("Параграф 316")
                        font_page316 = QFont()
                        font_page316.setPointSize(14)
                        message1_page316.setFont(font_page316)
                        message1_page316.setText("Хотите использовать заклинание копии?")
                        message1_page316.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m316 = message1_page316.exec_()
                        if m316 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_316_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_316()
                            self.strength_stamina_luck_information()
                            print("Игрок дважды ранил дракона")
                    else:                       
                        self.player1.battleground_316()
                        self.strength_stamina_luck_information()
                        print("Игрок дважды ранил дракона")
                    print("Игрок дважды ранил дракона")
                    if self.player1.strength_spell == True:
                        self.player1.strength_spell = False
                        # заклинание Силы прекратило свое действие
                        self.player1.strength -= 2
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '513':                                           
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 317-----------------------------------
            elif self.page_number == 317:
                self.read_page_text()
                if self.ui.lineEdit.text() == '225':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '127':
                    silver_ring = Item("Серебряное кольцо", "-")
                    if self.checking_bag_item(silver_ring) == True:
                        # удалить серебряное кольцо из инвентаря
                        self.delete_item(silver_ring)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 318-----------------------------------
            elif self.page_number == 318:
                self.read_page_text()
                if self.ui.lineEdit.text() == '193':
                    metal_key = Item("Метал.ключ", "-40")
                    self.add_item_and_print_console(metal_key)
                    self.add_item_to_table_widget(metal_key)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 319-----------------------------------
            elif self.page_number == 319:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image319 = QMessageBox(self)
                    message_image319.setWindowTitle("Охрана у ворот")
                    message_image319.setIconPixmap(QPixmap("GameText\Page319.png"))
                    message_image319.show()                 
                if self.ui.lineEdit.text() == '31' or self.ui.lineEdit.text() == '439' or self.ui.lineEdit.text() == '146':                                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '122':
                    password_122 = Item("Пароль-122", "п.122")
                    if self.checking_bag_item(password_122) == True:
                        # удалить пароль из списка
                        self.delete_item(password_122)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 320-----------------------------------
            elif self.page_number == 320:
                self.read_page_text()
                if self.ui.lineEdit.text() == '355' or self.ui.lineEdit.text() == '543':                                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 321-----------------------------------
            elif self.page_number == 321:
                self.read_page_text()
                if self.ui.lineEdit.text() == '75' or self.ui.lineEdit.text() == '247':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 322-----------------------------------
            elif self.page_number == 322:
                self.read_page_text()
                if self.ui.lineEdit.text() == '277' or self.ui.lineEdit.text() == '556':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 323-----------------------------------
            elif self.page_number == 323:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image323 = QMessageBox(self)
                    message_image323.setWindowTitle("Старушка")
                    message_image323.setIconPixmap(QPixmap("GameText\Page323.png"))
                    message_image323.show()
                if self.ui.lineEdit.text() == '522' or self.ui.lineEdit.text() == '137' or self.ui.lineEdit.text() == '194':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # показываем старушке пропуск    
                elif self.ui.lineEdit.text() == '343':
                    paper_pass = Item("Пропуск", "+20")
                    if self.checking_bag_item(paper_pass) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 324-----------------------------------
            elif self.page_number == 324:
                self.read_page_text()
                if self.ui.lineEdit.text() == '617' and self.player1.barlad_dart_is_dead == True:
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    self.player1.princess_is_saved = True
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '589':
                    self.player1.princess_is_saved = True
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                    self.player1.princess_is_saved = True
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 325-----------------------------------
            elif self.page_number == 325:
                self.read_page_text()
                if self.ui.lineEdit.text() == '162' or self.ui.lineEdit.text() == '76':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 326-----------------------------------
            elif self.page_number == 326:
                self.read_page_text()
                if self.ui.lineEdit.text() == '711':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '504':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.326
            elif self.page_number == 711:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    if self.player1.strength_spell == True:
                        self.player1.strength += 2
                        print("+2 мастерства")
                        self.strength_stamina_luck_information()

                    self.player1.round_number = 0
                    print("Сражение с водяным")
                    self.player1.battleground_one("Водяной", 7, 7)
                    print("Игрок победил водяного")

                    if self.player1.strength_spell == True:
                        self.player1.strength -= 2
                        print("-2 мастерства")
                        self.strength_stamina_luck_information()
                        self.player1.strength_spell = False
                    self.strength_stamina_luck_information()    

                if self.ui.lineEdit.text() == '573':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 327-----------------------------------
            elif self.page_number == 327:
                self.read_page_text()
                if self.ui.lineEdit.text() == '443':                                     # проверить, вычлось ли золото (отдать торговцу) на предыдущем параграфе
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 328-----------------------------------
            elif self.page_number == 328:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    message_page = QMessageBox(self)
                    message_page.resize(1000, 1000)
                    message_page.setWindowTitle("Параграф " + str(self.page_number))
                    font = QFont()
                    font.setPointSize(14)
                    message_page.setFont(font)                   
                    message_page.setText("Пока Орки не успели понять, в чем дело, вы нападаете на них.")
                    message_page.exec_()

                    print("Сражение с двумя орками")
                    self.player1.round_number = 0
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page328 = QMessageBox()
                        message1_page328.setWindowTitle("Параграф 328")
                        font_page328 = QFont()
                        font_page328.setPointSize(14)
                        message1_page328.setFont(font_page328)
                        message1_page328.setText("Хотите использовать заклинание копии?")
                        message1_page328.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m328 = message1_page328.exec_()
                        if m328 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_328_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_328()
                            self.strength_stamina_luck_information()
                            print("Игрок победил орков")
                    else:                       
                        self.player1.battleground_328()
                        self.strength_stamina_luck_information()
                        print("Игрок победил орков")

                    if self.player1.win_battle_328 == True:
                        print("Игрок победил орков")
                        message10_page328 = QMessageBox()
                        message10_page328.setWindowTitle("------>>")
                        font10_page328 = QFont()
                        font10_page328.setPointSize(14)
                        message10_page328.setFont(font10_page328)
                        message10_page328.setText("Переход к параграфу 505!")
                        message10_page328.exec_()
                        self.page_number = 505
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        print("Игрок не успел победить орков за 8 раундов атаки")
                        message11_page328 = QMessageBox()
                        message11_page328.setWindowTitle("------>>")
                        font10_page328 = QFont()
                        font10_page328.setPointSize(14)
                        message11_page328.setFont(font10_page328)
                        message11_page328.setText("Переход к параграфу 248!")
                        message11_page328.exec_()
                        self.page_number = 248
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)


            #--------------------------------параграф 329-----------------------------------
            elif self.page_number == 329:
                self.read_page_text()
                if self.ui.lineEdit.text() == '33':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 330-----------------------------------
            elif self.page_number == 330:
                self.read_page_text()
                if self.ui.lineEdit.text() == '532':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '592':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 331-----------------------------------
            elif self.page_number == 331:
                self.read_page_text()
                if self.ui.lineEdit.text() == '305' or self.ui.lineEdit.text() == '195':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 332-----------------------------------
            elif self.page_number == 332:
                self.read_page_text()
                if self.ui.lineEdit.text() == '250' or self.ui.lineEdit.text() == '461':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 333-----------------------------------
            elif self.page_number == 333:
                self.read_page_text()
                if self.ui.lineEdit.text() == '149' or self.ui.lineEdit.text() == '98':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 334-----------------------------------
            elif self.page_number == 334:
                self.read_page_text()
                if self.ui.lineEdit.text() == '99':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 335-----------------------------------
            elif self.page_number == 335:
                self.read_page_text()
                if self.ui.lineEdit.text() == '46':
                    self.player1.gold += 7
                    self.gold_food_water_information()
                    stork_feather = Item("Перо аиста", "-")
                    self.add_item_and_print_console(stork_feather)
                    self.add_item_to_table_widget(stork_feather)
                    bronze_jug = Item("Бронзовый кувшин", "-")
                    self.add_item_and_print_console(bronze_jug)
                    self.add_item_to_table_widget(bronze_jug)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 336-----------------------------------
            elif self.page_number == 336:
                self.read_page_text()
                if self.ui.lineEdit.text() == '24':
                    gold_orange = Item("Золотой апельсин", "+200")
                    self.add_item_and_print_console(gold_orange)
                    self.add_item_to_table_widget(gold_orange)
                    self.player1.luck += 1
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 337-----------------------------------
            elif self.page_number == 337:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image337 = QMessageBox(self)
                    message_image337.setWindowTitle("Начальник стражи")
                    message_image337.setIconPixmap(QPixmap("GameText\Page337.png"))
                    message_image337.show()
                if self.ui.lineEdit.text() == '613' or self.ui.lineEdit.text() == '249' or self.ui.lineEdit.text() == '65':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # перед входом надеть латы Зеленого Рыцаря    
                elif self.ui.lineEdit.text() == '397':
                    # +60 для надевания лат нужно прибавлять в коридоре
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 338-----------------------------------
            elif self.page_number == 338:
                self.read_page_text()
                if self.ui.lineEdit.text() == '151' or self.ui.lineEdit.text() == '231':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 339-----------------------------------
            elif self.page_number == 339:
                self.read_page_text()
                if self.ui.lineEdit.text() == '123' or self.ui.lineEdit.text() == '66':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 340-----------------------------------
            elif self.page_number == 340:
                self.read_page_text()
                if self.ui.lineEdit.text() == '509':
                    self.life_points_recovery(3)
                    print("+3 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 341-----------------------------------
            elif self.page_number == 341:
                self.read_page_text()
                if self.ui.lineEdit.text() == '164':
                    # проверка наличия заклинания силы у игрока
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("СИЛА")                                   # Warning  увеличить мастерство только до окончания битвы
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                elif self.ui.lineEdit.text() == '289':
                    # проверка наличия заклинания слабости у игрока
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):              # уменьшить силу удара на 2 у любого из орков (программно сделать)
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                elif self.ui.lineEdit.text() == '506':
                    # проверка наличия заклинания слабости у игрока
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '487':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                       
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 342-----------------------------------
            elif self.page_number == 342:
                self.read_page_text()
                if self.ui.lineEdit.text() == '181':
                    self.losing_life_points(3)
                    print("-3 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 343-----------------------------------
            elif self.page_number == 343:
                self.read_page_text()
                if self.ui.lineEdit.text() == '252' or self.ui.lineEdit.text() == '542':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 344-----------------------------------
            elif self.page_number == 344:
                self.read_page_text()
                if self.ui.lineEdit.text() == '319' or self.ui.lineEdit.text() == '232':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 345-----------------------------------
            elif self.page_number == 345:
                self.read_page_text()
                if self.ui.lineEdit.text() == '141':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 346-----------------------------------
            elif self.page_number == 346:
                self.read_page_text()
                if self.ui.lineEdit.text() == '153' or self.ui.lineEdit.text() == '68':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 347-----------------------------------
            elif self.page_number == 347:
                self.read_page_text()
                self.page_you_lost(347)


            #--------------------------------параграф 348-----------------------------------
            elif self.page_number == 348:
                self.read_page_text()
                if self.ui.lineEdit.text() == '544':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 349-----------------------------------
            elif self.page_number == 349:
                self.read_page_text()
                if self.ui.lineEdit.text() == '615' or self.ui.lineEdit.text() == '305' or self.ui.lineEdit.text() == '210':
                    comb = Item("Гребень", "-")
                    self.add_item_and_print_console(comb)
                    self.add_item_to_table_widget(comb)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 350-----------------------------------
            elif self.page_number == 350:
                self.read_page_text()
                if self.ui.lineEdit.text() == '253' or self.ui.lineEdit.text() == '39':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '545':
                    silver_vial = Item("Серебряный сосуд", "-")
                    self.add_item_and_print_console(silver_vial)
                    self.add_item_to_table_widget(silver_vial)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 351-----------------------------------
            elif self.page_number == 351:
                self.read_page_text()
                if self.ui.lineEdit.text() == '235' or self.ui.lineEdit.text() == '2':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '574':
                    if self.player1.gold >= 3:
                        self.player1.gold -= 3
                        print("-3 золотых")
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 352-----------------------------------
            elif self.page_number == 352:
                self.read_page_text()
                if self.ui.lineEdit.text() == '322':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 353-----------------------------------
            elif self.page_number == 353:
                self.read_page_text()
                if self.ui.lineEdit.text() == '154' or self.ui.lineEdit.text() == '237' or self.ui.lineEdit.text() == '181':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # применение Клубочка (clew)    
                elif self.ui.lineEdit.text() == '383':
                    clew = Item("Клубочек", "+30")
                    if self.checking_bag_item(clew) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear() 
                        return self.page_number   
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 354-----------------------------------
            elif self.page_number == 354:
                self.read_page_text()
                if self.ui.lineEdit.text() == '518' or self.ui.lineEdit.text() == '106':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '327':
                    if self.player1.gold >= 7:
                        self.player1.gold -= 7
                        print("-7 золотых")
                        self.gold_food_water_information()    
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 355-----------------------------------
            elif self.page_number == 355:
                self.read_page_text()
                if self.ui.lineEdit.text() == '233':
                    gold_ring = Item("Золотое кольцо", "+214")
                    if self.checking_bag_item(gold_ring) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '69':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    if self.checking_bag_item(bronze_whistle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '168':
                    rosary = Item("Чётки", "-")
                    if self.checking_bag_item(rosary) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '543':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 356-----------------------------------
            elif self.page_number == 356:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с троллем")
                    self.player1.battleground_one("Тролль", 9, 14)
                    print("Игрок победил тролля")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '712':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.356
            elif self.page_number == 712:
                self.read_page_text()
                if self.ui.lineEdit.text() == '207':
                    self.player1.luck += 1
                    print("+1 удача")
                    self.strength_stamina_luck_information()
                    gold_ring = Item("Золотое кольцо", "+214")
                    self.add_item_and_print_console(gold_ring)
                    self.add_item_to_table_widget(gold_ring)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 357-----------------------------------
            elif self.page_number == 357:
                self.read_page_text()
                # заклинание Силы, +2 мастерства только до окончания боя с драконом на п.316
                if self.ui.lineEdit.text() == '316':
                    self.player1.strength_spell = True
                    print("+2 к мастерству до окончания боя")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            #--------------------------------параграф 358-----------------------------------
            elif self.page_number == 358:
                self.read_page_text()
                if self.ui.lineEdit.text() == '510' or self.ui.lineEdit.text() == '214' or self.ui.lineEdit.text() == '38':
                    self.life_points_recovery(2)
                    print("+2 выносливости")
                    self.strength_stamina_luck_information()                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 359-----------------------------------
            elif self.page_number == 359:
                self.read_page_text()
                self.page_you_lost(359)


            # --------------------------------параграф 360-----------------------------------
            elif self.page_number == 360:
                self.read_page_text()
                if self.ui.lineEdit.text() == '2' or self.ui.lineEdit.text() == '184':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 361-----------------------------------
            elif self.page_number == 361:
                self.read_page_text()
                self.page_you_lost(361)


            # --------------------------------параграф 362-----------------------------------
            elif self.page_number == 362:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 363-----------------------------------
            elif self.page_number == 363:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 364-----------------------------------
            elif self.page_number == 364:
                self.read_page_text()
                if self.ui.lineEdit.text() == '480':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 365-----------------------------------
            elif self.page_number == 365:
                self.read_page_text()
                if self.ui.lineEdit.text() == '543':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 366-----------------------------------
            elif self.page_number == 366:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416' or self.ui.lineEdit.text() == '116':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 367-----------------------------------
            elif self.page_number == 367:
                self.read_page_text()
                # шкура лисы уже добавлена в п.62
                if self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 368-----------------------------------
            elif self.page_number == 368:
                self.read_page_text()
                self.page_you_lost(368)


            # --------------------------------параграф 369-----------------------------------
            elif self.page_number == 369:
                self.read_page_text()
                if self.ui.lineEdit.text() == '542' or self.ui.lineEdit.text() == '252':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 370-----------------------------------
            elif self.page_number == 370:
                self.read_page_text()
                if self.ui.lineEdit.text() == '68':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '538':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # # распечатаем в консоли список заклинаний
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 371-----------------------------------
            elif self.page_number == 371:
                self.read_page_text()
                if self.ui.lineEdit.text() == '276':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 372-----------------------------------
            elif self.page_number == 372:
                self.read_page_text()
                if self.ui.lineEdit.text() == '424':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 373-----------------------------------
            elif self.page_number == 373:
                self.read_page_text()
                if self.ui.lineEdit.text() == '221' or self.ui.lineEdit.text() == '121':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 374-----------------------------------
            elif self.page_number == 374:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с двумя человеками")
                    self.player1.battleground_two("Первый человек", 8, 5, "Второй человек", 6, 9)
                    print("Игрок победил двух человеков")
                    self.strength_stamina_luck_information()              
              
                if self.ui.lineEdit.text() == '34':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 375-----------------------------------
            elif self.page_number == 375:
                self.read_page_text()
                # идти к палаткам
                if self.ui.lineEdit.text() == '424':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # применение Плавания    
                elif self.ui.lineEdit.text() == '254':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # # распечатаем в консоли список заклинаний
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number                 
                # применение Левитации    
                elif self.ui.lineEdit.text() == '508':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # # распечатаем в консоли список заклинаний
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                # применение Плавания для проникновения в замок    
                elif self.ui.lineEdit.text() == '311':
                    if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # # распечатаем в консоли список заклинаний
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 376-----------------------------------
            elif self.page_number == 376:
                self.read_page_text()
                if self.ui.lineEdit.text() == '155':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 377-----------------------------------
            elif self.page_number == 377:
                self.read_page_text()
                if self.ui.lineEdit.text() == '197' or self.ui.lineEdit.text() == '309':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 378-----------------------------------
            elif self.page_number == 378:
                self.read_page_text()
                if self.ui.lineEdit.text() == '415' or self.ui.lineEdit.text() == '129':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 379-----------------------------------
            elif self.page_number == 379:
                self.read_page_text()
                if self.ui.lineEdit.text() == '544':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 380-----------------------------------
            elif self.page_number == 380:
                self.read_page_text()
                if self.ui.lineEdit.text() == '474' or self.ui.lineEdit.text() == '540' or self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 381-----------------------------------
            elif self.page_number == 381:
                self.read_page_text()
                if self.ui.lineEdit.text() == '84' or self.ui.lineEdit.text() == '281' or self.ui.lineEdit.text() == '496' or self.ui.lineEdit.text() == '547' or self.ui.lineEdit.text() == '501':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 382-----------------------------------
            elif self.page_number == 382:
                self.read_page_text()
                if self.ui.lineEdit.text() == '575' or self.ui.lineEdit.text() == '511' or self.ui.lineEdit.text() == '325':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 383-----------------------------------
            elif self.page_number == 383:
                self.read_page_text()
                if self.ui.lineEdit.text() == '576' or self.ui.lineEdit.text() == '353':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 384-----------------------------------
            elif self.page_number == 384:
                self.read_page_text()
                if self.ui.lineEdit.text() == '555':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 385-----------------------------------
            elif self.page_number == 385:
                self.read_page_text()
                if self.ui.lineEdit.text() == '502':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 386-----------------------------------
            elif self.page_number == 386:
                self.read_page_text()
                if self.ui.lineEdit.text() == '572':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 387-----------------------------------
            elif self.page_number == 387:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 388-----------------------------------
            elif self.page_number == 388:
                self.read_page_text()
                if self.ui.lineEdit.text() == '577' or self.ui.lineEdit.text() == '293' :
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '605':
                    gold_amulet = Item("Золотой амулет", "+217")
                    if self.checking_bag_item(gold_amulet):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '602':
                    gold_ring = Item("Золотое кольцо", "+214")
                    if self.checking_bag_item(gold_ring):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 389-----------------------------------
            elif self.page_number == 389:
                self.read_page_text()
                if self.ui.lineEdit.text() == '300':
                    self.player1.strength -= 1
                    print("-1 мастерство")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 390-----------------------------------
            elif self.page_number == 390:
                self.read_page_text()
                if self.ui.lineEdit.text() == '569':
                    self.player1.strength_spell = True                   # +2 мастерства (заклинание Силы) - только до окончания битвы с орками (п.569)
                    print("+2 мастерства") 
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 391-----------------------------------
            elif self.page_number == 391:
                self.read_page_text()
                if self.ui.lineEdit.text() == '502':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 392-----------------------------------
            elif self.page_number == 392:
                self.read_page_text()
                self.page_you_lost(392)


            # --------------------------------параграф 393-----------------------------------
            elif self.page_number == 393:
                self.read_page_text()
                if self.ui.lineEdit.text() == '337' or self.ui.lineEdit.text() == '595':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '291':
                    copper_key = Item("Медный ключик", "-")
                    if self.checking_bag_item(copper_key) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                elif self.ui.lineEdit.text() == '397':
                    green_armor = Item("Зеленые латы", "+60")                           # +60 для надевания лат нужно прибавлять в коридоре перед дверью
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 394-----------------------------------
            elif self.page_number == 394:
                self.read_page_text()
                if self.ui.lineEdit.text() == '93':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '294':
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    if self.checking_bag_item(bronze_whistle) == True:
                        # удалить бронзовый свисток из инвентаря
                        self.delete_item(bronze_whistle)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '596':
                    pocket_mirror = Item("Зеркальце", "-")
                    if self.checking_bag_item(pocket_mirror) == True:
                        # удалить зеркальце из инвентаря
                        self.delete_item(pocket_mirror)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '171':
                    perfume_bottle = Item("Флакончик духов", "-")
                    if self.checking_bag_item(perfume_bottle) == True:
                        # удалить флакончик духов из инвентаря
                        self.delete_item(perfume_bottle)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number                
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 395-----------------------------------
            elif self.page_number == 395:
                self.read_page_text()
                if self.ui.lineEdit.text() == '567':
                    self.page_number = 718
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 396-----------------------------------
            elif self.page_number == 396:
                self.read_page_text()
                if self.ui.lineEdit.text() == '100':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 397-----------------------------------
            elif self.page_number == 397:
                self.read_page_text()
                # приход с п.337, надеты латы Зеленого рыцаря
                if self.ui.lineEdit.text() == '130' or self.ui.lineEdit.text() == '512' or self.ui.lineEdit.text() == '315':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 398-----------------------------------
            elif self.page_number == 398:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 399-----------------------------------
            elif self.page_number == 399:
                self.read_page_text()
                if self.ui.lineEdit.text() == '198' or self.ui.lineEdit.text() == '255':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '459':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 400-----------------------------------
            elif self.page_number == 400:
                self.read_page_text()
                if self.ui.lineEdit.text() == '514' or self.ui.lineEdit.text() == '35':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '430':
                    clew = Item("Клубочек", "+30")
                    if self.checking_bag_item(clew) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 401-----------------------------------
            elif self.page_number == 401:
                self.read_page_text()
                message_page401 = QMessageBox(self)
                message_page401.resize(1000, 1000)
                message_page401.setWindowTitle("Удача")
                font401 = QFont()
                font401.setPointSize(14)
                message_page401.setFont(font401)               
                message_page401.setText("Проверьте свою удачу!")
                message_page401.exec_()
                print("Проверка удачи")
                if self.player1.checking_luck() == True:
                    self.page_number = 546
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message2_page401 = QMessageBox(self)
                    message2_page401.resize(1000, 1000)
                    message2_page401.setWindowTitle("------->>")
                    font401 = QFont()
                    font401.setPointSize(14)
                    message2_page401.setFont(font401)               
                    message2_page401.setText("Переход к параграфу 546")
                    message2_page401.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_number = 77
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message3_page401 = QMessageBox(self)
                    message3_page401.resize(1000, 1000)
                    message3_page401.setWindowTitle("------->>")
                    font401 = QFont()
                    font401.setPointSize(14)
                    message3_page401.setFont(font401)               
                    message3_page401.setText("Переход к параграфу 77")
                    message3_page401.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)


            # --------------------------------параграф 402-----------------------------------
            elif self.page_number == 402:
                self.read_page_text()
                if self.ui.lineEdit.text() == '547' or self.ui.lineEdit.text() == '501':
                    self.losing_life_points(1)
                    print("-1 выносливость")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 403-----------------------------------
            elif self.page_number == 403:
                self.read_page_text()
                if self.ui.lineEdit.text() == '199' or self.ui.lineEdit.text() == '244':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 404-----------------------------------
            elif self.page_number == 404:
                self.read_page_text()
                if self.ui.lineEdit.text() == '183':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                # использование заклинания Силы    
                elif self.ui.lineEdit.text() == '36':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.player1.strength_spell = True
                        # -3 выносливости
                        print("-3 выносливости") 
                        self.losing_life_points(3)
                        self.strength_stamina_luck_information()                      
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                # использование заклинания Слабости        
                elif self.ui.lineEdit.text() == '314':                                  # (ошибка в тексте книги, там стоит 334, а нужно - 314) (исправлено!)
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # -3 выносливости
                        print("-3 выносливости") 
                        self.losing_life_points(3)
                        self.strength_stamina_luck_information()                      
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()   
                        print(self.player1.spells)
                # использование заклинания Копии        
                elif self.ui.lineEdit.text() == '7':
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("КОПИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # -3 выносливости
                        print("-3 выносливости") 
                        self.losing_life_points(3)
                        self.strength_stamina_luck_information()                      
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                # использование заклинания Огня        
                elif self.ui.lineEdit.text() == '112':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # -3 выносливости
                        print("-3 выносливости") 
                        self.losing_life_points(3)
                        self.strength_stamina_luck_information()                      
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 405-----------------------------------
            elif self.page_number == 405:
                self.read_page_text()
                if self.ui.lineEdit.text() == '307' or self.ui.lineEdit.text() == '261':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 406-----------------------------------
            elif self.page_number == 406:
                self.read_page_text()
                if self.ui.lineEdit.text() == '98' or self.ui.lineEdit.text() == '515':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 407-----------------------------------
            elif self.page_number == 407:
                self.read_page_text()
                if self.ui.lineEdit.text() == '181':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 408-----------------------------------
            elif self.page_number == 408:
                self.read_page_text()
                if self.ui.lineEdit.text() == '131' or self.ui.lineEdit.text() == '305' or self.ui.lineEdit.text() == '210':
                    comb = Item("Гребень", "-")
                    self.add_item_and_print_console(comb)
                    self.add_item_to_table_widget(comb)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 409-----------------------------------
            elif self.page_number == 409:
                self.read_page_text()
                if self.ui.lineEdit.text() == '56':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '200':
                    if self.player1.check_for_use_necessary_spell("ИЛЛЮЗИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ИЛЛЮЗИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                           
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '114':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                           
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)            
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 410-----------------------------------
            elif self.page_number == 410:
                self.read_page_text()
                if self.ui.lineEdit.text() == '54':
                    self.strength_stamina_luck_information()
                    # 703 - дополнение к п.54 (см. программу п.54)
                    self.page_number = 703
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 411-----------------------------------
            elif self.page_number == 411:
                self.read_page_text()
                if self.ui.lineEdit.text() == '578' or self.ui.lineEdit.text() == '80':
                    self.life_points_recovery(6)
                    self.strength_stamina_luck_information()
                    print("+6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 412-----------------------------------
            elif self.page_number == 412:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page412 = QMessageBox(self)
                    message_page412.setWindowTitle("Дракон")
                    message_page412.setIconPixmap(QPixmap("GameText\Page412.png"))
                    message_page412.show()
                if self.ui.lineEdit.text() == '316' or self.ui.lineEdit.text() == '516':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '37':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                           
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '357':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '256':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 413-----------------------------------
            elif self.page_number == 413:
                self.read_page_text()
                if self.ui.lineEdit.text() == '132':                  
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 414-----------------------------------
            elif self.page_number == 414:
                self.read_page_text()
                if self.ui.lineEdit.text() == '338':
                    green_armor = Item("Зеленые латы", "+60")
                    self.add_item_and_print_console(green_armor)
                    self.add_item_to_table_widget(green_armor)
                    self.player1.gold += 7
                    print("+7 золотых")
                    self.gold_food_water_information()
                    peacock_feather = Item("Перо павлина", "-")
                    self.add_item_and_print_console(peacock_feather)
                    self.add_item_to_table_widget(peacock_feather)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 415-----------------------------------
            elif self.page_number == 415:
                self.read_page_text()
                message_page415 = QMessageBox(self)
                message_page415.resize(1000, 1000)
                message_page415.setWindowTitle("Удача")
                font415 = QFont()
                font415.setPointSize(14)
                message_page415.setFont(font415)               
                message_page415.setText("Проверьте свою удачу!")
                message_page415.exec_()
                print("Проверка удачи")
                if self.player1.checking_luck() == True:
                    self.page_number = 57
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message2_page415 = QMessageBox(self)
                    message2_page415.resize(1000, 1000)
                    message2_page415.setWindowTitle("------->>")
                    message2_page415.setFont(font415)               
                    message2_page415.setText("Переход к параграфу 57")
                    message2_page415.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_number = 579
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message3_page415 = QMessageBox(self)
                    message3_page415.resize(1000, 1000)
                    message3_page415.setWindowTitle("--------->>")
                    message3_page415.setFont(font415)               
                    message3_page415.setText("Переход к параграфу 579")
                    message3_page415.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)


            # --------------------------------параграф 416-----------------------------------
            elif self.page_number == 416:
                self.read_page_text()
                if self.ui.lineEdit.text() == '424' or self.ui.lineEdit.text() == '257':                  
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 417-----------------------------------
            elif self.page_number == 417:
                self.read_page_text()
                if self.ui.lineEdit.text() == '326': 
                    # заклинание Силы (+2 мастерства до конца битвы) - отнять 2 после окончания боя
                    self.player1.strength_spell = True
                    self.strength_stamina_luck_information()         
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 418-----------------------------------
            elif self.page_number == 418:
                self.read_page_text()
                if self.ui.lineEdit.text() == '179':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 419-----------------------------------
            elif self.page_number == 419:
                self.read_page_text()
                if self.ui.lineEdit.text() == '374':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '104':
                    if self.player1.food >= 1:
                        self.player1.food = 0
                        self.gold_food_water_information()
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        message_not_enough_food = QMessageBox()
                        message_not_enough_food.setWindowTitle("Нет еды")
                        message_not_enough_food.setText("У вас недостаточно еды")
                        font_not_enough_food = QFont()
                        font_not_enough_food.setPointSize(14)
                        message_not_enough_food.setFont(font_not_enough_food)
                        message_not_enough_food.exec_()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 420------------------------------------
            elif self.page_number == 420:
                self.read_page_text()
                if self.ui.lineEdit.text() == '38' or self.ui.lineEdit.text() == '214':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 421-----------------------------------
            elif self.page_number == 421:
                self.read_page_text()
                self.page_you_lost(421)


            # --------------------------------параграф 422------------------------------------
            elif self.page_number == 422:
                self.read_page_text()
                if self.ui.lineEdit.text() == '133':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '317':
                    silver_ring = Item("Серебряное кольцо", "-")
                    if self.checking_bag_item(silver_ring) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 423------------------------------------
            elif self.page_number == 423:
                self.read_page_text()
                if self.ui.lineEdit.text() == '40':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '58':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '580':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells) 
                elif self.ui.lineEdit.text() == '290':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 424------------------------------------
            elif self.page_number == 424:
                self.read_page_text()
                if self.ui.lineEdit.text() == '582' or self.ui.lineEdit.text() == '74':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 425------------------------------------
            elif self.page_number == 425:
                self.read_page_text()
                if self.ui.lineEdit.text() == '581':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '614':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    elif self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ПЛАВАНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)    
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)

                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 426------------------------------------
            elif self.page_number == 426:
                self.read_page_text()
                if self.ui.lineEdit.text() == '123':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 427------------------------------------
            elif self.page_number == 427:
                self.read_page_text()
                if self.ui.lineEdit.text() == '597' or self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206' or self.ui.lineEdit.text() == '350':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '583':
                    gold_whistle = Item("Золотой свисток", "-")
                    if self.checking_bag_item(gold_whistle) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 428------------------------------------
            elif self.page_number == 428:
                self.read_page_text()
                if self.ui.lineEdit.text() == '569':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '499':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '85':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '390':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 429------------------------------------
            elif self.page_number == 429:
                self.read_page_text()
                if self.ui.lineEdit.text() == '301':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 430------------------------------------
            elif self.page_number == 430:
                self.read_page_text()
                if self.ui.lineEdit.text() == '400':                            
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 431------------------------------------
            elif self.page_number == 431:
                self.read_page_text()
                message_page431 = QMessageBox(self)
                message_page431.resize(1000, 1000)
                message_page431.setWindowTitle("Удача")
                font431 = QFont()
                font431.setPointSize(14)
                message_page431.setFont(font431)               
                message_page431.setText("Проверьте свою удачу!")
                message_page431.exec_()
                print("Проверка удачи")
                if self.player1.checking_luck() == True:
                    self.page_number = 59
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message2_page431 = QMessageBox(self)
                    message2_page431.resize(1000, 1000)
                    message2_page431.setWindowTitle("------->>")
                    message2_page431.setFont(font431)               
                    message2_page431.setText("Переход к параграфу 59")
                    message2_page431.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_number = 713
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message3_page431 = QMessageBox(self)
                    message3_page431.resize(1000, 1000)
                    message3_page431.setWindowTitle("------->>")
                    message3_page431.setFont(font431)               
                    message3_page431.setText("Переход к параграфу 713")
                    message3_page431.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)

            # дополнение к п.431
            elif self.page_number == 713:
                self.read_page_text()
                self.page_you_lost(713)


            # --------------------------------параграф 432------------------------------------
            elif self.page_number == 432:
                self.read_page_text()
                if self.ui.lineEdit.text() == '421' or self.ui.lineEdit.text() == '73':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 433------------------------------------
            elif self.page_number == 433:
                self.read_page_text()
                if self.ui.lineEdit.text() == '500' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 434------------------------------------
            elif self.page_number == 434:
                self.read_page_text()
                if self.ui.lineEdit.text() == '584' or self.ui.lineEdit.text() == '60':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 435------------------------------------
            elif self.page_number == 435:
                self.read_page_text()
                if self.ui.lineEdit.text() == '544':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 436------------------------------------
            elif self.page_number == 436:
                self.read_page_text()
                if self.ui.lineEdit.text() == '338':
                    peacock_feather = Item("Перо павлина", "-")
                    self.add_item_and_print_console(peacock_feather)
                    self.add_item_to_table_widget(peacock_feather)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 437------------------------------------
            elif self.page_number == 437:
                self.read_page_text()
                if self.ui.lineEdit.text() == '531' or self.ui.lineEdit.text() == '72':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 438------------------------------------
            elif self.page_number == 438:
                self.read_page_text()
                if self.ui.lineEdit.text() == '106':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 439------------------------------------
            elif self.page_number == 439:
                self.read_page_text()
                if self.ui.lineEdit.text() == '259' or self.ui.lineEdit.text() == '585':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 440------------------------------------
            elif self.page_number == 440:
                self.read_page_text()
                if self.ui.lineEdit.text() == '348' or self.ui.lineEdit.text() == '61':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 441------------------------------------
            elif self.page_number == 441:
                self.read_page_text()
                if self.ui.lineEdit.text() == '378':
                    self.losing_life_points(3)
                    print("-3 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 442------------------------------------
            elif self.page_number == 442:
                self.read_page_text()
                if self.ui.lineEdit.text() == '119':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 443------------------------------------
            elif self.page_number == 443:
                self.read_page_text()
                if self.ui.lineEdit.text() == '106':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 444------------------------------------
            elif self.page_number == 444:
                self.read_page_text()
                if self.ui.lineEdit.text() == '502':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 445------------------------------------
            elif self.page_number == 445:
                self.read_page_text()
                if self.ui.lineEdit.text() == '102':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 446------------------------------------
            elif self.page_number == 446:
                self.read_page_text()
                if self.ui.lineEdit.text() == '328':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 447------------------------------------
            elif self.page_number == 447:
                self.read_page_text()
                if self.ui.lineEdit.text() == '529':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '62':
                    if self.player1.check_for_use_necessary_spell("ИСЦЕЛЕНИЕ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ИСЦЕЛЕНИЕ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 448------------------------------------
            elif self.page_number == 448:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.open_window_448()
                if self.ui.lineEdit.text() == '2' or self.ui.lineEdit.text() == '235':
                    if self.buying448_is_over == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        message_merchant448_not_finished = QMessageBox()
                        message_merchant448_not_finished.setWindowTitle("!!!")
                        message_merchant448_not_finished.setText("Завершите покупки и закройте окно торговли!")
                        font_448 = QFont()
                        font_448.setPointSize(14)
                        message_merchant448_not_finished.setFont(font_448)
                        message_merchant448_not_finished.exec_()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 449------------------------------------
            elif self.page_number == 449:
                self.read_page_text()
                if self.ui.lineEdit.text() == '396' or self.ui.lineEdit.text() == '271':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 450------------------------------------
            elif self.page_number == 450:
                self.read_page_text()
                if self.ui.lineEdit.text() == '292' or self.ui.lineEdit.text() == '51' or self.ui.lineEdit.text() == '586':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 451------------------------------------
            elif self.page_number == 451:
                self.read_page_text()
                if self.ui.lineEdit.text() == '454':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 452------------------------------------
            elif self.page_number == 452:
                self.read_page_text()
                if self.ui.lineEdit.text() == '10':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 453------------------------------------
            elif self.page_number == 453:
                self.read_page_text()
                if self.ui.lineEdit.text() == '46':
                    stork_feather = Item("Перо аиста", "-") 
                    self.add_item_and_print_console(stork_feather)
                    self.add_item_to_table_widget(stork_feather)                 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 454------------------------------------
            elif self.page_number == 454:
                self.read_page_text()
                if self.ui.lineEdit.text() == '319' or self.ui.lineEdit.text() == '232':                                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 455------------------------------------
            elif self.page_number == 455:
                self.read_page_text()
                if self.ui.lineEdit.text() == '141':                                    
                    self.page_number = int(self.ui.lineEdit.text())         # выяснить, с какого параграфа пришёл (Трое из Эвенло)
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 456-----------------------------------
            elif self.page_number == 456:
                self.read_page_text()
                self.page_you_lost(456)


            # --------------------------------параграф 457------------------------------------
            elif self.page_number == 457:
                self.read_page_text()
                if self.ui.lineEdit.text() == '44':
                    bear_amulet = Item("Медвежий амулет", "-")
                    self.add_item_and_print_console(bear_amulet)
                    self.add_item_to_table_widget(bear_amulet)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 458------------------------------------
            elif self.page_number == 458:
                self.read_page_text()
                if self.ui.lineEdit.text() == '252' or self.ui.lineEdit.text() == '542':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 459------------------------------------
            elif self.page_number == 459:
                self.read_page_text()
                if self.ui.lineEdit.text() == '325' or self.ui.lineEdit.text() == '255' or self.ui.lineEdit.text() == '399':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 460------------------------------------
            elif self.page_number == 460:
                self.read_page_text()
                # Серебряный свисток - пришёл с п.147
                if self.ui.lineEdit.text() == '537' or self.ui.lineEdit.text() == '348':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '587':
                    silver_whistle = Item("Серебряный свисток", "-")
                    # удалить серебряный свисток из инвентаря
                    self.delete_item(silver_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 461------------------------------------
            elif self.page_number == 461:
                self.read_page_text()
                if self.ui.lineEdit.text() == '340' or self.ui.lineEdit.text() == '442':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 462------------------------------------
            elif self.page_number == 462:
                self.read_page_text()
                if self.ui.lineEdit.text() == '178' or self.ui.lineEdit.text() == '333':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 463------------------------------------
            elif self.page_number == 463:
                self.read_page_text()
                if self.ui.lineEdit.text() == '158' or self.ui.lineEdit.text() == '308':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 464------------------------------------
            elif self.page_number == 464:
                self.read_page_text()
                if self.ui.lineEdit.text() == '55':
                    if self.window464_is_closed == True:
                        #! кольцо с бриллиантом записывается в п.600 после отдачи заклинания старичку                   
                        deer_skin = Item("Шкура оленя", "-")
                        self.add_item_and_print_console(deer_skin)
                        self.add_item_to_table_widget(deer_skin)
                        secret_door = Item("Потайная дверца", "п.260")
                        self.add_item_and_print_console(secret_door)
                        self.add_item_to_table_widget(secret_door)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        message_no_item_in_bag = QMessageBox()
                        message_no_item_in_bag.setWindowTitle("!!!")
                        message_no_item_in_bag.setText("Выберите заклинание или закройте окно")
                        font_not_enough_gold = QFont()
                        font_not_enough_gold.setPointSize(14)
                        message_no_item_in_bag.setFont(font_not_enough_gold)
                        message_no_item_in_bag.exec_()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '600':
                    self.open_window_464()
                    return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 465------------------------------------
            elif self.page_number == 465:
                self.read_page_text()
                if self.ui.lineEdit.text() == '140':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 466------------------------------------
            elif self.page_number == 466:
                self.read_page_text()
                if self.ui.lineEdit.text() == '352':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 467------------------------------------
            elif self.page_number == 467:
                self.read_page_text()
                if self.ui.lineEdit.text() == '182':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '527':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 468------------------------------------
            elif self.page_number == 468:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 469------------------------------------
            elif self.page_number == 469:
                self.read_page_text()
                if self.ui.lineEdit.text() == '257':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    print("-2 выносливости")                   
                    self.page_number = 706
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 470------------------------------------
            elif self.page_number == 470:
                self.read_page_text()
                if self.ui.lineEdit.text() == '221' or self.ui.lineEdit.text() == '55':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 471------------------------------------
            elif self.page_number == 471:
                self.read_page_text()
                if self.ui.lineEdit.text() == '80':
                    black_arrow = Item("Черная стрела", "-")
                    self.add_item_and_print_console(black_arrow)
                    self.add_item_to_table_widget(black_arrow)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 472------------------------------------
            elif self.page_number == 472:
                self.read_page_text()
                message_checking_luck_472 = QMessageBox()
                name_of_opening_file_472 = "Page472.txt"
                file_name_to_str_472 = Path("GameText", name_of_opening_file_472)
                page_file_472 = open(file_name_to_str_472, "r")
                text_from_page_files_472 = page_file_472.read()
                message_checking_luck_472.setText(text_from_page_files_472)
                del text_from_page_files_472
                page_file_472.close()
                message_checking_luck_472.setWindowTitle("Удача")
                font_checking_luck_472 = QFont()
                font_checking_luck_472.setPointSize(14)
                message_checking_luck_472.setFont(font_checking_luck_472)
                message_checking_luck_472.exec_()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    if self.player1.checking_luck():
                        self.page_number = 588
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        message_page_472 = QMessageBox()
                        message_page_472.setText("Переход к параграфу 588")
                        message_page_472.setWindowTitle("------>>")
                        font_page_472 = QFont()
                        font_page_472.setPointSize(14)
                        message_page_472.setFont(font_page_472)
                        message_page_472.exec_()
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.page_number = 391
                        self.player1.luck -= 1
                        self.strength_stamina_luck_information()
                        message2_page_472 = QMessageBox()
                        message2_page_472.setText("Переход к параграфу 391")
                        message2_page_472.setWindowTitle("------>>")
                        font_page_472 = QFont()
                        font_page_472.setPointSize(14)
                        message2_page_472.setFont(font_page_472)
                        message2_page_472.exec_()
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)


            # --------------------------------параграф 473------------------------------------
            elif self.page_number == 473:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 474------------------------------------
            elif self.page_number == 474:
                self.read_page_text()
                if self.ui.lineEdit.text() == '159' or self.ui.lineEdit.text() == '540' or self.ui.lineEdit.text() == '380' or self.ui.lineEdit.text() == '39':
                    self.player1.strength -= 1
                    print("-1 мастерство")
                    self.strength_stamina_luck_information()
                    self.losing_life_points(3)
                    print("-3 выносливости")
                    self.strength_stamina_luck_information()                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 475------------------------------------
            elif self.page_number == 475:
                self.read_page_text()
                if self.ui.lineEdit.text() == '589':
                    self.player1.princess_is_saved = True                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '617':
                    if self.player1.barlad_dart_is_dead == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        message_475 = QMessageBox()
                        message2_475 = QMessageBox()
                        message_475.setWindowTitle("!!!")
                        message2_475.setWindowTitle("------->>")
                        message_475.setText("Барлад Дэрт еще жив!")
                        message2_475.setText("Переход к параграфу 589")
                        font_475 = QFont()
                        font_475.setPointSize(14)
                        message_475.setFont(font_475)
                        message2_475.setFont(font_475)
                        message_475.exec_()
                        message2_475.exec_()
                        self.page_number = 589
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 476------------------------------------
            elif self.page_number == 476:
                self.read_page_text()
                if self.ui.lineEdit.text() == '347':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 477------------------------------------
            elif self.page_number == 477:
                self.read_page_text()
                if self.ui.lineEdit.text() == '106': 
                    self.player1.gold += 10
                    self.gold_food_water_information()  
                    apple = Item("Яблоко", "+1 выносл.")
                    self.add_item_and_print_console(apple)
                    self.add_item_to_table_widget(apple)
                    mandarine = Item("Мандарин", "+2 выносл.")
                    self.add_item_and_print_console(mandarine)
                    self.add_item_to_table_widget(mandarine)
                    orange = Item("Апельсин", "+1 выносл.")
                    self.add_item_and_print_console(orange)
                    self.add_item_to_table_widget(orange)
                    banana = Item("Банан", "+2 к выносл.")
                    self.add_item_and_print_console(banana)
                    self.add_item_to_table_widget(banana)
                    self.player1.water = 2    
                    self.player1.luck -= 1
                    print("-1 удача")
                    self.strength_stamina_luck_information()              
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 478------------------------------------
            elif self.page_number == 478:
                self.read_page_text()
                if self.ui.lineEdit.text() == '320' or self.ui.lineEdit.text() == '534':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 479------------------------------------
            elif self.page_number == 479:
                self.read_page_text()
                # использование серебряного сосуда (с п.536)
                if self.ui.lineEdit.text() == '392':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '590':
                    silver_vial = Item("Серебряный сосуд", "-")
                    # удалить серебряный сосуд из инвентаря
                    self.delete_item(silver_vial)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 480------------------------------------
            elif self.page_number == 480:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image480 = QMessageBox(self)
                    message_image480.setWindowTitle("Библиотекарь")
                    message_image480.setIconPixmap(QPixmap("GameText\Page480.png"))
                    message_image480.show()
                if self.ui.lineEdit.text() == '45' or self.ui.lineEdit.text() == '345' or self.ui.lineEdit.text() == '208' or self.ui.lineEdit.text() == '591':                
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '455':
                    three_from_evenlo = Item("'Трое из Эвенло'", "-25")
                    if self.checking_bag_item(three_from_evenlo):    
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 481------------------------------------
            elif self.page_number == 481:
                self.read_page_text()
                if self.ui.lineEdit.text() == '60': 
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()               
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 482------------------------------------
            elif self.page_number == 482:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 483------------------------------------
            elif self.page_number == 483:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39' or self.ui.lineEdit.text() == '566':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()                                            
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number    
                elif self.ui.lineEdit.text() == '609':
                    pegasus = Item("Вызов пегаса", "п.609")
                    if self.checking_bag_item(pegasus):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        print(self.player1.spells)
                elif self.ui.lineEdit.text() == '715':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнение к п.483
            elif self.page_number == 715:
                self.read_page_text()
                self.page_you_lost(715)


            # --------------------------------параграф 484------------------------------------
            elif self.page_number == 484:
                self.read_page_text()
                if self.ui.lineEdit.text() == '308':
                    self.player1.gold += 3
                    print("+3 золотых")
                    self.gold_food_water_information()
                    bronze_whistle = Item("Бронзовый свисток", "-")
                    self.add_item_and_print_console(bronze_whistle)
                    self.add_item_to_table_widget(bronze_whistle)
                    copper_bracelet = Item("Медный браслет", "-")
                    self.add_item_and_print_console(copper_bracelet)
                    self.add_item_to_table_widget(copper_bracelet)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 485------------------------------------
            elif self.page_number == 485:
                self.read_page_text()
                if self.ui.lineEdit.text() == '472' or self.ui.lineEdit.text() == '275':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 486------------------------------------
            elif self.page_number == 486:
                self.read_page_text()
                if self.ui.lineEdit.text() == '570' or self.ui.lineEdit.text() == '91' or self.ui.lineEdit.text() == '295':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 487------------------------------------
            elif self.page_number == 487:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    if self.player1.strength_spell == True:
                        self.player1.strength += 2
                        print("Применено заклинание Силы, +2 к мастерству")
                        self.strength_stamina_luck_information()

                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page487 = QMessageBox()
                        message1_page487.setWindowTitle("Параграф 487")
                        font_page487 = QFont()
                        font_page487.setPointSize(14)
                        message1_page487.setFont(font_page487)
                        message1_page487.setText("Хотите использовать заклинание копии?")
                        message1_page487.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m487 = message1_page487.exec_()
                        if m487 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_487_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_487()
                            self.strength_stamina_luck_information()
                            print("Игрок победил орков")
                    else:                       
                        self.player1.battleground_487()
                        self.strength_stamina_luck_information()
                        print("Игрок победил орков")

                    self.strength_stamina_luck_information()

                    if self.player1.strength_spell == True:
                        self.player1.strength_spell = False
                        self.player1.strength -= 2
                        print("Действие заклинания Силы закончилось. -2 к мастерству.")
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '100':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 488------------------------------------
            elif self.page_number == 488:
                self.read_page_text()
                # применение Пера аиста в диалоге с Драконом (п.516)
                if self.ui.lineEdit.text() == '454':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 489------------------------------------
            elif self.page_number == 489:
                self.read_page_text()
                if self.ui.lineEdit.text() == '501' or self.ui.lineEdit.text() == '547':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 490------------------------------------
            elif self.page_number == 490:
                self.read_page_text()
                if self.ui.lineEdit.text() == '255':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 491-----------------------------------
            elif self.page_number == 491:
                self.read_page_text()
                message_page491 = QMessageBox(self)
                message_page491.resize(1000, 1000)
                message_page491.setWindowTitle("Удача")
                font491 = QFont()
                font491.setPointSize(14)
                message_page491.setFont(font491)               
                message_page491.setText("Проверьте свою удачу!")
                message_page491.exec_()
                print("Проверка удачи")
                if self.player1.checking_luck() == True:
                    self.page_number = 571
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message2_page491 = QMessageBox(self)
                    message2_page491.resize(1000, 1000)
                    message2_page491.setWindowTitle("------->>")
                    font491 = QFont()
                    font491.setPointSize(14)
                    message2_page491.setFont(font491)               
                    message2_page491.setText("Переход к параграфу 571")
                    message2_page491.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_number = 593
                    self.player1.luck -= 1
                    self.strength_stamina_luck_information()
                    message3_page491 = QMessageBox(self)
                    message3_page491.resize(1000, 1000)
                    message3_page491.setWindowTitle("------->>")
                    font491 = QFont()
                    font491.setPointSize(14)
                    message3_page491.setFont(font491)               
                    message3_page491.setText("Переход к параграфу 593")
                    message3_page491.exec_()
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)


            # --------------------------------параграф 492------------------------------------
            elif self.page_number == 492:
                self.read_page_text()
                if self.ui.lineEdit.text() == '151':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 493------------------------------------
            elif self.page_number == 493:
                self.read_page_text()
                self.page_you_lost(493)


            # --------------------------------параграф 494------------------------------------
            elif self.page_number == 494:
                self.read_page_text()
                self.page_you_lost(494)


            # --------------------------------параграф 495------------------------------------
            elif self.page_number == 495:
                self.read_page_text()
                if self.ui.lineEdit.text() == '325':
                    self.player1.luck += 1
                    self.strength_stamina_luck_information()
                    print("+1 удача")
                    mirrors = Item("Секрет зеркал", "-13")
                    self.add_item_and_print_console(mirrors)
                    self.add_item_to_table_widget(mirrors)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 496------------------------------------
            elif self.page_number == 496:
                self.read_page_text()
                if self.ui.lineEdit.text() == '402' or self.ui.lineEdit.text() == '547' or self.ui.lineEdit.text() == '501':
                    candlestick = Item("Подсвечник", "-")
                    self.add_item_and_print_console(candlestick)
                    self.add_item_to_table_widget(candlestick)
                    rope = Item("Веревка", "-")
                    self.add_item_and_print_console(rope)
                    self.add_item_to_table_widget(rope)
                    whip = Item("Кнут", "-")
                    self.add_item_and_print_console(whip)
                    self.add_item_to_table_widget(whip)              
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 497------------------------------------
            elif self.page_number == 497:
                self.read_page_text()
                if self.ui.lineEdit.text() == '572':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 498------------------------------------
            elif self.page_number == 498:
                self.read_page_text()
                if self.ui.lineEdit.text() == '300':
                    self.player1.strength += 1
                    self.strength_stamina_luck_information()
                    print("+1 мастерство")
                    shield = Item("Щит", "-")
                    self.add_item_and_print_console(shield)
                    self.add_item_to_table_widget(shield)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 499------------------------------------
            elif self.page_number == 499:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page499 = QMessageBox()
                    message_page499.setWindowTitle("Параграф 499")
                    font_message_page499 = QFont()
                    font_message_page499.setPointSize(14)
                    message_page499.setFont(self.font_for_messageboxes)
                    text_message499 = ""
                    text_message499 += "Вы накладываете заклятие Огня, и возникший в воздухе огненный шар испепеляет расспрашивавшего "
                    text_message499 += "вас Орка. Остаются двое: один в ужасе убегает в лес, бросив у ворот оружие, а второй принимает ваш вызов."
                    message_page499.setText(text_message499)
                    message_page499.exec_()

                    print("Битва с орком")
                    self.player1.battleground_one("Орк", 7, 7)
                    print("Игрок победил орка")
                    self.strength_stamina_luck_information()
            
                if self.ui.lineEdit.text() == '48':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 500------------------------------------
            elif self.page_number == 500:
                self.read_page_text()
                if self.ui.lineEdit.text() == '416':
                    self.life_points_recovery(6)
                    self.strength_stamina_luck_information()
                    print("+6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 501------------------------------------
            elif self.page_number == 501:
                self.read_page_text()
                if self.ui.lineEdit.text() == '534':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 502------------------------------------
            elif self.page_number == 502:
                self.read_page_text()
                self.page_you_lost(502)


            # --------------------------------параграф 503------------------------------------
            elif self.page_number == 503:
                self.read_page_text()
                if self.ui.lineEdit.text() == '125':
                    hyena = Item("'Привет от гиены'", "'Гиена'") 
                    self.add_item_and_print_console(hyena)
                    self.add_item_to_table_widget(hyena)                 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 504------------------------------------
            elif self.page_number == 504:
                self.read_page_text()
                if self.ui.lineEdit.text() == '332':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 505------------------------------------
            elif self.page_number == 505:
                self.read_page_text()
                if self.ui.lineEdit.text() == '337' or self.ui.lineEdit.text() == '393' or self.ui.lineEdit.text() == '595':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 506------------------------------------
            elif self.page_number == 506:
                self.read_page_text()
                if self.ui.lineEdit.text() == '100':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 507------------------------------------
            elif self.page_number == 507:
                self.read_page_text()
                if self.ui.lineEdit.text() == '598' or self.ui.lineEdit.text() == '501':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 508------------------------------------
            elif self.page_number == 508:
                self.read_page_text()
                if self.ui.lineEdit.text() == '366':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 509------------------------------------
            elif self.page_number == 509:
                self.read_page_text()
                if self.ui.lineEdit.text() == '119':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 510------------------------------------
            elif self.page_number == 510:
                self.read_page_text()
                if self.ui.lineEdit.text() == '38' or self.ui.lineEdit.text() == '214':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 511------------------------------------
            elif self.page_number == 511:
                self.read_page_text()
                if self.ui.lineEdit.text() == '544':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 512------------------------------------
            elif self.page_number == 512:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    print("-2 выносливости")                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 513------------------------------------
            elif self.page_number == 513:
                self.read_page_text()
                if self.ui.lineEdit.text() == '41':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ОГОНЬ")
                        # # распечатаем в консоли список заклинаний
                        # print(self.player1.spells)
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                elif self.ui.lineEdit.text() == '476':
                    # заклинание подействует, но будет конец игры (поэтому не надо описывать +2 мастерства)
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СИЛА")
                        # # распечатаем в консоли список заклинаний
                        # print(self.player1.spells)
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '172':
                    # заклинание подействует, но будет конец игры
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("СЛАБОСТЬ")
                        # # распечатаем в консоли список заклинаний
                        # print(self.player1.spells)
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number
                elif self.ui.lineEdit.text() == '347': 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '601': 
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 514------------------------------------
            elif self.page_number == 514:
                self.read_page_text()
                if self.ui.lineEdit.text() == '358' or self.ui.lineEdit.text() == '441':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 515------------------------------------
            elif self.page_number == 515:
                self.read_page_text()
                if self.ui.lineEdit.text() == '98':
                    self.losing_life_points(8)
                    print("-8 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 516------------------------------------
            elif self.page_number == 516:
                self.read_page_text()
                if self.ui.lineEdit.text() == '134':
                    dragon_claw = Item("Коготь дракона", "-")
                    if self.checking_bag_item(dragon_claw) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '42':
                    diamond = Item("Бриллиант", "-")
                    if self.checking_bag_item(diamond) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '161':
                    comb = Item("Гребень", "-")
                    if self.checking_bag_item(comb) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '488':
                    stork_feather = Item("Перо аиста", "-")
                    if self.checking_bag_item(stork_feather) == True:
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '316':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 517------------------------------------
            elif self.page_number == 517:
                self.read_page_text()
                if self.ui.lineEdit.text() == '359':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '105':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")
                        # # распечатаем в консоли список заклинаний
                        # print(self.player1.spells)
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        # если заклинания нет в списке
                        self.ui.lineEdit.clear()
                        self.using_spell_error()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 518------------------------------------
            elif self.page_number == 518:
                self.read_page_text()               
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    message_page518 = QMessageBox()
                    message_page518.setWindowTitle("Параграф 518")
                    font_message_page518 = QFont()
                    font_message_page518.setPointSize(14)
                    message_page518.setFont(self.font_for_messageboxes)
                    text_page518 = ""
                    text_page518 += "Вы обнажаете меч и кидаетесь в бой. Торговец неповоротлив, но удар его очень силен."
                    text_page518 += "Поэтому всякий раз, когда он ранит вас, вычитайте у себя не 2, а 3 ВЫНОСЛИВОСТИ."
                    message_page518.setText(text_page518)
                    message_page518.exec_()

                    print("Битва с торговцем")
                    self.player1.battleground_518()
                    print("Игрок победил торговца")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '477':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 


            # --------------------------------параграф 519------------------------------------
            elif self.page_number == 519:
                self.read_page_text()
                if self.ui.lineEdit.text() == '278' or self.ui.lineEdit.text() == '43' or self.ui.lineEdit.text() == '136':                                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 520------------------------------------
            elif self.page_number == 520:
                self.read_page_text()
                if self.ui.lineEdit.text() == '3':
                    pocket_mirror = Item("Зеркальце", "-")
                    self.add_item_and_print_console(pocket_mirror)
                    self.add_item_to_table_widget(pocket_mirror)
                    gold_whistle = Item("Золотой свисток", "-")
                    self.add_item_and_print_console(gold_whistle)
                    self.add_item_to_table_widget(gold_whistle)
                    three_from_evenlo = Item("'Трое из Эвенло'", "-25")
                    self.add_item_and_print_console(three_from_evenlo)
                    self.add_item_to_table_widget(three_from_evenlo)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 521------------------------------------
            elif self.page_number == 521:
                self.read_page_text()
                if self.ui.lineEdit.text() == '326':
                    self.losing_life_points(2)
                    print("-2 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 522------------------------------------
            elif self.page_number == 522:
                self.read_page_text()
                if self.ui.lineEdit.text() == '252' or self.ui.lineEdit.text() == '542':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 523------------------------------------
            elif self.page_number == 523:
                self.read_page_text()
                if self.ui.lineEdit.text() == '39':
                    self.losing_life_points(6)
                    self.strength_stamina_luck_information()
                    print("-6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 524------------------------------------
            elif self.page_number == 524:
                self.read_page_text()
                if self.ui.lineEdit.text() == '89' or self.ui.lineEdit.text() == '616':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 525------------------------------------
            elif self.page_number == 525:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page525 = QMessageBox(self)
                    message_page525.setWindowTitle("Обезьяна")
                    message_page525.setIconPixmap(QPixmap("GameText\Page525.png"))
                    message_page525.show()
                if self.ui.lineEdit.text() == '349':
                    banana = Item("Банан", "+2 к выносл.")
                    if self.checking_bag_item(banana):
                        # удалить банан из сумки
                        self.delete_item(banana)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                elif self.ui.lineEdit.text() == '215':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 526------------------------------------
            elif self.page_number == 526:
                self.read_page_text()
                if self.ui.lineEdit.text() == '2' or self.ui.lineEdit.text() == '235':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 527------------------------------------
            elif self.page_number == 527:
                self.read_page_text()
                if self.ui.lineEdit.text() == '182':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 528------------------------------------
            elif self.page_number == 528:
                self.read_page_text()

                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с оборотнем") 
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page528 = QMessageBox()
                        message1_page528.setWindowTitle("Параграф 528")
                        font_page528 = QFont()
                        font_page528.setPointSize(14)
                        message1_page528.setFont(font_page528)
                        message1_page528.setText("Хотите использовать заклинание копии?")
                        message1_page528.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m528 = message1_page528.exec_()
                        if m528 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_one_copy_spell("Оборотень", 10, 10)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_one("Оборотень", 10, 10)
                            self.strength_stamina_luck_information()
                            print("Игрок победил оборотня")
                    else:                       
                        self.player1.battleground_one("Оборотень", 10, 10)
                        self.strength_stamina_luck_information()
                        print("Игрок победил оборотня")

                    print("Игрок победил оборотня")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '240':
                    talisman = Item("Оберег", "-")
                    self.add_item_and_print_console(talisman)
                    self.add_item_to_table_widget(talisman)                  
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 529------------------------------------
            elif self.page_number == 529:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                   
                    message_page529 = QMessageBox()
                    message_page529.setWindowTitle("Параграф 529")
                    font_page529 = QFont()
                    font_page529.setPointSize(14)
                    message_page529.setFont(self.font_for_messageboxes)
                    text1_page529 = ""
                    text1_page529 += "Вы можете воспользоваться заклятием Силы, увеличив на 2 свою СИЛУ УДАРА, или заклятием Слабости, "
                    text1_page529 += "уменьшив на 2 СИЛУ УДАРА медведицы, а также заклятием Копии."
                    message_page529.setText(text1_page529)
                    message_page529.exec_()

                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        message2_page529 = QMessageBox()
                        message2_page529.setWindowTitle("Параграф 529")
                        font_page529 = QFont()
                        font_page529.setPointSize(14)
                        message2_page529.setFont(font_page529)
                        message2_page529.setText("Хотите воспользоваться заклинанием Силы?")
                        message2_page529.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m529_2 = message2_page529.exec_()
                        if m529_2 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СИЛА")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            # индикатор применения заклинания Силы
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 720
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue

                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        message3_page529 = QMessageBox()
                        message3_page529.setWindowTitle("Параграф 529")
                        font_page529 = QFont()
                        font_page529.setPointSize(14)
                        message3_page529.setFont(font_page529)
                        message3_page529.setText("Хотите воспользоваться заклинанием Слабости?")
                        message3_page529.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m529_3 = message3_page529.exec_()
                        if m529_3 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СЛАБОСТЬ")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 721
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue    

                    print("Битва с медведицей") 
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page529 = QMessageBox()
                        message1_page529.setWindowTitle("Параграф 529")
                        font_page529 = QFont()
                        font_page529.setPointSize(14)
                        message1_page529.setFont(font_page529)
                        message1_page529.setText("Хотите использовать заклинание копии?")
                        message1_page529.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m529 = message1_page529.exec_()
                        if m529 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_one_copy_spell("Медведица", 8, 10)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_one("Медведица", 8, 10)
                            self.strength_stamina_luck_information()
                            print("Игрок победил медведицу")
                    else:                       
                        self.player1.battleground_one("Медведица", 8, 10)
                        self.strength_stamina_luck_information()
                        print("Игрок победил медведицу")    
                    self.player1.battleground()
                    print("Игрок победил медведицу")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.529
            elif self.page_number == 720:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    self.player1.strength += 2
                    self.strength_stamina_luck_information()
                    print("+2 к мастерству")
                    print("Битва с медведицей")

                    self.player1.battleground_one("Медведица", 8, 10)

                    print("Игрок победил медведицу")
                    print("Действие заклинания Силы закончилось, -2 мастерства")
                    self.player1.strength -= 2
                    self.player1.strength_spell = False
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # второй дополнительный параграф к п.529
            elif self.page_number == 721:
                self.read_page_text() 
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Битва с медведицей")
                    self.player1.battleground_one("Медведица", 6, 10)
                    print("Игрок победил медведицу")

                if self.ui.lineEdit.text() == '44':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number             



            # --------------------------------параграф 530------------------------------------
            elif self.page_number == 530:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 531------------------------------------
            elif self.page_number == 531:
                self.read_page_text()
                if self.ui.lineEdit.text() == '49' or self.ui.lineEdit.text() == '338':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 532------------------------------------
            elif self.page_number == 532:
                self.read_page_text()
                if self.ui.lineEdit.text() == '716':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                elif self.ui.lineEdit.text() == '552':
                    paper_pass = Item("Пропуск", "+20")
                    if self.checking_bag_item(paper_pass):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '592':
                    green_armor = Item("Зеленые латы", "+60")
                    if self.checking_bag_item(green_armor):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.532
            elif self.page_number == 716:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0

                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        message2_page532 = QMessageBox()
                        message2_page532.setWindowTitle("Параграф 532")
                        font_page532 = QFont()
                        font_page532.setPointSize(14)
                        message2_page532.setFont(font_page532)
                        message2_page532.setText("Хотите воспользоваться заклинанием Силы?")
                        message2_page532.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m532_2 = message2_page532.exec_()
                        if m532_2 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СИЛА")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            # индикатор применения заклинания Силы
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 722
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue

                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        message3_page532 = QMessageBox()
                        message3_page532.setWindowTitle("Параграф 532")
                        font_page532 = QFont()
                        font_page532.setPointSize(14)
                        message3_page532.setFont(font_page532)
                        message3_page532.setText("Хотите воспользоваться заклинанием Слабости?")
                        message3_page532.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m532_3 = message3_page532.exec_()
                        if m532_3 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СЛАБОСТЬ")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 723
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue    

                    print("Бой с двумя гоблинами") 
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):                     # нужны 2 доп.параграфа для Силы и Слабости
                        message1_page532 = QMessageBox()
                        message1_page532.setWindowTitle("Параграф 532")
                        font_page532 = QFont()
                        font_page532.setPointSize(14)
                        message1_page532.setFont(font_page532)
                        message1_page532.setText("Хотите использовать заклинание копии?")
                        message1_page532.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m532 = message1_page532.exec_()
                        if m532 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_two_copy_spell("Первый гоблин", 8, 10, "Второй гоблин", 6, 8)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_two("Первый гоблин", 8, 10, "Второй гоблин", 6, 8)
                            self.strength_stamina_luck_information()
                            print("Игрок победил гоблинов")
                    else:                       
                        self.player1.battleground_two("Первый гоблин", 8, 10, "Второй гоблин", 6, 8)
                        self.strength_stamina_luck_information()
                        print("Игрок победил гоблинов")
                    self.strength_stamina_luck_information()
                    print("Игрок победил гоблинов")

                if self.ui.lineEdit.text() == '323':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # второй дополнительный параграф к п.532
            elif self.page_number == 722:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    self.player1.strength += 2
                    print("Применено заклинание Силы, +2 мастерства до окончания боя")
                    print("Бой с гоблинами")
                    self.strength_stamina_luck_information()

                    self.player1.battleground_two("Первый гоблин", 8, 10, "Второй гоблин", 6, 8)

                    print("Игрок победил гоблинов")
                    self.player1.strength -= 2
                    print("Заклинание Силы прекратило действие, -2 к мастерству")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '323':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number 

            # третий дополнительный параграф к п.532
            elif self.page_number == 723:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Бой с гоблинами")

                    self.player1.battleground_two("Первый гоблин", 6, 10, "Второй гоблин", 6, 8)

                    print("Игрок победил гоблинов")                   
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '323':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number                           



            # --------------------------------параграф 533------------------------------------
            elif self.page_number == 533:
                self.read_page_text()
                if self.ui.lineEdit.text() == '137' or self.ui.lineEdit.text() == '522':         # удалить белую стрелу из мешка (сломана)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 534------------------------------------
            elif self.page_number == 534:
                self.read_page_text()
                if self.ui.lineEdit.text() == '478' or self.ui.lineEdit.text() == '603' or self.ui.lineEdit.text() == '282':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '71':
                    white_arrow = Item("Белая стрела", "-")
                    if self.checking_bag_item(white_arrow) == True:
                        # удаляем белую стрелу из инвентаря
                        self.delete_item(white_arrow)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number 
                elif self.ui.lineEdit.text() == '362':
                    badge_with_eagle = Item("Бляха с орлом", "-")
                    if self.checking_bag_item(badge_with_eagle) == True:
                        # удаляем бляху с орлом из инвентаря
                        self.delete_item(badge_with_eagle)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number           
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 535------------------------------------
            elif self.page_number == 535:
                self.read_page_text()
                if self.ui.lineEdit.text() == '55':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 536------------------------------------
            elif self.page_number == 536:
                self.read_page_text()
                if self.ui.lineEdit.text() == '283' or self.ui.lineEdit.text() == '567':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '363':
                    talisman = Item("Оберег", "-")
                    if self.checking_bag_item(talisman):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '479':
                    silver_vial = Item("Серебряный сосуд", "-")
                    if self.checking_bag_item(silver_vial):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number        
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 537------------------------------------
            elif self.page_number == 537:
                self.read_page_text()
                if self.ui.lineEdit.text() == '140':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 538------------------------------------
            elif self.page_number == 538:
                self.read_page_text()
                if self.ui.lineEdit.text() == '68':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '370':
                    if self.player1.check_for_use_necessary_spell("ИЛЛЮЗИЯ") == True:
                        # если заклинание есть в списке, оно удаляется (1 штука)
                        self.player1.spells.remove("ИЛЛЮЗИЯ")
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number     
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 539------------------------------------
            elif self.page_number == 539:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    message1_page539 = QMessageBox()
                    message1_page539.setWindowTitle("Параграф 539")
                    font_page539 = QFont()
                    font_page539.setPointSize(14)
                    message1_page539.setFont(self.font_for_messageboxes)
                    message1_page539.setText("Гоблин успевает позвать на помощь. Вам же приходится обнажать меч и драться.")
                    message1_page539.exec_()

                    print("Сражение с первым гоблином")
                    self.player1.battleground_one("Первый гоблин", 4, 7)
                    print("Игрок победил первого гоблина")
                    self.strength_stamina_luck_information()

                    message2_page539 = QMessageBox()
                    message2_page539.setWindowTitle("Параграф 539")
                    message2_page539.setFont(font_page539)
                    message2_page539.setText("Как только вы убиваете Гоблина, из дома появляется еще один. Он менее пьян и будет не столь легким противником.")
                    message2_page539.exec_()

                    print("Сражение со вторым гоблином")
                    self.player1.battleground_one("Первый гоблин", 8, 9)
                    print("Игрок победил второго гоблина")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '484' or self.ui.lineEdit.text() == '308':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 540------------------------------------
            elif self.page_number == 540:
                self.read_page_text()
                if self.ui.lineEdit.text() == '474' or self.ui.lineEdit.text() == '380' or self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                elif self.ui.lineEdit.text() == '284':
                    figure_key = Item("Фигурный ключ", "-")
                    if self.checking_bag_item(figure_key):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 541------------------------------------
            elif self.page_number == 541:
                self.read_page_text()
                if self.ui.lineEdit.text() == '494':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                elif self.ui.lineEdit.text() == '364':
                    green_sword = Item("Меч зел.рыцаря", "-")
                    if self.checking_bag_item(green_sword):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 542------------------------------------
            elif self.page_number == 542:
                self.read_page_text()
                if self.ui.lineEdit.text() == '411' or self.ui.lineEdit.text() == '578' or self.ui.lineEdit.text() == '80':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 543------------------------------------
            elif self.page_number == 543:
                self.read_page_text()
                if self.ui.lineEdit.text() == '365' or self.ui.lineEdit.text() == '717':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.543
            elif self.page_number == 717:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    print("Сражение с зеленым рыцарем")
                    self.player1.battleground_one("Зеленый рыцарь", 11, 14)
                    print("Игрок победил зеленого рыцаря")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '241':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 544------------------------------------
            elif self.page_number == 544:
                self.read_page_text()
                if self.ui.lineEdit.text() == '285' or self.ui.lineEdit.text() == '489':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 545------------------------------------
            elif self.page_number == 545:
                self.read_page_text()
                # Серебряный сосуд взят в п.350
                if self.ui.lineEdit.text() == '253' or self.ui.lineEdit.text() == '39':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 546------------------------------------
            elif self.page_number == 546:
                self.read_page_text()
                if self.ui.lineEdit.text() == '181':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 547------------------------------------
            elif self.page_number == 547:
                self.read_page_text()
                if self.ui.lineEdit.text() == '501':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '507':
                    metal_key = Item("Метал.ключ", "-40")
                    ring_with_diamond = Item("Кольцо с брил.", "-40")
                    if self.checking_bag_item(metal_key) or self.checking_bag_item(ring_with_diamond):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.warning_no_item_in_bag()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 548------------------------------------
            elif self.page_number == 548:
                self.read_page_text()
                if self.ui.lineEdit.text() == '297' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 549------------------------------------
            elif self.page_number == 549:
                self.read_page_text()
                if self.ui.lineEdit.text() == '285' or self.ui.lineEdit.text() == '489':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 550------------------------------------
            elif self.page_number == 550:
                self.read_page_text()
                if self.ui.lineEdit.text() == '607':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 551------------------------------------
            elif self.page_number == 551:
                self.read_page_text()
                if self.ui.lineEdit.text() == '255':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                elif self.ui.lineEdit.text() == '92':
                    pocket_mirror = Item("Зеркальце", "-")
                    if self.checking_bag_item(pocket_mirror):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '296':
                    comb = Item("Гребень", "-")                
                    if self.checking_bag_item(comb):
                        # удалить гребень из инвентаря
                        self.delete_item(comb)
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number
                elif self.ui.lineEdit.text() == '490':
                    talisman = Item("Оберег", "-")
                    if self.checking_bag_item(talisman):
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.ui.lineEdit.clear()
                        self.warning_no_item_in_bag()
                        return self.page_number                
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 552------------------------------------
            elif self.page_number == 552:
                self.read_page_text()
                if self.ui.lineEdit.text() == '323':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 553------------------------------------
            elif self.page_number == 553:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page553 = QMessageBox()
                    message_page553.setWindowTitle("Параграф 553")
                    font_page553 = QFont()
                    font_page553.setPointSize(14)
                    message_page553.setFont(self.font_for_messageboxes)
                    text_page553 = ""
                    text_page553 += "Первое, что вам бросается в глаза — огромный письменный стол посреди комнаты. "
                    text_page553 += "Он весь завален большими свитками, в которых без труда можно узнать карты. "
                    text_page553 += "Волшебник готовит нашествие на королевство — вы пришли как нельзя вовремя. "
                    text_page553 += "За столом — невысокий усталого вида человек, который оторвал взгляд от бумаг и смотрит на вас. "
                    text_page553 += "Неужели это и есть всемогущий маг? Но вы-то его представляли себе совсем другим. "
                    text_page553 += "Барлад Дэрт терпеливо смотрит некоторое время, потом щелкает пальцами, как бы совершая привычное и давно уже надоевшее ему действие. "
                    text_page553 += "Он обращает внимание на вас внимания не больше, чем на надоедливую муху. "
                    text_page553 += "После этого чародей вновь погружается в работу. А к вам приближается одна из фигур, стоявшая на постаменте в углу комнаты — вы сначала "
                    text_page553 += "приняли ее за скульптуру. Но колдовство оживило ее: к вам подходит отвратительная Гарпия — полуженщина-полуптица. "
                    text_page553 += "Вам придется драться с ней, надеясь только на себя да на заклятие Копии, если оно у вас есть."
                    message_page553.setText(text_page553)
                    message_page553.exec_()

                    pocket_mirror = Item("Зеркальце", "-")
                    if self.checking_bag_item(pocket_mirror):
                        message2_page553 = QMessageBox()
                        message2_page553.setWindowTitle("Параграф 553")
                        message2_page553.setFont(font_page553)
                        text2_page553 = ""
                        text2_page553 += "Вы кинули гарпии зеркальце, и она стала наслаждаться своим отражением. Больше она не обращает на вас внимания."
                        message2_page553.setText(text2_page553)
                        message2_page553.exec_()
                        self.delete_item(pocket_mirror)
                        self.page_number = 388
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                        continue
                    else:
                        print("Бой с гарпией")
                        if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                            message1_page553 = QMessageBox()
                            message1_page553.setWindowTitle("Параграф 553")
                            message1_page553.setFont(font_page553)
                            message1_page553.setText("Хотите использовать заклинание копии?")
                            message1_page553.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                            m553 = message1_page553.exec_()
                            if m553 == QMessageBox.Yes:
                                self.player1.spells.remove("КОПИЯ")                      
                                # обновим список заклинаний на экране в таблице
                                self.output_spells()
                                self.player1.battleground_one_copy_spell("Гарпия", 10, 12)
                                self.strength_stamina_luck_information()
                            else:
                                self.player1.battleground_one("Гарпия", 10, 12)
                                self.strength_stamina_luck_information()
                                print("Игрок победил гарпию")
                        else:                       
                            self.player1.battleground_one("Гарпия", 10, 12)
                            self.strength_stamina_luck_information()
                            print("Игрок побеждает гарпию")

                if self.ui.lineEdit.text() == '388':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 554------------------------------------
            elif self.page_number == 554:
                self.read_page_text()
                if self.ui.lineEdit.text() == '301':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 555------------------------------------
            elif self.page_number == 555:
                self.read_page_text()
                if self.ui.lineEdit.text() == '450':
                    clew = Item("Клубочек", "+30")
                    self.add_item_and_print_console(clew)
                    self.add_item_to_table_widget(clew)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 556------------------------------------
            elif self.page_number == 556:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_image556 = QMessageBox(self)
                    message_image556.setWindowTitle("Женщина-вампир")
                    message_image556.setIconPixmap(QPixmap("GameText\Page556.png"))
                    message_image556.show()
                if self.ui.lineEdit.text() == '394' or self.ui.lineEdit.text() == '93':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 557------------------------------------
            elif self.page_number == 557:
                self.read_page_text()
                if self.ui.lineEdit.text() == '120' or self.ui.lineEdit.text() == '416':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 558------------------------------------
            elif self.page_number == 558:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page558 = QMessageBox()
                    message_page558.setWindowTitle("Параграф 558")
                    font_page558 = QFont()
                    font_page558.setPointSize(14)
                    message_page558.setFont(self.font_for_messageboxes)
                    text_page558 = "Вам удается перерубить лестницу мечом и спрыгнуть на землю. "
                    text_page558 += "Конечно, Паук погонится за вами, но теперь вы будете драться на равных, "
                    text_page558 += "используя либо заклятие Силы, которое позволит вам прибавить 2 к вашей СИЛЕ УДАРА, либо заклятие Слабости, "
                    text_page558 += "которое позволит вычитать 2 из СИЛЫ УДАРА гигантского Паука, либо заклятие Копии."
                    message_page558.setText(text_page558)
                    message_page558.exec_()

                    print("Бой с гигиантским пауком")

                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        message2_page558 = QMessageBox()
                        message2_page558.setWindowTitle("Параграф 558")
                        font_page558 = QFont()
                        font_page558.setPointSize(14)
                        message2_page558.setFont(font_page558)
                        message2_page558.setText("Хотите воспользоваться заклинанием Силы?")
                        message2_page558.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m558_2 = message2_page558.exec_()
                        if m558_2 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СИЛА")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            # индикатор применения заклинания Силы
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 724
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue

                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        message3_page558 = QMessageBox()
                        message3_page558.setWindowTitle("Параграф 558")
                        font_page558 = QFont()
                        font_page558.setPointSize(14)
                        message3_page558.setFont(font_page558)
                        message3_page558.setText("Хотите воспользоваться заклинанием Слабости?")
                        message3_page558.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m558_3 = message3_page558.exec_()
                        if m558_3 == QMessageBox.Yes:
                            # если заклинание есть в списке, оно удаляется
                            self.player1.spells.remove("СЛАБОСТЬ")                    
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.strength_spell = True
                            # переход на следующую страницу
                            self.page_number = 725
                            self.ui.lineEdit.clear()
                            print("Next Page = ", self.page_number)
                            continue  

                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page558 = QMessageBox()
                        message1_page558.setWindowTitle("Параграф 558")
                        message1_page558.setFont(font_page558)
                        message1_page558.setText("Хотите использовать заклинание копии?")
                        message1_page558.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m558 = message1_page558.exec_()
                        if m558 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_one_copy_spell("Гигантский паук", 8, 8)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_one("Гигантский паук", 8, 8)
                            self.strength_stamina_luck_information()
                            print("Игрок победил гигантского паука")
                    else:                       
                        self.player1.battleground_one("Гигантский паук", 8, 8)
                        self.strength_stamina_luck_information()
                        print("Игрок победил гигантского паука")

                if self.ui.lineEdit.text() == '189':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.558
            elif self.page_number == 724:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.strength += 2
                    print("+2 к мастерству до окончания боя")
                    self.strength_stamina_luck_information()

                    self.player1.battleground_one("Гигантский паук", 8, 8)

                    self.player1.strength -= 2
                    print("Действие заклинания Силы окончено, -2 мастерства")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '189':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

             # второй дополнительный параграф к п.558
            elif self.page_number == 725:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    self.player1.battleground_one("Гигантский паук", 6, 8)

                if self.ui.lineEdit.text() == '189':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number            
                

            # --------------------------------параграф 559------------------------------------
            elif self.page_number == 559:
                self.read_page_text()
                if self.ui.lineEdit.text() == '184' or self.ui.lineEdit.text() == '13':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 560------------------------------------
            elif self.page_number == 560:
                self.read_page_text()
                if self.ui.lineEdit.text() == '165' or self.ui.lineEdit.text() == '288' or self.ui.lineEdit.text() == '493':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 561------------------------------------
            elif self.page_number == 561:
                self.read_page_text()
                if self.ui.lineEdit.text() == '192':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 562------------------------------------
            elif self.page_number == 562:
                self.read_page_text()
                if self.ui.lineEdit.text() == '613' or self.ui.lineEdit.text() == '65':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 563------------------------------------
            elif self.page_number == 563:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page563 = QMessageBox()
                    message_page563.setWindowTitle("Параграф 563")
                    font_page563 = QFont()
                    font_page563.setPointSize(14)
                    message_page563.setFont(self.font_for_messageboxes)
                    text_page563 = "Вы достаете меч и кидаетесь на Лесовичка. "
                    text_page563 += "Он немало удивлен, но готов дать отпор и вынимает свой меч, который вам кажется кинжалом."
                    message_page563.setText(text_page563)
                    message_page563.exec_()

                    print("Бой с лесовичком")
                    self.player1.battleground_one("Лесовичок", 6, 8)
                    print("Игрок победил лесовичка")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '450':
                    silver_whistle = Item("Серебряный свисток", "-")
                    self.add_item_and_print_console(silver_whistle)
                    self.add_item_to_table_widget(silver_whistle)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 564------------------------------------
            elif self.page_number == 564:
                self.read_page_text()
                if self.ui.lineEdit.text() == '480':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 565------------------------------------
            elif self.page_number == 565:
                self.read_page_text()
                if self.ui.lineEdit.text() == '94' or self.ui.lineEdit.text() == '469' or self.ui.lineEdit.text() == '298':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 566------------------------------------
            elif self.page_number == 566:
                self.read_page_text()
                if self.ui.lineEdit.text() == '556' or self.ui.lineEdit.text() == '277':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '483' or self.ui.lineEdit.text() == '39':
                    if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ЛЕВИТАЦИЯ")                    
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number    
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 567------------------------------------
            elif self.page_number == 567:
                self.read_page_text()
                if self.ui.lineEdit.text() == '395':
                    if self.player1.check_for_use_necessary_spell("СИЛА"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("СИЛА")                    
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.player1.strength_spell_567 = True
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '299':
                    if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("СЛАБОСТЬ")                    
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        self.player1.weakness_spell_567 = True
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '96':
                    if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
                        # если заклинание есть в списке, оно удаляется
                        self.player1.spells.remove("ОГОНЬ")                    
                        # обновим список заклинаний на экране в таблице
                        self.output_spells()
                        # переход на следующую страницу
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Next Page = ", self.page_number)
                    else:
                        self.using_spell_error()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '718':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)                         
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.567
            elif self.page_number == 718:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True

                    if self.player1.strength_spell_567 == True:
                        print("-2 мастерства, Рыцарь забрал заклинание Силы себе")
                        self.strength_stamina_luck_information()
                        print("Сражение с зеленым рыцарем")
                        self.player1.battleground_one("Зеленый рыцарь", 12, 10)
                        print("Игрок победил зеленого рыцаря")
                        self.strength_stamina_luck_information()
                    else:    
                        if self.player1.weakness_spell_567 == True:
                            self.player1.strength -= 2
                            print("-2 мастерства, Рыцарь отразил заклинание Слабости на игрока")
                            self.strength_stamina_luck_information()

                        print("Сражение с зеленым рыцарем")
                        self.player1.battleground_one("Зеленый рыцарь", 10, 10)
                        print("Игрок победил зеленого рыцаря")
                        self.strength_stamina_luck_information()

                    if self.player1.strength_spell_567 == True:
                        self.player1.strength_spell_567 = False
                        self.strength_stamina_luck_information()                 
                    
                    if self.player1.weakness_spell_567 == True:
                        self.player1.strength += 2
                        print("+2 мастерства, Рыцарь побежден, заклинание Слабости развеялось")
                        self.player1.weakness_spell_567 = False
                        self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '241':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 568------------------------------------
            elif self.page_number == 568:
                self.read_page_text()
                if self.ui.lineEdit.text() == '300':
                    sword_death_of_orcs = Item("Меч 'Смерть орков'", "-")
                    self.add_item_and_print_console(sword_death_of_orcs)
                    self.add_item_to_table_widget(sword_death_of_orcs)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 569------------------------------------
            elif self.page_number == 569:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    self.player1.round_number = 0
                    print("Битва с орками")
                    if self.player1.strength_spell == True:
                        self.player1.strength += 2 
                        self.strength_stamina_luck_information()

                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page569 = QMessageBox()
                        message1_page569.setWindowTitle("Параграф 569")
                        font_page569 = QFont()
                        font_page569.setPointSize(14)
                        message1_page569.setFont(font_page569)
                        message1_page569.setText("Хотите использовать заклинание копии?")
                        message1_page569.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m569 = message1_page569.exec_()
                        if m569 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_569_copy_spell()
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_569()
                            self.strength_stamina_luck_information()
                            print("Игрок победил орков")
                    else:                       
                        self.player1.battleground_569()
                        self.strength_stamina_luck_information()
                        print("Игрок победил орков")

                    if self.player1.strength_spell == True:
                        self.player1.strength_spell = False
                        self.player1.strength -= 2
                        self.strength_stamina_luck_information()
                    print("Игрок победил орков")
                    self.strength_stamina_luck_information()
                
                if self.ui.lineEdit.text() == '48':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 570------------------------------------
            elif self.page_number == 570:
                self.read_page_text()
                if self.ui.lineEdit.text() == '604':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 571------------------------------------
            elif self.page_number == 571:
                self.read_page_text()
                if self.ui.lineEdit.text() == '76':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 572------------------------------------
            elif self.page_number == 572:
                self.read_page_text()
                self.page_you_lost(572)


            # --------------------------------параграф 573------------------------------------
            elif self.page_number == 573:
                self.read_page_text()
                if self.ui.lineEdit.text() == '561' or self.ui.lineEdit.text() == '332':
                    candle = Item("Свеча", "+10")
                    self.add_item_and_print_console(candle)
                    self.add_item_to_table_widget(candle)
                    white_arrow = Item("Белая стрела", "-")
                    self.add_item_and_print_console(white_arrow)
                    self.add_item_to_table_widget(white_arrow)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 574------------------------------------
            elif self.page_number == 574:
                self.read_page_text()
                self.page_you_lost(574)


            # --------------------------------параграф 575------------------------------------
            elif self.page_number == 575:
                self.read_page_text()
                if self.ui.lineEdit.text() == '323':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 576------------------------------------
            elif self.page_number == 576:
                self.read_page_text()
                if self.ui.lineEdit.text() == '559' or self.ui.lineEdit.text() == '181' or self.ui.lineEdit.text() == '445':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 577------------------------------------
            elif self.page_number == 577:
                self.read_page_text()
                if self.ui.lineEdit.text() == '293':
                    self.player1.strength -= 1
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 578------------------------------------
            elif self.page_number == 578:
                self.read_page_text()
                if self.ui.lineEdit.text() == '411' or self.ui.lineEdit.text() == '80':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 579------------------------------------
            elif self.page_number == 579:
                self.read_page_text()
                self.page_you_lost(579)


            # --------------------------------параграф 580------------------------------------
            elif self.page_number == 580:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    
                    print("Сражение с двумя гоблинами")
                    if self.player1.check_for_use_necessary_spell("КОПИЯ"):
                        message1_page580 = QMessageBox()
                        message1_page580.setWindowTitle("Параграф 580")
                        font_page580 = QFont()
                        font_page580.setPointSize(14)
                        message1_page580.setFont(font_page580)
                        message1_page580.setText("Хотите использовать заклинание копии?")
                        message1_page580.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        m580 = message1_page580.exec_()
                        if m580 == QMessageBox.Yes:
                            self.player1.spells.remove("КОПИЯ")                      
                            # обновим список заклинаний на экране в таблице
                            self.output_spells()
                            self.player1.battleground_two_copy_spell("Второй гоблин", 7, 5, "Первый гоблин", 4, 9)
                            self.strength_stamina_luck_information()
                        else:
                            self.player1.battleground_two("Второй гоблин", 7, 5, "Первый гоблин", 4, 9)
                            self.strength_stamina_luck_information()
                            print("Игрок победил гоблинов")
                    else:                       
                        self.player1.battleground_two("Второй гоблин", 7, 5, "Первый гоблин", 4, 9)
                        self.strength_stamina_luck_information()
                        print("Игрок победил гоблинов")

                    print("Игрок победил гоблинов")
                    self.strength_stamina_luck_information()

                if self.ui.lineEdit.text() == '118':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number) 
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 581------------------------------------
            elif self.page_number == 581:
                self.read_page_text()
                self.page_you_lost(581)


            # --------------------------------параграф 582------------------------------------
            elif self.page_number == 582:
                self.read_page_text()
                if self.ui.lineEdit.text() == '74' or self.ui.lineEdit.text() == '174':
                    password_shield_of_darkness = Item("Пароль 'Щит тьмы'", "-")
                    self.add_item_and_print_console(password_shield_of_darkness)
                    self.add_item_to_table_widget(password_shield_of_darkness)
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 583------------------------------------
            elif self.page_number == 583:
                self.read_page_text()
                if self.ui.lineEdit.text() == '607' or self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206' or self.ui.lineEdit.text() == '350':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 584------------------------------------
            elif self.page_number == 584:
                self.read_page_text()
                if self.ui.lineEdit.text() == '616' or self.ui.lineEdit.text() == '89':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 585------------------------------------
            elif self.page_number == 585:
                self.read_page_text()
                if self.ui.lineEdit.text() == '428':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 586------------------------------------
            elif self.page_number == 586:
                self.read_page_text()
                if self.ui.lineEdit.text() == '608' or self.ui.lineEdit.text() == '6':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 587------------------------------------
            elif self.page_number == 587:
                self.read_page_text()
                if self.ui.lineEdit.text() == '348' or self.ui.lineEdit.text() == '537':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 588------------------------------------
            elif self.page_number == 588:
                self.read_page_text()
                if self.ui.lineEdit.text() == '275':
                    self.losing_life_points(6)
                    print("-6 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 589------------------------------------
            elif self.page_number == 589:
                self.read_page_text()
                if self.ui.lineEdit.text() == '266':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 590------------------------------------
            elif self.page_number == 590:
                self.read_page_text()
                if self.ui.lineEdit.text() == '241':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 591------------------------------------
            elif self.page_number == 591:
                self.read_page_text()
                if self.ui.lineEdit.text() == '139':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 592------------------------------------
            elif self.page_number == 592:
                self.read_page_text()
                if self.ui.lineEdit.text() == '323':                   
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 593------------------------------------
            elif self.page_number == 593:
                self.read_page_text()
                if self.ui.lineEdit.text() == '409':
                    self.losing_life_points(3)
                    print("-3 выносливости")
                    self.strength_stamina_luck_information()
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 594------------------------------------
            elif self.page_number == 594:
                self.read_page_text()
                if self.ui.lineEdit.text() == '553':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 595------------------------------------
            elif self.page_number == 595:
                self.read_page_text()
                if self.ui.lineEdit.text() == '393' or self.ui.lineEdit.text() == '337':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                elif self.ui.lineEdit.text() == '719':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number

            # дополнительный параграф к п.595
            elif self.page_number == 719:
                # бросаем два кубика, чтобы сломать дверь, нужно 1-1 или 6-6
                x1_719 = random.randint(1, 6)
                x2_719 = random.randint(1, 6)
                self.losing_life_points(1)
                self.strength_stamina_luck_information()
                print("-1 выносливость")
                if (x1_719 == x2_719 == 1) or (x1_719 == x2_719 == 6):
                    message_page719 = QMessageBox()
                    message_page719.setWindowTitle("Кидаем кубик")
                    message_page719.setText("На кубиках выпало: " + str(x1_719) + "-" + str(x2_719))
                    font_page719 = QFont()
                    font_page719.setPointSize(14)
                    message_page719.setFont(font_page719)
                    message_page719.exec_()
                    message2_page719 = QMessageBox()
                    message2_page719.setWindowTitle("------->>")
                    message2_page719.setText("Переход к параграфу 610")
                    message2_page719.setFont(font_page719)
                    message2_page719.exec_()
                    self.page_number = 610
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    message4_page719 = QMessageBox()
                    message4_page719.setWindowTitle("Кидаем кубик")
                    message4_page719.setText("На кубиках выпало: " + str(x1_719) + "-" + str(x2_719))
                    font_page719 = QFont()
                    font_page719.setPointSize(14)
                    message4_page719.setFont(font_page719)
                    message4_page719.exec_()
                    message3_page719 = QMessageBox()
                    message3_page719.setWindowTitle(":-(")
                    message3_page719.setText("Не вышло! Хотите повторить попытку?")
                    message3_page719.setFont(font_page719)
                    message3_page719.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    m719 = message3_page719.exec_()
                    if m719 == QMessageBox.Yes:
                        self.page_number = 719
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:    
                        self.page_number = 595
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                        return self.page_number


            # --------------------------------параграф 596------------------------------------
            elif self.page_number == 596:
                self.read_page_text()
                if self.ui.lineEdit.text() == '93':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 597------------------------------------
            elif self.page_number == 597:
                self.read_page_text()
                if self.ui.lineEdit.text() == '350' or self.ui.lineEdit.text() == '398' or self.ui.lineEdit.text() == '206':
                    self.losing_life_points(2)
                    self.strength_stamina_luck_information()
                    print("-2 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 598------------------------------------
            elif self.page_number == 598:
                self.read_page_text()
                if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
                    message_page598 = QMessageBox(self)
                    message_page598.resize(1000, 1000)
                    message_page598.setWindowTitle("Параграф " + str(self.page_number))
                    font598 = QFont()
                    font598.setPointSize(14)
                    message_page598.setFont(self.font_for_messageboxes)
                    name_of_opening_file_598 = "Page" + str(self.page_number) + ".txt"
                    str_to_file_name_598 = Path("GameText", name_of_opening_file_598)
                    page_file_598 = open(str_to_file_name_598, "r")
                    message_page598.setText(page_file_598.read())
                    message_page598.exec_()
                    page_file_598.close()
                    message3_page598 = QMessageBox()
                    message3_page598.setWindowTitle("!!!")
                    message3_page598.setText("У вас есть заклинание Левитации")
                    message3_page598.setFont(font598)
                    message3_page598.exec_()
                    message2_page598 = QMessageBox()
                    message2_page598.setWindowTitle("------->>")
                    message2_page598.setText("Переход к параграфу 501")
                    message2_page598.setFont(font598)
                    message2_page598.exec_()
                    self.page_number = 501
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_you_lost(598)


            # --------------------------------параграф 599------------------------------------
            elif self.page_number == 599:
                self.read_page_text()
                pegasus = Item("Вызов пегаса", "п.609")
                if self.checking_bag_item(pegasus):
                    message_page599 = QMessageBox(self)
                    message_page599.resize(1000, 1000)
                    message_page599.setWindowTitle("Параграф " + str(self.page_number))
                    font599 = QFont()
                    font599.setPointSize(14)
                    message_page599.setFont(self.font_for_messageboxes)
                    name_of_opening_file_599 = "Page" + str(self.page_number) + ".txt"
                    str_to_file_name_599 = Path("GameText", name_of_opening_file_599)
                    page_file_599 = open(str_to_file_name_599, "r")
                    message_page599.setText(page_file_599.read())
                    message_page599.exec_()
                    page_file_599.close()
                    message3_page599 = QMessageBox()
                    message3_page599.setWindowTitle("!!!")
                    message3_page599.setText("Вы вызываете Пегаса")
                    message3_page599.setFont(font599)
                    message3_page599.exec_()
                    message2_page599 = QMessageBox()
                    message2_page599.setWindowTitle("------->>")
                    message2_page599.setText("Переход к параграфу 609")
                    message2_page599.setFont(font599)
                    message2_page599.exec_()
                    self.page_number = 609
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    self.page_you_lost(599)


            # --------------------------------параграф 600------------------------------------
            elif self.page_number == 600:
                self.read_page_text()
                if self.ui.lineEdit.text() == '55':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 601------------------------------------
            elif self.page_number == 601:
                self.read_page_text()
                if self.ui.lineEdit.text() == '232':
                    self.losing_life_points(6)
                    self.strength_stamina_luck_information()
                    print("-6 выносливости")
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 602------------------------------------
            elif self.page_number == 602:
                self.read_page_text()
                if self.ui.lineEdit.text() == '169':
                    self.player1.barlad_dart_is_dead = True                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 603------------------------------------
            elif self.page_number == 603:
                self.read_page_text()
                self.page_you_lost(603)


            # --------------------------------параграф 604------------------------------------
            elif self.page_number == 604:
                self.read_page_text()
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message_page604 = QMessageBox()
                    message_page604.setWindowTitle("Параграф 604")
                    font_page604 = QFont()
                    font_page604.setPointSize(14)
                    message_page604.setFont(self.font_for_messageboxes)
                    message_page604.setText("Вы достаете меч и внезапно наносите удар ближайшему поваренку. Он падает замертво. Потом поворачиваетесь к повару.")
                    message_page604.exec_()

                    self.player1.round_number = 0
                    print("Бой с поваром")
                    self.player1.battleground_one("Повар", 8, 10)
                    print("Игрок победил повара")

                if self.ui.lineEdit.text() == '173' or self.ui.lineEdit.text() == '379':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 605------------------------------------
            elif self.page_number == 605:
                self.read_page_text()
                if self.ui.lineEdit.text() == '169':
                    self.player1.barlad_dart_is_dead = True                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 606------------------------------------
            elif self.page_number == 606:
                self.read_page_text()
                if self.ui.lineEdit.text() == '594' or self.ui.lineEdit.text() == '599':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 607------------------------------------
            elif self.page_number == 607:
                self.read_page_text()
                if self.ui.lineEdit.text() == '323':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 608------------------------------------
            elif self.page_number == 608:
                self.read_page_text()
                if self.ui.lineEdit.text() == '214' or self.ui.lineEdit.text() == '38':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 609------------------------------------
            elif self.page_number == 609:
                self.read_page_text()
                self.page_you_lost(609)


            # --------------------------------параграф 610------------------------------------
            elif self.page_number == 610:
                self.read_page_text()
                if self.ui.lineEdit.text() == '607' or self.ui.lineEdit.text() == '393' or self.ui.lineEdit.text() == '337':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 611------------------------------------
            elif self.page_number == 611:
                self.read_page_text()
                if self.ui.lineEdit.text() == '128' or self.ui.lineEdit.text() == '32' or self.ui.lineEdit.text() == '226' or self.ui.lineEdit.text() == '356':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 612------------------------------------
            elif self.page_number == 612:
                self.read_page_text()
                if self.ui.lineEdit.text() == '196' or self.ui.lineEdit.text() == '258' or self.ui.lineEdit.text() == '169':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 613------------------------------------
            elif self.page_number == 613:
                self.read_page_text()
                if self.ui.lineEdit.text() == '246':
                    if self.player1.gold >= 10:
                        self.player1.gold -= 10 
                        print("-10 золотых")
                        self.gold_food_water_information()                   
                        self.page_number = int(self.ui.lineEdit.text())
                        self.ui.lineEdit.clear()
                        print("Следующая страница = ", self.page_number)
                    else:
                        self.not_enough_gold()
                        self.ui.lineEdit.clear()
                        return self.page_number
                elif self.ui.lineEdit.text() == '65':
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 614------------------------------------
            elif self.page_number == 614:
                self.read_page_text()
                if self.ui.lineEdit.text() == '192':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 615------------------------------------
            elif self.page_number == 615:
                self.read_page_text()
                if self.ui.lineEdit.text() == '232':                    
                    self.page_number = int(self.ui.lineEdit.text())
                    self.ui.lineEdit.clear()
                    print("Следующая страница = ", self.page_number)
                else:
                    if self.ui.lineEdit.text() != "":
                        self.warning_wrong_page_number()
                        self.ui.lineEdit.clear()
                        return self.page_number
                    else:
                        print("Введите номер страницы")
                        return self.page_number


            # --------------------------------параграф 616------------------------------------
            elif self.page_number == 616:
                self.read_page_text()
                self.page_you_lost(616)


            # --------------------------------параграф 617------------------------------------
            elif self.page_number == 617:
                self.read_page_text()
                message_page617 = QMessageBox(self)
                message_page617.resize(1000, 1000)
                message_page617.setWindowTitle("Параграф 617")
                font617 = QFont()
                font617.setPointSize(14)
                message_page617.setFont(self.font_for_messageboxes)
                name_of_opening_file_617 = "Page" + str(self.page_number) + ".txt"
                str_to_file_name_617 = Path("GameText", name_of_opening_file_617)
                page_file_617 = open(str_to_file_name_617, "r")
                message_page617.setText(page_file_617.read())
                message_page617.exec_()
                page_file_617.close
                if self.button_click_on_page[self.page_number] == False:
                    self.button_click_on_page[self.page_number] = True
                    message2_page617 = QMessageBox(self)
                    message2_page617.resize(1000, 1000)
                    message2_page617.setWindowTitle("УРА!!!!!!")
                    message2_page617.setFont(font617)
                    message2_page617.setText("ПОЗДРАВЛЯЕМ, ВЫ ВЫИГРАЛИ!!!")
                    message2_page617.exec_()
                    message3_page617 = QMessageBox(self)
                    message3_page617.setWindowTitle("Happy end")
                    message3_page617.setIconPixmap(QPixmap("GameText\Page617.jpg"))
                    message3_page617.exec_()
                    message4_page617 = QMessageBox(self)
                    message4_page617.setWindowTitle("Happy end")
                    message4_page617.setIconPixmap(QPixmap("GameText\Page617_2.jpg"))
                    message4_page617.exec_()
                    message5_page617 = QMessageBox(self)
                    message5_page617.setWindowTitle("Happy end")
                    message5_page617.setIconPixmap(QPixmap("GameText\Page617_3.jpg"))
                    message5_page617.exec_()
                sys.exit("Game over")

                     
            else:
                print("Game over")
                break   


    # ----------------------------------------------- ОКНО ТОРГОВЦА п.176 -----------------------------------------------------            
    # окно лавки торговца п.176
    def open_window_176(self):
        self.window = QtWidgets.QMainWindow()
        self.ui2 = Ui_MainWindow2()
        self.ui2.setupUi(self.window)
        name_of_opening_file_176 = "Page176.txt"
        file_name_to_str_176 = Path("GameText", name_of_opening_file_176)
        page_file_176 = open(file_name_to_str_176, "r")
        text_from_page_files_176 = page_file_176.read()
        self.ui2.textEdit.append(text_from_page_files_176)
        page_file_176.close
        self.ui2.label_7.setText("Золото = " + str(self.player1.gold))
        self.ui2.pushButton.clicked.connect(self.button1_176_clicked)
        self.ui2.pushButton_2.clicked.connect(self.button2_176_clicked)
        self.ui2.pushButton_3.clicked.connect(self.button3_176_clicked)
        self.ui2.pushButton_4.clicked.connect(self.button4_176_clicked)
        self.ui2.pushButton_5.clicked.connect(self.button5_176_clicked)
        self.ui2.pushButton_6.clicked.connect(lambda: self.button6_176_clicked(self.window))
        self.window.show()

    # купить яблоко у торговца (окно на п. 176)
    def button1_176_clicked(self):
        apple = Item("Яблоко", "+1 к выносл.")
        if self.player1.gold > 0:
            self.player1.gold -= 1
            self.ui2.label_7.setText("Золото = " + str(self.player1.gold))
            self.ui2.textEdit_2.append("Вы купили яблоко, у вас осталось " + str(self.player1.gold) + " золота.")
            self.gold_food_water_information()
            self.add_item_and_print_console(apple)
            self.add_item_to_table_widget(apple)
        else:
            self.not_enough_gold()
            return self.player1.gold

    # купить мандарин у торговца (окно на п. 176)
    def button2_176_clicked(self):
        mandarin = Item("Мандарин", "+2 к выносл.")
        if self.player1.gold > 1:
            self.player1.gold -= 2
            self.ui2.label_7.setText("Золото = " + str(self.player1.gold))
            self.ui2.textEdit_2.append("Вы купили мандарин, у вас осталось " + str(self.player1.gold) + " золота.")
            self.gold_food_water_information()
            self.add_item_and_print_console(mandarin)
            self.add_item_to_table_widget(mandarin)
        else:
            self.not_enough_gold()
            return self.player1.gold

    # купить апельсин у торговца (окно на п. 176)
    def button3_176_clicked(self):
        orange = Item("Апельсин", "+1 к выносл.")
        if self.player1.gold > 0:
            self.player1.gold -= 1
            self.ui2.label_7.setText("Золото = " + str(self.player1.gold))
            self.ui2.textEdit_2.append("Вы купили апельсин, у вас осталось " + str(self.player1.gold) + " золота.")
            self.gold_food_water_information()
            self.add_item_and_print_console(orange)
            self.add_item_to_table_widget(orange)
        else:
            self.not_enough_gold()
            return self.player1.gold

    # купить банан у торговца (окно на п. 176)
    def button4_176_clicked(self):
        banana = Item("Банан", "+2 к выносл.")
        if self.player1.gold > 1:
            self.player1.gold -= 2
            self.ui2.label_7.setText("Золото = " + str(self.player1.gold))
            self.ui2.textEdit_2.append("Вы купили банан, у вас осталось " + str(self.player1.gold) + " золота.")
            self.gold_food_water_information()
            self.add_item_and_print_console(banana)
            self.add_item_to_table_widget(banana)
        else:
            self.not_enough_gold()
            return self.player1.gold

    # наполнить флягу у торговца у торговца (окно на п. 176)
    def button5_176_clicked(self):
        if self.player1.water == 2:
            message_not_enough_gold = QMessageBox()
            message_not_enough_gold.setWindowTitle("Нет места")
            message_not_enough_gold.setText("У вас полная фляга")
            font_not_enough_gold = QFont()
            font_not_enough_gold.setPointSize(14)
            message_not_enough_gold.setFont(font_not_enough_gold)
            message_not_enough_gold.exec_()
            return self.player1.gold
        else:
            if self.player1.gold <= 1:
                self.player1.water += 1
                self.player1.gold -= 1
                self.ui2.textEdit_2.append("Вы пополнили флягу (+1 вода), у вас осталось " + str(self.player1.gold) + " золота.")
            else:
                self.not_enough_gold()
                return self.player1.gold

    # закрыть окно торговца (окно на п. 176)
    def button6_176_clicked(self, window):
        window.close()

    # ----------------------------------------- ОКНО ТОРГОВЦА п.176 (конец) ---------------------------------------------------
   


    # ----------------------------------------------- ОКНО КРЕСТЬЯНИНА п.448 -----------------------------------------------------

    # окно лавки крестьянина п.448
    def open_window_448(self):
        self.window = QtWidgets.QMainWindow()
        self.ui3 = Ui_MainWindow3()
        self.ui3.setupUi(self.window)
        name_of_opening_file_448 = "Page448.txt"
        file_name_to_str_448 = Path("GameText", name_of_opening_file_448)
        page_file_448 = open(file_name_to_str_448, "r")
        text_from_page_files_448 = page_file_448.read()
        self.ui3.textEdit.append(text_from_page_files_448)
        page_file_448.close
        self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
        self.ui3.pushButton.clicked.connect(lambda: self.button6_176_clicked(self.window))
        listWidget_items_list = []
        # создаем ячейки
        [listWidget_items_list.append(QListWidgetItem()) for i in range(0, 8, 1)]
        listWidget_items_list[0].setText("Ананас(2 золотых, +3 выносл.)")
        listWidget_items_list[1].setText("Банан(2 золотых, +2 выносл.)")
        listWidget_items_list[2].setText("Кусочек дерева(1 золотой)")
        listWidget_items_list[3].setText("Фигурный ключ(2 золотых)")
        listWidget_items_list[4].setText("Попона для лошади(5 золотых)")
        listWidget_items_list[5].setText("Кусок металла(3 золотых)")
        listWidget_items_list[6].setText("Золотая устрица(8 золотых)")
        listWidget_items_list[7].setText("Серебряный браслет(4 золотых)")
        # заполняем ячейки в listWidget
        [self.ui3.listWidget.insertItem(i, listWidget_items_list[i]) for i in range(0, 8, 1)]
        # устанавливаем цвет выделения ячеек
        self.ui3.listWidget.setStyleSheet("QListWidget::item:selected {background:steelblue; color:white;}"
                                          "QListWidget::Item:hover{background:steelblue; }")  
        self.ui3.listWidget.clicked.connect(lambda: self.listWidget_448_clicked(self.ui3.listWidget.currentRow(), self.item_list_448))                                      
        self.window.show()

    # событие клика на товаре (покупки у крестьянина п.448)
    def listWidget_448_clicked(self, item_number, item_name):
        #self.ui3.listWidget.takeItem(item_number)
        if item_name[item_number] == "Ананас":
            if self.player1.gold >= 2:
                self.player1.gold -= 2
                print("-2 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили ананас\nУ вас осталось золота: " + str(self.player1.gold))
                pineapple = Item("Ананас", "+3 выносл.")
                self.add_item_and_print_console(pineapple)
                self.add_item_to_table_widget(pineapple)
                item_name.remove("Ананас")
                self.ui3.listWidget.takeItem(item_number)
                return item_name
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name
        elif item_name[item_number] == "Банан":
            banana2 = Item("Банан", "+2 к выносл.")
            if self.player1.gold >= 2:
                self.player1.gold -= 2
                print("-2 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили банан\nУ вас осталось золота: " + str(self.player1.gold))
                self.add_item_and_print_console(banana2)
                self.add_item_to_table_widget(banana2)
                item_name.remove("Банан")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
        elif item_name[item_number] == "Кусочек дерева":
            if self.player1.gold >= 1:
                self.player1.gold -= 1
                print("-1 золотой")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили кусочек дерева\nУ вас осталось золота: " + str(self.player1.gold))
                wooden_piece = Item("Кусочек дерева", "-")
                self.add_item_and_print_console(wooden_piece)
                self.add_item_to_table_widget(wooden_piece)
                item_name.remove("Кусочек дерева")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
        elif item_name[item_number] == "Фигурный ключ":
            if self.player1.gold >= 2:
                self.player1.gold -= 2
                print("-2 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили Фигурный ключ\nУ вас осталось золота: " + str(self.player1.gold))
                figure_key = Item("Фигурный ключ", "-")
                self.add_item_and_print_console(figure_key)
                self.add_item_to_table_widget(figure_key)
                item_name.remove("Фигурный ключ")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
        elif item_name[item_number] == "Попона":
            if self.player1.gold >= 5:
                self.player1.gold -= 5
                print("-5 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили попону\nУ вас осталось золота: " + str(self.player1.gold))
                horsecloth = Item("Попона", "-")
                self.add_item_and_print_console(horsecloth)
                self.add_item_to_table_widget(horsecloth)
                item_name.remove("Попона")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
        elif item_name[item_number] == "Кусок металла":
            if self.player1.gold >= 3:
                self.player1.gold -= 3
                print("-3 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили Кусок металла\nУ вас осталось золота: " + str(self.player1.gold))
                metal_piece = Item("Кусок металла", "-")
                self.add_item_and_print_console(metal_piece)
                self.add_item_to_table_widget(metal_piece)
                item_name.remove("Кусок металла")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
        elif item_name[item_number] == "Золотая устрица":
            if self.player1.gold >= 8:
                self.player1.gold -= 8
                print("-8 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили золотую устрицу\nУ вас осталось золота: " + str(self.player1.gold))
                gold_oyster = Item("Золотая устрица", "-")
                self.add_item_and_print_console(gold_oyster)
                self.add_item_to_table_widget(gold_oyster)
                item_name.remove("Золотая устрица")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name
        elif item_name[item_number] == "Серебр. браслет":
            if self.player1.gold >= 4:
                self.player1.gold -= 4
                print("-4 золотых")
                self.gold_food_water_information()
                self.ui3.label_3.setText("Золото = " + str(self.player1.gold))
                self.ui3.textEdit_2.append("Вы купили серебряный браслет\nУ вас осталось золота: " + str(self.player1.gold))
                silver_bracelet = Item("Серебр. браслет", "-")
                self.add_item_and_print_console(silver_bracelet)
                self.add_item_to_table_widget(silver_bracelet)
                item_name.remove("Серебр. браслет")
                self.ui3.listWidget.takeItem(item_number)
                return item_number
            else:
                self.not_enough_gold()
                self.ui3.textEdit_2.append("Недостаточно золота")
                return item_name    
           
    # закрыть окно крестьянина (окно на п. 448)
    def button6_176_clicked(self, window):
        self.buying448_is_over = True
        window.close()    


    # --------------------------------------------- ОКНО КРЕСТЬЯНИНА п.448 (конец) --------------------------------------------------




    # --------------------------------------------- ОКНО СТАРИЧКА п.464 ---------------------------------------------------------------

    # окно выбора заклинания, которое игрок отдает старичку за перстень
    def open_window_464(self):
        self.window2_464 = QMainWindow()
        self.ui4 = Ui_MainWindow4()
        self.ui4.setupUi(self.window2_464)
        self.window464_is_closed = False
        self.closeEvent(self.window2_464)
        self.ui4.pushButton.clicked.connect(lambda: self.button1_464_clicked(self.window2_464))
        self.ui4.pushButton_2.clicked.connect(lambda: self.button2_464_clicked(self.window2_464))
        self.ui4.pushButton_3.clicked.connect(lambda: self.button3_464_clicked(self.window2_464))
        self.ui4.pushButton_4.clicked.connect(lambda: self.button4_464_clicked(self.window2_464))
        self.ui4.pushButton_5.clicked.connect(lambda: self.button5_464_clicked(self.window2_464))
        self.ui4.pushButton_6.clicked.connect(lambda: self.button6_464_clicked(self.window2_464))
        self.ui4.pushButton_7.clicked.connect(lambda: self.button7_464_clicked(self.window2_464))
        self.ui4.pushButton_8.clicked.connect(lambda: self.button8_464_clicked(self.window2_464))
        self.ui4.pushButton_9.clicked.connect(lambda: self.button9_464_clicked(self.window2_464))
        self.window2_464.show()

    def closeEvent(self, window):
        self.window464_is_closed = True
        #window = True
            
    # отдать заклинание Левитации
    def button1_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("ЛЕВИТАЦИЯ"):
            self.spell_is_selected_464 = 1
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("ЛЕВИТАЦИЯ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close()
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.play_page()   

    # отдать заклинание Огня
    def button2_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("ОГОНЬ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("ОГОНЬ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close() 
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Иллюзии
    def button3_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("ИЛЛЮЗИЯ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("ИЛЛЮЗИЯ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close()
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Силы
    def button4_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("СИЛА"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("СИЛА")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close() 
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Слабости
    def button5_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("СЛАБОСТЬ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("СЛАБОСТЬ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close()
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Копии
    def button6_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("КОПИЯ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("КОПИЯ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close()
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Исцеления
    def button7_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("ИСЦЕЛЕНИЕ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("ИСЦЕЛЕНИЕ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close() 
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    # отдать заклинание Плавания
    def button8_464_clicked(self, window):
        if self.player1.check_for_use_necessary_spell("ПЛАВАНИЕ"):
            # если заклинание есть в списке, оно удаляется (1 штука)
            self.player1.spells.remove("ПЛАВАНИЕ")
            # обновим список заклинаний на экране в таблице
            self.output_spells()
            deer_skin = Item("Шкура оленя", "-")
            self.add_item_and_print_console(deer_skin)
            self.add_item_to_table_widget(deer_skin)
            secret_door = Item("Потайная дверца", "п.260")
            self.add_item_and_print_console(secret_door)
            self.add_item_to_table_widget(secret_door)
            ring_with_diamond = Item("Кольцо с брил.", "-40")
            self.add_item_and_print_console(ring_with_diamond)
            self.add_item_to_table_widget(ring_with_diamond)
            # переход на следующую страницу
            self.page_number = 600
            self.ui.lineEdit.clear()
            print("Следующая страница = ", self.page_number)
            self.window464_is_closed = True
            self.play_page()
            window.close()
            return True
        else:
            # если заклинания нет в списке
            self.ui.lineEdit.clear()
            self.using_spell_error()
            self.page_number = 464
            print("Следующая страница = ", self.page_number)
            self.play_page()

    def button9_464_clicked(self, window):
        self.page_number = 464
        self.ui.lineEdit.clear()
        print("Следующая страница = ", self.page_number)
        self.window464_is_closed = True
        self.play_page()
        window.close()
            

    # --------------------------------------------- ОКНО СТАРИЧКА п.464 (конец) -------------------------------------------------------
        


    # ----------------------------------------- ТЕКСТ ИГРЫ И АУДИО -------------------------------------------------------
          
    # функция текст игры (в textEdit из файла с нужным номером)
    def read_page_text(self):
        """
            Функция текст игры (в textEdit из файла с нужным номером)
        """
        self.ui.textEdit.clear()
        name_of_opening_file = "Page" + str(self.page_number) + ".txt"
        file_name_to_str = Path("GameText", name_of_opening_file)
        page_file = open(file_name_to_str, "r")
        text_from_page_files = page_file.read()
        self.ui.textEdit.append(text_from_page_files)
        del text_from_page_files
        page_file.close
        self.ui.label.setText("ТЕКСТ ИГРЫ" + " (п." + str(self.page_number) + ")")

    # сыграть АУДИОФАЙЛ
    def PlayAudioFile(self, audiofile: QMediaPlayer(), way_to_file):
        """
            Сыграть АУДИОФАЙЛ
        """
        full_file_path = os.path.join(os.getcwd(), str(way_to_file))
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        audiofile.setMedia(content)
        audiofile.play()

    # остановить АУДИОФАЙЛ
    def StopAudio(self, audiofile: QMediaPlayer()):
        """
            Остановить АУДИОФАЙЛ
        """
        audiofile.stop() 

    # ----------------------------------------- ТЕКСТ ИГРЫ И АУДИО (конец) -------------------------------------------------------       



    # ------------------------------ СООБЩЕНИЯ ОБ ОШИБКЕ------------------------------------ 

    # сообщение об ошибке, если ввели неверную страницу
    def warning_wrong_page_number(self):
        """
            Сообщение об ошибке, если ввели неверную страницу
        """
        print("Введите другой номер параграфа, сейчас вы на параграфе №", self.page_number)

    # сообщение об ошибке, если нет нужного предмета
    def warning_no_item_in_bag(self):
        """
            Сообщение об ошибке, если нет нужного предмета
        """
        print("У вас нет данного предмета")
        message_no_item_in_bag = QMessageBox()
        message_no_item_in_bag.setWindowTitle("Нет предмета")
        message_no_item_in_bag.setText("У вас нет данного предмета")
        font_not_enough_gold = QFont()
        font_not_enough_gold.setPointSize(14)
        message_no_item_in_bag.setFont(font_not_enough_gold)
        message_no_item_in_bag.exec_()
        return self.player1.gold

    # сообщение об ошибке, что недостаточно золота
    def not_enough_gold(self):
        """
            Сообщение об ошибке, что недостаточно золота
        """
        message_not_enough_gold = QMessageBox()
        message_not_enough_gold.setWindowTitle("Нет денег")
        message_not_enough_gold.setText("У вас недостаточно золота")
        font_not_enough_gold = QFont()
        font_not_enough_gold.setPointSize(14)
        message_not_enough_gold.setFont(font_not_enough_gold)
        message_not_enough_gold.exec_()
        return self.player1.gold  

    # сообщение об ошибке при использовании заклинания
    def using_spell_error(self):
        """
            Сообщение об ошибке при использовании заклинания
        """
        message_no_spell = QMessageBox()
        message_no_spell.setWindowTitle(":-(")
        message_no_spell.setText("Вы не можеет использовать данное заклинание")
        font_not_enough_gold = QFont()
        font_not_enough_gold.setPointSize(14)
        message_no_spell.setFont(font_not_enough_gold)
        message_no_spell.exec_() 

    # --------------------------- СООБЩЕНИЯ ОБ ОШИБКЕ (конец) -----------------------------------         



    # ----------------------------------- ИНФОРМАЦИЯ --------------------------------------------

    # функция обновления информации о мастерстве, выносливости и удаче
    def strength_stamina_luck_information(self):
        """
            Функция обновления информации о мастерстве, выносливости и удаче
        """
        self.ui.label_5.clear()
        self.ui.label_6.clear()
        self.ui.label_7.clear()
        self.ui.label_5.setText("МАСТЕРСТВО = " + str(self.player1.strength))
        self.ui.label_6.setText("ВЫНОСЛИВОСТЬ = " + str(self.player1.life_points))
        self.ui.label_7.setText("УДАЧА = " + str(self.player1.luck))

    # функция обновления информации о золоте, еде и воде
    def gold_food_water_information(self):
        """
            Функция обновления информации о золоте, еде и воде
        """
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.player1.gold)))
        self.ui.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.player1.food)))
        self.ui.tableWidget.setItem(2, 1, QTableWidgetItem(str(self.player1.water)))
        self.ui.tableWidget.item(0, 1).setForeground(QBrush(QColor("#c58916")))
        self.ui.tableWidget.item(1, 1).setForeground(QBrush(QColor("red")))
        self.ui.tableWidget.item(2, 1).setForeground(QBrush(QColor("blue")))
        # выравнивание текста по центру в таблице 1 (во всех ячейках)
        self.Cell_alignment_1()    

    # функция информации о заклинаниях в таблице 2 и в консоли
    def output_spells(self):
        """
            Функция информации о заклинаниях в таблице 2 и в консоли
        """
        # обновим список заклинаний на экране в таблице
        self.ui.tableWidget_2.clear()
        # редактируем титульные ячейки
        self.ui.tableWidget_2.setHorizontalHeaderLabels([""])
        # вставляем новый список заклинаний в tableWidget_2
        print(self.player1.spells)
        [self.ui.tableWidget_2.setItem(k, 0, QTableWidgetItem(str(self.player1.spells[k]))) for k in range(0, len(self.player1.spells), 1)]
        # выравниваем по центру
        self.Cell_alignment_2()   

    # ----------------------------------- ИНФОРМАЦИЯ (конец) -----------------------------------------



    # ------------------------------------- ПРЕДМЕТЫ ---------------------------------------------------

    # функция дописывает предмет в заплечный мешок
    def add_item_and_print_console(self, added_item: Item):
        """
            Функция дописывает предмет в заплечный мешок
        """
        self.player1.bag.append(added_item)
        # распечатаем список в консоли
        print(*self.player1.bag, sep=";  ")

    # проверка, если у игрока необходимый предмет
    def checking_bag_item(self, item: Item):
        """
            Проверка, если у игрока необходимый предмет
        """
        using_item_enabled = False
        if self.player1.bag == []:
            return using_item_enabled
        else:    
            for i in range(0, len(self.player1.bag), 1):
                if item.item_name == self.player1.bag[i].item_name and item.item_parameter == self.player1.bag[i].item_parameter:
                    using_item_enabled = True
                    break
                else:
                    continue
            return using_item_enabled        

    # функция добавления предмета в инвентарь
    def add_item_to_table_widget(self, item: Item):
        """
            Функция добавления предмета в инвентарь
        """
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, QTableWidgetItem(item.item_name))
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 1, QTableWidgetItem(item.item_parameter))
        self.Cell_alignment_1()

    # функция удаления предмета из инвентаря
    def delete_item(self, item: Item):
        """
            Функция удаления предмета из инвентаря
        """
        if self.player1.bag == []:
            return self.player1.bag
        else:
            for i in range(0, len(self.player1.bag), 1):
                if item.item_name == self.player1.bag[i].item_name:
                    self.player1.bag.pop(i)
                    self.ui.tableWidget.removeRow(i+3)
                    break
                else:
                    continue    
        print(*self.player1.bag, sep=";  ")

     

    # ------------------------------------- ПРЕДМЕТЫ (конец) ---------------------------------------------------    



    # параграф, где игрок проигрывает
    def page_you_lost(self, page_number):
        """
            Параграф, где игрок проигрывает
        """
        message_page = QMessageBox(self)
        message_page.resize(1000, 1000)
        message_page.setWindowTitle("Параграф " + str(self.page_number))
        message_page.setFont(self.font_for_messageboxes)
        name_of_opening_file = "Page" + str(page_number) + ".txt"
        str_to_file_name = Path("GameText", name_of_opening_file)
        page_file = open(str_to_file_name, "r")
        message_page.setText(page_file.read())
        message_page.exec_()
        print(page_file.read())
        page_file.close()
        self.player1.game_over = True
        self.checking_game_over()   
      
    # функция выравнивания текста по центру в таблице 1 (во всех ячейках)
    def Cell_alignment_1(self):
        """
            Функция выравнивания текста по центру в таблице 1 (во всех ячейках)
        """
        for i in range(0, self.ui.tableWidget.rowCount(), 1):
            [self.ui.tableWidget.item(i, j).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter) for j in range(0, self.ui.tableWidget.columnCount(), 1)]

    # функция выравнивания текста по центру в таблице 2 (во всех ячейках)
    def Cell_alignment_2(self):
        """
            Функция выравнивания текста по центру в таблице 2 (во всех ячейках)
        """
        for i in range(0, len(self.player1.spells), 1):
            self.ui.tableWidget_2.item(i, 0).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter) 

    # функция использования золота, еды или воды
    def using_gold_food_water(self, gold, food, water):
        """
            Функция использования золота, еды или воды
        """
        if self.player1.gold - gold < 0:
            message_not_enough_gold = QMessageBox()
            message_not_enough_gold.setWindowTitle("Нет денег")
            message_not_enough_gold.setText("У вас недостаточно золота")
            font_not_enough_gold = QFont()
            font_not_enough_gold.setPointSize(14)
            message_not_enough_gold.setFont(font_not_enough_gold)
            message_not_enough_gold.exec_()
            return self.player1.gold
        elif self.player1.food - food < 0:
            message_not_enough_food = QMessageBox()
            message_not_enough_food.setWindowTitle("Нет еды")
            message_not_enough_food.setText("У вас недостаточно еды")
            font_not_enough_food = QFont()
            font_not_enough_food.setPointSize(14)
            message_not_enough_food.setFont(font_not_enough_food)
            message_not_enough_food.exec_()
            return self.player1.food
        elif self.player1.water - water < 0:    
            message_not_enough_water = QMessageBox()
            message_not_enough_water.setWindowTitle("Нет воды")
            message_not_enough_water.setText("У вас недостаточно воды")
            font_not_enough_water = QFont()
            font_not_enough_water.setPointSize(14)
            message_not_enough_water.setFont(font_not_enough_water)
            message_not_enough_water.exec_()
            return self.player1.water
        else:
            self.player1.gold -= gold
            self.player1.food -= food
            self.player1.water -= water
            return 1 

    # функция восстановления выносливости
    def life_points_recovery(self, life_points):
        """
            Функция восстановления выносливости
        """
        self.player1.life_points += life_points
        if self.player1.life_points > self.player1.max_life_points:
            self.player1.life_points = self.player1.max_life_points
        self.strength_stamina_luck_information()    
    
    # функция вычитает указанное количество выносливости
    def losing_life_points(self, life_points):
        """
            Функция вычитает указанное количество выносливости
        """
        self.player1.life_points -= life_points
        if self.player1.life_points <= 0 or self.player1.game_over == True:
            self.strength_stamina_luck_information()
            self.checking_game_over()
        else:
            self.strength_stamina_luck_information()
            return self.player1.game_over

    # функция проверки на окончание игры
    def checking_game_over(self):
        """
            Функция проверки на окончание игры
        """
        if self.player1.life_points <= 0 or self.player1.game_over == True:
            message_game_over = QMessageBox()
            print("Игра окончена")
            message_game_over.setText("Вы проиграли!\nИгра окончена!")
            message_game_over.setIcon(QMessageBox.Information)
            message_game_over.setWindowTitle(":-(")
            message_game_over.setStandardButtons(QMessageBox.Ok)
            font_game_over_message = QFont()
            font_game_over_message.setPointSize(14)
            message_game_over.setFont(font_game_over_message)
            message_game_over.exec_()
            sys.exit("Game over")
        else:
            return self.player1.game_over   


    def click_next_button(self):
        """
            Событие перехода к следующему параграфу вступления intro (по нажатию кнопки)
        """
        if self.intro_number <= 15:
            self.play_intro()
            self.intro_number += 1
        else:
            self.play_page()


    def keyPressEvent(self, e):
        """
            Cобытие нажатия клавиши Enter (левой и правой)
        """
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self.click_next_button()
            return super().keyPressEvent(e)


    def tableWidget_using_item(self, row, column):
        """
            Функция использования исцеляющих предметов при нажатии на их название в таблице 1
        """
        if self.ui.tableWidget.item(row, column).text() == "Яблоко":
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Использовать предмет")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите использовать данный предмет?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                apple = Item("Яблоко", "+1 к выносл.")
                self.delete_item(apple)
                self.player1.life_points += 1
                print("Восстановили 1 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points

        elif self.ui.tableWidget.item(row, column).text() == "Апельсин":
            if self.ui.tableWidget.item(row, column).text() == "Апельсин":
                message_using_healing = QMessageBox()
                message_using_healing.setWindowTitle("Использовать предмет")
                font_message_using_healing = QFont()
                font_message_using_healing.setPointSize(14)
                message_using_healing.setFont(font_message_using_healing)
                message_using_healing.setText("Хотите использовать данный предмет?")
                message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                m_healing = message_using_healing.exec_()
                if m_healing == QMessageBox.Yes:
                    orange = Item("Апельсин", "+1 к выносл.")
                    self.delete_item(orange)
                    self.player1.life_points += 1
                    print("Восстановили 1 выносливости")
                    if self.player1.life_points > self.player1.max_life_points:
                        self.player1.life_points = self.player1.max_life_points
                    self.strength_stamina_luck_information()    
                    return self.player1.life_points
                else:
                    self.strength_stamina_luck_information()
                    return self.player1.life_points

        elif self.ui.tableWidget.item(row, column).text() == "Банан":
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Использовать предмет")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите использовать данный предмет?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                banana = Item("Банан", "+2 к выносл.")
                self.delete_item(banana)             
                self.player1.life_points += 2
                print("Восстановили 2 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points

        elif self.ui.tableWidget.item(row, column).text() == "Мандарин":
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Использовать предмет")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите использовать данный предмет?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                mandarin = Item("Мандарин", "+2 к выносл.") 
                self.delete_item(mandarin)
                self.player1.life_points += 2
                print("Восстановили 2 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points        

        elif self.ui.tableWidget.item(row, column).text() == "Ананас":
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Использовать предмет")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите использовать данный предмет?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                pineapple = Item("Ананас", "+3 к выносл.")
                self.delete_item(pineapple)
                self.player1.life_points += 3
                print("Восстановили 3 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points

        elif self.ui.tableWidget.item(row, column).text() == "ВОДА" and self.player1.water > 0:
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Попить воды")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите попить воды?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                self.player1.water -= 1
                self.gold_food_water_information()
                self.player1.life_points += 2
                print("Восстановили 2 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points

        elif self.ui.tableWidget.item(row, column).text() == "ЕДА" and self.player1.food > 0:
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Поесть")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите поесть?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                self.player1.food -= 1
                self.gold_food_water_information()
                self.player1.life_points += 2
                print("Восстановили 2 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points                       



    def tableWidget2_using_spell(self, row, column):
        """
            Функция использования заклинания Исцеления при нажатии на него в таблице 2
        """      
        if self.ui.tableWidget_2.item(row, column).text() == "ИСЦЕЛЕНИЕ":
            message_using_healing = QMessageBox()
            message_using_healing.setWindowTitle("Заклинание Исцеления")
            font_message_using_healing = QFont()
            font_message_using_healing.setPointSize(14)
            message_using_healing.setFont(font_message_using_healing)
            message_using_healing.setText("Хотите использовать Исцеление (+8 к выносливости) ?")
            message_using_healing.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            m_healing = message_using_healing.exec_()
            if m_healing == QMessageBox.Yes:
                self.player1.spells.remove("ИСЦЕЛЕНИЕ")
                # обновим список заклинаний на экране в таблице
                self.output_spells()
                self.player1.life_points += 8
                print("Восстановили 8 выносливости")
                if self.player1.life_points > self.player1.max_life_points:
                    self.player1.life_points = self.player1.max_life_points
                self.strength_stamina_luck_information()    
                return self.player1.life_points
            else:
                self.strength_stamina_luck_information()
                return self.player1.life_points


app = QtWidgets.QApplication([])
application = My_window()


application.show()
 
sys.exit(app.exec())