from .notation import notation


class Domain:  # dziedzina
    def __init__(self, inp=None, mode='normal'):
        self.domain = set()

        if inp is None:
            inp = set()
        if mode == 'normal':
            self.domain = inp
        elif mode == 'rpn':  # generowanie dziedziny z inputu
            inp = inp.split()  # input to rpn_string
            for item in inp:
                if item in notation['constant']:
                    self.domain.add(item)
            if len(self.domain) == 0:  # dziedzina nie może być pusta
                self.domain.add('a')

    def __str__(self):
        return ', '.join(sorted(self.domain))

    def __iter__(self):
        return iter(self.domain)

    def extend_by_new_const(self):  # dodaje nową stałą do dziedziny, używane w delcie
        for letter in notation['constant']:
            if letter not in self.domain:
                self.domain.add(letter)
                return letter
