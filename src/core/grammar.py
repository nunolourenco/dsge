from utilities import OrderedSet
import re, copy, itertools
import pdb
import random

class Grammar:
    """Class that represents a grammar. It works with the prefix notation."""
    NT = "NT"
    T = "T"
    def __init__(self, grammar_path = None, init_depth=6, max_depth = 17):
        if grammar_path == None:
            raise Exception("Grammar file not detected!!")
        else:
            self.grammar_file = grammar_path
        self.needs_python_filter = not ("mux11_grammar" in self.grammar_file or "5_bit_parity_grammar" in self.grammar_file)
        self.grammar = {}
        self.productions_labels = {}
        self.non_terminals, self.terminals = set(), set()
        self.ordered_non_terminals = OrderedSet()
        self.start_rule = None
        self.max_depth = max_depth
        self.max_init_depth = init_depth
        self.read_grammar()
        self.non_recursive_options = {}
        self.compute_non_recursive_options()


    def read_grammar(self):
        """
        Reads a Grammar in the BNF format and converts it to a python dictionary
        This method was adapted from PonyGE version 0.1.3 by Erik Hemberg and James McDermott
        """
        nt_pattern = "(<.+?>)"
        rule_separator = "::="
        production_separator = "|"
        f = open(self.grammar_file, "r")
        for line in f:
            if not line.startswith("#") and line.strip() != "":
                if line.find(rule_separator):
                    left_side, productions = line.split(rule_separator)
                    left_side = left_side.strip()
                    if not re.search(nt_pattern, left_side):
                        raise ValueError("left side not a non-terminal!")
                    self.non_terminals.add(left_side)
                    self.ordered_non_terminals.add(left_side)
                    if self.start_rule == None:
                        self.start_rule = (left_side, self.NT)
                    temp_productions = []
                    for production in [production.strip() for production in productions.split(production_separator)]:
                        temp_production = []
                        if not re.search(nt_pattern, production):
                            if production == "None":
                                production = ""
                            self.terminals.add(production)
                            temp_production.append((production, self.T))
                        else:
                            for value in re.findall("<.+?>|[^<>]*", production):
                                if value != "":
                                    if re.search(nt_pattern, value) == None:
                                        sym = (value, self.T)
                                        self.terminals.add(value)
                                    else:
                                        sym = (value, self.NT)
                                    temp_production.append(sym)
                        temp_productions.append(temp_production)
                    if left_side not in self.grammar:
                        self.grammar[left_side] = temp_productions
        f.close()


    def derivation_tree(self, mapping_rules):
        return self.new_build_tree(self.start_rule, [0], [0], mapping_rules, [0] * len(mapping_rules), 0)

    def new_build_tree(self, current_sym, wraps, count, mapping_rules, mapping_values, len_choices):
        if current_sym[1] == self.T:
            return current_sym
        current_sym_pos = self.ordered_non_terminals.index(current_sym[0])
        choices = self.grammar[current_sym[0]]
        #print mapping_rules[count][current_reference]
        #print mapping_rules[count][0][mapping_rules[count][current_reference]]
        #print mapping_rules[current_sym_pos][0]
        current_production = mapping_rules[current_sym_pos][0][mapping_values[current_sym_pos]]
        #print current_production
        mapping_values[current_sym_pos] += 1
        final = []
        for i in choices[current_production]:
            temp = self.new_build_tree(i, wraps, count, mapping_rules, mapping_values, len(choices))
            if temp == None:
                return None
            final.append(temp)
        #print final
        return (current_sym[0], final)


    def compute_non_recursive_options(self):
        self.non_recursive_options = {}
        for nt in self.ordered_non_terminals:
            choices = []
            for nrp in self.list_non_recursive_productions(nt):
                choices.append(self.grammar[nt].index(nrp))
            self.non_recursive_options[nt] = choices

    def recursive_individual_creation(self, genome, symbol, size_of_gene, current_depth):
        if current_depth > self.max_init_depth:
            possibilities = []
            for index, option in enumerate(self.grammar[symbol]):
                #print symbol
                #print index
                #print option
                #raw_input()
                for s in option:
                    if s[0] == symbol:
                        break
                else:
                    possibilities.append(index)
            expansion_possibility = random.choice(possibilities)
        else:
            expansion_possibility = random.randint(0, size_of_gene[symbol] - 1)

        genome[self.get_non_terminals().index(symbol)].append(expansion_possibility)
        expansion_symbols = self.grammar[symbol][expansion_possibility]
        depths = [current_depth]
        for sym in expansion_symbols:
            if sym[1] != self.T:
                depths.append(self.recursive_individual_creation(genome, sym[0], size_of_gene, current_depth + 1))
        #print depths
        return max(depths)

    def get_non_terminals(self):
        return self.ordered_non_terminals

    def list_non_recursive_productions(self, nt):
        non_recursive_elements = []
        for options in self.grammar[nt]:
            for option in options:
                if option[1] == self.NT and option[0] == nt:
                    break
            else:
                non_recursive_elements += [options]
        return non_recursive_elements


    def mapping(self, mapping_rules, positions_to_map):
        output = []
        max_depth = self.recursive_mapping(mapping_rules, positions_to_map, self.start_rule, 0, output)
        output = "".join(output)
        if self.needs_python_filter:
            output = self.python_filter(output)
        return output, max_depth

    def recursive_mapping(self, mapping_rules, positions_to_map, current_sym, current_depth, output):
        depths = [current_depth]
        if current_sym[1] == self.T:
            output.append(current_sym[0])
        else:
            current_sym_pos = self.ordered_non_terminals.index(current_sym[0])
            choices = self.grammar[current_sym[0]]
            size_of_gene = self.count_number_of_options_in_production()
            if positions_to_map[current_sym_pos] >= len(mapping_rules[current_sym_pos]):
                if current_depth > self.max_depth:
                    #print "True"
                    possibilities = []
                    for index, option in enumerate(self.grammar[current_sym[0]]):
                        for s in option:
                            if s[0] == current_sym[0]:
                                break
                        else:
                            possibilities.append(index)
                    expansion_possibility = random.choice(possibilities)
                else:
                    expansion_possibility = random.randint(0, size_of_gene[current_sym[0]] - 1)
                mapping_rules[current_sym_pos].append(expansion_possibility)
            current_production = mapping_rules[current_sym_pos][positions_to_map[current_sym_pos]]
            positions_to_map[current_sym_pos] += 1
            next_to_expand = choices[current_production]
            for next_sym in next_to_expand:
                depths.append(self.recursive_mapping(mapping_rules, positions_to_map, next_sym, current_depth + 1, output))
        return max(depths)



    def count_number_of_non_terminals(self):
        return len(self.ordered_non_terminals)

    def count_number_of_options_in_production(self):
        number_of_options_by_non_terminal = {}
        g = self.grammar
        for nt in self.ordered_non_terminals:
            number_of_options_by_non_terminal.setdefault(nt, len(g[nt]))
        return number_of_options_by_non_terminal


    def python_filter(self, txt):
        """ Create correct python syntax.
        We use {: and :} as special open and close brackets, because
        it's not possible to specify indentation correctly in a BNF
        grammar without this type of scheme."""
        txt = txt.replace("\le", "<=")
        txt = txt.replace("\ge", ">=")
        txt = txt.replace("\l", "<")
        txt = txt.replace("\g", ">")
        txt = txt.replace("\eb", "|")
        indent_level = 0
        tmp = txt[:]
        i = 0
        while i < len(tmp):
            tok = tmp[i:i+2]
            if tok == "{:":
                indent_level += 1
            elif tok == ":}":
                indent_level -= 1
            tabstr = "\n" + "  " * indent_level
            if tok == "{:" or tok == ":}" or tok == "\\n":
                tmp = tmp.replace(tok, tabstr, 1)
            i += 1
            # Strip superfluous blank lines.
            txt = "\n".join([line for line in tmp.split("\n") if line.strip() != ""])
        return txt

    def __str__(self):
        grammar = self.grammar
        #print self.grammar
        #print self.count_references_to_non_terminals()
        text = ""
        for key in self.ordered_non_terminals:
            text += key + " ::= "
            for options in grammar[key]:
                for option in options:
                    text += option[0]
                if options != grammar[key][-1]:
                    text += " | "
            text += "\n"
        return text


if __name__ == "__main__":
    random.seed(42)
    g = Grammar("grammars/regression.txt",9)
    genome = [[[0]], [[2]], [[]], [[]], [[1]]]
    mapping_numbers = [0] * len(genome)
    #print g.mapping(genome, mapping_numbers)
    print g.old_mapping(genome, mapping_numbers)