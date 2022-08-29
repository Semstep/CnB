import string as strg
# import configparser as cfg  # чтоб сохранять настройки в файл https://python-scripts.com/configparser-python-example
import random as rnd


class CnBSettings:
    """
    quest_set: set 'символы для квестовой последовательности'\n
    quest_size: int 'кол-во символов в задаче'\n
    may_be_repeated: bool 'в классике символы не повторяются'\n
    """
    __quest_set: list = strg.digits  #
    __quest_size: int = 6  #
    __may_be_repeated: bool = False  #

    def set_user_settings(self, questset=strg.digits, questsize=6, isrepeats=False):
        self.quest_set, self.quest_size, self.may_be_repeated = questset, questsize, isrepeats

    @property
    def quest_set(self):
        return self.__quest_set

    @quest_set.setter
    def quest_set(self, value):
        self.__quest_set = value

    @property
    def quest_size(self):
        return self.__quest_size

    @quest_size.setter
    def quest_size(self, value):
        self.__quest_size = value

    @property
    def may_be_repeated(self):
        return self.__may_be_repeated

    @may_be_repeated.setter
    def may_be_repeated(self, value):
        self.__may_be_repeated = value


class CnBHistory:  # можно приоптимизировать в основной класс, это просто словарь!
    """
    Структура: словарь {номер хода: {'u_ans': '', 'b_n_c': (0, 0, ), 'memos': ''}}
    """
    history: dict
    RECORD_DEF = {'u_ans': '', 'b_n_c': (0, 0,), 'memos': ''}

    def __init__(self):
        self.history = {}
        self._cur_rec_key = None

    def new_record(self, step_num):
        self.history.setdefault(step_num, self.RECORD_DEF.copy())
        self._cur_rec_key = step_num

    def edit_memo(self, step_num, value):  # idx - индекс в списке-значении словаря по ключу step_num
        ...

    def clear(self):
        self.history.clear()

    def append(self, key, val):
        self.history[self._cur_rec_key][key] = val


class CnBConsoleUI:
    FIRST_COL = 4
    SEC_COL = 15
    THIRD_COL = 15

    def __init__(self, hist_storage: CnBHistory = None, settings: CnBSettings = None):
        self.commands = {  # Положение записей в словаре не менять! Добавлять и переименовывать можно.
            '--H': self.get_inline_help,  # --HА вывести алфавит.
            '--S': self.show_history,
            '--E': self.surrend,
            '--A': self.hint
        }
        self.history_storage = hist_storage
        self.settings = settings

    def get_inline_help(self, *args):
        if isinstance(args[0], str):
            if args[0] in 'АAaа':  # кириллица и латиница
                print(f'В загадке такие символы:\n{", ".join(self.settings.quest_set)}. По условию символы '
                      f'{"могут повторяться" if self.settings.may_be_repeated else "повторяться не могут"}.')
        print('Это такой хелп пока что.')

    def surrend(self):
        ...

    def hint(self):
        ...

    def parse_cmd(self, text: str):
        txt = text.strip()
        for c in self.commands:
            if txt.startswith(c):
                self.commands[c](txt.lstrip(c))  # выполняем функцию из словаря
                return True
        return False

    def show_input_error(self, err_lst: list):
        ...


    @staticmethod
    def _form_chars_for_output(txt: str):  # на входе строка 'abcd', на выходе строка 'a, b, c и d'
        txt = ''.join(set(txt))
        if len(txt) < 2:
            return txt
        return f'{", ".join(txt[:-2])} и {txt[-1]}'

    def test_user_answer(self, txt):
        err_list = []

        # проверка длинны
        if len(txt) != self.settings.quest_size:
            err_list.append(f'Вы, уважаемый, отправили нам символов в количестве {len(txt)} шт., '
                            f'а хотелось бы {self.settings.quest_size}...')

        # проверка допустимых символов
        fake_chars_str = ''.join([c for c in txt if c not in self.settings.quest_set])
        if fake_chars_str:
            wrong_chars_str = self._form_chars_for_output(fake_chars_str)
            err_list.append(f'{"Символов" if len(wrong_chars_str) > 1 else "Символа"} '
                            f'<{wrong_chars_str}> быть не должно.\n'
                            f'Напомнить алфавит? Пиши латиницей (по-английски) {list(self.commands.keys())[0]}А')

        # проверка повторов
        rep_chars = ''
        if not self.settings.may_be_repeated and len(txt) != len(set(txt)):
            rep_chars = ''.join([c for c in txt if txt.count(c) > 1])
            err_list.append(f'По условию задачи символы не повторяются, а тут повтор '
                            f'{self._form_chars_for_output(rep_chars)}')

        if err_list:
            [print(es) for es in err_list]
            return None

        return txt

    def get_user_input(self, step_numb) -> str:
        """Получает, проверяет, выделяет команды из юзерского ввода. Висим здесь пока не получится вменяемого ответа"""
        inp_greet_str = f'{step_numb:>{self.FIRST_COL - 2}}> '

        uinp, cmd_finded = None, True
        while not uinp or cmd_finded:
            inp = (input(inp_greet_str))
            if not self.parse_cmd(inp):
                cmd_finded = False
                uinp = self.test_user_answer(inp)

        return uinp

    def reset(self):
        ...

    def show_victory(self, *args):
        print('Точняк, кросавчег')

    def _show_history_rec(self, stepnum: int, stepdata: dict):
        stepnum_str = f'{stepnum:>{self.FIRST_COL - 2}}'
        uinput, bulls_n_cows, *memo = stepdata.values()  # memo, т.е. юзерские заметки, может быть не везде
        bulls, cows = bulls_n_cows
        uans_str = f'{uinput:<{self.SEC_COL}}'
        bnc_raw_str = f'{bulls:>2} Б / {cows:>2} К'
        bnc_str = f'{bnc_raw_str:<{self.THIRD_COL}}'
        memo_str = str(*memo)
        print(f'{stepnum_str}> {uans_str} | {bnc_str} || {memo_str}')

    def show_history(self, *args):  # аргз это нужная затычка, чтоб вызывать из парсера команд
        for k in sorted(self.history_storage.history.keys()):  # ключ это номер хода
            self._show_history_rec(k, self.history_storage.history[k])


class CnB:
    quest: str = None  # задание для отгадки
    cur_move_numb: int = 0  # номер текущего хода
    is_guessed = False  # отгадано ли число
    # is_surrender = False

    def __init__(self, ui=CnBConsoleUI):
        self.settings = CnBSettings()
        self.history = CnBHistory()
        self.ui = ui(hist_storage=self.history, settings=self.settings)
        self.prepare()
        self.usr_answer = (None, '',)  # ввод юзера: результат команды и строка с ответом

    def make_quest(self, settings: CnBSettings) -> str:
        """Подготовка задания в зависимости от настроек"""
        if settings.may_be_repeated:
            quest = rnd.choices(settings.quest_set, k=settings.quest_size)
        else:
            quest = rnd.sample(settings.quest_set, settings.quest_size)
        return ''.join(quest)

    def prepare(self):
        """Сбор всей подготовки в кучу"""
        self.quest = self.make_quest(self.settings)
        self.cur_move_numb = 0
        self.history.clear()
        self.ui.reset()
        self.is_guessed = False

    def __call__(self, *args, **kwargs) -> bool:
        """Вызывается на каждый ход возвращает инфу, ходить ли дальше"""
        return self.is_guessed

    def get_b_and_c(self, ans, quest):
        bulls = cows = 0
        for i, letter in enumerate(ans):
            if letter in quest:
                if letter == quest[i]:
                    bulls += 1
                else:
                    cows += 1

        return bulls, cows

    def make_move(self):
        """Логика одного хода от начала до конца"""
        self.cur_move_numb += 1
        self.history.new_record(self.cur_move_numb)
        usr_ans = self.ui.get_user_input(self.cur_move_numb)

        if usr_ans == self.quest:
            self.ui.show_victory()
            self.is_guessed = True
        else:
            buls, cows = self.get_b_and_c(usr_ans, self.quest)
            self.history.append('u_ans', usr_ans)
            self.history.append('b_n_c', (buls, cows,))
            self.ui.show_history()


def _main():
    game = CnB()
    game.prepare()
    while not game():
        game.make_move()


if __name__ == '__main__':
    _main()
