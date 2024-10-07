import graphviz
from graphviz import Digraph

nd_table = {}
d_table = {}
unused_st = []
used_st = set()
alphabet = set()

def make_state(v):
    name = ''.join(v)
    for i in alphabet:
        for j in v:
            tmp_pair = (j, i)
            if tmp_pair in nd_table:
                tmp_vec = nd_table[tmp_pair]
                nd_table[(name, i)] = nd_table[(name, i)].union(tmp_vec) if (name, i) in nd_table else tmp_vec
    return name

def print_table(table):
    for k, v in table.items():
        print(f"{k[0]},{k[1]}={v}")

def determ():
    alph_size = len(alphabet)
    while unused_st:
        Qcur = unused_st.pop(0)
        for i in alphabet:
            tmp_pair = (Qcur, i)
            if tmp_pair not in nd_table:
                continue
            tmp_vec = nd_table[tmp_pair]
            state = make_state(tmp_vec)
            if state not in used_st:
                unused_st.append(state)
            d_table[tmp_pair] = state
            used_st.add(Qcur)

def parse_automate(file_name):
    with open(file_name, 'r') as file:
        for str in file:
            str = str.strip()
            if '=' not in str:
                print(f"Skipping invalid line: {str}")
                continue
            q, rest = str.split(',', 1)
            c, f = rest.split('=')
            unused_st.append(q)
            alphabet.add(c)
            nd_table.setdefault((q, c), set()).add(f)
    is_determ = all(len(v) <= 2 for v in nd_table.values())
    if is_determ:
        for k, v in nd_table.items():
            d_table[k] = next(iter(v))
    else:
        determ()
        print_table(d_table)

def parse_str(str):
    Qcur = "q0"
    for i in str:
        tmp_pair = (Qcur, i)
        if tmp_pair not in d_table:
            return -1
        Qcur = d_table[tmp_pair]
        if 'f' in Qcur and i == str[-1]:
            return 0
        elif 'f' not in Qcur and i == str[-1]:
            return -1
    return -1

def parsing_loop():
    while True:
        str = input()
        ret = parse_str(str)
        print("Valid string" if ret == 0 else "Not a valid string")

def visualize_graph():
    dot = Digraph()
    for k, v in d_table.items():
        dot.edge(k[0], v, label=k[1])
    dot.render('graph.gv', view=True)

if __name__ == "__main__":
    parse_automate("transitions.txt")
    visualize_graph()
    parsing_loop()