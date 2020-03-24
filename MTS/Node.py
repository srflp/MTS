from .Domain import Domain
from .helpers import strip_parentheses


class Node:  # węzeł
    def __init__(self, data=None):
        self.id = None  # id i parent_id przypisywane są dopiero po zarejestrowaniu węzła na liście węzłów (NodeList)
        self.parent_id = None

        self.formulas = []
        self.status = ''  # ['w trakcie', 'liść otwarty', 'liść domknięty']
        self.performed_rule = ''
        self.domain = Domain()

        if data is None:
            data = {}
        for key in data:
            setattr(self, key, data[key])

    def check_for_complementary_literals(self):
        # (STOP 1 – wyższy priorytet) w węźle jest para literałów komplementarnych lub formuł
        # komplementarnych; węzeł oznaczamy jako domknięty (⊗)
        for formula in self.formulas:
            if formula.negated:
                if strip_parentheses(formula.formula_str).strip(' ¬') in [form.formula_str for form in self.formulas]:
                    self.status = '⊗ liść domknięty; STOP 1'
                    return True
        return False

    def check_if_every_formula_done(self):
        # (STOP 2 – niższy priorytet) w węźle są tylko literały oraz opcjonalnie formuły typu γ, które
        # były już aktywowane dla każdego elementu dziedziny; jeżeli jest para literałów komplementarnych
        # węzeł oznaczamy jako domknięty (⊗) w przeciwnym razie węzeł oznaczamy jako otwarty
        all_formulas_done = True
        for formula in self.formulas:
            if formula.rule_name != 'gamma':
                if not formula.done:
                    all_formulas_done = False
                    break
            else:  # gamma
                if str(self.domain) != str(formula.launched_for):
                    all_formulas_done = False
                    break
        if all_formulas_done:
            self.status = '⊙ liść otwarty; STOP 2'
        return all_formulas_done
