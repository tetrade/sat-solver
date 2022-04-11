from typing import List
from random import choice


def pars_file(path):
    with open(path) as f:
        all_cnf = f.read()

    file = all_cnf.split("\n")
    cnf = []

    for i in range(len(file)):
        if file[i][0] == 'c' or file[i][0] == 'p': continue
        if file[i][0] == '%': break
        new_line = file[i].split()
        if new_line[-1] == "0":
            cnf.append(list(map(int, new_line[:-1])))
        else:
            cnf.append(list(map(int, new_line)))
    return cnf


class Cnf:
    def __init__(self, cnf_: List[List[int]], solve=None, uniq_literals=None):
        if solve is None:
            solve = []
        self.solve = solve
        self.cluster_list = cnf_
        self.is_bad_solve = False
        if uniq_literals is None:
            uniq_literals = self.get_uniq_literals()
        self.uniq_literals = uniq_literals

    def get_uniq_literals(self):
        return set([literal for cluster in self.cluster_list for literal in cluster])

    def solve_ready(self) -> bool:
        return self.cluster_list == []

    def pure_literal_assign(self):
        literals_to_check = iter(self.uniq_literals.copy())
        literal = next(literals_to_check, None)
        while literal is not None:
            if -literal not in self.uniq_literals:  # означает, что перед нами "чистый" литерал
                self.solve.append(literal)
                self.uniq_literals.remove(literal)
                self.cluster_list = list(filter(lambda cluster: literal not in cluster, self.cluster_list))
            literal = next(literals_to_check, None)

    def unit_propagate(self):
        i = 0
        while i < len(self.cluster_list):
            le = len(self.cluster_list[i])
            if le == 1:
                literal = self.cluster_list[i][0]
                self.solve.append(literal)
                self.uniq_literals.remove(literal)
                self.cluster_list = self.use_new_literal(
                    literal)  # удаляем все кластера где есть литерал из единичного клоза
                i = 0
            elif le == 0:
                self.is_bad_solve = True
                break
            else:
                i += 1

    def use_new_literal(self, literal) -> List[List[int]]:
        new_cnf = filter(lambda cluster: literal not in cluster, self.cluster_list)
        new_cnf = list(map(
            lambda cluster: list(filter(lambda lit: lit != -literal, cluster)), new_cnf
        ))
        return new_cnf

    def next_cnf(self):
        literal = choice(choice(self.cluster_list))
        return Cnf(self.use_new_literal(literal), self.solve + [literal], self.uniq_literals.copy()), \
               Cnf(self.use_new_literal(-literal), self.solve + [-literal], self.uniq_literals)

    def get_solution(self):

        self.pure_literal_assign()
        self.unit_propagate()

        if self.is_bad_solve: return []
        if self.solve_ready(): return sorted(self.solve, key=abs)

        cnf1, cnf2 = self.next_cnf()

        return sorted(cnf1.get_solution() or cnf2.get_solution(), key=abs)
