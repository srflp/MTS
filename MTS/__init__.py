import copy

from .rules import rule_symbols
from .rpn_to_infix import rpn_to_infix, normalize
from .helpers import color_text
from .Domain import Domain
from .Node import Node
from .NodeList import NodeList
from .Formula import Formula


class MTS:
    def __init__(self, rpn_formula_str):
        # przygotowanie początkowej formuły do badania - zamiana z ONP na notację nawiasową
        infix_input = normalize(rpn_to_infix(rpn_formula_str))
        init_formula = Formula(infix_input)

        # generowanie dziedziny z inputu (formuły w ONP)
        domain = Domain(rpn_formula_str, mode='rpn')

        # dodanie węzła z początkową formułą i dziedziną ({formuła}, {a, b})
        self.node_list = NodeList()
        node = Node({
            'formulas': [init_formula],
            'domain': domain,
        })
        self.node_list.register(node)

    def solve(self):  # rozpoczyna rozwiązywanie formuły
        self._next_step()  # rekurencyjnie wywołuje samą siebie
        self._pretty_print()
        # self._debug_print()

    def _pretty_print(self):
        for node_id, node in enumerate(self.node_list):
            formulas_str = ', '.join(
                color_text(formula.formula_str, formula.color) for formula in node.formulas
            )
            front_spaces = ' ' * 4 * node.depth

            print('{}{{ {} }}, {{ {} }} {}'.format(front_spaces,
                                                   formulas_str, str(node.domain),
                                                   color_text('[' + rule_symbols[node.performed_rule] + ']',
                                                              'blue') if node.performed_rule in rule_symbols else node.performed_rule)
                  )
            if node.status != '':
                color = 'green'
                if node.status[0] == '⊗':
                    color = 'red'
                print(front_spaces + color_text(node.status, color))
        print('\n-> {}'.format(color_text('SPEŁNIALNA', 'green') if self._is_satisfiable() else color_text('NIESPEŁNIALNA', 'red')))

    # def _debug_print(self):  # dawno nieaktualizowany, może wywalać
    #     for node_id, node in enumerate(self.node_list):
    #         formulas_str = ', '.join(underline(formula.formula_str) if formula.underline else formula.formula_str for formula in node.formulas)
    #         print('({}) {{{}}}, {{{}}} ({}) | {}{}'.format(
    #             node_id, formulas_str, str(node.domain), node.parent_id,
    #             rule_symbols[node.performed_rule] + ' | ' if node.performed_rule in rule_symbols else node.performed_rule, node.status)
    #         )
    #         for i, formula in enumerate(node.formulas):
    #             print('    {}: {} | {} | {} | {} | {} | neg? - {} | done? - {} | {{{}}}'.format(
    #                 i+1, formula.formula_str, formula.first_arg, formula.operator, formula.second_arg, formula.rule_name, formula.negated, formula.done, str(formula.launched_for)))

    def _is_satisfiable(self):
        for node in self.node_list:
            if node.status and node.status[0] == '⊙':
                return True
        return False

    def _next_step(self):  # główna logika MTSa, funkcja rekurencyjna
        node = self.node_list.get_last()

        # ETAP OZNACZANIA LIŚCI (jako liści alpha, beta, gamma, delta, aby móc stosować później reguły wg priorytetów)
        for formula in node.formulas:
            formula.color = None  # zerowanie kolorowania
            if not formula.done:
                formula.mark()

        # ETAP SPRAWDZANIA, CZY NIE NALEŻY DOKONAĆ STOPU
        stop = self._is_done()

        # PRIORYTET ALPHA->BETA->DELTA (wyższy priorytet)
        if not stop:
            self._apply_rule()
            self._next_step()

    def _is_done(self):
        node = self.node_list.get_last()

        stop1 = node.check_for_complementary_literals()
        stop2 = False
        if not stop1:
            stop2 = node.check_if_every_formula_done()
        if stop1 or stop2:
            if len(self.node_list.queue_list) > 0:
                self.node_list.take_node_from_queue()
                self._next_step()
            return True

    def _apply_rule(self):
        node = self.node_list.get_last()

        # ALPHA
        for rule in ['alpha', 'beta', 'delta', 'gamma']:
            for formula in node.formulas:
                if not formula.done and formula.rule_name == rule:
                    formula.color = 'blue'
                    applied = False
                    # ALPHA
                    if formula.rule_name == 'alpha':
                        new_formulas = node.formulas[:]
                        new_formulas.remove(formula)
                        new_formulas = [copy.deepcopy(x) for x in new_formulas]
                        new_formulas.extend([Formula(x) for x in [formula.rule[0].format(formula.first_arg),
                                                                  formula.rule[1].format(formula.second_arg)]])
                        self.node_list.register(Node({
                            'formulas': new_formulas,
                            'domain': node.domain
                        }))
                        applied = True

                    # BETA
                    if formula.rule_name == 'beta':
                        new_formulas_both_branches = node.formulas[:]
                        new_formulas_both_branches.remove(formula)
                        new_formulas_left_branch = [copy.deepcopy(x) for x in new_formulas_both_branches]
                        new_formulas_right_branch = [copy.deepcopy(x) for x in new_formulas_both_branches]
                        new_formulas_left_branch.append(Formula(formula.rule[0].format(formula.first_arg)))
                        new_formulas_right_branch.append(Formula(formula.rule[1].format(formula.second_arg)))
                        self.node_list.register(Node({
                            'formulas': new_formulas_left_branch,
                            'domain': node.domain
                        }))
                        self.node_list.register_in_queue(Node({
                            'formulas': new_formulas_right_branch,
                            'domain': node.domain
                        }))
                        applied = True

                    # DELTA
                    if formula.rule_name == 'delta':
                        new_domain = Domain(set(node.domain))
                        new_letter = new_domain.extend_by_new_const()
                        formula.second_arg = formula.second_arg.replace(formula.first_arg, new_letter)
                        new_formulas = node.formulas[:]
                        new_formulas.remove(formula)
                        new_formulas = [copy.deepcopy(x) for x in new_formulas]
                        new_formulas.append(Formula(formula.rule[0].format(formula.second_arg)))
                        self.node_list.register(Node({
                            'formulas': new_formulas,
                            'domain': new_domain
                        }))
                        applied = True

                    # GAMMA (niższy priorytet)
                    if formula.rule_name == 'gamma':  # gamma jako jedyna nie ma własności .done (celowo)
                        if len(set(node.domain) - set(formula.launched_for)) > 0:
                            new_formulas = node.formulas[:]
                            i = new_formulas.index(formula)
                            new_formulas = [copy.deepcopy(x) for x in new_formulas]
                            new_formulas[i].launched_for = node.domain
                            for const in sorted(set(node.domain) - set(formula.launched_for)):
                                new_formula = Formula(
                                    formula.rule[0].format(formula.second_arg.replace(formula.first_arg, const)))
                                new_formulas.insert(i + 1, new_formula)
                                i += 1

                            self.node_list.register(Node({
                                'formulas': new_formulas,
                                'domain': node.domain
                            }))
                            applied = True

                    if applied:
                        node.performed_rule = rule
                        return
