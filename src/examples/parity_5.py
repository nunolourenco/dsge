"""
Lots of code taken from deap
"""
input_names = ['b0', 'b1', 'b2', 'b3', 'b4']

PARITY_FANIN_M = 5
PARITY_SIZE_M = 2**PARITY_FANIN_M

inputs = [None] * PARITY_SIZE_M
outputs = [None] * PARITY_SIZE_M

for i in range(PARITY_SIZE_M):
    inputs[i] = [None] * PARITY_FANIN_M
    value = i
    dividor = PARITY_SIZE_M
    parity = 1
    for j in range(PARITY_FANIN_M):
        dividor /= 2
        if value >= dividor:
            inputs[i][j] = 1
            parity = int(not parity)
            value -= dividor
        else:
            inputs[i][j] = 0
    outputs[i] = parity

class Parity5():
    def evaluate(self, individual):
        error = PARITY_SIZE_M
        for i, inpt in enumerate(inputs):
            res = eval(individual, dict(zip(input_names, inpt)))
            if res == outputs[i]:
                error -= 1
        return (error, {})

if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    experience_name = "5Parity/"
    grammar = grammar.Grammar("grammars/5_bit_parity_grammar.txt", 6, 17)
    evaluation_function = Parity5() 
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)