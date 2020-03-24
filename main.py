from MTS import MTS

# handle input and put it into input_lines
input_lines = []
while True:
    try:
        raw_input = input()
        if raw_input.strip() != '' and raw_input[0] != '#':  # komentowanie linii inputu - linie rozpoczynające się od # nie są brane pod uwagę
            input_lines.append(raw_input.strip(' #'))
    except EOFError:
        break

horizontal_line = '─' * 90
print(horizontal_line)
for line in input_lines:
    inp_formula = MTS(line)
    # print(normalize(rpn_to_infix(line)))  # printuje formułę wejściową w notacji nawiasowej
    inp_formula.solve()  # aplikuje Metodę Tablic Semantycznych i printuje drzewko wywodu
    print(horizontal_line)
