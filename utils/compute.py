from functools import reduce


class Compute:

    @staticmethod
    def compute_u_set_with_letters(s_set, alphabet, w_set):

        compute_alphabet = [''] + alphabet

        u_set = []

        for s in s_set:
            for a in compute_alphabet:
                for w in w_set:
                    ss = s + a + w
                    if not ss in u_set:
                        u_set.append(ss)
        return u_set

    @staticmethod
    def compare_two_lists(r1, r2):
        z = list(zip(r1, r2))
        m = list(map(lambda a: a[0] == a[1] if a[0] >= 0 and a[1] >= 0 else True, z))
        return reduce(lambda a, b: a and b, m)

    @staticmethod
    def compute_s_set(s_set, table):

        new_s_set = [s_set[0]]
        length = len(s_set)
        row_index = 1
        while row_index < length:
            i = 0
            b = False
            while i < row_index and not b:
                b = Compute.compare_two_lists(table[i], table[row_index])
                i += 1
            if not b:
                new_s_set.append(s_set[row_index])
            row_index += 1

        return new_s_set

    @staticmethod
    def compute_w_set(w_set, table):
        new_w_set = [w_set[0]]
        length = len(w_set)
        col_index = 1
        while col_index < length:
            b = False
            i = 0
            while i < col_index and not b:
                b = Compute.compare_two_lists([r[i] for r in table], [r[col_index] for r in table])
                i += 1
            if not b:
                new_w_set.append(w_set[col_index])
            col_index += 1

        return new_w_set
