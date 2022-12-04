from itertools import combinations
from functools import cmp_to_key

def read_input_from_file(path): #Đọc file từ đường dẫn
    file = open(path, "r")
    alpha = set(file.readline().strip().split(' OR '))
    n = int(file.readline())  # Số mệnh đề có trong KB
    KB = set()
    for i in range(n):
        KB.add(frozenset(file.readline().strip().split(' OR ')))
    file.close()
    return KB, alpha

def PL_RESOLUTION(KB, alpha):
    clauses = KB.union(negation_of_clause(alpha))
    new = set()
    empty_clause = frozenset()
    result = []
    entail = True
    while True:
        list_pair_of_clauses = combinations(clauses, 2)  # Sinh ra tất cả các cặp clause
        for (clause1, clause2) in list(list_pair_of_clauses):
            resolvents = PL_RESOLVE(clause1, clause2)
            new = new.union(resolvents)
        new_clauses = new.difference(clauses)
        result.append(new_clauses)
        if len(new_clauses) == 0:  # Không phát sinh mệnh đề mới
            entail = False
            return result, entail
        if empty_clause in new_clauses:  # Có mệnh đề rỗng
            return result, entail
        clauses.update(new)

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
                resolvents.add(frozenset(resolvent))
    return resolvents

def check_tautological_clause(clause):  # Kiêm tra một clause luôn có giá trị True hay không
    for literal in clause:
        if complementary_literal(literal) in clause:
            return True
    return False

def negation_of_clause(clause): # Dùng để phủ định mệnh đề alpha
    result = set()
    for literal in clause:
        negation_of_literal = complementary_literal(literal)
        new_clause = set()
        new_clause.add(negation_of_literal)
        result.add(frozenset(new_clause))
    return result

def complementary_literal(literal: str): #Trả về literal đối ngẫu
    if literal[0] == '-':
        return literal[1:]
    else:
        return str('-' + literal)


def export_output_to_file(path, result, entail): #Xuất output
    file = open(path, "w")
    for set_of_clauses in result:
        file.write(str(len(set_of_clauses)) + "\n")
        for clause in set_of_clauses:
            clause=sorted(clause,key=cmp_to_key(compare)) #Sort lại các literal cho đúng định dạng
            if len(clause) == 0:
                file.write('{}' + "\n") #Clause rỗng
            else:
                file.write(' OR '.join(clause) + "\n")
    if entail == True:
        file.write('YES')
    else:
        file.write('NO')
    file.close()

def compare(literal_1, literal_2):  # So sánh thứ tự 2 literal khi sort
    if len(literal_1) == len(literal_2) and len(literal_1) == 1:
        return compare_string(literal_1, literal_2)
    elif len(literal_1) == len(literal_2):
        return compare_string(literal_1[1:], literal_2[1:])
    elif len(literal_1) == 2:
        return compare_string(literal_1[1:], literal_2)
    else:
        return compare_string(literal_1[0], literal_2[1:])

def compare_string(string_1, string_2):  # So sánh 2 string
    if string_1 < string_2:
        return -1
    elif string_1 > string_2:
        return 1
    return 0