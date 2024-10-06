from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self):
        self.transitions = {}
        self.final_states = set()
        self.initial_state = 'q0'

    def add_transition(self, current_state, symbol, next_state):
        if current_state not in self.transitions:
            self.transitions[current_state] = {}
        if symbol in self.transitions[current_state]:
            raise Exception(f"Невозможный переход: {current_state} по символу {symbol} уже определен")
        self.transitions[current_state][symbol] = next_state

    def is_deterministic(self):
        for current_state, symbols in self.transitions.items():
            if len(symbols) != len(set(symbols.keys())):
                return False
        return True

    def __repr__(self):
        representation = []
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                representation.append(f"{state},{symbol}={next_state}")
        return "\n".join(representation)


def read_automaton_from_file(filename):
    fa = FiniteAutomaton()

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split('=')
            left = parts[0].strip()
            right = parts[1].strip()

            current = left.split(',')
            next_state = right.strip()

            qN = current[0]  # q<N>
            C = current[1]   # <C>
            if next_state.startswith('f'):
                fa.final_states.add(next_state[1:])  # добавляем финальное состояние
                next_state = next_state[1:]  # убираем 'f'

            fa.add_transition(qN, C, next_state)

    return fa


def determinize(fa):
    new_fa = FiniteAutomaton()
    unvisited_states = {fa.initial_state}
    new_state_mapping = {fa.initial_state: 'q0'}
    state_counter = 1

    while unvisited_states:
        current_state = unvisited_states.pop()
        for symbol, next_state in fa.transitions.get(current_state, {}).items():
            if next_state not in new_state_mapping:
                new_state_mapping[next_state] = f'q{state_counter}'
                state_counter += 1
                unvisited_states.add(next_state)
            new_fa.add_transition(new_state_mapping[current_state], symbol, new_state_mapping[next_state])

    for original_state, mapped_state in new_state_mapping.items():
        if original_state in fa.final_states:
            new_fa.final_states.add(mapped_state)

    return new_fa


def analyze_string(fa, input_string):
    current_state = fa.initial_state
    for symbol in input_string:
        if current_state not in fa.transitions or symbol not in fa.transitions[current_state]:
            return False  # Перехода нет, строка не принимается
        current_state = fa.transitions[current_state][symbol]

    return current_state in fa.final_states


def visualize_automaton(fa):
    dot = Digraph()

    for state in fa.transitions:
        if state in fa.final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for state in fa.transitions:
        for symbol, next_state in fa.transitions[state].items():
            dot.edge(state, next_state, label=symbol)

    dot.render('automaton', format='png', cleanup=True)


if __name__ == "__main__":
    filename = 'transitions.txt'  # укажите путь к вашему файлу
    input_string = input("Введите строку для анализа: ")

    fa = read_automaton_from_file(filename)

    if fa.is_deterministic():
        print("Автомат детерминирован.")
    else:
        print("Автомат недетерминирован.")

    determinized_fa = determinize(fa)
    print("Детерминизированный автомат:")
    print(determinized_fa)

    if analyze_string(fa, input_string):
        print(f"Строка '{input_string}' принимается автоматом.")
    else:
        print(f"Строка '{input_string}' не принимается автоматом.")

    # Визуализация автомата
    visualize_automaton(fa)
