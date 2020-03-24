from .Domain import Domain
from .helpers import strip_parentheses
from .notation import notation
from .rules import rules


class Formula:
    def __init__(self, formula_str):
        self.formula_str = formula_str

        self.done = False
        self.rule_name = None
        self.rule = None
        self.negated = None
        self.operator = None
        self.first_arg = None
        self.second_arg = None
        self.color = None
        self.launched_for = Domain()  # dotyczy gammy, dziedzina na której została już odpalona ta gamma

    def mark(self):
        # z początku formuła ma jedynie wartość self.formula_str
        # a ta funkcja uzupełnia obiekt formuły o całą resztę potrzebnych informacji
        formula_str = self.formula_str
        formula_str = strip_parentheses(formula_str)

        negation = False
        if formula_str[0] == '¬':
            negation = True
            formula_str = formula_str.strip(' ¬')
            formula_str = strip_parentheses(formula_str)

        if formula_str[0] in '∀∃':
            self._break_down_gamma_delta(formula_str)
        elif formula_str[0] in notation['predicate']:
            self.done = True
            if negation:  # to nieużywane jest nigdzie, można wywalić
                self.rule_name = 'negated literal'
            else:
                self.rule_name = 'literal'
        else:
            self._break_down_alpha_beta(formula_str)


        if not self.done:
            self.rule_name = rules[negation][self.operator][0]  # marks formulas as alpha/beta/gamma/delta
            self.rule = rules[negation][self.operator][1:]
        self.negated = negation

    def _break_down_alpha_beta(self, formula_str):  # rozbija formuły alpha/beta na argumenty i operator
        bracket_depth = 0
        close_bracket_pos = 0
        for i, letter in enumerate(formula_str):
            if letter == '(':
                bracket_depth += 1
            elif letter == ')':
                bracket_depth -= 1
            if bracket_depth == 0:
                close_bracket_pos = i
                break
        self.first_arg = formula_str[:close_bracket_pos+1]
        self.operator = formula_str[close_bracket_pos+2]
        self.second_arg = formula_str[close_bracket_pos+4:]

    def _break_down_gamma_delta(self, formula_str):  # rozbija formuły gamma/delta na argumenty i operator
        formula_str = strip_parentheses(formula_str)
        self.operator, self.first_arg, self.second_arg = formula_str.split(maxsplit=2)
