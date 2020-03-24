from collections import deque
from .notation import notation, operators


def rpn_to_infix(s):  # bez nawiasowania
    formula = deque(s.split())
    stack = deque()
    for term in formula:
        predicate = term.split('/')
        if term in operators:
            last = stack.pop()
            if term in notation['operator']['not']:
                stack.append('({} {})'.format(term, last)) # 'not arg' last powinien zawierać informację o
            else:
                second_last = stack.pop()
                if term in notation['operator']['forall'] or term in notation['operator']['exists']:
                    stack.append('({} {} {})'.format(term, second_last, last)) # 'forall arg_letter rest'
                else:
                    stack.append('({} {} {})'.format(second_last, term, last)) # '\1 spójnik \2'
        elif len(predicate) == 2:
            predicate_name = predicate[0]
            args_count = int(predicate[1])
            args = deque()
            for i in range(args_count):
                args.appendleft(stack.pop())
            stack.append('({}({}))'.format(predicate_name, ', '.join(args)))
        else:
            stack.append(term)
    return stack[0]


# normalizuje całą formułę
# przykładowo zamieni 'NOT', '~' lub '¬' na '¬' (wg notacji, 'not': ['NOT', '~', '¬'])
def normalize(formula):
    for operator_group in notation['operator'].values():
        for operator in operator_group[:-1]:
            formula = formula.replace(operator, operator_group[-1])
    return formula