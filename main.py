from itertools import combinations


def read_input_from_file(path):
    file = open(path, "r")
    alpha = set(file.readline()[:-1].split(' OR '))
    n = int(file.readline())  # Số mệnh đề có trong KB
    KB = set()
    for i in range(n):
        KB.add(set(file.readline()[:-1].split(' OR ')))
    file.close()
    return KB, alpha


def check_tautological_clause(clause):  # Kiêm tra một clause luôn có giá trị True hay không
    for literal in clause:
        if complementary_literal(literal) in clause:
            return True
    return False


def PL_RESOLVE(clause1, clause2):
    resolvents = set()
    for literal1 in clause1:
        resolvent = set()
        if complementary_literal(literal1) in clause2:
            # Tiến hành thêm tất cả literal từ 2 clause mà khác 2 literal đối ngẫu nhau
            for literal_1 in clause1:
                if literal_1 != literal1:
                    resolvent.add(literal_1)
            for literal_2 in clause2:
                if literal_2 != complementary_literal(literal1):
                    resolvent.add(literal_2)
            if check_tautological_clause(resolvent) == False:  # Chỉ xét các clause không là một tautology
                resolvents.add(resolvent)
    return resolvents

def compare(literal_1,literal_2): #So sánh thứ tự 2 literal khi sort
    if len(literal_1)==len(literal_2):
        return literal_1[0]-literal_2[0]
    elif len(literal_1)==2:
        return literal_1[1]-literal_2[0]
    else:
        return literal_1[0]-literal_2[1]
def PL_RESOLUTION(KB, alpha):
    clauses = KB.union(negation_of_clause(alpha))
    new = set()
    empty_clause = set()
    result = []
    entail = True
    while True:
        list_pair_of_clauses = combinations(clauses, 2)  # Sinh ra tất cả các cặp clause
        for (clause1, clause2) in list(list_pair_of_clauses):
            resolvents = PL_RESOLVE(clause1, clause2)
            new = new.union(resolvents)
        new_clauses = new.intersection(clauses)
        result.append(new_clauses)
        if len(new_clauses) == 0:  # Không phát sinh mệnh đề mới
            entail = False
            return result, entail
        if empty_clause in new_clauses:  # Có mệnh đề rỗng
            return result, entail
        clauses.update(new)

def output_set_of_clauses(set_of_clauses):
    for clauses in set_of_clauses:

def negation_of_clause(clause):
    result = set()
    for literal in clause:
        result.add(complementary_literal(literal))
    return result


def complementary_literal(literal): #
    if literal[0] == '-':
        return literal[1:]
    else:
        return '-' + literal
