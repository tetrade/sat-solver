from typing import List
from collections import Counter


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
        self.clause_list = cnf_
        self.is_bad_solve = False
        if uniq_literals is None:
            uniq_literals = self.get_uniq_literals()
        self.uniq_literals = uniq_literals

    def get_uniq_literals(self):
        return Counter(literal for clause in self.clause_list for literal in clause)

    def solve_ready(self) -> bool:
        return self.clause_list == []

    def pure_literal_assign(self):
        literals_to_check = iter(tuple(self.uniq_literals.keys()))
        literal = next(literals_to_check, None)
        while literal is not None:
            if self.uniq_literals[-literal] == 0:  # означает, что перед нами "чистый" литерал
                self.solve.append(literal)
                self.clause_list = self.use_new_literal(literal)
            literal = next(literals_to_check, None)

    def unit_propagate(self):
        i = 0
        while i < len(self.clause_list):
            le = len(self.clause_list[i])
            if le == 1:
                literal = self.clause_list[i][0]
                self.solve.append(literal)
                # удаляем все кластера где есть литерал из единичного клоза
                self.clause_list = self.use_new_literal(literal)
                i = 0
            elif le == 0:
                self.is_bad_solve = True
                break
            else:
                i += 1

    def use_new_literal(self, literal, new=False):
        uniqs = self.uniq_literals.copy() if new else self.uniq_literals
        new_cnf = []
        i = 0
        while i < len(self.clause_list):
            if uniqs[literal] == 0 and uniqs[-literal] == 0:
                new_cnf.extend(self.clause_list[i:])
                break
            else:
                bad_clause = False
                new_clause = []
                for lit in self.clause_list[i]:
                    if lit == literal:
                        bad_clause = True
                        for lit_ in self.clause_list[i]:
                            uniqs[lit_] -= 1
                        break
                    elif lit == -literal:
                        uniqs[lit] -= 1
                    else:
                        new_clause.append(lit)
                if not bad_clause:
                    new_cnf.append(new_clause)
            i += 1

        uniqs += Counter()
        if new:
            return new_cnf, uniqs
        else:
            return new_cnf

    def next_cnf(self):
        literal = self.uniq_literals.most_common(1)[0][0]
        cnf1, uniqs1 = self.use_new_literal(literal, new=True)
        cnf2 = self.use_new_literal(-literal)
        return Cnf(cnf1, self.solve + [literal], uniqs1), \
               Cnf(cnf2, self.solve + [-literal], self.uniq_literals)

    def get_solution(self):

        self.pure_literal_assign()
        self.unit_propagate()

        if self.is_bad_solve: return []
        if self.solve_ready(): return sorted(self.solve, key=abs)

        cnf1, cnf2 = self.next_cnf()

        return cnf1.get_solution() or cnf2.get_solution()