notation = {
    'constant': 'abcde',
    'variable': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'function': 'fghijklmn',
    'predicate': 'pqrstuvwxyz',
    'operator': {
        'forall': ['FORALL', '∀'],
        'exists': ['EXISTS', '∃'],
        'not': ['NOT', '~', '¬'],
        'and': ['AND', '&', '∧'],
        'or': ['OR', '|', '∨'],
        'imp': ['IMPLIES', '→'],
        'xnor': ['IFF', '↔'],
        'xor': ['XOR', '⊕']
    }
}

operators = [item for sublist in notation['operator'].values() for item in sublist]
