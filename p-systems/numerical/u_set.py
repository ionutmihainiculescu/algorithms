from algorithms.learning.algorithm import LearningAutomata
from utils.compute import Compute


def compute_u_set(alphabet, language):

    maximumLength = max(list(map(lambda a: len(a), language)))
    print(maximumLength)

    learningAutomata = LearningAutomata(alphabet, language, maximumLength, debug=True)

    learningAutomata.compute()
    Q, F, table = learningAutomata.buildAutomaton()

    s_set = learningAutomata.s_set
    w_set = learningAutomata.w_set

    observation_table = learningAutomata.get_table(s_set, w_set)

    new_s_set = Compute.compute_s_set(s_set, observation_table)

    observation_table_new_s_set = learningAutomata.get_table(new_s_set, w_set)

    new_w_set = Compute.compute_w_set(w_set, observation_table_new_s_set)

    u_set = Compute.compute_u_set_with_letters(s_set=new_s_set, alphabet=alphabet, w_set=new_w_set)

    u_set = list(filter(lambda a: len(a) <= maximumLength, u_set))

    u_set_sort = sorted(u_set, key=lambda a: (len(a), a))
    u_set_sort.remove('')

    return u_set_sort


