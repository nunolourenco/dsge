import re
import random
from math import sin, cos, tan
from core.protectedmath import _log_, _div_, _exp_, _inv_, _sqrt_, protdiv

dataset_path = 'resources/housing.txt'
folds_path = 'resources/housing.folds'

class BostonHousing():

    def __init__(self, run):
        """
        VERY IMPORTANT:
        The run can go from 1 to 30
        """
        self.__train_set = []
        self.__test_set = []
        self.__invalid_fitness = 9999999
        self.__run = run
        self.read_dataset();

        self.test_set_size = len(self.__test_set)
        self.__RRSE_train_denominator = 0
        self.__RRSE_test_denominator = 0
        self.calculate_RRSE_denominators()

    def calculate_RRSE_denominators(self):
        self.__RRSE_train_denominator = 0
        self.__RRSE_test_denominator = 0

        train_outputs = [entry[-1] for entry in self.__train_set]
        test_outputs = [entry[-1] for entry in self.__test_set]

        train_output_mean = float(sum(train_outputs)) / len(train_outputs)
        test_output_mean = float(sum(test_outputs)) / len(test_outputs)
        self.__RRSE_train_denominator = sum([(i - train_output_mean)**2 for i in train_outputs])
        self.__RRSE_test_denominator = sum([(i - test_output_mean)**2 for i in test_outputs])

    def read_dataset(self):
        dataset = []
        training_indexes = []
        test_indexes = []
        with open(dataset_path, 'r') as dataset_file:
            for line in dataset_file:
                dataset.append([float(value.strip(" ")) for value in line.split(" ") if value != ""])
        with open(folds_path, 'r') as folds_file:
            for i in range(self.__run - 1): folds_file.readline()
            test_indexes = folds_file.readline()
            test_indexes = [int(value.strip(" ")) - 1 for value in test_indexes.split(" ") if value != ""]
            training_indexes = filter(lambda x: x not in test_indexes, range(len(dataset))) #Not the most efficient way
        self.__train_set = [dataset[i] for i in training_indexes]
        self.__test_set = [dataset[i] for i in test_indexes]


    def get_error(self, individual, dataset):
        pred_error = 0
        for fit_case in dataset:
            case_output = fit_case[-1]
            try:
                result = eval(individual, globals(), {"x": fit_case[:-1]})
                pred_error += (case_output - result)**2
            except (OverflowError, ValueError) as e:
                return self.__invalid_fitness
        return pred_error

    def evaluate(self, individual):
        if individual == None:
            return None
        error = self.get_error(individual, self.__train_set)
        error = _sqrt_( error /self.__RRSE_train_denominator);
        test_error = self.get_error(individual, self.__test_set)
        test_error = _sqrt_( test_error / float(self.__RRSE_test_denominator))
        return (error,{'generation':0, "evals" : 1, "test_error" : test_error})

    def __str__(self):
        descr = "len(train):%d len(test):%d\n\n"%(len(self.__train_set), len(self.__test_set))
        descr += "Training_set:\n"
        for i in self.__train_set[0:5]: descr += str(i) + "\n"
        descr += "Test_set:\n"
        for i in self.__test_set[0:5]: descr += str(i) + "\n"
        return descr


if __name__ == "__main__":
    import core.grammar as grammar
    import core.sge
    from configs.standard import RUN
    experience_name = "BostonHousing/"
    grammar = grammar.Grammar("grammars/boston_housing_grammar.txt", 6, 17)
    evaluation_function = BostonHousing(RUN) 
    core.sge.evolutionary_algorithm(grammar = grammar, eval_func=evaluation_function, exp_name=experience_name)
