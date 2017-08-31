# DSGE: Dynamic Structured Grammatical Evolution

Structured Grammatical Evolution (SGE) is a recent Grammatical Evolution (GE) variant that aims at addressing some of its locality and redundancy issues. The SGE distinctive feature is having a one-to-one correspondence between genes and non-terminals of the grammar being used. If you use this code, a reference to the following work would be greatly appreciated:

```
@article{Lourenco2016,
 title={Unveiling the properties of structured grammatical evolution},
  author={Louren{\c{c}}o, Nuno and Pereira, Francisco B and Costa, Ernesto},
  journal={Genetic Programming and Evolvable Machines},
  volume={17},
  number={3},
  pages={251--289},
  year={2016},
  publisher={Springer}
}
```

This project corresponds to a new implementation of the SGE engine. SGE has been criticised for the fact that we need to specify the maximum levels of recursion in order to remove it from the grammar beforehand. In this new version we specify the maximum tree depth (similarly to what happens in standard tree-based GP), and the algorithm adds the mapping numbers as required during the evolutionary search. Thus, we do not need to pre-process the grammar to remove the recursive productions. Additionally, we provide mechanisms and operators to ensure that the generated trees are always within the allowed limits.


As in for the SGE frameowork we provide the implementations of some problems that we used to test the DSGE. Extending it to your own needs should be fairly easy. 


When running the framework a folder called *dumps* will be created together with an additional one that corresponds to the experience. Inside, there will be directories for each run. Each run folder contains snapshots of the population at a given generation, and a file called *progress_report.csv*,  which is assembled by the end of the evolutionary run. By default we take snapshots of the population at the following generations: 0,25 and 50. This can be changed, together with all the numeric values in the *configs* folder.

### Requirements
Currently this codebase only works with python 2. 

### Instalation

To run the default examples, you should be inside the *src* directory and then type:

`python -m examples.[problem_name] [run]`

If you use the PyCharm IDE you can use it to open the *src* folder, and them, for the run configurations do the following:

![](https://www.dropbox.com/s/prz16aajb8md2es/Screen%20Shot%202017-04-27%20at%2010.02.09.png?dl=1)

##### Additional info
Grant Dick implemented SGE in C, as a module of his framework: [libgges: Grammar-Guided Evolutionary Search ](https://github.com/grantdick/libgges#libgges-grammar-guided-evolutionary-search)

If you prefer C instead of python, please refer to his work.

### Support

Any questions, comments or suggestion should be directed to Nuno Lourenço ([naml@dei.uc.pt](mailto:naml@dei.uc.pt))

### Acknowledgments

I am gratefull to my advisors Francisco B. Pereira and Ernesto Costa for their guidance during my PhD. I am also gratefull to Filipe Assunção and Joaquim Ferrer for their help and comments on the development of this framework. 

### Works using or referencing SGE

Nicolau, Miguel. "Understanding grammatical evolution: initialisation." Genetic Programming and Evolvable Machines: 1-41.

Medvet, Eric, Fabio Daolio, and Danny Tagliapietra. "Evolvability in Grammatical Evolution." Proceedings of the Genetic and Evolutionary Computation Conference, GECCO. 2017.

Medvet, Eric, and Tea Tušar. "The DU Map: A Visualization to Gain Insights into Genotype-Phenotype Mapping and Diversity." (2017).

Assunçao, F., Lourenço, N., Machado, P., & Ribeiro, B. (2017). Towards the Evolution of Multi-Layered Neural Networks: A Dynamic Structured Grammatical Evolution Approach.

Assunçao, F., Lourenço, N., Machado, P., & Ribeiro, B. (2017). Automatic Generation of Neural Networks with Structured Grammatical Evolution. In 2017 IEEE Congress on Evolutionary Computation (CEC). IEEE.

Lourenço, N., Ferrer, J., Pereira, F. B., & Costa, E. (2017, April). A Comparative Study of Different Grammar-Based Genetic Programming Approaches. In European Conference on Genetic Programming (pp. 311-325). Springer, Cham.

Medvet, E., Bartoli, A., & Talamini, J. (2017, April). Road Traffic Rules Synthesis Using Grammatical Evolution. In European Conference on the Applications of Evolutionary Computation (pp. 173-188). Springer, Cham.

Medvet, E. (2017, April). A Comparative Analysis of Dynamic Locality and Redundancy in Grammatical Evolution. In European Conference on Genetic Programming (pp. 326-342). Springer, Cham.

Lourenço, N., Pereira, F. B., & Costa, E. (2015, October). SGE: a structured representation for grammatical evolution. In International Conference on Artificial Evolution (Evolution Artificielle) (pp. 136-148). Springer International Publishing.