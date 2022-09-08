import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Game_window import *

class Player():

    def __init__(self):
        self.life_points = random.randint(14, 24)
        self.max_life_points = self.life_points
        self.food = 2
        self.water = 2
        self.strength = random.randint(7, 12)
        self.luck = random.randint(7, 12)
        self.gold = 15
        self.spells = ["ЛЕВИТАЦИЯ", "ОГОНЬ", "ИЛЛЮЗИЯ", "СИЛА", "СЛАБОСТЬ",
                       "КОПИЯ", "ОГОНЬ", "ПЛАВАНИЕ", "ИСЦЕЛЕНИЕ", "ИСЦЕЛЕНИЕ"]
        self.bag = []
        self.game_over = False
        self.strength_36 = False
        self.weakness_314 = False
        self.strength_spell = False
        self.weakness_spell = False
        self.strength_spell_567 = False
        self.weakness_spell_567 = False
        # индикатор спасенной принцессы
        self.princess_is_saved = False
        # индикатор убитого Барлада Дэрта (главного босса)
        self.barlad_dart_is_dead = False
        self.battle_text = ""
        self.win_battle_328 = True
        self.round_number = 0
        self.round_number_328 = 0
        self.page_number_65_next_page = 705

    # установить значение Мастерства у игрока
    def set_Strength(self, strength_input): 
        return self.strength


    # проверка, есть ли заклинание в списке у игрока (можно ли его применить)
    def check_for_use_necessary_spell(self, spell):
        yes_spell = False
        for i in self.spells:
            if i == spell:
                yes_spell = True
                break
            else:
                continue
        print(self.spells)    
        return yes_spell


    # проверка удачи
    def checking_luck(self):
        luck = random.randint(2, 12)      
        print("Your luck =", self.luck)
        print("Number on dice =", luck)                                                   # Warning проверка удачи
        if luck <= self.luck:
            message_checking_luck = QMessageBox()
            message_checking_luck.setText("Ваша удача = "+ str(self.luck) +"\nНа кубике выпало: "+ str(luck) + "\nУдача вам улыбнулась!")
            message_checking_luck.setIcon(QMessageBox.Information)
            message_checking_luck.setWindowTitle(":-)")
            message_checking_luck.setStandardButtons(QMessageBox.Ok)
            font_checking_luck = QFont()
            font_checking_luck.setPointSize(14)
            message_checking_luck.setFont(font_checking_luck)
            message_checking_luck.exec_()
            print("You are lucky")
            return True
        else:
            message_checking_luck = QMessageBox()
            message_checking_luck.setText("Ваша удача = "+ str(self.luck) +"\nНа кубике выпало: "+ str(luck) + "\nУдача от вас отвернулась :-(")
            message_checking_luck.setIcon(QMessageBox.Information)
            message_checking_luck.setWindowTitle(":-(")
            message_checking_luck.setStandardButtons(QMessageBox.Ok)
            font_checking_luck = QFont()
            font_checking_luck.setPointSize(14)
            message_checking_luck.setFont(font_checking_luck)
            message_checking_luck.exec_()
            print("You are unlucky, sorry")
            return False


    def battleground(self):
        pass


    def battleground_one(self, monster_name, monster_strength, monster_life_points):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        while True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "У вас выпало: " + str(your_cubic) + ", у противника выпало: " + str(enemy_cubic) + "\n" 
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара противника = " + str(monster_strength + enemy_cubic) + "\n"
            if self.strength + your_cubic == monster_strength + enemy_cubic:
                self.battle_text += "Противник парировал удар.\n"
                continue
            elif self.strength + your_cubic >= monster_strength + enemy_cubic:
                monster_life_points -= 2
                self.battle_text += "Вы ударили противника.\nВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(monster_life_points) + "\n"
                if monster_life_points <= 0:
                    self.battle_text += "Вы выиграли!!!"
                    break
                else:
                    continue
            else:
                self.life_points -= 2
                self.battle_text += "Противник ударил вас.\nВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(monster_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    continue
        message_battleground_one = QDialog()
        message_battleground_one.setWindowTitle("Окно битвы")
        message_battleground_one.setFixedSize(800, 600)
        textEdit_battleground_one = QTextEdit(message_battleground_one)
        textEdit_battleground_one.setFixedSize(800, 555)
        textEdit_battleground_one.clear()
        textEdit_battleground_one.setText(self.battle_text)
        buttonBox_battleground_one = QDialogButtonBox(message_battleground_one)
        buttonBox_battleground_one.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_one.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_one.accepted.connect(message_battleground_one.accept)
        font_battleground_one = QFont()
        font_battleground_one.setPointSize(10)
        message_battleground_one.setFont(font_battleground_one)
        # установить фокус на кнопке ОК
        buttonBox_battleground_one.setFocus()
        message_battleground_one.exec_()
        if self.life_points <= 0:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle(":-(")
            message3_battleground_one.setText("Вы проиграли.\nКонец игры...")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle(":-)")
            message3_battleground_one.setText("Вы выиграли!!!")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            return self.life_points


    def pushButton_battleground_one_clicked(self, message_window):
        message_window.close()


    def battleground_one_copy_spell(self, monster_name, monster_strength, monster_life_points):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        monster_copy_strength = monster_strength
        monster_copy_life_points = monster_life_points
        self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(monster_copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(monster_life_points) + "\n"
        while True:
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "У вас выпало: " + str(your_cubic) + ", у противника выпало: " + str(enemy_cubic) + "\n" 
            self.battle_text += "Сила удара копии  = " + str(monster_copy_strength + your_cubic) + ",  Сила удара противника = " + str(monster_strength + enemy_cubic) + "\n"
            if monster_copy_strength + your_cubic == monster_strength + enemy_cubic:
                self.battle_text += "Противник парировал удар.\n"
                continue
            elif monster_copy_strength + your_cubic >= monster_strength + enemy_cubic:
                monster_life_points -= 2
                self.battle_text += "Копия ударила противника.\nВЫНОСЛИВОСТЬ КОПИИ = " + str(monster_copy_life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(monster_life_points) + "\n"
                if monster_life_points <= 0:
                    self.battle_text += "Вы выиграли!!!"
                    break
                else:
                    continue
            else:
                monster_copy_life_points -= 2
                self.battle_text += "Противник ударил копию.\nВЫНОСЛИВОСТЬ КОПИИ = " + str(monster_copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(monster_life_points) + "\n"
                if monster_copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
                else:
                    continue
        message_battleground_one_copy_spell = QDialog()
        message_battleground_one_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_one_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_one_copy_spell = QTextEdit(message_battleground_one_copy_spell)
        textEdit_battleground_one_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_one_copy_spell.clear()
        textEdit_battleground_one_copy_spell.setText(self.battle_text)
        buttonBox_battleground_one_copy_spell = QDialogButtonBox(message_battleground_one_copy_spell)
        buttonBox_battleground_one_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_one_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_one_copy_spell.accepted.connect(message_battleground_one_copy_spell.accept)
        font_battleground_one = QFont()
        font_battleground_one.setPointSize(10)
        message_battleground_one_copy_spell.setFont(font_battleground_one)
        # установить фокус на кнопке ОК
        buttonBox_battleground_one_copy_spell.setFocus()
        message_battleground_one_copy_spell.exec_()
        if monster_copy_life_points <= 0:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle("!!!")
            message3_battleground_one.setText("Копия проиграла.\nТеперь ваша очередь вступить в бой!")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            self.battleground_one(monster_name, monster_strength, monster_life_points)
            return self.life_points
        else:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle(":-)")
            message3_battleground_one.setText("Противник повержен!!!")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            return self.life_points


    def battleground_two(self, monster1_name, monster1_strength, monster1_life_points, monster2_name, monster2_strength, monster2_life_points):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        self.round_number = 0
        man1_alive = True
        man2_alive = True
        while man1_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy1_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n" 
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара первого противника = " + str(monster1_strength + enemy1_cubic) + "\n"
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара второго противника = " + str(monster2_strength + enemy2_cubic) + "\n"           
            if self.strength + your_cubic <= monster1_strength + enemy1_cubic:
                self.life_points -= 2
                self.battle_text += "Первый противник ударил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            elif self.strength + your_cubic >= monster1_strength + enemy1_cubic:
                monster1_life_points -= 2
                self.battle_text += "Вы ударили первого противника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"
                if monster1_life_points <= 0:
                    self.battle_text += "Первый противник повержен. Остался Второй!!!"
                    man1_alive = False
                    break
            else:
                self.battle_text += "Первый противник парировал ваш удар.\n"
           
            if self.strength + your_cubic >= monster1_strength + enemy2_cubic:
                self.battle_text += "Вы парировали удар Второго противника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"                          
            else:
                self.life_points -= 2
                self.battle_text += "Второй противник ударил вас.\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

        message_battleground_two = QDialog()
        message_battleground_two.setWindowTitle("Окно битвы")
        message_battleground_two.setFixedSize(800, 600)
        textEdit_battleground_two = QTextEdit(message_battleground_two)
        textEdit_battleground_two.setFixedSize(800, 555)
        textEdit_battleground_two.clear()
        textEdit_battleground_two.setText(self.battle_text)
        buttonBox_battleground_two = QDialogButtonBox(message_battleground_two)
        buttonBox_battleground_two.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_two.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_two.accepted.connect(message_battleground_two.accept)
        font_battleground_two = QFont()
        font_battleground_two.setPointSize(10)
        message_battleground_two.setFont(font_battleground_two)
        # установить фокус на кнопке ОК
        buttonBox_battleground_two.setFocus()
        message_battleground_two.exec_()
        if self.life_points <= 0:
            message2_battleground_two = QMessageBox()
            message2_battleground_two.setWindowTitle(":-(")
            message2_battleground_two.setText("Вы проиграли.\nКонец игры...")
            font_battleground_two.setPointSize(14)
            message2_battleground_two.setFont(font_battleground_two)
            message2_battleground_two.exec_()
            sys.exit("Game over")
        elif man1_alive == False:
            message3_battleground_two = QMessageBox()
            message3_battleground_two.setWindowTitle("!!!!!!")
            message3_battleground_two.setText("Один противник повержен. Остался еще один.")
            font_battleground_two.setPointSize(14)
            message3_battleground_two.setFont(font_battleground_two)
            message3_battleground_two.exec_()
        else:
            message3_battleground_two = QMessageBox()
            message3_battleground_two.setWindowTitle("!!!!!!!")
            message3_battleground_two.setText("Один противник повержен. Остался еще один.")
            font_battleground_two.setPointSize(14)
            message3_battleground_two.setFont(font_battleground_two)
            message3_battleground_two.exec_()

        self.battle_text = ""
        while man2_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n" 
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара Второго противника = " + str(monster2_strength + enemy2_cubic) + "\n"
            if self.strength + your_cubic <= monster2_strength + enemy2_cubic:
                self.life_points -= 2
                self.battle_text += "Второй противник ударил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            elif self.strength + your_cubic >= monster2_strength + enemy2_cubic:
                monster2_life_points -= 2
                self.battle_text += "Вы ударили второго противника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster2_life_points) + "\n"
                if monster2_life_points <= 0:
                    self.battle_text += "Второй противник повержен. Вы выиграли!!!"
                    man2_alive = False
                    break
            else:
                self.battle_text += "Первый противник парировал ваш удар.\n"
                continue

        message4_battleground_two = QDialog()
        message4_battleground_two.setWindowTitle("Окно битвы")
        message4_battleground_two.setFixedSize(800, 600)
        textEdit4_battleground_two = QTextEdit(message4_battleground_two)
        textEdit4_battleground_two.setFixedSize(800, 555)
        textEdit4_battleground_two.clear()
        textEdit4_battleground_two.setText(self.battle_text)
        buttonBox4_battleground_two = QDialogButtonBox(message4_battleground_two)
        buttonBox4_battleground_two.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox4_battleground_two.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox4_battleground_two.accepted.connect(message4_battleground_two.accept)
        font_battleground_two = QFont()
        font_battleground_two.setPointSize(10)
        message4_battleground_two.setFont(font_battleground_two)
        # установить фокус на кнопке ОК
        buttonBox4_battleground_two.setFocus()
        message4_battleground_two.exec_()
        if self.life_points <= 0:
            message5_battleground_two = QMessageBox()
            message5_battleground_two.setWindowTitle(":-(")
            message5_battleground_two.setText("Вы проиграли.\nКонец игры...")
            font_battleground_two.setPointSize(14)
            message5_battleground_two.setFont(font_battleground_two)
            message5_battleground_two.exec_()
            sys.exit("Game over")        
        elif man2_alive == False:
            message6_battleground_two = QMessageBox()
            message6_battleground_two.setWindowTitle(":-)")
            message6_battleground_two.setText("Вы выиграли!!!")
            font_battleground_two.setPointSize(14)
            message6_battleground_two.setFont(font_battleground_two)
            message6_battleground_two.exec_()
            return self.life_points
        else:
            message6_battleground_two = QMessageBox()
            message6_battleground_two.setWindowTitle(":-)")
            message6_battleground_two.setText("Вы выиграли!!!")
            font_battleground_two.setPointSize(14)
            message6_battleground_two.setFont(font_battleground_two)
            message6_battleground_two.exec_()
            return self.life_points       
            

    def battleground_two_copy_spell(self, monster1_name, monster1_strength, monster1_life_points, monster2_name, monster2_strength, monster2_life_points):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        self.round_number = 0
        copy_strength = monster1_strength
        copy_life_points = monster1_life_points
        man1_alive = True
        man2_alive = True
        while man1_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy1_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n" 
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + ",  Сила удара первого противника = " + str(monster1_strength + enemy1_cubic) + "\n"
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + ",  Сила удара второго противника = " + str(monster2_strength + enemy2_cubic) + "\n"           
            if copy_strength + your_cubic <= monster1_strength + enemy1_cubic:
                copy_life_points -= 2
                self.battle_text += "Первый противник ударил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            elif copy_strength + your_cubic >= monster1_strength + enemy1_cubic:
                monster1_life_points -= 2
                self.battle_text += "Копия ударила первого противника.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"
                if monster1_life_points <= 0:
                    self.battle_text += "Первый противник повержен. Остался Второй!!!"
                    man1_alive = False
                    break
            else:
                self.battle_text += "Первый противник парировал ваш удар.\n"
           
            if copy_strength + your_cubic >= monster1_strength + enemy2_cubic:
                self.battle_text += "Копия парировала удар Второго противника.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster1_life_points) + "\n"                          
            else:
                copy_life_points -= 2
                self.battle_text += "Второй противник ударил копию.\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

        message_battleground_two_copy_spell = QDialog()
        message_battleground_two_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_two_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_two_copy_spell = QTextEdit(message_battleground_two_copy_spell)
        textEdit_battleground_two_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_two_copy_spell.clear()
        textEdit_battleground_two_copy_spell.setText(self.battle_text)
        buttonBox_battleground_two_copy_spell = QDialogButtonBox(message_battleground_two_copy_spell)
        buttonBox_battleground_two_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_two_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_two_copy_spell.accepted.connect(message_battleground_two_copy_spell.accept)
        font_battleground_two_copy_spell = QFont()
        font_battleground_two_copy_spell.setPointSize(10)
        message_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_two_copy_spell.setFocus()
        message_battleground_two_copy_spell.exec_()
        if copy_life_points <= 0:
            message2_battleground_two_copy_spell = QMessageBox()
            message2_battleground_two_copy_spell.setWindowTitle("!!!")
            message2_battleground_two_copy_spell.setText("Копия проигралаи исчезает!!!")
            font_battleground_two_copy_spell.setPointSize(14)
            message2_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message2_battleground_two_copy_spell.exec_()
            self.battleground_two("Противник 1", monster1_strength, monster1_life_points, "Противник 2", monster2_strength, monster2_life_points)
            return self.life_points
        elif man1_alive == False:
            message3_battleground_two_copy_spell = QMessageBox()
            message3_battleground_two_copy_spell.setWindowTitle("!!!!!!")
            message3_battleground_two_copy_spell.setText("Первый противник повержен. Остался Второй.")
            font_battleground_two_copy_spell.setPointSize(14)
            message3_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message3_battleground_two_copy_spell.exec_()
        else:
            message3_battleground_two_copy_spell = QMessageBox()
            message3_battleground_two_copy_spell.setWindowTitle("!!!!!!!")
            message3_battleground_two_copy_spell.setText("Первый противник повержен. Остался Второй.")
            font_battleground_two_copy_spell.setPointSize(14)
            message3_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message3_battleground_two_copy_spell.exec_()

        self.battle_text = ""
        while man2_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n" 
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + ",  Сила удара Второго противника = " + str(monster2_strength + enemy2_cubic) + "\n"
            if copy_strength + your_cubic <= monster2_strength + enemy2_cubic:
                copy_life_points -= 2
                self.battle_text += "Второй противник ударил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster2_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            elif copy_strength + your_cubic >= monster2_strength + enemy2_cubic:
                monster2_life_points -= 2
                self.battle_text += "Копия ударила второго противника.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(monster2_life_points) + "\n"
                if monster2_life_points <= 0:
                    self.battle_text += "Второй противник повержен. Вы выиграли!!!"
                    man2_alive = False
                    break
            else:
                self.battle_text += "Первый противник парировал ваш удар.\n"
                continue

        message4_battleground_two_copy_spell = QDialog()
        message4_battleground_two_copy_spell.setWindowTitle("Окно битвы")
        message4_battleground_two_copy_spell.setFixedSize(800, 600)
        textEdit4_battleground_two_copy_spell = QTextEdit(message4_battleground_two_copy_spell)
        textEdit4_battleground_two_copy_spell.setFixedSize(800, 555)
        textEdit4_battleground_two_copy_spell.clear()
        textEdit4_battleground_two_copy_spell.setText(self.battle_text)
        buttonBox4_battleground_two_copy_spell = QDialogButtonBox(message4_battleground_two_copy_spell)
        buttonBox4_battleground_two_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox4_battleground_two_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox4_battleground_two_copy_spell.accepted.connect(message4_battleground_two_copy_spell.accept)
        font_battleground_two_copy_spell = QFont()
        font_battleground_two_copy_spell.setPointSize(10)
        message4_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox4_battleground_two_copy_spell.setFocus()
        message4_battleground_two_copy_spell.exec_()
        if copy_life_points <= 0:
            message5_battleground_two_copy_spell = QMessageBox()
            message5_battleground_two_copy_spell.setWindowTitle("!!!")
            message5_battleground_two_copy_spell.setText("Копия проиграла и исчезает!!!")
            font_battleground_two_copy_spell.setPointSize(14)
            message5_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message5_battleground_two_copy_spell.exec_()
            self.battleground_one("Противник 2", monster2_strength, monster2_life_points)
            return self.life_points      
        elif man2_alive == False:
            message6_battleground_two_copy_spell = QMessageBox()
            message6_battleground_two_copy_spell.setWindowTitle(":-)")
            message6_battleground_two_copy_spell.setText("Вы выиграли!!!")
            font_battleground_two_copy_spell.setPointSize(14)
            message6_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message6_battleground_two_copy_spell.exec_()
            return self.life_points
        else:
            message6_battleground_two_copy_spell = QMessageBox()
            message6_battleground_two_copy_spell.setWindowTitle(":-)")
            message6_battleground_two_copy_spell.setText("Вы выиграли!!!")
            font_battleground_two_copy_spell.setPointSize(14)
            message6_battleground_two_copy_spell.setFont(font_battleground_two_copy_spell)
            message6_battleground_two_copy_spell.exec_()
            return self.life_points 


    def battleground_16_3(self):
        self.battle_text = ""
        bat1_alive = True
        bat2_alive = True
        bat3_alive = True
        bat1_strength = 6
        bat2_strength = bat3_strength = 5
        bat1_life_points = 8
        bat2_life_points = 7
        bat3_life_points = 6
        while bat1_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            bat1_cubic = random.randint(2, 12)
            bat2_cubic = random.randint(2, 12)
            bat3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первой летучей мыши = " + str(bat1_strength) + "\n"
            self.battle_text += "Сила удара Второй летучей мыши = " + str(bat2_strength) + "\n"
            self.battle_text += "Сила удара Третьей летучей мыши = " + str(bat3_strength) + "\n"
            if self.strength + your_cubic > bat1_strength + bat1_cubic:
                self.battle_text += "Вы ранили первую летучую мышь.\n"
                bat1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОЙ ЛЕТУЧЕЙ МЫШИ = " + str(bat1_life_points) + "\n"
                if bat1_life_points <= 0:
                    bat1_alive = False
                    self.battle_text += "Первая летучая мышь повержена!!!\n"
            elif self.strength + your_cubic < bat1_strength + bat1_cubic:
                self.life_points -= 2
                self.battle_text += "Первая летучая мышь ранила вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОЙ ЛЕТУЧЕЙ МЫШИ = " + str(bat1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОЙ ЛЕТУЧЕЙ МЫШИ = " + str(bat1_life_points) + "\n"

            if self.strength + your_cubic >= bat2_strength + bat2_cubic:
                self.battle_text += "Вы парировали удар второй летучей мыши.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Вторая летучая мышь ранила вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

            if self.strength + your_cubic >= bat3_strength + bat3_cubic:
                self.battle_text += "Вы парировали удар третьей летучей мыши.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третья летучая мышь ранила вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break 

        message_battleground_16_3 = QDialog()
        message_battleground_16_3.setWindowTitle("Окно битвы")
        message_battleground_16_3.setFixedSize(800, 600)
        textEdit_battleground_16_3 = QTextEdit(message_battleground_16_3)
        textEdit_battleground_16_3.setFixedSize(800, 555)
        textEdit_battleground_16_3.clear()
        textEdit_battleground_16_3.setText(self.battle_text)
        buttonBox_battleground_16_3 = QDialogButtonBox(message_battleground_16_3)
        buttonBox_battleground_16_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_16_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_16_3.accepted.connect(message_battleground_16_3.accept)
        font_battleground_16_3 = QFont()
        font_battleground_16_3.setPointSize(10)
        message_battleground_16_3.setFont(font_battleground_16_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_16_3.setFocus()
        message_battleground_16_3.exec_()
        if self.life_points <= 0:
            message3_battleground_16_3 = QMessageBox()
            message3_battleground_16_3.setWindowTitle(":-(")
            message3_battleground_16_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_16_3.setPointSize(14)
            message3_battleground_16_3.setFont(font_battleground_16_3)
            message3_battleground_16_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_16_3 = QMessageBox()
            message3_battleground_16_3.setWindowTitle("!!!")
            message3_battleground_16_3.setText("Первая летучая мышь повержена!!! Осталось две.")
            font_battleground_16_3.setPointSize(14)
            message3_battleground_16_3.setFont(font_battleground_16_3)
            message3_battleground_16_3.exec_()
            self.battleground_two("Вторая летучая мышь", 5, 7, "Третья летучая мышь", 5, 6)
            return self.life_points

    def battleground_123_1(self, rogue3_name, rogue3_strength, rogue3_life_points):
        self.battle_text = ""
        rogue3_alive = True
        while rogue3_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + ", Сила удара третьего противника = " + str(rogue3_strength + rogue3_cubic) + "\n"
            if self.strength + your_cubic > rogue3_strength + rogue3_cubic:
                self.battle_text += "Вы ранили третьего противника.\n"
                rogue3_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"
                if rogue3_life_points <= 0:
                    rogue3_alive = False
                    self.battle_text += "Третий противник повержен!!!\n"
                    break
            elif self.strength + your_cubic < rogue3_strength + rogue3_cubic:
                self.life_points -= 2
                self.battle_text += "Третий противник ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"

        message_battleground_123_3 = QDialog()
        message_battleground_123_3.setWindowTitle("Окно битвы")
        message_battleground_123_3.setFixedSize(800, 600)
        textEdit_battleground_123_3 = QTextEdit(message_battleground_123_3)
        textEdit_battleground_123_3.setFixedSize(800, 555)
        textEdit_battleground_123_3.clear()
        textEdit_battleground_123_3.setText(self.battle_text)
        buttonBox_battleground_123_3 = QDialogButtonBox(message_battleground_123_3)
        buttonBox_battleground_123_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_3.accepted.connect(message_battleground_123_3.accept)
        font_battleground_123_3 = QFont()
        font_battleground_123_3.setPointSize(10)
        message_battleground_123_3.setFont(font_battleground_123_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_3.setFocus()
        message_battleground_123_3.exec_()
        if self.life_points <= 0:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle(":-(")
            message3_battleground_123_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle("!!!")
            message3_battleground_123_3.setText("Вы выиграли!!!")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            return self.life_points

    def battleground_123_2(self, rogue2_name, rogue2_strength, rogue2_life_points, rogue3_name, rogue3_strength, rogue3_life_points):
        self.battle_text = ""
        rogue2_alive = True
        rogue3_alive = True
        while rogue2_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue2_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго противника = " + str(rogue2_strength) + "\n"
            self.battle_text += "Сила удара Третьего противника = " + str(rogue3_strength) + "\n"
            if self.strength + your_cubic > rogue2_strength + rogue2_cubic:
                self.battle_text += "Вы ранили второго противника.\n"
                rogue2_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(rogue2_life_points) + "\n"
                if rogue2_life_points <= 0:
                    rogue2_alive = False
                    self.battle_text += "Второй противник повержен!!!\n"
            elif self.strength + your_cubic < rogue2_strength + rogue2_cubic:
                self.life_points -= 2
                self.battle_text += "Второй противник ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(rogue2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ПРОТИВНИКА = " + str(rogue2_life_points) + "\n"

            if self.strength + your_cubic >= rogue3_strength + rogue3_cubic:
                self.battle_text += "Вы парировали удар третьего противника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третий противник ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

        message_battleground_123_3 = QDialog()
        message_battleground_123_3.setWindowTitle("Окно битвы")
        message_battleground_123_3.setFixedSize(800, 600)
        textEdit_battleground_123_3 = QTextEdit(message_battleground_123_3)
        textEdit_battleground_123_3.setFixedSize(800, 555)
        textEdit_battleground_123_3.clear()
        textEdit_battleground_123_3.setText(self.battle_text)
        buttonBox_battleground_123_3 = QDialogButtonBox(message_battleground_123_3)
        buttonBox_battleground_123_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_3.accepted.connect(message_battleground_123_3.accept)
        font_battleground_123_3 = QFont()
        font_battleground_123_3.setPointSize(10)
        message_battleground_123_3.setFont(font_battleground_123_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_3.setFocus()
        message_battleground_123_3.exec_()
        if self.life_points <= 0:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle(":-(")
            message3_battleground_123_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle("!!!")
            message3_battleground_123_3.setText("Второй разбойник повержен!!! Остался один.")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            self.battleground_123_1("Третий разбойник", 5, 5)
            return self.life_points

    def battleground_123_3(self, rogue1_name, rogue1_strength, rogue1_life_points, rogue2_name, rogue2_strength, 
                            rogue2_life_points, rogue3_name, rogue3_strength, rogue3_life_points):
        self.battle_text = ""
        rogue1_alive = True
        rogue2_alive = True
        rogue3_alive = True
        rogue1_strength = 6
        rogue2_strength = 7
        rogue3_strength = 5
        rogue1_life_points = 4
        rogue2_life_points = 8
        rogue3_life_points = 5
        while rogue1_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue1_cubic = random.randint(2, 12)
            rogue2_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого разбойника = " + str(rogue1_strength) + "\n"
            self.battle_text += "Сила удара Второго разбойника = " + str(rogue2_strength) + "\n"
            self.battle_text += "Сила удара Третьего разбойника = " + str(rogue3_strength) + "\n"
            if self.strength + your_cubic > rogue1_strength + rogue1_cubic:
                self.battle_text += "Вы ранили первого разбойника.\n"
                rogue1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"
                if rogue1_life_points <= 0:
                    rogue1_alive = False
                    self.battle_text += "Первый разбойник повержен!!!\n"
            elif self.strength + your_cubic < rogue1_strength + rogue1_cubic:
                self.life_points -= 2
                self.battle_text += "Первый разбойник ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"

            if self.strength + your_cubic >= rogue2_strength + rogue2_cubic:
                self.battle_text += "Вы парировали удар второго разбойника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Второй разбойник ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

            if self.strength + your_cubic >= rogue3_strength + rogue3_cubic:
                self.battle_text += "Вы парировали удар третьего разбойника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третий разбойник ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break 

        message_battleground_123_3 = QDialog()
        message_battleground_123_3.setWindowTitle("Окно битвы")
        message_battleground_123_3.setFixedSize(800, 600)
        textEdit_battleground_123_3 = QTextEdit(message_battleground_123_3)
        textEdit_battleground_123_3.setFixedSize(800, 555)
        textEdit_battleground_123_3.clear()
        textEdit_battleground_123_3.setText(self.battle_text)
        buttonBox_battleground_123_3 = QDialogButtonBox(message_battleground_123_3)
        buttonBox_battleground_123_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_3.accepted.connect(message_battleground_123_3.accept)
        font_battleground_123_3 = QFont()
        font_battleground_123_3.setPointSize(10)
        message_battleground_123_3.setFont(font_battleground_123_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_3.setFocus()
        message_battleground_123_3.exec_()
        if self.life_points <= 0:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle(":-(")
            message3_battleground_123_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_123_3 = QMessageBox()
            message3_battleground_123_3.setWindowTitle("!!!")
            message3_battleground_123_3.setText("Первый разбойник повержен!!! Осталось два.")
            font_battleground_123_3.setPointSize(14)
            message3_battleground_123_3.setFont(font_battleground_123_3)
            message3_battleground_123_3.exec_()
            self.battleground_123_2("Второй разбойник", 7, 8, "Третий разбойник", 5, 5)
            return self.life_points

    def battleground_123_1_copy_spell(self, copy_strength, copy_life_points, rogue3_name, rogue3_strength, rogue3_life_points):
        self.battle_text = ""
        rogue3_alive = True
        while rogue3_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Сила Удара копии = " + str(copy_strength + your_cubic) + ", Сила удара противника = " + str(rogue3_strength + rogue3_cubic) + "\n"
            if copy_strength + your_cubic > rogue3_strength + rogue3_cubic:
                self.battle_text += "Копия ранила противника.\n"
                rogue3_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"
                if rogue3_life_points <= 0:
                    rogue3_alive = False
                    self.battle_text += "Третий противник повержен!!!\n"
                    break
            elif copy_strength + your_cubic < rogue3_strength + rogue3_cubic:
                copy_life_points -= 2
                self.battle_text += "Противник ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(rogue3_life_points) + "\n"

        message_battleground_123_1_copy_spell = QDialog()
        message_battleground_123_1_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_123_1_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_123_1_copy_spell = QTextEdit(message_battleground_123_1_copy_spell)
        textEdit_battleground_123_1_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_123_1_copy_spell.clear()
        textEdit_battleground_123_1_copy_spell.setText(self.battle_text)
        buttonBox_battleground_123_1_copy_spell = QDialogButtonBox(message_battleground_123_1_copy_spell)
        buttonBox_battleground_123_1_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_1_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_1_copy_spell.accepted.connect(message_battleground_123_1_copy_spell.accept)
        font_battleground_123_1_copy_spell = QFont()
        font_battleground_123_1_copy_spell.setPointSize(10)
        message_battleground_123_1_copy_spell.setFont(font_battleground_123_1_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_1_copy_spell.setFocus()
        message_battleground_123_1_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_123_1_copy_spell = QMessageBox()
            message3_battleground_123_1_copy_spell.setWindowTitle("!!!")
            message3_battleground_123_1_copy_spell.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_123_1_copy_spell.setPointSize(14)
            message3_battleground_123_1_copy_spell.setFont(font_battleground_123_1_copy_spell)
            message3_battleground_123_1_copy_spell.exec_()
            self.battleground_123_1("Третий орк", 7, rogue3_life_points)
            return self.life_points                
        else:
            message3_battleground_123_1_copy_spell = QMessageBox()
            message3_battleground_123_1_copy_spell.setWindowTitle("!!!")
            message3_battleground_123_1_copy_spell.setText("Противник повержен. Вы выиграли!!!")
            font_battleground_123_1_copy_spell.setPointSize(14)
            message3_battleground_123_1_copy_spell.setFont(font_battleground_123_1_copy_spell)
            message3_battleground_123_1_copy_spell.exec_()
            return self.life_points

    def battleground_123_2_copy_spell(self, copy_strength, copy_life_points, rogue2_name, rogue2_strength, rogue2_life_points, 
                                            rogue3_name, rogue3_strength, rogue3_life_points):
        self.battle_text = ""
        rogue2_alive = True
        rogue3_alive = True
        while rogue2_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue2_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго разбойника = " + str(rogue2_strength) + "\n"
            self.battle_text += "Сила удара Третьего разбойника = " + str(rogue3_strength) + "\n"
            if copy_strength + your_cubic > rogue2_strength + rogue2_cubic:
                self.battle_text += "Копия ранила второго разбойника.\n"
                rogue2_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО РАЗБОЙНИКА = " + str(rogue2_life_points) + "\n"
                if rogue2_life_points <= 0:
                    rogue2_alive = False
                    self.battle_text += "Второй разбойник повержен!!!\n"
            elif copy_strength + your_cubic < rogue2_strength + rogue2_cubic:
                copy_life_points -= 2
                self.battle_text += "Второй разбойник ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО РАЗБОЙНИКА = " + str(rogue2_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО РАЗБОЙНИКА = " + str(rogue2_life_points) + "\n"

            if copy_strength + your_cubic >= rogue3_strength + rogue3_cubic:
                self.battle_text += "Копия парировала удар третьего разбойника.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
            else:
                self.battle_text += "Третий разбойник ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

        message_battleground_123_2_copy_spell = QDialog()
        message_battleground_123_2_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_123_2_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_123_2_copy_spell = QTextEdit(message_battleground_123_2_copy_spell)
        textEdit_battleground_123_2_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_123_2_copy_spell.clear()
        textEdit_battleground_123_2_copy_spell.setText(self.battle_text)
        buttonBox_battleground_123_2_copy_spell = QDialogButtonBox(message_battleground_123_2_copy_spell)
        buttonBox_battleground_123_2_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_2_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_2_copy_spell.accepted.connect(message_battleground_123_2_copy_spell.accept)
        font_battleground_123_2_copy_spell = QFont()
        font_battleground_123_2_copy_spell.setPointSize(10)
        message_battleground_123_2_copy_spell.setFont(font_battleground_123_2_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_2_copy_spell.setFocus()
        message_battleground_123_2_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_123_2_copy_spell = QMessageBox()
            message3_battleground_123_2_copy_spell.setWindowTitle("!!!")
            message3_battleground_123_2_copy_spell.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_123_2_copy_spell.setPointSize(14)
            message3_battleground_123_2_copy_spell.setFont(font_battleground_123_2_copy_spell)
            message3_battleground_123_2_copy_spell.exec_()
            self.battleground_123_2("Второй разбойник", 7, rogue2_life_points, "Третий разбойник", 5, 5)
            return self.life_points                 
        else:
            message3_battleground_123_2_copy_spell = QMessageBox()
            message3_battleground_123_2_copy_spell.setWindowTitle("!!!")
            message3_battleground_123_2_copy_spell.setText("Второй разбойник повержен!!! Остался третий разбойник.")
            font_battleground_123_2_copy_spell.setPointSize(14)
            message3_battleground_123_2_copy_spell.setFont(font_battleground_123_2_copy_spell)
            message3_battleground_123_2_copy_spell.exec_()
            self.battleground_123_1_copy_spell(copy_strength, copy_life_points, "Третий разбойник", 5, 5)
            return self.life_points

    def battleground_123_3_copy_spell(self):
        self.battle_text = ""
        rogue1_alive = True
        rogue2_alive = True
        rogue3_alive = True
        rogue1_strength = 6
        copy_strength = rogue2_strength = 7
        rogue3_strength = 5
        rogue1_life_points = 4
        copy_life_points = rogue2_life_points = 8
        rogue3_life_points = 5
        while rogue1_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            rogue1_cubic = random.randint(2, 12)
            rogue2_cubic = random.randint(2, 12)
            rogue3_cubic = random.randint(2, 12)
            self.battle_text += "Сила Удара копии = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого разбойника = " + str(rogue1_strength) + "\n"
            self.battle_text += "Сила удара Второго разбойника = " + str(rogue2_strength) + "\n"
            self.battle_text += "Сила удара Третьего разбойника = " + str(rogue3_strength) + "\n"
            if copy_strength + your_cubic > rogue1_strength + rogue1_cubic:
                self.battle_text += "Вы ранили первого разбойника.\n"
                rogue1_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"
                if rogue1_life_points <= 0:
                    rogue1_alive = False
                    self.battle_text += "Первый разбойник повержен!!!\n"
            elif copy_strength + your_cubic < rogue1_strength + rogue1_cubic:
                copy_life_points -= 2
                self.battle_text += "Первый разбойник ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РАЗБОЙНИКА = " + str(rogue1_life_points) + "\n"

            if self.strength + your_cubic >= rogue2_strength + rogue2_cubic:
                self.battle_text += "Копия парировала удар второго разбойника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(copy_life_points) + "\n"
            else:
                self.battle_text += "Второй разбойник ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

            if copy_strength + your_cubic >= rogue3_strength + rogue3_cubic:
                self.battle_text += "Копия парировала удар третьего разбойника.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третий разбойник ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(self.life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break 

        message_battleground_123_3_copy_spell = QDialog()
        message_battleground_123_3_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_123_3_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_123_3_copy_spell = QTextEdit(message_battleground_123_3_copy_spell)
        textEdit_battleground_123_3_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_123_3_copy_spell.clear()
        textEdit_battleground_123_3_copy_spell.setText(self.battle_text)
        buttonBox_battleground_123_3_copy_spell = QDialogButtonBox(message_battleground_123_3_copy_spell)
        buttonBox_battleground_123_3_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_123_3_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_123_3_copy_spell.accepted.connect(message_battleground_123_3_copy_spell.accept)
        font_battleground_123_3_copy_spell = QFont()
        font_battleground_123_3_copy_spell.setPointSize(10)
        message_battleground_123_3_copy_spell.setFont(font_battleground_123_3_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_123_3_copy_spell.setFocus()
        message_battleground_123_3_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_123_3_copy_spell = QMessageBox()
            message3_battleground_123_3_copy_spell.setWindowTitle(":-(")
            message3_battleground_123_3_copy_spell.setText("Вы проиграли.\nКонец игры...")
            font_battleground_123_3_copy_spell.setPointSize(14)
            message3_battleground_123_3_copy_spell.setFont(font_battleground_123_3_copy_spell)
            message3_battleground_123_3_copy_spell.exec_()
            self.battleground_123_3("Первый разбойник", 6, rogue1_life_points, "Второй разбойник", 7, 8, "Третий разбойник", 5, 5)
            return self.life_points        
        else:
            message3_battleground_123_3_copy_spell = QMessageBox()
            message3_battleground_123_3_copy_spell.setWindowTitle("!!!")
            message3_battleground_123_3_copy_spell.setText("Первый разбойник повержен!!! Осталось два.")
            font_battleground_123_3_copy_spell.setPointSize(14)
            message3_battleground_123_3_copy_spell.setFont(font_battleground_123_3_copy_spell)
            message3_battleground_123_3_copy_spell.exec_()
            self.battleground_123_2_copy_spell(copy_strength, copy_life_points, "Второй разбойник", 7, 8, "Третий разбойник", 5, 5)
            return self.life_points

    def battleground_65(self):
        self.battle_text = "Начало битвы.\n"
        enemy_strength = 9
        enemy_life_points = 5
        enemy_alive = True
        while self.round_number < 3:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Ваша сила удара = " + str(self.strength + your_cubic) + ", Сила удара начальника стражи = " + str(enemy_strength + enemy_cubic) + "\n"
            if self.strength + your_cubic >= enemy_strength + enemy_cubic:
                self.battle_text += "Вы ранили начальника стражи.\n"
                enemy_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                if enemy_life_points <= 0:
                    enemy_alive = False
                    self.battle_text += "Начальник стражи убит за 3 раунда атаки.\n"
            elif self.strength + your_cubic <= enemy_strength + enemy_cubic:
                self.battle_text += "Начальник стражи ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Начальник стражи парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                
        message_battleground_65 = QDialog()
        message_battleground_65.setWindowTitle("Окно битвы")
        message_battleground_65.setFixedSize(800, 600)
        textEdit_battleground_65 = QTextEdit(message_battleground_65)
        textEdit_battleground_65.setFixedSize(800, 555)
        textEdit_battleground_65.clear()
        textEdit_battleground_65.setText(self.battle_text)
        buttonBox_battleground_65 = QDialogButtonBox(message_battleground_65)
        buttonBox_battleground_65.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_65.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_65.accepted.connect(message_battleground_65.accept)
        font_battleground_65 = QFont()
        font_battleground_65.setPointSize(10)
        message_battleground_65.setFont(font_battleground_65)
        # установить фокус на кнопке ОК
        buttonBox_battleground_65.setFocus()
        message_battleground_65.exec_() 
        if self.life_points <= 0:
            message3_battleground_65 = QMessageBox()
            message3_battleground_65.setWindowTitle(":-(")
            message3_battleground_65.setText("Вы проиграли.\nКонец игры...")
            font_battleground_65.setPointSize(14)
            message3_battleground_65.setFont(font_battleground_65)
            message3_battleground_65.exec_()
            sys.exit("Game over")        
        elif enemy_alive == False:
            self.page_number_65_next_page = 705
            message3_battleground_65 = QMessageBox()
            message3_battleground_65.setWindowTitle(":-)")
            message3_battleground_65.setText("Вы выиграли за 3 раунда атаки!!!")
            font_battleground_65.setPointSize(14)
            message3_battleground_65.setFont(font_battleground_65)
            message3_battleground_65.exec_()
            return self.life_points
        else:
            self.page_number_65_next_page = 726
            message3_battleground_65 = QMessageBox()
            message3_battleground_65.setWindowTitle("!!!")
            message3_battleground_65.setText("Вы не выиграли за 3 раунда атаки!!!")
            font_battleground_65.setPointSize(14)
            message3_battleground_65.setFont(font_battleground_65)
            message3_battleground_65.exec_()
            return self.life_points


    def battleground_65_copy_spell(self):
        self.battle_text = "Начало битвы.\n"
        copy_strength = enemy_strength = 9
        copy_life_points = enemy_life_points = 5
        enemy_alive = True
        while self.round_number < 3:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + ", Сила удара начальника стражи = " + str(enemy_strength + enemy_cubic) + "\n"
            if copy_strength + your_cubic >= enemy_strength + enemy_cubic:
                self.battle_text += "Копия ранила начальника стражи.\n"
                enemy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                if enemy_life_points <= 0:
                    enemy_alive = False
                    self.battle_text += "Начальник стражи убит за 3 раунда атаки.\n"
            elif copy_strength + your_cubic <= enemy_strength + enemy_cubic:
                self.battle_text += "Начальник стражи ранил копию.\n"
                self.life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Начальник стражи парировал удар.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n" + "ВЫНОСЛИВОСТЬ НАЧАЛЬНИКА СТРАЖИ = " + str(enemy_life_points) + "\n"
                
        message_battleground_65_copy_spell = QDialog()
        message_battleground_65_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_65_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_65_copy_spell = QTextEdit(message_battleground_65_copy_spell)
        textEdit_battleground_65_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_65_copy_spell.clear()
        textEdit_battleground_65_copy_spell.setText(self.battle_text)
        buttonBox_battleground_65_copy_spell = QDialogButtonBox(message_battleground_65_copy_spell)
        buttonBox_battleground_65_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_65_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_65_copy_spell.accepted.connect(message_battleground_65_copy_spell.accept)
        font_battleground_65_copy_spell = QFont()
        font_battleground_65_copy_spell.setPointSize(10)
        message_battleground_65_copy_spell.setFont(font_battleground_65_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_65_copy_spell.setFocus()
        message_battleground_65_copy_spell.exec_() 
        if copy_life_points <= 0:
            message3_battleground_65_copy_spell = QMessageBox()
            message3_battleground_65_copy_spell.setWindowTitle("!!!!")
            message3_battleground_65_copy_spell.setText("Копия проиграла и исчезает!!!")
            font_battleground_65_copy_spell.setPointSize(14)
            message3_battleground_65_copy_spell.setFont(font_battleground_65_copy_spell)
            message3_battleground_65_copy_spell.exec_()
            self.battleground_65()
            return self.life_points                  
        elif enemy_alive == False:
            self.page_number_65_next_page = 705
            message3_battleground_65_copy_spell = QMessageBox()
            message3_battleground_65_copy_spell.setWindowTitle(":-)")
            message3_battleground_65_copy_spell.setText("Вы выиграли за 3 раунда атаки!!!")
            font_battleground_65_copy_spell.setPointSize(14)
            message3_battleground_65_copy_spell.setFont(font_battleground_65_copy_spell)
            message3_battleground_65_copy_spell.exec_()
            return self.life_points
        else:
            self.page_number_65_next_page = 726
            message3_battleground_65_copy_spell = QMessageBox()
            message3_battleground_65_copy_spell.setWindowTitle("!!!")
            message3_battleground_65_copy_spell.setText("Вы не выиграли за 3 раунда атаки!!!")
            font_battleground_65_copy_spell.setPointSize(14)
            message3_battleground_65_copy_spell.setFont(font_battleground_65_copy_spell)
            message3_battleground_65_copy_spell.exec_()
            return self.life_points


    def battleground_301(self):
        enemy1_alive = True
        enemy2_alive = True
        enemy3_alive = True
        enemy1_strength = enemy2_strength = enemy3_strength = 10
        captain_strength = 12
        enemy1_life_points = enemy2_life_points = enemy3_life_points = 10
        captain_life_points = 12
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        round_number = 0
        # 1-5 раунды боя
        while round_number < 5:
            your_cubic = random.randint(2, 12)
            enemy1_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "У вас выпало: " + str(your_cubic) + ". Ваша сила удара  = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "У первого рыцаря выпало: " + str(enemy1_cubic) + ", Сила удара первого рыцаря = " + str(enemy1_strength + enemy1_cubic) + "\n"
            self.battle_text += "У второго рыцаря выпало: " + str(enemy2_cubic) + ", Сила удара второго рыцаря = " + str(enemy2_strength + enemy2_cubic) + "\n"
           
            if self.strength + your_cubic > enemy1_strength + enemy1_cubic:
                # 1-й вариант - вы ранили первого рыцаря
                self.battle_text += "Вы ранили первого рыцаря."
                enemy1_life_points -= 2
                # проверка Выносливости 1-го рыцаря, если она <= 0, то еще один ход делает 2-й рыцарь, а затем цикл прерывается
                if enemy1_life_points <= 0:
                    self.battle_text += "Первый рыцарь побежден!!!\n"
                    enemy1_alive = False
                    if self.strength + your_cubic >= enemy2_strength + enemy2_cubic:
                        self.battle_text += " Вы парировали удар второго рыцаря.\n"
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = 0" + 
                                            ",  ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")                       
                        break
                    else:
                        self.battle_text += " Второй рыцарь ранил вас.\n"
                        self.life_points -= 2
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                            ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                        if self.life_points <= 0:
                            self.battle_text += "Вы проиграли!!!\n"
                            break
                        else:
                            break
                else:                      
                    if self.strength + your_cubic >= enemy2_strength + enemy2_cubic:
                        self.battle_text += " Вы парировали удар второго рыцаря.\n"
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                            ",  ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                        if enemy1_life_points <= 0:
                            self.battle_text += "Первый рыцарь побежден!!!\n"
                            enemy1_alive = False
                            break
                        else:
                            continue
                    else:
                        self.battle_text += " Второй рыцарь ранил вас.\n"
                        self.life_points -= 2
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                            ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                        if self.life_points <= 0:
                            self.battle_text += "Вы проиграли!!!\n"
                            break
                        else:
                            continue              

            elif self.strength + your_cubic < enemy1_strength + enemy1_cubic:
                # 2-й вариант - первый рыцарь ранил вас
                self.battle_text += "Первый рыцарь ранил вас."
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:                  
                    if self.strength + your_cubic >= enemy2_strength + enemy2_cubic:
                        self.battle_text += " Вы парировали удар второго рыцаря.\n"
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                            ",  ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                        if enemy1_life_points <= 0:
                            self.battle_text += "Первый рыцарь побежден!!!\n"
                            enemy1_alive = False
                            break
                        else:
                            continue                    
                    elif self.strength + your_cubic < enemy2_strength + enemy2_cubic:
                        self.battle_text += " Второй рыцарь ранил вас.\n"
                        self.life_points -= 2
                        self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                            ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                        if self.life_points <= 0:
                            self.battle_text += "Вы проиграли!!!\n"
                            break
                        else:
                            continue
            else:
                # 3-й вариант - равные Силы ударов, первый рыцарь парировал удар
                self.battle_text += "Первый рыцарь парировал удар."
                if self.strength + your_cubic >= enemy2_strength + enemy2_cubic:
                    self.battle_text += " Вы парировали удар второго рыцаря.\n"
                    self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                        ",  ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                    continue
                elif self.strength + your_cubic < enemy2_strength + enemy2_cubic:
                    self.battle_text += " Второй рыцарь ранил вас.\n"
                    self.life_points -= 2
                    self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                        ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")
                    if self.life_points <= 0:
                        self.battle_text += "Вы проиграли!!!\n"
                        break
                    else:
                        continue

        # 6-й раунд опишем отдельно                    
        if enemy1_alive == True:
            your_cubic = random.randint(2, 12)
            enemy1_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд 6.\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic)
            self.battle_text += ", Сила Удара Первого Рыцаря = " + str(enemy1_cubic + 10)
            self.battle_text += ", Сила Удара Второго Рыцаря = " + str(enemy2_cubic + 10) + "\n"
            if your_cubic + self.strength >= enemy1_cubic + 10:
                enemy1_life_points -= 2
                if enemy1_life_points <= 0:
                    self.battle_text += "Первый рыцарь повержен!!!\n"
                    enemy1_alive = False
                else:
                    self.battle_text += "Вы ранили первого рыцаря.\n"    
            elif your_cubic + self.strength < enemy1_cubic + 10:
                self.battle_text += "Первый рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                else:
                    self.battle_text += ""    
            else:
                self.battle_text += "Первый рыцарь парировал удар.\n"

            if your_cubic + self.strength >= enemy2_cubic + 10:
                self.battle_text += "Вы парировали удар второго рыцаря\n"
            else:
                self.battle_text += "Второй рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                else:
                    self.battle_text += ""
            self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + 
                                        ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n") 
        else:
            your_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд 6.\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic)
            self.battle_text += ", Сила Удара Второго Рыцаря = " + str(enemy2_cubic + 10) + "\n"
            if your_cubic + self.strength >= enemy2_cubic + 10:
                self.battle_text += "Вы ударили второго рыцаря\n"
                enemy2_life_points -= 2
            elif your_cubic + self.strength <= enemy2_cubic + 10:
                self.battle_text += "Второй рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Второй рыцарь парировал удар.\n"
            self.battle_text += ("ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n")        



        message_battleground_301 = QDialog()
        message_battleground_301.setWindowTitle("Окно битвы")
        message_battleground_301.setFixedSize(800, 600)
        textEdit_battleground_301 = QTextEdit(message_battleground_301)
        textEdit_battleground_301.setFixedSize(800, 555)
        textEdit_battleground_301.clear()
        textEdit_battleground_301.setText(self.battle_text)
        buttonBox_battleground_301 = QDialogButtonBox(message_battleground_301)
        buttonBox_battleground_301.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_301.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_301.accepted.connect(message_battleground_301.accept)
        font_battleground_301 = QFont()
        font_battleground_301.setPointSize(10)
        message_battleground_301.setFont(font_battleground_301)
        # установить фокус на кнопке ОК
        buttonBox_battleground_301.setFocus()
        message_battleground_301.exec_() 
        if self.life_points <= 0:
            message2_battleground_301 = QMessageBox()
            message2_battleground_301.setWindowTitle(":-(")
            message2_battleground_301.setText("Вы проиграли.\nКонец игры...")
            font_battleground_301.setPointSize(14)
            message2_battleground_301.setFont(font_battleground_301)
            message2_battleground_301.exec_()
            sys.exit("Game over")
        elif enemy1_alive == False:
            message4_battleground_301 = QMessageBox()
            message4_battleground_301.setWindowTitle("!!!!")
            message4_battleground_301.setText("Первый рыцарь повержен!!!")
            font_battleground_301.setPointSize(14)
            message4_battleground_301.setFont(font_battleground_301)
            message4_battleground_301.exec_()
            message4_battleground_301 = QMessageBox()
            message4_battleground_301.setWindowTitle("!!!!")
            message4_battleground_301.setText("Закончились 6 раундов атаки, к битве присоединяется третий Зеленый рыцарь")
            font_battleground_301.setPointSize(14)
            message4_battleground_301.setFont(font_battleground_301)
            message4_battleground_301.exec_()            
        else:
            message3_battleground_301 = QMessageBox()
            message3_battleground_301.setWindowTitle("!!!!")
            message3_battleground_301.setText("Закончились 6 раундов атаки, к битве присоединяется третий Зеленый рыцарь")
            font_battleground_301.setPointSize(14)
            message3_battleground_301.setFont(font_battleground_301)
            message3_battleground_301.exec_()

        # к битве присоединяется 3-й рыцарь
        # бой с 7-го раунда
        # если 1-й рыцарь еще жив 
        self.battle_text = ""      
        while enemy1_alive == True:
            your_cubic = random.randint(2, 12)
            enemy1_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            enemy3_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила Удара Первого Рыцаря = " + str(enemy1_cubic + 10)
            self.battle_text += ", Сила Удара Второго Рыцаря = " + str(enemy2_cubic + 10)
            self.battle_text += ", Сила Удара Третьего Рыцаря = " + str(enemy3_cubic + 10) + "\n"

            if self.strength + your_cubic > enemy1_cubic +10:
                self.battle_text += "Вы ранили Первого рыцаря.\n"
                enemy1_life_points -= 2
                if enemy1_life_points <= 0:
                    self.battle_text += "Первый рыцарь повержен!!!\n"
                    enemy1_alive = False
                else:
                    self.battle_text += ""
            elif self.strength + your_cubic < enemy1_cubic +10:
                self.battle_text += "Первый рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Первый рыцарь парировал удар.\n"    

            if self.strength + your_cubic >= enemy2_cubic +10:
                self.battle_text += "Вы парировали удар второго рыцаря.\n"
            else:
                self.battle_text += "Второй рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""        

            if self.strength + your_cubic >= enemy3_cubic +10:
                self.battle_text += "Вы парировали удар третьего рыцаря.\n"
                continue
            else:
                self.battle_text += "Третий рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ".\n"
            self.battle_text += "ВЫНОСЛИВОСТЬ ПЕРВОГО РЫЦАРЯ = " + str(enemy1_life_points) + ".\n"
            self.battle_text += "ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n"
            self.battle_text += "ВЫНОСЛИВОСТЬ ТРЕТЬЕГО РЫЦАРЯ = " + str(enemy3_life_points) + ".\n"        
   
                           
        # бой со вторым и третьим рыцарем, пока второй не погибнет
        while enemy2_alive == True:
            your_cubic = random.randint(2, 12)
            enemy2_cubic = random.randint(2, 12)
            enemy3_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic)
            self.battle_text += ", Сила Удара Второго Рыцаря = " + str(enemy2_cubic + 10)
            self.battle_text += ", Сила Удара Третьего Рыцаря = " + str(enemy3_cubic + 10) + "\n"

            if self.strength + your_cubic > enemy2_cubic + 10:
                self.battle_text += "Вы ранили Второго рыцаря.\n"
                enemy2_life_points -= 2
                if enemy2_life_points <= 0:
                    self.battle_text += "Второй рыцарь повержен!!!\n"
                    enemy2_alive = False
                else:
                    self.battle_text += ""
            elif self.strength + your_cubic < enemy1_cubic +10:
                self.battle_text += "Второй рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Второй рыцарь парировал удар.\n"
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО РЫЦАРЯ = " + str(enemy2_life_points) + ".\n"

            if self.strength + your_cubic >= enemy3_cubic + 10:
                self.battle_text += "Вы парировали удар третьего рыцаря.\n"
            else:
                self.battle_text += "Третий рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points)  + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО РЫЦАРЯ = " + str(enemy3_life_points) + ".\n"    

        message6_battleground_301 = QDialog()
        message6_battleground_301.setWindowTitle("Окно битвы")
        message6_battleground_301.setFixedSize(800, 600)
        textEdit6_battleground_301 = QTextEdit(message6_battleground_301)
        textEdit6_battleground_301.setFixedSize(800, 555)
        textEdit6_battleground_301.clear()
        textEdit6_battleground_301.setText(self.battle_text)
        buttonBox6_battleground_301 = QDialogButtonBox(message6_battleground_301)
        buttonBox6_battleground_301.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox6_battleground_301.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox6_battleground_301.accepted.connect(message6_battleground_301.accept)
        font_battleground_301 = QFont()
        font_battleground_301.setPointSize(10)
        message6_battleground_301.setFont(font_battleground_301)
        # установить фокус на кнопке ОК
        buttonBox6_battleground_301.setFocus()
        message6_battleground_301.exec_()

        if self.life_points <= 0:
            message5_battleground_301 = QMessageBox()
            message5_battleground_301.setWindowTitle(":-(")
            message5_battleground_301.setText("Вы проиграли.\nКонец игры...")
            font_battleground_301.setPointSize(14)
            message5_battleground_301.setFont(font_battleground_301)
            message5_battleground_301.exec_()
            sys.exit("Game over")
        elif enemy2_alive == False:
            message7_battleground_301 = QMessageBox()
            message7_battleground_301.setWindowTitle("!!!!")
            message7_battleground_301.setText("Остался третий рыцарь. В бой вступает Капитан Рыцарей.")
            font_battleground_301.setPointSize(14)
            message7_battleground_301.setFont(font_battleground_301)
            message7_battleground_301.exec_()
        else:
            message5_battleground_301 = QMessageBox()
            message5_battleground_301.setWindowTitle("!!!!")
            message5_battleground_301.setText("Остались второй и третий рыцари.")
            font_battleground_301.setPointSize(14)
            message5_battleground_301.setFont(font_battleground_301)
            message5_battleground_301.exec_()  

        # бой с третьим рыцарем и капитаном, пока не погибнет третий рыцарь 
        self.battle_text = ""      
        while enemy3_alive == True:
            your_cubic = random.randint(2, 12)
            enemy3_cubic = random.randint(2, 12)
            captain_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic)
            self.battle_text += ", Сила Удара Третьего Рыцаря = " + str(enemy3_cubic + 10)
            self.battle_text += ", Сила Удара Капитана Рыцарей = " + str(captain_cubic + 12) + "\n"

            if self.strength + your_cubic > enemy3_cubic + 10:
                self.battle_text += "Вы ранили Третьего рыцаря.\n"
                enemy3_life_points -= 2
                if enemy3_life_points <= 0:
                    self.battle_text += "Третий рыцарь повержен!!!\n"
                    enemy3_alive = False
                else:
                    self.battle_text += ""
            elif self.strength + your_cubic < enemy3_cubic + 10:
                self.battle_text += "Третий рыцарь ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Третий рыцарь парировал удар.\n"
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО РЫЦАРЯ = " + str(enemy3_life_points) + ".\n"

            if self.strength + your_cubic >= captain_cubic + 12:
                self.battle_text += "Вы парировали удар капитана рыцарей.\n"
            else:
                self.battle_text += "Капитан рыцарей ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points)  + ", ВЫНОСЛИВОСТЬ КАПИТАНА РЫЦАРЕЙ = " + str(captain_life_points) + ".\n"

        message8_battleground_301 = QDialog()
        message8_battleground_301.setWindowTitle("Окно битвы")
        message8_battleground_301.setFixedSize(800, 600)
        textEdit8_battleground_301 = QTextEdit(message8_battleground_301)
        textEdit8_battleground_301.setFixedSize(800, 555)
        textEdit8_battleground_301.clear()
        textEdit8_battleground_301.setText(self.battle_text)
        buttonBox8_battleground_301 = QDialogButtonBox(message8_battleground_301)
        buttonBox8_battleground_301.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox8_battleground_301.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox8_battleground_301.accepted.connect(message8_battleground_301.accept)
        font_battleground_301 = QFont()
        font_battleground_301.setPointSize(10)
        message8_battleground_301.setFont(font_battleground_301)
        # установить фокус на кнопке ОК
        buttonBox8_battleground_301.setFocus()
        message8_battleground_301.exec_() 

        if self.life_points <= 0:
            message9_battleground_301 = QMessageBox()
            message9_battleground_301.setWindowTitle(":-(")
            message9_battleground_301.setText("Вы проиграли.\nКонец игры...")
            font_battleground_301.setPointSize(14)
            message9_battleground_301.setFont(font_battleground_301)
            message9_battleground_301.exec_()
            sys.exit("Game over") 
        elif enemy3_alive == False:
            message10_battleground_301 = QMessageBox()
            message10_battleground_301.setWindowTitle("!!!!")
            message10_battleground_301.setText("Третий рыцарь повержен. Остался Капитан.")
            font_battleground_301.setPointSize(14)
            message10_battleground_301.setFont(font_battleground_301)
            message10_battleground_301.exec_()
        else:
            message11_battleground_301 = QMessageBox()
            message11_battleground_301.setWindowTitle("!!!!")
            message11_battleground_301.setText("Остался Капитан.")
            font_battleground_301.setPointSize(14)
            message11_battleground_301.setFont(font_battleground_301)
            message11_battleground_301.exec_() 

        # остался Капитан Рыцарей
        self.battle_text = ""
        while True:
            your_cubic = random.randint(2, 12)
            captain_cubic = random.randint(2, 12)
            round_number += 1
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic)
            self.battle_text += ", Сила Удара Капитана Рыцарей = " + str(captain_cubic + 12) + "\n"

            if self.strength + your_cubic > captain_cubic + 12:
                self.battle_text += "Вы ранили Капитана Рыцарей.\n"
                captain_life_points -= 2
                if captain_life_points <= 0:
                    self.battle_text += "Капитан Рыцарей повержен!!!\n"
                    captain_alive = False
                    break
                else:
                    self.battle_text += ""
            elif self.strength + your_cubic < captain_cubic + 12:
                self.battle_text += "Капитан Рыцарей ранил вас.\n"
                self.life_points -= 2
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Капитан Рыцарей парировал удар.\n"
            self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ КАПИТАНА РЫЦАРЕЙ = " + str(captain_life_points) + ".\n"

        message15_battleground_301 = QDialog()
        message15_battleground_301.setWindowTitle("Окно битвы")
        message15_battleground_301.setFixedSize(800, 600)
        textEdit15_battleground_301 = QTextEdit(message15_battleground_301)
        textEdit15_battleground_301.setFixedSize(800, 555)
        textEdit15_battleground_301.clear()
        textEdit15_battleground_301.setText(self.battle_text)
        buttonBox15_battleground_301 = QDialogButtonBox(message15_battleground_301)
        buttonBox15_battleground_301.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox15_battleground_301.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox15_battleground_301.accepted.connect(message15_battleground_301.accept)
        font_battleground_301 = QFont()
        font_battleground_301.setPointSize(10)
        message15_battleground_301.setFont(font_battleground_301)
        # установить фокус на кнопке ОК
        buttonBox15_battleground_301.setFocus()
        message15_battleground_301.exec_()     
        if self.life_points <= 0:
            message12_battleground_301 = QMessageBox()
            message12_battleground_301.setWindowTitle(":-(")
            message12_battleground_301.setText("Вы проиграли.\nКонец игры...")
            font_battleground_301.setPointSize(14)
            message12_battleground_301.setFont(font_battleground_301)
            message12_battleground_301.exec_()
            sys.exit("Game over") 
        elif captain_alive == False:
            message13_battleground_301 = QMessageBox()
            message13_battleground_301.setWindowTitle(":-)")
            message13_battleground_301.setText("Вы выиграли!!!")
            font_battleground_301.setPointSize(14)
            message13_battleground_301.setFont(font_battleground_301)
            message13_battleground_301.exec_()
            return self.life_points
        else:
            message14_battleground_301 = QMessageBox()
            message14_battleground_301.setWindowTitle(":-)")
            message14_battleground_301.setText("Вы выиграли!!!")
            font_battleground_301.setPointSize(14)
            message14_battleground_301.setFont(font_battleground_301)
            message14_battleground_301.exec_()
            return self.life_points    


    def battleground_316(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        dragon_strength = 12
        dragon_life_points = 8
        dragon_alive = True
        while dragon_alive == True:
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара противника = " + str(dragon_strength + enemy_cubic) + "\n"
            if self.strength + your_cubic > dragon_strength + enemy_cubic:
                dragon_life_points -= 2
                self.battle_text += "Вы ранили дракона.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ДРАКОНА = " + str(dragon_life_points) + "\n"
                if dragon_life_points == 4:
                    dragon_alive = False
                    self.battle_text += "Вы дважды ранили дракона. Переход к следующему параграфу.\n"
                    break
                else:
                    self.battle_text += ""
            elif self.strength + your_cubic < dragon_strength + enemy_cubic:
                self.life_points -= 2
                self.battle_text += "Дракон ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ДРАКОНА = " + str(dragon_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Дракон парировал удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ДРАКОНА = " + str(dragon_life_points) + "\n"
                continue
        message_battleground_316 = QDialog()
        message_battleground_316.setWindowTitle("Окно битвы")
        message_battleground_316.setFixedSize(800, 600)
        textEdit_battleground_316 = QTextEdit(message_battleground_316)
        textEdit_battleground_316.setFixedSize(800, 555)
        textEdit_battleground_316.clear()
        textEdit_battleground_316.setText(self.battle_text)
        buttonBox_battleground_316 = QDialogButtonBox(message_battleground_316)
        buttonBox_battleground_316.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_316.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_316.accepted.connect(message_battleground_316.accept)
        font_battleground_316 = QFont()
        font_battleground_316.setPointSize(10)
        message_battleground_316.setFont(font_battleground_316)
        # установить фокус на кнопке ОК
        buttonBox_battleground_316.setFocus()
        message_battleground_316.exec_()
        if self.life_points <= 0:
            message3_battleground_316 = QMessageBox()
            message3_battleground_316.setWindowTitle("!!!")
            message3_battleground_316.setText("Вы проиграли!!!")
            font_battleground_316.setPointSize(14)
            message3_battleground_316.setFont(font_battleground_316)
            message3_battleground_316.exec_()
            self.battleground_316()
            return self.life_points
        elif dragon_life_points <= 4:
            message3_battleground_316 = QMessageBox()
            message3_battleground_316.setWindowTitle("!!!")
            message3_battleground_316.setText("Вам удалось дваджы ранить дракона!!!")
            font_battleground_316.setPointSize(14)
            message3_battleground_316.setFont(font_battleground_316)
            message3_battleground_316.exec_()
            return self.life_points
        else:
            message3_battleground_316 = QMessageBox()
            message3_battleground_316.setWindowTitle("!!!")
            message3_battleground_316.setText("Вам удалось дваджы ранить дракона!!!")
            font_battleground_316.setPointSize(14)
            message3_battleground_316.setFont(font_battleground_316)
            message3_battleground_316.exec_()
            return self.life_points        


    def battleground_316_copy_spell(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        copy_strength = dragon_strength = 12
        copy_life_points = dragon_life_points = 8
        dragon_alive = True 
        while dragon_alive == True:
            copy_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Сила удара копии  = " + str(copy_strength + copy_cubic) + ",  Сила удара дракона = " + str(dragon_strength + enemy_cubic) + "\n"
            if copy_strength + copy_cubic > dragon_strength + enemy_cubic:
                dragon_life_points -= 2
                self.battle_text += "Копия ранила дракона.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(dragon_life_points) + "\n"
                if dragon_life_points == 4:
                    dragon_alive = False
                    self.battle_text += "Вы дважды ранили дракона. Переход к следующему параграфу.\n"
                    break
                else:
                    self.battle_text += ""
            elif copy_strength + copy_cubic < dragon_strength + enemy_cubic:
                copy_life_points -= 2
                self.battle_text += "Дракон ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(dragon_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
                else:
                    self.battle_text += ""
            else:
                self.battle_text += "Дракон парировал удар.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(dragon_life_points) + "\n"
                continue
        message_battleground_316_copy_spell = QDialog()
        message_battleground_316_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_316_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_316_copy_spell = QTextEdit(message_battleground_316_copy_spell)
        textEdit_battleground_316_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_316_copy_spell.clear()
        textEdit_battleground_316_copy_spell.setText(self.battle_text)
        buttonBox_battleground_316_copy_spell = QDialogButtonBox(message_battleground_316_copy_spell)
        buttonBox_battleground_316_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_316_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_316_copy_spell.accepted.connect(message_battleground_316_copy_spell.accept)
        font_battleground_316 = QFont()
        font_battleground_316.setPointSize(10)
        message_battleground_316_copy_spell.setFont(font_battleground_316)
        # установить фокус на кнопке ОК
        buttonBox_battleground_316_copy_spell.setFocus()
        message_battleground_316_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle("!!!")
            message3_battleground_one.setText("Копия проиграла.\nТеперь ваша очередь вступить в бой!")
            font_battleground_316.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_316)
            message3_battleground_one.exec_()
            self.battleground_316()
            return self.life_points
        elif dragon_life_points <= 4:
            message3_battleground_316 = QMessageBox()
            message3_battleground_316.setWindowTitle("!!!")
            message3_battleground_316.setText("Вам удалось дваджы ранить дракона!!!")
            font_battleground_316.setPointSize(14)
            message3_battleground_316.setFont(font_battleground_316)
            message3_battleground_316.exec_()
            return self.life_points
        else:
            message3_battleground_316 = QMessageBox()
            message3_battleground_316.setWindowTitle("!!!")
            message3_battleground_316.setText("Вам удалось дваджы ранить дракона!!!")
            font_battleground_316.setPointSize(14)
            message3_battleground_316.setFont(font_battleground_316)
            message3_battleground_316.exec_()
            return self.life_points                    


    def battleground_328(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        orc1_strength = 8
        orc1_life_points = 5
        orc2_strength = 7
        orc2_life_points = 7
        orc1_alive = True
        orc2_alive = True
        while orc1_alive == True:
            self.round_number_328 += 1
            if self.round_number_328 >= 9:
                self.battle_text += "8 раундов прошло!!!"
                break
            self.battle_text += "Раунд " + str(self.round_number_328) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого Орка = " + str(orc1_strength + orc1_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength + orc2_cubic) + "\n"

            if self.strength + your_cubic >= orc1_strength + orc1_cubic:
                orc1_life_points -= 2
                self.battle_text += "Вы ранили Первого Орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!!!\n"
                    orc1_alive = False
            elif self.strength + your_cubic < orc1_strength + orc1_cubic:
                self.life_points -= 2
                self.battle_text += "Первый орк вас ранил.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                    break
            else:
                self.battle_text += "Первый Орк парировал удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc2_life_points) + "\n"

            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Вы парировали удар Второго Орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"                
            else:
                self.life_points -= 2
                self.battle_text += "Второй орк вас ранил.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                    break  

        message_battleground_328 = QDialog()
        message_battleground_328.setWindowTitle("Окно битвы")
        message_battleground_328.setFixedSize(800, 600)
        textEdit_battleground_328 = QTextEdit(message_battleground_328)
        textEdit_battleground_328.setFixedSize(800, 555)
        textEdit_battleground_328.clear()
        textEdit_battleground_328.setText(self.battle_text)
        buttonBox_battleground_328 = QDialogButtonBox(message_battleground_328)
        buttonBox_battleground_328.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_328.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_328.accepted.connect(message_battleground_328.accept)
        font_battleground_328 = QFont()
        font_battleground_328.setPointSize(10)
        message_battleground_328.setFont(font_battleground_328)
        # установить фокус на кнопке ОК
        buttonBox_battleground_328.setFocus()
        message_battleground_328.exec_()
        if self.life_points <= 0:
            message3_battleground_328 = QMessageBox()
            message3_battleground_328.setWindowTitle("!!!")
            message3_battleground_328.setText("Вы проиграли!!!")
            font_battleground_328.setPointSize(14)
            message3_battleground_328.setFont(font_battleground_328)
            message3_battleground_328.exec_()
            return self.life_points
        elif self.round_number_328 >= 8:
            message4_battleground_328 = QMessageBox()
            message4_battleground_328.setWindowTitle("!!!")
            message4_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font_battleground_328.setPointSize(14)
            message4_battleground_328.setFont(font_battleground_328)
            message4_battleground_328.exec_()
            return self.life_points
        elif orc1_alive == False:
            message5_battleground_328 = QMessageBox()
            message5_battleground_328.setWindowTitle("!!!")
            message5_battleground_328.setText("Первый Орк повержен. Остался Второй.")
            font_battleground_328.setPointSize(14)
            message5_battleground_328.setFont(font_battleground_328)
            message5_battleground_328.exec_()
        else:
            message4_battleground_328 = QMessageBox()
            message4_battleground_328.setWindowTitle("!!!")
            message4_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font_battleground_328.setPointSize(14)
            message4_battleground_328.setFont(font_battleground_328)
            message4_battleground_328.exec_()
            return self.life_points 

        self.battle_text = ""       
        while self.round_number_328 < 8:
            self.round_number_328 += 1
            if self.round_number_328 >= 9:
                self.battle_text += "8 раундов прошло!!!"
                break
            self.battle_text += "Продолжение битвы.\n"
            self.battle_text += "Раунд " + str(self.round_number_328) + ".\n"
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength + orc2_cubic) + "\n"
            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                orc2_life_points -= 2
                self.battle_text += "Вы ранили Второго Орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    self.battle_text += "Второй орк повержен!!!\n"
                    orc2_alive = False
                    self.win_battle_328 = True
                    break
            elif self.strength + your_cubic < orc2_strength + orc2_cubic:
                self.life_points -= 2
                self.battle_text += "Второй орк вас ранил.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!"
                    break
            else:
                self.battle_text += "Второй Орк парировал удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
        else:
            self.win_battle_328 = False               

        message1_battleground_328 = QDialog()
        message1_battleground_328.setWindowTitle("Окно битвы")
        message1_battleground_328.setFixedSize(800, 600)
        textEdit1_battleground_328 = QTextEdit(message1_battleground_328)
        textEdit1_battleground_328.setFixedSize(800, 555)
        textEdit1_battleground_328.clear()
        textEdit1_battleground_328.setText(self.battle_text)
        buttonBox1_battleground_328 = QDialogButtonBox(message1_battleground_328)
        buttonBox1_battleground_328.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox1_battleground_328.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox1_battleground_328.accepted.connect(message1_battleground_328.accept)
        font1_battleground_328 = QFont()
        font1_battleground_328.setPointSize(10)
        message1_battleground_328.setFont(font1_battleground_328)
        # установить фокус на кнопке ОК
        buttonBox1_battleground_328.setFocus()
        message1_battleground_328.exec_()
        if self.life_points <= 0:
            message6_battleground_328 = QMessageBox()
            message6_battleground_328.setWindowTitle("!!!")
            message6_battleground_328.setText("Вы проиграли!!!")
            font_battleground_328.setPointSize(14)
            message6_battleground_328.setFont(font_battleground_328)
            message6_battleground_328.exec_()
            return self.life_points
        elif self.win_battle_328 == False:
            message4_battleground_328 = QMessageBox()
            message4_battleground_328.setWindowTitle("!!!")
            message4_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font_battleground_328.setPointSize(14)
            message4_battleground_328.setFont(font_battleground_328)
            message4_battleground_328.exec_()
            return self.life_points 
        else:
            message5_battleground_328 = QMessageBox()
            message5_battleground_328.setWindowTitle("!!!")
            message5_battleground_328.setText("Вы выиграли бой!")
            font_battleground_328.setPointSize(14)
            message5_battleground_328.setFont(font_battleground_328)
            message5_battleground_328.exec_()           


    def battleground_328_copy_spell(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        copy_strength = orc1_strength = 8
        copy_life_points = orc1_life_points = 5
        orc2_strength = 7
        orc2_life_points = 7
        orc1_alive = True
        orc2_alive = True
        self.round_number_328 = 0
        while orc1_alive == True:
            self.round_number_328 += 1
            if self.round_number_328 >= 9:
                self.battle_text += "8 раундов прошло!!!"
                break
            self.battle_text += "Раунд " + str(self.round_number_328) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            self.battle_text += "Сила удара копии  = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого Орка = " + str(orc1_strength + orc1_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength + orc2_cubic) + "\n"

            if copy_strength + your_cubic >= orc1_strength + orc1_cubic:
                orc1_life_points -= 2
                self.battle_text += "Копия ранила Первого Орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!!!\n"
                    orc1_alive = False
            elif copy_strength + your_cubic < orc1_strength + orc1_cubic:
                copy_life_points -= 2
                self.battle_text += "Первый орк ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает. Теперь ваша очередь вступить в бой!!!"
                    break
            else:
                self.battle_text += "Первый Орк парировал удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc2_life_points) + "\n"

            if copy_strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Копия парировала удар Второго Орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"                
            else:
                copy_life_points -= 2
                self.battle_text += "Второй орк ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает. Теперь ваша очередь вступить в бой!!!"
                    break

        message12_battleground_328 = QDialog()
        message12_battleground_328.setWindowTitle("Окно битвы")
        message12_battleground_328.setFixedSize(800, 600)
        textEdit12_battleground_328 = QTextEdit(message12_battleground_328)
        textEdit12_battleground_328.setFixedSize(800, 555)
        textEdit12_battleground_328.clear()
        textEdit12_battleground_328.setText(self.battle_text)
        buttonBox12_battleground_328 = QDialogButtonBox(message12_battleground_328)
        buttonBox12_battleground_328.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox12_battleground_328.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox12_battleground_328.accepted.connect(message12_battleground_328.accept)
        font12_battleground_328 = QFont()
        font12_battleground_328.setPointSize(10)
        message12_battleground_328.setFont(font12_battleground_328)
        # установить фокус на кнопке ОК
        buttonBox12_battleground_328.setFocus()
        message12_battleground_328.exec_() 
        if copy_life_points <= 0:
            message13_battleground_328 = QMessageBox()
            message13_battleground_328.setWindowTitle("!!!")
            message13_battleground_328.setText("Копия проиграла и исчезает. Теперь ваша очередь вступить в бой!!!")
            font12_battleground_328.setPointSize(14)
            message13_battleground_328.setFont(font12_battleground_328)
            message13_battleground_328.exec_()
            self.battleground_328()
            return self.life_points
        elif self.round_number_328 >= 8:
            message14_battleground_328 = QMessageBox()
            message14_battleground_328.setWindowTitle("!!!")
            message14_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font12_battleground_328.setPointSize(14)
            message14_battleground_328.setFont(font12_battleground_328)
            message14_battleground_328.exec_()
            return self.life_points
        elif orc1_alive == False:
            message15_battleground_328 = QMessageBox()
            message15_battleground_328.setWindowTitle("!!!")
            message15_battleground_328.setText("Первый Орк повержен. Остался Второй.")
            font12_battleground_328.setPointSize(14)
            message15_battleground_328.setFont(font12_battleground_328)
            message15_battleground_328.exec_()
        else:
            message14_battleground_328 = QMessageBox()
            message14_battleground_328.setWindowTitle("!!!")
            message14_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font12_battleground_328.setPointSize(14)
            message14_battleground_328.setFont(font12_battleground_328)
            message14_battleground_328.exec_()
            return self.life_points

        self.battle_text = ""       
        while self.round_number_328 < 8:
            self.round_number_328 += 1
            if self.round_number_328 >= 9:
                self.battle_text += "8 раундов прошло!!!"
                break
            self.battle_text += "Продолжение битвы.\n"
            self.battle_text += "Раунд " + str(self.round_number_328) + ".\n"
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength + orc2_cubic) + "\n"
            if copy_strength + your_cubic >= orc2_strength + orc2_cubic:
                orc2_life_points -= 2
                self.battle_text += "Вы ранили Второго Орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    self.battle_text += "Второй орк повержен!!!\n"
                    orc2_alive = False
                    self.win_battle_328 = True
                    break
            elif copy_strength + your_cubic < orc2_strength + orc2_cubic:
                self.life_points -= 2
                self.battle_text += "Второй орк вас ранил.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает. Теперь ваша очередь вступить в бой!!!"
                    break
            else:
                self.battle_text += "Второй Орк парировал удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
        else:
            self.win_battle_328 = False

        message1_battleground_328 = QDialog()
        message1_battleground_328.setWindowTitle("Окно битвы")
        message1_battleground_328.setFixedSize(800, 600)
        textEdit1_battleground_328 = QTextEdit(message1_battleground_328)
        textEdit1_battleground_328.setFixedSize(800, 555)
        textEdit1_battleground_328.clear()
        textEdit1_battleground_328.setText(self.battle_text)
        buttonBox1_battleground_328 = QDialogButtonBox(message1_battleground_328)
        buttonBox1_battleground_328.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox1_battleground_328.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox1_battleground_328.accepted.connect(message1_battleground_328.accept)
        font12_battleground_328 = QFont()
        font12_battleground_328.setPointSize(10)
        message1_battleground_328.setFont(font12_battleground_328)
        # установить фокус на кнопке ОК
        buttonBox1_battleground_328.setFocus()
        message1_battleground_328.exec_()
        if self.life_points <= 0:
            message6_battleground_328 = QMessageBox()
            message6_battleground_328.setWindowTitle("!!!")
            message6_battleground_328.setText("Копия проиграла и исчезает. Теперь ваша очередь вступить в бой!!!")
            font12_battleground_328.setPointSize(14)
            message6_battleground_328.setFont(font12_battleground_328)
            message6_battleground_328.exec_()
            self.battleground_328()
            return self.life_points
        elif self.win_battle_328 == False:
            message4_battleground_328 = QMessageBox()
            message4_battleground_328.setWindowTitle("!!!")
            message4_battleground_328.setText("Вы не смогли выиграть бой за 8 раундов атаки!!!")
            self.win_battle_328 = False
            font12_battleground_328.setPointSize(14)
            message4_battleground_328.setFont(font12_battleground_328)
            message4_battleground_328.exec_()
            return self.life_points 
        else:
            message5_battleground_328 = QMessageBox()
            message5_battleground_328.setWindowTitle("!!!")
            message5_battleground_328.setText("Вы выиграли бой!")
            font12_battleground_328.setPointSize(14)
            message5_battleground_328.setFont(font12_battleground_328)
            message5_battleground_328.exec_()    


    def battleground_487(self):
        self.battle_text = ""
        orc1_strength = 10
        orc1_life_points = 6
        orc1_alive = True
        # начало боя, первые три раунда
        while self.round_number < 3:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "У вас выпало: " + str(your_cubic) + ", у противника выпало: " + str(orc1_cubic) + "\n" 
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            if self.strength + your_cubic >= orc1_strength + orc1_cubic:
                self.battle_text += "Вы ранили первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!!!\n"
                    orc1_alive = False
                    break
            elif self.strength + your_cubic < orc1_strength + orc1_cubic:
                self.battle_text += "Первый орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Первый орк парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc1_life_points) + "\n"

        message_battleground_487 = QDialog()
        message_battleground_487.setWindowTitle("Окно битвы")
        message_battleground_487.setFixedSize(800, 600)
        textEdit_battleground_487 = QTextEdit(message_battleground_487)
        textEdit_battleground_487.setFixedSize(800, 555)
        textEdit_battleground_487.clear()
        textEdit_battleground_487.setText(self.battle_text)
        buttonBox_battleground_487 = QDialogButtonBox(message_battleground_487)
        buttonBox_battleground_487.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487.accepted.connect(message_battleground_487.accept)
        font_battleground_487 = QFont()
        font_battleground_487.setPointSize(10)
        message_battleground_487.setFont(font_battleground_487)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487.setFocus()
        message_battleground_487.exec_()
        if self.life_points <= 0:
            message2_battleground_487 = QMessageBox()
            message2_battleground_487.setWindowTitle(":-(")
            message2_battleground_487.setText("Вы проиграли.\nКонец игры...")
            font_battleground_487.setPointSize(14)
            message2_battleground_487.setFont(font_battleground_487)
            message2_battleground_487.exec_()
            sys.exit("Game over")        
        elif orc1_alive == False: 
            message3_battleground_487 = QMessageBox()
            message3_battleground_487.setWindowTitle("!!!!")
            message3_battleground_487.setText("Первый орк повержен! В бой вступают оставшиеся два орка.\n")
            font_battleground_487.setPointSize(14)
            message3_battleground_487.setFont(font_battleground_487)
            message3_battleground_487.exec_()
            self.battleground_487_1("Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        elif orc1_alive == True:
            message3_battleground_487 = QMessageBox()
            message3_battleground_487.setWindowTitle("!!!!")
            message3_battleground_487.setText("Вы не смогли расправиться с первым орком за 3 раунда атаки. В бой вступают оставшиеся два орка. Теперь против вас трое.\n")
            font_battleground_487.setPointSize(14)
            message3_battleground_487.setFont(font_battleground_487)
            message3_battleground_487.exec_()
            self.battleground_487_2("Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
            
    # функция боя п.487 (остались второй и третий орк)
    def battleground_487_1(self, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc2_alive = True
        orc3_alive = True
        while orc2_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Ваша сила удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара второго орка = " + str(orc2_strength + orc2_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Вы ранили второго орка.\n"
                orc2_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    self.battle_text += "Второй орк повержен!!!\n"
                    orc2_alive = False
                    break
            elif self.strength + your_cubic < orc2_strength + orc2_cubic:
                self.battle_text += "Второй орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Второй орк парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"

            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Вы парировали удар третьего орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

        message_battleground_487_1 = QDialog()
        message_battleground_487_1.setWindowTitle("Окно битвы")
        message_battleground_487_1.setFixedSize(800, 600)
        textEdit_battleground_487_1 = QTextEdit(message_battleground_487_1)
        textEdit_battleground_487_1.setFixedSize(800, 555)
        textEdit_battleground_487_1.clear()
        textEdit_battleground_487_1.setText(self.battle_text)
        buttonBox_battleground_487_1 = QDialogButtonBox(message_battleground_487_1)
        buttonBox_battleground_487_1.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_1.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_1.accepted.connect(message_battleground_487_1.accept)
        font_battleground_487_1 = QFont()
        font_battleground_487_1.setPointSize(10)
        message_battleground_487_1.setFont(font_battleground_487_1)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_1.setFocus()
        message_battleground_487_1.exec_()        
        if self.life_points <= 0:
            message2_battleground_487_1 = QMessageBox()
            message2_battleground_487_1.setWindowTitle(":-(")
            message2_battleground_487_1.setText("Вы проиграли.\nКонец игры...")
            font_battleground_487_1.setPointSize(14)
            message2_battleground_487_1.setFont(font_battleground_487_1)
            message2_battleground_487_1.exec_()
            sys.exit("Game over")
        elif orc2_alive == False:
            message3_battleground_487_1 = QMessageBox()
            message3_battleground_487_1.setWindowTitle("!!!")
            message3_battleground_487_1.setText("Второй орк повержен.\nОстался третий.\n")
            font_battleground_487_1.setPointSize(14)
            message3_battleground_487_1.setFont(font_battleground_487_1)
            message3_battleground_487_1.exec_()
            self.battleground_487_3("Третий орк", 7, 7)
            return self.life_points
        else:
            message4_battleground_487_1 = QMessageBox()
            message4_battleground_487_1.setWindowTitle("!!!")
            message4_battleground_487_1.setText("Второй орк повержен.\nОстался третий.\n")
            font_battleground_487_1.setPointSize(14)
            message4_battleground_487_1.setFont(font_battleground_487_1)
            message4_battleground_487_1.exec_()
            self.battleground_487_3("Третий орк", 7, 7)
            return self.life_points
            

    # функция боя п.487 (остались все три орка)
    def battleground_487_2(self, orc1_name, orc1_strength, orc1_life_points, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        orc1_alive = True
        orc2_alive = True
        orc3_alive = True
        self.battle_text = ""
        while orc1_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Ваша сила удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            self.battle_text += "Сила удара второго орка = " + str(orc2_strength + orc2_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if self.strength + your_cubic >= orc1_strength + orc1_cubic:
                self.battle_text += "Вы ранили первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!\n"
                    orc1_alive = False
                    break
            elif self.strength + your_cubic < orc1_strength + orc1_cubic:
                self.battle_text += "Первый орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!\n"
                    break
            else:
                self.battle_text += "Первый орк парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Вы парировали удар второго орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
            else:
                self.battle_text += "Второй орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!\n"
                    break    

            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Вы парировали удар третьего орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!\n"
                    break
        message_battleground_487_2 = QDialog()
        message_battleground_487_2.setWindowTitle("Окно битвы")
        message_battleground_487_2.setFixedSize(800, 600)
        textEdit_battleground_487_2 = QTextEdit(message_battleground_487_2)
        textEdit_battleground_487_2.setFixedSize(800, 555)
        textEdit_battleground_487_2.clear()
        textEdit_battleground_487_2.setText(self.battle_text)
        buttonBox_battleground_487_2 = QDialogButtonBox(message_battleground_487_2)
        buttonBox_battleground_487_2.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_2.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_2.accepted.connect(message_battleground_487_2.accept)
        font_battleground_487_2 = QFont()
        font_battleground_487_2.setPointSize(10)
        message_battleground_487_2.setFont(font_battleground_487_2)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_2.setFocus()
        message_battleground_487_2.exec_() 
        if self.life_points <= 0:
            message2_battleground_487_2 = QMessageBox()
            message2_battleground_487_2.setWindowTitle(":-(")
            message2_battleground_487_2.setText("Вы проиграли.\nКонец игры...")
            font_battleground_487_2.setPointSize(14)
            message2_battleground_487_2.setFont(font_battleground_487_2)
            message2_battleground_487_2.exec_()
            sys.exit("Game over")
        elif orc1_alive == False:
            message3_battleground_487_2 = QMessageBox()
            message3_battleground_487_2.setWindowTitle("!!!")
            message3_battleground_487_2.setText("Первый орк повержен.\nОсталось еще два.\n")
            font_battleground_487_2.setPointSize(14)
            message3_battleground_487_2.setFont(font_battleground_487_2)
            message3_battleground_487_2.exec_()
            self.battleground_487_1("Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        else:
            message4_battleground_487_2 = QMessageBox()
            message4_battleground_487_2.setWindowTitle("!!!")
            message4_battleground_487_2.setText("Первый орк повержен.\nОсталось еще два.\n")
            font_battleground_487_2.setPointSize(14)
            message4_battleground_487_2.setFont(font_battleground_487_2)
            message4_battleground_487_2.exec_()
            self.battleground_487_1("Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points           


    # функция боя п.487 (остался третий орк)
    def battleground_487_3(self, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc3_alive = True
        while orc3_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Ваша сила удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Вы ранили третьего орка.\n"
                orc3_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if orc3_life_points <= 0:
                    self.battle_text += "Третий орк повержен!!!\n"
                    orc3_alive = False
                    break
            elif self.strength + your_cubic < orc3_strength + orc3_cubic:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Третий орк парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"

        message_battleground_487_3 = QDialog()
        message_battleground_487_3.setWindowTitle("Окно битвы")
        message_battleground_487_3.setFixedSize(800, 600)
        textEdit_battleground_487_3 = QTextEdit(message_battleground_487_3)
        textEdit_battleground_487_3.setFixedSize(800, 555)
        textEdit_battleground_487_3.clear()
        textEdit_battleground_487_3.setText(self.battle_text)
        buttonBox_battleground_487_3 = QDialogButtonBox(message_battleground_487_3)
        buttonBox_battleground_487_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_3.accepted.connect(message_battleground_487_3.accept)
        font_battleground_487_3 = QFont()
        font_battleground_487_3.setPointSize(10)
        message_battleground_487_3.setFont(font_battleground_487_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_3.setFocus()
        message_battleground_487_3.exec_()        
        if self.life_points <= 0:
            message2_battleground_487_3 = QMessageBox()
            message2_battleground_487_3.setWindowTitle(":-(")
            message2_battleground_487_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_487_3.setPointSize(14)
            message2_battleground_487_3.setFont(font_battleground_487_3)
            message2_battleground_487_3.exec_()
            sys.exit("Game over")
        elif orc3_alive == False:
            message3_battleground_487_3 = QMessageBox()
            message3_battleground_487_3.setWindowTitle("!!!")
            message3_battleground_487_3.setText("Третий орк повержен. Вы выиграли бой!!!\n")
            font_battleground_487_3.setPointSize(14)
            message3_battleground_487_3.setFont(font_battleground_487_3)
            message3_battleground_487_3.exec_()
            return self.life_points
        else:
            message4_battleground_487_3 = QMessageBox()
            message4_battleground_487_3.setWindowTitle("!!!")
            message4_battleground_487_3.setText("Третий орк повержен. Вы выиграли бой!!!\n")
            font_battleground_487_3.setPointSize(14)
            message4_battleground_487_3.setFont(font_battleground_487_3)
            message4_battleground_487_3.exec_()
            return self.life_points


    def battleground_487_copy_spell(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        self.round_number = 0
        copy_strength = orc1_strength = 10
        copy_life_points = orc1_life_points = 6
        orc1_alive = True
        # начало боя, первые три раунда
        while self.round_number < 3:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n" 
            self.battle_text += "Сила удара копии = " + str(self.strength + your_cubic) + ",  Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            if copy_strength + your_cubic >= orc1_strength + orc1_cubic:
                self.battle_text += "Вы ранили первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!!!\n"
                    orc1_alive = False
                    break
            elif copy_strength + your_cubic < orc1_strength + orc1_cubic:
                self.battle_text += "Первый орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия повержена и исчезает!\n"
                    break
            else:
                self.battle_text += "Первый орк парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

        message_battleground_487_copy_spell = QDialog()
        message_battleground_487_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_487_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_487_copy_spell = QTextEdit(message_battleground_487_copy_spell)
        textEdit_battleground_487_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_487_copy_spell.clear()
        textEdit_battleground_487_copy_spell.setText(self.battle_text)
        buttonBox_battleground_487_copy_spell = QDialogButtonBox(message_battleground_487_copy_spell)
        buttonBox_battleground_487_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_copy_spell.accepted.connect(message_battleground_487_copy_spell.accept)
        font_battleground_487_copy_spell = QFont()
        font_battleground_487_copy_spell.setPointSize(10)
        message_battleground_487_copy_spell.setFont(font_battleground_487_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_copy_spell.setFocus()
        message_battleground_487_copy_spell.exec_()
        if copy_life_points <= 0:
            message2_battleground_487_copy_spell = QMessageBox()
            message2_battleground_487_copy_spell.setWindowTitle(":-(")
            message2_battleground_487_copy_spell.setText("Копия повержена и исчезает!.\n")
            font_battleground_487_copy_spell.setPointSize(14)
            message2_battleground_487_copy_spell.setFont(font_battleground_487_copy_spell)
            message2_battleground_487_copy_spell.exec_()
            self.battleground_487()
            return self.life_points       
        elif orc1_alive == False: 
            message3_battleground_487_copy_spell = QMessageBox()
            message3_battleground_487_copy_spell.setWindowTitle("!!!!")
            message3_battleground_487_copy_spell.setText("Первый орк повержен! В бой вступают оставшиеся два орка.\n")
            font_battleground_487_copy_spell.setPointSize(14)
            message3_battleground_487_copy_spell.setFont(font_battleground_487_copy_spell)
            message3_battleground_487_copy_spell.exec_()
            self.battleground_487_1_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        elif orc1_alive == True:
            message3_battleground_487_copy_spell = QMessageBox()
            message3_battleground_487_copy_spell.setWindowTitle("!!!!")
            message3_battleground_487_copy_spell.setText("Вы не смогли расправиться с первым орком за 3 раунда атаки. В бой вступают оставшиеся два орка. Теперь против вас трое.\n")
            font_battleground_487_copy_spell.setPointSize(14)
            message3_battleground_487_copy_spell.setFont(font_battleground_487_copy_spell)
            message3_battleground_487_copy_spell.exec_()
            self.battleground_487_2_copy_spell(copy_strength, copy_life_points, "Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points


    def battleground_487_1_copy_spell(self, copy_strength, copy_life_points, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc2_alive = True
        orc3_alive = True
        while orc2_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара второго орка = " + str(orc2_strength + orc2_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if copy_strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Копия ранила второго орка.\n"
                orc2_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    self.battle_text += "Второй орк повержен!!!\n"
                    orc2_alive = False
                    break
            elif copy_strength + your_cubic < orc2_strength + orc2_cubic:
                self.battle_text += "Второй орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Второй орк парировал удар.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"

            if copy_strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Копия парировала удар третьего орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

        message_battleground_487_1_copy_spell = QDialog()
        message_battleground_487_1_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_487_1_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_487_1_copy_spell = QTextEdit(message_battleground_487_1_copy_spell)
        textEdit_battleground_487_1_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_487_1_copy_spell.clear()
        textEdit_battleground_487_1_copy_spell.setText(self.battle_text)
        buttonBox_battleground_487_1_copy_spell = QDialogButtonBox(message_battleground_487_1_copy_spell)
        buttonBox_battleground_487_1_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_1_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_1_copy_spell.accepted.connect(message_battleground_487_1_copy_spell.accept)
        font_battleground_487_1_copy_spell = QFont()
        font_battleground_487_1_copy_spell.setPointSize(10)
        message_battleground_487_1_copy_spell.setFont(font_battleground_487_1_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_1_copy_spell.setFocus()
        message_battleground_487_1_copy_spell.exec_()        
        if copy_life_points <= 0:
            message2_battleground_487_1_copy_spell = QMessageBox()
            message2_battleground_487_1_copy_spell.setWindowTitle("!!!")
            message2_battleground_487_1_copy_spell.setText("Копия проиграла и исчезает!!!")
            font_battleground_487_1_copy_spell.setPointSize(14)
            message2_battleground_487_1_copy_spell.setFont(font_battleground_487_1_copy_spell)
            message2_battleground_487_1_copy_spell.exec_()
            self.battleground_487_1("Второй орк", 7, orc2_life_points, "Третий орк", 7, 7)
            return self.life_points
        elif orc2_alive == False:
            message3_battleground_487_1_copy_spell = QMessageBox()
            message3_battleground_487_1_copy_spell.setWindowTitle("!!!")
            message3_battleground_487_1_copy_spell.setText("Второй орк повержен.\nОстался третий.\n")
            font_battleground_487_1_copy_spell.setPointSize(14)
            message3_battleground_487_1_copy_spell.setFont(font_battleground_487_1_copy_spell)
            message3_battleground_487_1_copy_spell.exec_()
            self.battleground_487_3_copy_spell(copy_strength, copy_life_points, "Третий орк", 7, 7)
            return self.life_points
        else:
            message4_battleground_487_1_copy_spell = QMessageBox()
            message4_battleground_487_1_copy_spell.setWindowTitle("!!!")
            message4_battleground_487_1_copy_spell.setText("Второй орк повержен.\nОстался третий.\n")
            font_battleground_487_1_copy_spell.setPointSize(14)
            message4_battleground_487_1_copy_spell.setFont(font_battleground_487_1_copy_spell)
            message4_battleground_487_1_copy_spell.exec_()
            self.battleground_487_3_copy_spell(copy_strength, copy_life_points, "Третий орк", 7, 7)
            return self.life_points


    def battleground_487_2_copy_spell(self, copy_strength, copy_life_points, orc1_name, orc1_strength, orc1_life_points, orc2_name, 
                                                orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        orc1_alive = True
        orc2_alive = True
        orc3_alive = True
        self.battle_text = ""
        while orc1_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Сила удара копии = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            self.battle_text += "Сила удара второго орка = " + str(orc2_strength + orc2_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if copy_strength + your_cubic >= orc1_strength + orc1_cubic:
                self.battle_text += "Копия ранила первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    self.battle_text += "Первый орк повержен!\n"
                    orc1_alive = False
                    break
            elif copy_strength + your_cubic < orc1_strength + orc1_cubic:
                self.battle_text += "Первый орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!\n"
                    break
            else:
                self.battle_text += "Первый орк парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Копия парировала удар второго орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
            else:
                self.battle_text += "Второй орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!\n"
                    break    

            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Копия парировала удар третьего орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc1_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!\n"
                    break

        message_battleground_487_2_copy_spell = QDialog()
        message_battleground_487_2_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_487_2_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_487_2_copy_spell = QTextEdit(message_battleground_487_2_copy_spell)
        textEdit_battleground_487_2_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_487_2_copy_spell.clear()
        textEdit_battleground_487_2_copy_spell.setText(self.battle_text)
        buttonBox_battleground_487_2_copy_spell = QDialogButtonBox(message_battleground_487_2_copy_spell)
        buttonBox_battleground_487_2_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_2_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_2_copy_spell.accepted.connect(message_battleground_487_2_copy_spell.accept)
        font_battleground_487_2_copy_spell = QFont()
        font_battleground_487_2_copy_spell.setPointSize(10)
        message_battleground_487_2_copy_spell.setFont(font_battleground_487_2_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_2_copy_spell.setFocus()
        message_battleground_487_2_copy_spell.exec_() 
        if copy_life_points <= 0:
            message2_battleground_487_2_copy_spell = QMessageBox()
            message2_battleground_487_2_copy_spell.setWindowTitle("!!!")
            message2_battleground_487_2_copy_spell.setText("Копия проиграла и исчезает!!!")
            font_battleground_487_2_copy_spell.setPointSize(14)
            message2_battleground_487_2_copy_spell.setFont(font_battleground_487_2_copy_spell)
            message2_battleground_487_2_copy_spell.exec_()
            self.battleground_487_2("Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        elif orc1_alive == False:
            message3_battleground_487_2_copy_spell = QMessageBox()
            message3_battleground_487_2_copy_spell.setWindowTitle("!!!")
            message3_battleground_487_2_copy_spell.setText("Первый орк повержен.\nОсталось еще два.\n")
            font_battleground_487_2_copy_spell.setPointSize(14)
            message3_battleground_487_2_copy_spell.setFont(font_battleground_487_2_copy_spell)
            message3_battleground_487_2_copy_spell.exec_()
            self.battleground_487_1_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        else:
            message4_battleground_487_2_copy_spell = QMessageBox()
            message4_battleground_487_2_copy_spell.setWindowTitle("!!!")
            message4_battleground_487_2_copy_spell.setText("Первый орк повержен.\nОсталось еще два.\n")
            font_battleground_487_2_copy_spell.setPointSize(14)
            message4_battleground_487_2_copy_spell.setFont(font_battleground_487_2_copy_spell)
            message4_battleground_487_2_copy_spell.exec_()
            self.battleground_487_1_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points        


    def battleground_487_3_copy_spell(self, copy_strength, copy_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc3_alive = True
        while orc3_alive == True:
            self.round_number += 1
            your_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            self.battle_text += "Ваша сила удара = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if copy_strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Копия ранила третьего орка.\n"
                orc3_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if orc3_life_points <= 0:
                    self.battle_text += "Третий орк повержен!!!\n"
                    orc3_alive = False
                    break
            elif copy_strength + your_cubic < orc3_strength + orc3_cubic:
                self.battle_text += "Третий орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Третий орк парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ",  ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"

        message_battleground_487_3_copy_spell = QDialog()
        message_battleground_487_3_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_487_3_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_487_3_copy_spell = QTextEdit(message_battleground_487_3_copy_spell)
        textEdit_battleground_487_3_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_487_3_copy_spell.clear()
        textEdit_battleground_487_3_copy_spell.setText(self.battle_text)
        buttonBox_battleground_487_3_copy_spell = QDialogButtonBox(message_battleground_487_3_copy_spell)
        buttonBox_battleground_487_3_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_487_3_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_487_3_copy_spell.accepted.connect(message_battleground_487_3_copy_spell.accept)
        font_battleground_487_3_copy_spell = QFont()
        font_battleground_487_3_copy_spell.setPointSize(10)
        message_battleground_487_3_copy_spell.setFont(font_battleground_487_3_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_487_3_copy_spell.setFocus()
        message_battleground_487_3_copy_spell.exec_()        
        if copy_life_points <= 0:
            message2_battleground_487_3_copy_spell = QMessageBox()
            message2_battleground_487_3_copy_spell.setWindowTitle("!!!")
            message2_battleground_487_3_copy_spell.setText("Копия проиграла и исчезает!!!")
            font_battleground_487_3_copy_spell.setPointSize(14)
            message2_battleground_487_3_copy_spell.setFont(font_battleground_487_3_copy_spell)
            message2_battleground_487_3_copy_spell.exec_()
            self.battleground_487_3("Третий орк", 7, orc3_life_points)
            return self.life_points
        elif orc3_alive == False:
            message3_battleground_487_3_copy_spell = QMessageBox()
            message3_battleground_487_3_copy_spell.setWindowTitle("!!!")
            message3_battleground_487_3_copy_spell.setText("Третий орк повержен. Вы выиграли бой!!!\n")
            font_battleground_487_3_copy_spell.setPointSize(14)
            message3_battleground_487_3_copy_spell.setFont(font_battleground_487_3_copy_spell)
            message3_battleground_487_3_copy_spell.exec_()
            return self.life_points
        else:
            message4_battleground_487_3_copy_spell = QMessageBox()
            message4_battleground_487_3_copy_spell.setWindowTitle("!!!")
            message4_battleground_487_3_copy_spell.setText("Третий орк повержен. Вы выиграли бой!!!\n")
            font_battleground_487_3_copy_spell.setPointSize(14)
            message4_battleground_487_3_copy_spell.setFont(font_battleground_487_3_copy_spell)
            message4_battleground_487_3_copy_spell.exec_()
            return self.life_points


    def battleground_518(self):
        self.battle_text = ""
        self.battle_text += "Начало битвы.\n"
        round_number = 0
        merchant_strength = 6
        merchant_strength = 12
        while True:
            round_number += 1
            your_cubic = random.randint(2, 12)
            enemy_cubic = random.randint(2, 12)
            self.battle_text += "Раунд " + str(round_number) + ".\n"
            self.battle_text += "У вас выпало: " + str(your_cubic) + ", у противника выпало: " + str(enemy_cubic) + "\n" 
            self.battle_text += "Ваша сила удара  = " + str(self.strength + your_cubic) + ",  Сила удара противника = " + str(merchant_strength + enemy_cubic) + "\n"
            if self.strength + your_cubic == merchant_strength + enemy_cubic:
                self.battle_text += "Противник парировал удар.\n"
                continue
            elif self.strength + your_cubic >= merchant_strength + enemy_cubic:
                merchant_strength -= 2
                self.battle_text += "Вы ударили противника.\nВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ",  ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(merchant_strength) + "\n"
                if merchant_strength <= 0:
                    self.battle_text += "Вы выиграли!!!"
                    break
                else:
                    continue
            else:
                self.life_points -= 3
                self.battle_text += "Противник ударил вас.\nВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(merchant_strength) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
                else:
                    continue
        message_battleground_one = QDialog()
        message_battleground_one.setWindowTitle("Окно битвы")
        message_battleground_one.setFixedSize(800, 600)
        textEdit_battleground_one = QTextEdit(message_battleground_one)
        textEdit_battleground_one.setFixedSize(800, 555)
        textEdit_battleground_one.clear()
        textEdit_battleground_one.setText(self.battle_text)
        buttonBox_battleground_one = QDialogButtonBox(message_battleground_one)
        buttonBox_battleground_one.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_one.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_one.accepted.connect(message_battleground_one.accept)
        font_battleground_one = QFont()
        font_battleground_one.setPointSize(10)
        message_battleground_one.setFont(font_battleground_one)
        # установить фокус на кнопке ОК
        buttonBox_battleground_one.setFocus()
        message_battleground_one.exec_()
        if self.life_points <= 0:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle(":-(")
            message3_battleground_one.setText("Вы проиграли.\nКонец игры...")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_one = QMessageBox()
            message3_battleground_one.setWindowTitle(":-)")
            message3_battleground_one.setText("Вы выиграли!!!")
            font_battleground_one.setPointSize(14)
            message3_battleground_one.setFont(font_battleground_one)
            message3_battleground_one.exec_()
            return self.life_points


    # первые три раунда боя на п.569
    def battleground_569(self):
        self.battle_text = ""
        orc1_strength = 10
        orc1_life_points = 6
        orc1_alive = True
        while self.round_number < 3:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + ", Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            if self.strength + your_cubic > orc1_strength + orc1_cubic:
                self.battle_text += "Вы ранили первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    orc1_alive = False
                    self.battle_text += "Первый орк повержен!!!\n"
                    break
            elif self.strength + your_cubic < orc1_strength + orc1_cubic:
                self.life_points -= 2
                self.battle_text += "Первый орк ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

        message_battleground_569 = QDialog()
        message_battleground_569.setWindowTitle("Окно битвы")
        message_battleground_569.setFixedSize(800, 600)
        textEdit_battleground_569 = QTextEdit(message_battleground_569)
        textEdit_battleground_569.setFixedSize(800, 555)
        textEdit_battleground_569.clear()
        textEdit_battleground_569.setText(self.battle_text)
        buttonBox_battleground_569 = QDialogButtonBox(message_battleground_569)
        buttonBox_battleground_569.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569.accepted.connect(message_battleground_569.accept)
        font_battleground_569 = QFont()
        font_battleground_569.setPointSize(10)
        message_battleground_569.setFont(font_battleground_569)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569.setFocus()
        message_battleground_569.exec_()
        if self.life_points <= 0:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle(":-(")
            message3_battleground_569.setText("Вы проиграли.\nКонец игры...")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            sys.exit("Game over")        
        elif orc1_alive == False:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle("!!!")
            message3_battleground_569.setText("Первый орк повержен!!!")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            message4_battleground_569 = QMessageBox()
            message4_battleground_569.setWindowTitle("!!!")
            message4_battleground_569.setText("Проверьте свою удачу!!!")
            font_battleground_569.setPointSize(14)
            message4_battleground_569.setFont(font_battleground_569)
            message4_battleground_569.exec_()
            if self.checking_luck == True:
                self.luck -= 1
                print("-1 к удаче (проверка удачи)")
                message1_battleground_569 = QMessageBox()
                message1_battleground_569.setWindowTitle("!!!")
                message1_battleground_569.setText("Удача вам улыбнулась. Третий орк не захотел умирать и убежал в лес. У вас остался один противник.")
                font_battleground_569.setPointSize(14)
                message1_battleground_569.setFont(font_battleground_569)
                message1_battleground_569.exec_()
                self.battleground_one("Второй орк", 7, 7)
            else:
                self.luck -= 1
                print("-1 к удаче (проверка удачи)")
                message1_battleground_569 = QMessageBox()
                message1_battleground_569.setWindowTitle("!!!")
                message1_battleground_569.setText("Удача от вас отвернулась. Третий орк остается. Вам придется драться с двумя оставшимися противниками.")
                font_battleground_569.setPointSize(14)
                message1_battleground_569.setFont(font_battleground_569)
                message1_battleground_569.exec_()
                self.battleground_569_2("Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
        else:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle("!!!!")
            message3_battleground_569.setText("Оставшиеся два орка вступают в бой.")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            self.battleground_569_3("Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points


    # битва с последним третьим орком
    def battleground_569_1(self, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc3_alive = True
        while orc3_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + ", Сила удара третьего орка = " + str(orc3_strength + orc3_cubic) + "\n"
            if self.strength + your_cubic > orc3_strength + orc3_cubic:
                self.battle_text += "Вы ранили третьего орка.\n"
                orc3_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if orc3_life_points <= 0:
                    orc3_alive = False
                    self.battle_text += "Третий противник повержен!!!\n"
                    break
            elif self.strength + your_cubic < orc3_strength + orc3_cubic:
                self.life_points -= 2
                self.battle_text += "Третий орк ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ТРЕТЬЕГО ОРКА = " + str(orc3_life_points) + "\n"

        message_battleground_569_3 = QDialog()
        message_battleground_569_3.setWindowTitle("Окно битвы")
        message_battleground_569_3.setFixedSize(800, 600)
        textEdit_battleground_569_3 = QTextEdit(message_battleground_569_3)
        textEdit_battleground_569_3.setFixedSize(800, 555)
        textEdit_battleground_569_3.clear()
        textEdit_battleground_569_3.setText(self.battle_text)
        buttonBox_battleground_569_3 = QDialogButtonBox(message_battleground_569_3)
        buttonBox_battleground_569_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_3.accepted.connect(message_battleground_569_3.accept)
        font_battleground_569_3 = QFont()
        font_battleground_569_3.setPointSize(10)
        message_battleground_569_3.setFont(font_battleground_569_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_3.setFocus()
        message_battleground_569_3.exec_()
        if self.life_points <= 0:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle(":-(")
            message3_battleground_569_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle("!!!")
            message3_battleground_569_3.setText("Вы выиграли!!!")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            return self.life_points


    # битва со вторым и третьим орком
    def battleground_569_2(self, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc2_alive = True
        orc3_alive = True
        while orc2_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength) + "\n"
            self.battle_text += "Сила удара Третьего Орка = " + str(orc3_strength) + "\n"
            if self.strength + your_cubic > orc2_strength + orc2_cubic:
                self.battle_text += "Вы ранили второго орка.\n"
                orc2_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    orc2_alive = False
                    self.battle_text += "Второй орк повержен!!!\n"
            elif self.strength + your_cubic < orc2_strength + orc2_cubic:
                self.life_points -= 2
                self.battle_text += "Второй орк ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"

            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Вы парировали удар третьего орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

        message_battleground_569_3 = QDialog()
        message_battleground_569_3.setWindowTitle("Окно битвы")
        message_battleground_569_3.setFixedSize(800, 600)
        textEdit_battleground_569_3 = QTextEdit(message_battleground_569_3)
        textEdit_battleground_569_3.setFixedSize(800, 555)
        textEdit_battleground_569_3.clear()
        textEdit_battleground_569_3.setText(self.battle_text)
        buttonBox_battleground_569_3 = QDialogButtonBox(message_battleground_569_3)
        buttonBox_battleground_569_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_3.accepted.connect(message_battleground_569_3.accept)
        font_battleground_569_3 = QFont()
        font_battleground_569_3.setPointSize(10)
        message_battleground_569_3.setFont(font_battleground_569_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_3.setFocus()
        message_battleground_569_3.exec_()
        if self.life_points <= 0:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle(":-(")
            message3_battleground_569_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle("!!!")
            message3_battleground_569_3.setText("Второй орк повержен!!! Остался третий орк.")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            self.battleground_569_1("Третий орк", 7, 7)
            return self.life_points             


    # битва со всеми тремя орками (если первый выжил после первых трех раундов атаки)
    def battleground_569_3(self, orc1_name, orc1_strength, orc1_life_points, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc1_alive = True
        orc2_alive = True
        orc3_alive = True
        while orc1_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(self.strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого Орка = " + str(orc1_strength) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength) + "\n"
            self.battle_text += "Сила удара Третьего Орка = " + str(orc3_strength) + "\n"
            if self.strength + your_cubic > orc1_strength + orc1_cubic:
                self.battle_text += "Вы ранили первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    orc1_alive = False
                    self.battle_text += "Первый орк повержен!!!\n"
            elif self.strength + your_cubic < orc1_strength + orc1_cubic:
                self.life_points -= 2
                self.battle_text += "Первый орк ранил вас.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал ваш удар.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

            if self.strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Вы парировали удар второго орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Второй орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break

            if self.strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Вы парировали удар третьего орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил вас.\n"
                self.life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(self.life_points) + "\n"
                if self.life_points <= 0:
                    self.battle_text += "Вы проиграли!!!\n"
                    break 

        message_battleground_569_3 = QDialog()
        message_battleground_569_3.setWindowTitle("Окно битвы")
        message_battleground_569_3.setFixedSize(800, 600)
        textEdit_battleground_569_3 = QTextEdit(message_battleground_569_3)
        textEdit_battleground_569_3.setFixedSize(800, 555)
        textEdit_battleground_569_3.clear()
        textEdit_battleground_569_3.setText(self.battle_text)
        buttonBox_battleground_569_3 = QDialogButtonBox(message_battleground_569_3)
        buttonBox_battleground_569_3.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_3.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_3.accepted.connect(message_battleground_569_3.accept)
        font_battleground_569_3 = QFont()
        font_battleground_569_3.setPointSize(10)
        message_battleground_569_3.setFont(font_battleground_569_3)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_3.setFocus()
        message_battleground_569_3.exec_()
        if self.life_points <= 0:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle(":-(")
            message3_battleground_569_3.setText("Вы проиграли.\nКонец игры...")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            sys.exit("Game over")        
        else:
            message3_battleground_569_3 = QMessageBox()
            message3_battleground_569_3.setWindowTitle("!!!")
            message3_battleground_569_3.setText("Первый орк повержен!!! Оставшиеся два орка вступают в бой.")
            font_battleground_569_3.setPointSize(14)
            message3_battleground_569_3.setFont(font_battleground_569_3)
            message3_battleground_569_3.exec_()
            self.battleground_569_2("Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points
          

    def battleground_569_copy_spell(self):
        self.battle_text = ""
        copy_strength = orc1_strength = 10
        copy_life_points = orc1_life_points = 6
        orc1_alive = True
        while self.round_number < 3:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            self.battle_text += "Сила Удара копии = " + str(copy_strength + your_cubic) + ", Сила удара первого орка = " + str(orc1_strength + orc1_cubic) + "\n"
            if copy_strength + your_cubic > orc1_strength + orc1_cubic:
                self.battle_text += "Копия ранила первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    orc1_alive = False
                    self.battle_text += "Первый орк повержен!!!\n"
                    break
            elif copy_strength + your_cubic < orc1_strength + orc1_cubic:
                copy_life_points -= 2
                self.battle_text += "Первый орк ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

        message_battleground_569 = QDialog()
        message_battleground_569.setWindowTitle("Окно битвы")
        message_battleground_569.setFixedSize(800, 600)
        textEdit_battleground_569 = QTextEdit(message_battleground_569)
        textEdit_battleground_569.setFixedSize(800, 555)
        textEdit_battleground_569.clear()
        textEdit_battleground_569.setText(self.battle_text)
        buttonBox_battleground_569 = QDialogButtonBox(message_battleground_569)
        buttonBox_battleground_569.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569.accepted.connect(message_battleground_569.accept)
        font_battleground_569 = QFont()
        font_battleground_569.setPointSize(10)
        message_battleground_569.setFont(font_battleground_569)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569.setFocus()
        message_battleground_569.exec_()
        if copy_life_points <= 0:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle("!!!")
            message3_battleground_569.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            self.battleground_569()
            return self.life_points
        elif orc1_alive == False:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle("!!!")
            message3_battleground_569.setText("Первый орк повержен!!!")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            message4_battleground_569 = QMessageBox()
            message4_battleground_569.setWindowTitle("!!!")
            message4_battleground_569.setText("Проверьте свою удачу!!!")
            font_battleground_569.setPointSize(14)
            message4_battleground_569.setFont(font_battleground_569)
            message4_battleground_569.exec_()
            if self.checking_luck == True:
                self.luck -= 1
                print("-1 к удаче (проверка удачи)")
                message1_battleground_569 = QMessageBox()
                message1_battleground_569.setWindowTitle("!!!")
                message1_battleground_569.setText("Удача вам улыбнулась. Третий орк не захотел умирать и убежал в лес. У вас остался один противник.")
                font_battleground_569.setPointSize(14)
                message1_battleground_569.setFont(font_battleground_569)
                message1_battleground_569.exec_()
                self.battleground_569_1_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, copy_life_points)
                return self.life_points
            else:
                self.luck -= 1
                print("-1 к удаче (проверка удачи)")
                message1_battleground_569 = QMessageBox()
                message1_battleground_569.setWindowTitle("!!!")
                message1_battleground_569.setText("Удача от вас отвернулась. Третий орк остается. Вам придется драться с двумя оставшимися противниками.")
                font_battleground_569.setPointSize(14)
                message1_battleground_569.setFont(font_battleground_569)
                message1_battleground_569.exec_()
                self.battleground_569_2_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
                return self.life_points
        else:
            message3_battleground_569 = QMessageBox()
            message3_battleground_569.setWindowTitle("!!!!")
            message3_battleground_569.setText("Оставшиеся два орка вступают в бой.")
            font_battleground_569.setPointSize(14)
            message3_battleground_569.setFont(font_battleground_569)
            message3_battleground_569.exec_()
            self.battleground_569_3_copy_spell(copy_strength, copy_life_points, "Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points


    def battleground_569_1_copy_spell(self, copy_strength, copy_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc3_alive = True
        while orc3_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Сила Удара копии = " + str(copy_strength + your_cubic) + ", Сила удара противника = " + str(orc3_strength + orc3_cubic) + "\n"
            if copy_strength + your_cubic > orc3_strength + orc3_cubic:
                self.battle_text += "Копия ранила противника.\n"
                orc3_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc3_life_points) + "\n"
                if orc3_life_points <= 0:
                    orc3_alive = False
                    self.battle_text += "Третий орк повержен!!!\n"
                    break
            elif copy_strength + your_cubic < orc3_strength + orc3_cubic:
                copy_life_points -= 2
                self.battle_text += "Противник ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc3_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПРОТИВНИКА = " + str(orc3_life_points) + "\n"

        message_battleground_569_1_copy_spell = QDialog()
        message_battleground_569_1_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_569_1_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_569_1_copy_spell = QTextEdit(message_battleground_569_1_copy_spell)
        textEdit_battleground_569_1_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_569_1_copy_spell.clear()
        textEdit_battleground_569_1_copy_spell.setText(self.battle_text)
        buttonBox_battleground_569_1_copy_spell = QDialogButtonBox(message_battleground_569_1_copy_spell)
        buttonBox_battleground_569_1_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_1_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_1_copy_spell.accepted.connect(message_battleground_569_1_copy_spell.accept)
        font_battleground_569_1_copy_spell = QFont()
        font_battleground_569_1_copy_spell.setPointSize(10)
        message_battleground_569_1_copy_spell.setFont(font_battleground_569_1_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_1_copy_spell.setFocus()
        message_battleground_569_1_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_569_1_copy_spell = QMessageBox()
            message3_battleground_569_1_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_1_copy_spell.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_569_1_copy_spell.setPointSize(14)
            message3_battleground_569_1_copy_spell.setFont(font_battleground_569_1_copy_spell)
            message3_battleground_569_1_copy_spell.exec_()
            self.battleground_569_1("Третий орк", 7, orc3_life_points)
            return self.life_points                
        else:
            message3_battleground_569_1_copy_spell = QMessageBox()
            message3_battleground_569_1_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_1_copy_spell.setText("Противник повержен. Вы выиграли!!!")
            font_battleground_569_1_copy_spell.setPointSize(14)
            message3_battleground_569_1_copy_spell.setFont(font_battleground_569_1_copy_spell)
            message3_battleground_569_1_copy_spell.exec_()
            return self.life_points

    def battleground_569_2_copy_spell(self, copy_strength, copy_life_points, orc2_name, orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc2_alive = True
        orc3_alive = True
        while orc2_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Ваша Сила Удара = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength) + "\n"
            self.battle_text += "Сила удара Третьего Орка = " + str(orc3_strength) + "\n"
            if copy_strength + your_cubic > orc2_strength + orc2_cubic:
                self.battle_text += "Копия ранила второго орка.\n"
                orc2_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if orc2_life_points <= 0:
                    orc2_alive = False
                    self.battle_text += "Второй орк повержен!!!\n"
            elif copy_strength + your_cubic < orc2_strength + orc2_cubic:
                copy_life_points -= 2
                self.battle_text += "Второй орк ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ВТОРОГО ОРКА = " + str(orc2_life_points) + "\n"

            if copy_strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Копия парировала удар третьего орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

        message_battleground_569_2_copy_spell = QDialog()
        message_battleground_569_2_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_569_2_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_569_2_copy_spell = QTextEdit(message_battleground_569_2_copy_spell)
        textEdit_battleground_569_2_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_569_2_copy_spell.clear()
        textEdit_battleground_569_2_copy_spell.setText(self.battle_text)
        buttonBox_battleground_569_2_copy_spell = QDialogButtonBox(message_battleground_569_2_copy_spell)
        buttonBox_battleground_569_2_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_2_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_2_copy_spell.accepted.connect(message_battleground_569_2_copy_spell.accept)
        font_battleground_569_2_copy_spell = QFont()
        font_battleground_569_2_copy_spell.setPointSize(10)
        message_battleground_569_2_copy_spell.setFont(font_battleground_569_2_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_2_copy_spell.setFocus()
        message_battleground_569_2_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_569_2_copy_spell = QMessageBox()
            message3_battleground_569_2_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_2_copy_spell.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_569_2_copy_spell.setPointSize(14)
            message3_battleground_569_2_copy_spell.setFont(font_battleground_569_2_copy_spell)
            message3_battleground_569_2_copy_spell.exec_()
            self.battleground_569_2("Второй орк", 7, orc2_life_points, "Третий орк", 7, 7)
            return self.life_points                 
        else:
            message3_battleground_569_2_copy_spell = QMessageBox()
            message3_battleground_569_2_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_2_copy_spell.setText("Второй орк повержен!!! Остался третий орк.")
            font_battleground_569_2_copy_spell.setPointSize(14)
            message3_battleground_569_2_copy_spell.setFont(font_battleground_569_2_copy_spell)
            message3_battleground_569_2_copy_spell.exec_()
            self.battleground_569_1_copy_spell(copy_strength, copy_life_points, "Третий орк", 7, 7)
            return self.life_points 

    def battleground_569_3_copy_spell(self, copy_strength, copy_life_points, orc1_name, orc1_strength, orc1_life_points, orc2_name, 
                                        orc2_strength, orc2_life_points, orc3_name, orc3_strength, orc3_life_points):
        self.battle_text = ""
        orc1_alive = True
        orc2_alive = True
        orc3_alive = True
        while orc1_alive == True:
            self.round_number += 1
            self.battle_text += "Раунд " + str(self.round_number) + ".\n"
            your_cubic = random.randint(2, 12)
            orc1_cubic = random.randint(2, 12)
            orc2_cubic = random.randint(2, 12)
            orc3_cubic = random.randint(2, 12)
            self.battle_text += "Сила Удара копии = " + str(copy_strength + your_cubic) + "\n"
            self.battle_text += "Сила удара Первого Орка = " + str(orc1_strength) + "\n"
            self.battle_text += "Сила удара Второго Орка = " + str(orc2_strength) + "\n"
            self.battle_text += "Сила удара Третьего Орка = " + str(orc3_strength) + "\n"
            if copy_strength + your_cubic > orc1_strength + orc1_cubic:
                self.battle_text += "Копия ранила первого орка.\n"
                orc1_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if orc1_life_points <= 0:
                    orc1_alive = False
                    self.battle_text += "Первый орк повержен!!!\n"
            elif copy_strength + your_cubic < orc1_strength + orc1_cubic:
                copy_life_points -= 2
                self.battle_text += "Первый орк ранил копию.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break
            else:
                self.battle_text += "Противник парировал удар копии.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + ", ВЫНОСЛИВОСТЬ ПЕРВОГО ОРКА = " + str(orc1_life_points) + "\n"

            if copy_strength + your_cubic >= orc2_strength + orc2_cubic:
                self.battle_text += "Копия парировала удар второго орка.\n"
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
            else:
                self.battle_text += "Второй орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВЫНОСЛИВОСТЬ КОПИИ = " + str(copy_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break

            if copy_strength + your_cubic >= orc3_strength + orc3_cubic:
                self.battle_text += "Копия парировала удар третьего орка.\n"
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(copy_life_points) + "\n"
            else:
                self.battle_text += "Третий орк ранил копию.\n"
                copy_life_points -= 2
                self.battle_text += "ВАША ВЫНОСЛИВОСТЬ = " + str(copy_life_points) + "\n"
                if copy_life_points <= 0:
                    self.battle_text += "Копия проиграла и исчезает!!!\n"
                    break 

        message_battleground_569_3_copy_spell = QDialog()
        message_battleground_569_3_copy_spell.setWindowTitle("Окно битвы")
        message_battleground_569_3_copy_spell.setFixedSize(800, 600)
        textEdit_battleground_569_3_copy_spell = QTextEdit(message_battleground_569_3_copy_spell)
        textEdit_battleground_569_3_copy_spell.setFixedSize(800, 555)
        textEdit_battleground_569_3_copy_spell.clear()
        textEdit_battleground_569_3_copy_spell.setText(self.battle_text)
        buttonBox_battleground_569_3_copy_spell = QDialogButtonBox(message_battleground_569_3_copy_spell)
        buttonBox_battleground_569_3_copy_spell.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox_battleground_569_3_copy_spell.move(375, 565)
        # событие кнопки ОК (стандартное)
        buttonBox_battleground_569_3_copy_spell.accepted.connect(message_battleground_569_3_copy_spell.accept)
        font_battleground_569_3_copy_spell = QFont()
        font_battleground_569_3_copy_spell.setPointSize(10)
        message_battleground_569_3_copy_spell.setFont(font_battleground_569_3_copy_spell)
        # установить фокус на кнопке ОК
        buttonBox_battleground_569_3_copy_spell.setFocus()
        message_battleground_569_3_copy_spell.exec_()
        if copy_life_points <= 0:
            message3_battleground_569_3_copy_spell = QMessageBox()
            message3_battleground_569_3_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_3_copy_spell.setText("Копия проиграла и исчезает!!! Ваша очередь вступать в бой!")
            font_battleground_569_3_copy_spell.setPointSize(14)
            message3_battleground_569_3_copy_spell.setFont(font_battleground_569_3_copy_spell)
            message3_battleground_569_3_copy_spell.exec_()
            self.battleground_569_3("Первый орк", 10, orc1_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points      
        else:
            message3_battleground_569_3_copy_spell = QMessageBox()
            message3_battleground_569_3_copy_spell.setWindowTitle("!!!")
            message3_battleground_569_3_copy_spell.setText("Первый орк повержен!!! Оставшиеся два орка вступают в бой.")
            font_battleground_569_3_copy_spell.setPointSize(14)
            message3_battleground_569_3_copy_spell.setFont(font_battleground_569_3_copy_spell)
            message3_battleground_569_3_copy_spell.exec_()
            self.battleground_569_2_copy_spell(copy_strength, copy_life_points, "Второй орк", 7, 7, "Третий орк", 7, 7)
            return self.life_points

                         

class Unit():

    def __init__(self, strength, life_points):
        self.life_points = life_points
        self.strength = strength
        self.death = False


class Item():

    def __init__(self, item_name, item_parameter):
        self.item_name = item_name
        self.condition = False
        self.item_parameter = item_parameter

    def __str__(self):
        return f"{self.item_name}, {self.item_parameter}"

    


# first_woodman_6 = Unit(5, 4)
# second_woodman_6 = Unit(6, 7)
# first_bat_16 = Unit(6, 8)
# second_bat_16 = Unit(5, 7)
# third_bat_16 = Unit(5, 6)
# orc_33 = Unit(6, 8)
# goblin_33 = Unit(7, 5)
# dragon_37 = Unit(9, 4)
# first_goblin_40 = Unit(6, 9)
# second_goblin_40 = Unit(7, 5)
# dragon_41 = Unit(9, 4)
# spider_54 = Unit(8, 8)
# chief_guard_65 = Unit(9, 5)
# woman_vampire_83 = Unit(11, 14)

# goblin_102 = Unit(8, 9)
# green_knight_112 = Unit(10, 10)
# first_rogue_123 = Unit(6, 4)
# second_rogue_123 = Unit(7, 8)
# third_rogue_123 = Unit(5, 5)
# first_green_knight_183 = Unit(10, 10)
# second_green_knight_183 = Unit(10, 10)
# goblin_192 = Unit(7, 9)

# monkey_215 = Unit(9, 14)
# spider_219 = Unit(5, 8)
# ghost_243 = Unit(10, 9)
# spider_244 = Unit(8, 8)
# dead_spirit_247 = Unit(10, 12)
# lion_257 = Unit(9, 15)
# hyena_265 = Unit(6, 6)
# goblin_290 = Unit(6, 9)
# barlad_dearth_293 = Unit(14, 12)

# first_knight_301 = Unit(10, 10)
# second_knight_301 = Unit(10, 10)
# third_knight_301 = Unit(10, 10)
# captain_knight_301 = Unit(12, 12)
# green_knight_309 = Unit(10, 10)
# dragon_316 = Unit(12, 8)
# aqua_man_326 = Unit(7, 7)
# first_orc_328 = Unit(8, 5)
# second_orc_328 = Unit(7, 7)
# troll_356 = Unit(9, 14)
# first_man_374 = Unit(8, 5)
# second_man_374 = Unit(6, 9)

# first_orc_487 = Unit(10, 6)
# second_orc_487 = Unit(7, 7)
# third_orc_487 = Unit(7, 7)
# orc_499 = Unit(7, 7)

# merchant_518 = Unit(6, 12)
# werewolf_528 = Unit(10, 10)
# bear_529 = Unit(8, 10)
# first_goblin_532 = Unit(8, 10)
# second_goblin_532 = Unit(6, 8)
# first_goblin_539 = Unit(4, 7)
# second_goblin_539 = Unit(8, 9)
# green_knight_543 = Unit(11, 14)
# harpy_553 = Unit(10, 12)
# spider_558 = Unit(8, 8)
# forester_563 = Unit(6, 8)
# green_knight_567 = Unit(10, 10)
# first_orc_569 = Unit(10, 6)
# second_orc_569 = Unit(7, 7)
# third_orc_569 = Unit(7, 7)
# first_goblin_580 = Unit(4, 9)
# second_goblin_580 = Unit(7, 5)

# cook_604 = Unit(8, 10)

