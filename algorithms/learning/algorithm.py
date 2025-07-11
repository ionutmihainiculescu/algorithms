from functools import reduce

from tabulate import tabulate


class LearningAutomata:

    def __init__(self, alphabet, language, length, debug=False):
        self.__alphabet = alphabet
        self.__language = language
        self.__remaining_language = sorted(self.__language, key=lambda a: (len(a), a))
        self.__length = length
        self.__s_set = ['']
        self.__sa_set = []
        self.__w_set = ['']
        self.__observation_table = dict()
        self.__debug = debug

    @property
    def alphabet(self): return self.__alphabet

    @property
    def s_set(self): return self.__s_set

    @property
    def w_set(self): return self.__w_set

    def get_table(self, s_set, w_set):
        table = []
        for s in s_set:
            t = []
            for w in w_set:
                sw = s + w
                r = 1 if s + w in self.__language else -1 if len(s + w) > self.__length else 0
                t.append(r)
            table.append(t)
        return table

    def computeSA(self):
        self.__sa_set = list(map(lambda a: a, self.__alphabet))

    def buildTable(self):
        self.__w_set = sorted(self.__w_set, key=lambda a: (len(a), a))
        self.__s_set = sorted(self.__s_set, key=lambda a: (len(a), a))
        self.__sa_set = sorted(self.__sa_set, key=lambda a: (len(a), a))
        self.__observation_table = dict()
        for s in self.__s_set + self.__sa_set:
            for w in self.__w_set:
                self.__observation_table[s + w] = 1 if s + w in self.__language else -1 if len(s + w) > self.__length else 0

    def buildAutomaton(self):
        states, statesMap = self.getUniqueStates()
        maps = dict()
        for s in self.__s_set:
            if not s in statesMap:
                maps[s] = list(map(lambda w: self.__observation_table[s + w], self.__w_set))
        for sa in self.__sa_set:
            maps[sa] = list(map(lambda w: self.__observation_table[sa + w], self.__w_set))
        table = []
        for i, qs in enumerate(states):
            row = []
            for a in self.__alphabet:
                if qs + a in statesMap:
                    row.append(statesMap[qs + a][0])
                else:
                    r = maps[qs + a]
                    indexs = 0
                    isFound = False
                    while indexs < len(states) and not isFound:
                        s = states[indexs]
                        rr = statesMap[s][1]
                        isFound = self.computeRows(rr, r)
                        if not isFound:
                            indexs += 1
                    if isFound:
                        row.append(indexs)
            table.append(row)
        F = list(map(lambda a: (a[0], a[1][0]), statesMap.values()))
        F = list(filter(lambda a: a[1] == 1, F))
        F = list(map(lambda a: a[0], F))
        return states, F, table

    def checkWordInAutomaton(self, F, table, word):
        currentState = 0
        for c in word:
            currentState = table[currentState][self.__alphabet.index(c)]
        return currentState in F

    def checkLanguageQuery(self, F, table):
        isFound = True
        s = ''
        while isFound and len(self.__remaining_language) > 0:
                word = self.__remaining_language[0]
                isFound = self.checkWordInAutomaton(F, table, word)
                if isFound:
                    self.__remaining_language.remove(word)
                else:
                    s = word
                    return isFound, s
        return isFound, s

    def checkForCounterexampleInSA(self, F, table):
        indexS1 = 0
        while indexS1 < len(self.__sa_set):
            indexS2 = indexS1 + 1
            while indexS2 < len(self.__sa_set):
                word = self.__sa_set[indexS1] + self.__sa_set[indexS2]
                if not word in self.__language and len(word) <= self.__length:
                    isFound = self.checkWordInAutomaton(F, table, word)
                    if isFound:
                        return True, word
                indexS2 += 1
            indexS1 += 1
        return False, ''

    def getUniqueStates(self):
        Q = []
        for s in self.__s_set:
            rowS = list(map(lambda w: self.__observation_table[s + w], self.__w_set))
            if len(Q) == 0:
                Q.append((s, rowS))
            else:
                isFound = False
                indexq = 0
                while indexq < len(Q) and not isFound:
                    sq = Q[indexq][0]
                    row = list(map(lambda w: self.__observation_table[sq + w], self.__w_set))
                    isFound = self.computeRows(row, rowS)
                    indexq += 1
                if not isFound:
                    Q.append((s, rowS))
        m = dict()
        # Q = list(filter(lambda o:o[0] !='bb', Q))
        for i, q in enumerate(Q):
            m[q[0]] = (i, q[1])
        return list(map(lambda a: a[0], Q)), m

    def computeRows(self, r1, r2):
        z = list(zip(r1, r2))
        m = list(map(lambda a: a[0] == a[1] if a[0] >= 0 and a[1] >= 0 else True, z))
        return reduce(lambda a, b: a and b, m)

    def consistency(self):
        if self.__debug:
            length_w_set = len(self.__w_set)
        for i, w in enumerate(self.__w_set):
            if self.__debug:
                print('\t Consistency \t {} / {}  {}'.format(i, length_w_set, i/length_w_set*100))
            a = self.consistencySearchA(w)
            if a is not None:
                if not a + w in self.__w_set:
                    self.__w_set.append(a + w)
                    self.buildTable()
                    if self.__debug:
                        length_w_set = len(self.__w_set)

    def consistencySearchA(self, w):
        a = None
        c = self.__length - len(w) - 1
        wLength = len(w)
        for is1, s1 in enumerate(self.__s_set):
            if len(s1) <= c and is1 + 1 < len(self.__s_set):
                for s2 in self.__s_set[is1 + 1:]:
                    if len(s2) <= c:
                        for a in self.__alphabet:
                            k = max(len(s1), len(s2)) + wLength + 1
                            # o1 = self.observationTable[s1 + a + w] if s1 + a + w in self.observationTable else 2
                            # o2 = self.observationTable[s2 + a + w] if s2 + a + w in self.observationTable else 3
                            o1 = self.__observation_table[s1 + a + w]
                            o2 = self.__observation_table[s2 + a + w]
                            b2 = o1 != o2
                            if self.checkSimilarity(s1, s2, k) and b2:
                                return a
        return a

    def closedness(self):
        isFound = False
        indexs = 0
        while indexs < len(self.__s_set) and not isFound:
            s = self.__s_set[indexs]
            aa = self.closednessSearchA(s)
            if len(aa) > 0:
                for a in aa:
                    if not s + a in self.__s_set and self.checkIfExistsSimilarityRowInS(s + a) == False:
                        self.addCounterexample(s + a)
                        self.buildTable()
                        isFound = True
                        break
            indexs += 1
            if self.__debug:
                length_s_set = len(self.__s_set)
                print('\t Closedness \t {} / {}  {}'.format(indexs, length_s_set, indexs / length_s_set * 100))
        return isFound

    def closednessSearchA(self, s):
        saList = list(map(lambda a:(a, s + a), self.__alphabet))
        a = []
        for t in self.__s_set:
            for sa in saList:
                if len(t) <= len(sa[1]):
                    if not self.checkSimilarity(sa[0], t, self.__length):
                        a.append(sa[0])
                else:
                    break
        return a

    def checkIfExistsSimilarityRowInS(self, sa):
        isFound = False
        sar = list(map(lambda w: self.__observation_table[sa + w], self.__w_set))
        indexs = 0
        while indexs < len(self.__s_set) and not isFound:
            s = self.__s_set[indexs]
            ar = list(map(lambda w: self.__observation_table[s + w], self.__w_set))
            isFound = self.computeRows(sar, ar)
            indexs += 1
        return isFound

    def addToS(self, s):
        self.__s_set.append(s)
        if s in self.__sa_set:
            self.__sa_set.remove(s)

    def compute(self, progress=None):
        self.computeSA()
        self.buildTable()
        ok = True
        i = 1
        while ok:
            i+=1
            self.consistencyAndClosedness()
            _, F, table = self.buildAutomaton()
            ok, word = self.checkLanguageQuery(F, table)
            if not ok:
                self.addCounterexample(word)
                self.buildTable()
                ok = True
            else:
                ok, word = self.checkForCounterexampleInSA(F, table)
                if ok:
                    self.addCounterexample(word)
                    self.buildTable()
            if progress is not None:
                progress(len(self.__language) - len(self.__remaining_language), len(self.__language))

    def addCounterexample(self, s):
        ss = ''
        for c in s:
            ss += c
            if not ss in self.__s_set:
                self.__s_set.append(ss)
            if ss in self.__sa_set:
                self.__sa_set.remove(ss)
            for a in self.__alphabet:
                if not ss + a in self.__s_set and not ss + a in self.__sa_set:
                    self.__sa_set.append(ss + a)

    def consistencyAndClosedness(self):
        newRowAdded = True
        while newRowAdded:
            self.consistency()
            newRowAdded = self.closedness()

    def checkSimilarity(self, s, t, k):
        isSimilar = True
        i = 0
        while i < len(self.__w_set) and isSimilar:
            w = self.__w_set[i]
            if len(w) <= k - max(len(s), len(t)):
                isSimilar = self.__observation_table[s + w] == self.__observation_table[t + w]
            i += 1
        return isSimilar

    def __repr__(self):
        a = [['S U SA \ W'] + self.__w_set]
        for s in self.__s_set:
            aa = [s]
            for w in self.__w_set:
                aa.append(self.__observation_table[s + w])
            a.append(aa)
        a.append(list(map(lambda a: '-', [''] + self.__w_set)))
        for s in self.__sa_set:
            aa = [s]
            for w in self.__w_set:
                aa.append(self.__observation_table[s + w])
            a.append(aa)
        s = tabulate(a)
        return "W = {}\nS = {}\nSA = {}\n{}".format(self.__w_set, self.__s_set, self.__sa_set, s)

