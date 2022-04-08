from typing import List
from random import choice


def pars_file(path):
    with open(path) as f:
        all_cnf = f.read()

    cnf = all_cnf.split("\n")

    for i in range(len(cnf)):
        if cnf[i][-1] == "0":
            cnf[i] = list(map(int, cnf[i][:-1].split()))
        else:
            cnf[i] = list(map(int, cnf[i][:].split()))
    return cnf


class Cnf:
    def __init__(self, cnf_: List[List[int]], solve=None):
        if solve is None:
            solve = []
        self.solve = solve
        self.cluster_list = cnf_

    def __str__(self):
        return self.cluster_list.__str__()

    def get_uniq_literals(self):
        return set([literal for cluster in self.cluster_list for literal in cluster])

    def bad_solve(self) -> bool:
        return self.cluster_list.count([]) > 0

    def solve_ready(self) -> bool:
        return self.cluster_list == []

    def pure_literal_assign(self):
        literals_to_check = self.get_uniq_literals()
        while len(literals_to_check) != 0:
            literal = literals_to_check.pop()
            if -literal not in literals_to_check:  # означает, что перед нами "чистый" литерал
                self.solve.append(literal)
                self.cluster_list = list(filter(lambda cluster: literal not in cluster, self.cluster_list))
                literals_to_check = self.get_uniq_literals()
            else:
                literals_to_check.remove(-literal)

    def unit_propagate(self):
        i = 0
        while i < len(self.cluster_list):
            if len(self.cluster_list[i]) == 1:
                literal = self.cluster_list[i][0]
                self.solve.append(literal)
                # удаляем все кластера где есть литерал из единичного клоза
                self.cluster_list = self.use_new_literal(literal)
                i = 0
            else:
                i += 1

    def use_new_literal(self, literal) -> List[List[int]]:
        new_cnf = list(filter(lambda cluster: literal not in cluster, self.cluster_list))
        new_cnf = list(map(
            lambda cluster: list(filter(lambda lit: lit != -literal, cluster)), new_cnf
        ))
        return new_cnf

    def next_cnf(self):
        literal = choice(choice(self.cluster_list))
        return Cnf(self.use_new_literal(literal), self.solve + [literal]), \
               Cnf(self.use_new_literal(-literal), self.solve + [-literal])

    def get_solution(self):
        if self.solve_ready(): return sorted(self.solve, key=abs)
        if self.bad_solve(): return []

        self.pure_literal_assign()
        self.unit_propagate()

        if self.solve_ready(): return sorted(self.solve, key=abs)
        if self.bad_solve(): return []

        cnf1, cnf2 = self.next_cnf()

        return sorted(cnf1.get_solution() or cnf2.get_solution(), key=abs)
