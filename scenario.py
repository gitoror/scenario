import itertools as it
import numpy as np


def calc_partitions(J):
    if len(J) == 1:
        return [[J]]
    else:
        e = J[0]  # arbitraire
        H = J.copy()
        H.pop(0)
        # ensemble d'ensembles de partitions
        Pcursif = calc_partitions(H)
        partitions_seul = []
        partitions_pls = []
        for partition in Pcursif:
            p_seul = partition.copy()
            p_seul.append([e])  # partie = singleton
            partitions_seul.append(p_seul)
            for i in range(len(partition)):
                partie = partition[i]
                p = partie.copy()
                p.append(e)
                partition_pls = partition.copy()
                partition_pls.pop(i)
                partition_pls.append(p)
                partitions_pls.append(partition_pls)
        partitions_ret = []
        for partition in partitions_seul:
            partitions_ret.append(partition)
        for partition in partitions_pls:
            partitions_ret.append(partition)
        return partitions_ret


def add_scenarios(scenarios, ens_AL, j=0, V=None):
    if j == 0:
        for sous_scenario in ens_AL[j]:
            scenarios.append([V, sous_scenario])
        add_scenarios(scenarios, ens_AL, j+1)
    elif j < len(ens_AL):
        new_scenarios = []
        for scenario in scenarios:
            for sous_scenario in ens_AL[j]:
                sc = scenario.copy()
                sc.append(sous_scenario)
                new_scenarios.append(sc)
        scenarios[:] = new_scenarios[:]  # garder même pointeur
        add_scenarios(scenarios, ens_AL, j+1)
    return


def gen(L):
    if len(L) == 1:
        return L
    else:
        scenarios = []
        for i in range(0, len(L)):
            # Calc toutes les partitions de L\{e} en L1 ... Lk
            for k in range(1, len(L)):
                J = L.copy()
                J.pop(i)
                partitions = calc_partitions(J, k)
                for partition in partitions:
                    # Calc les ensembles d'arbres AL1 ... ALk pour la partition donnée
                    ens_AL = []  # sera un ensemble d'ensembles de scenarios
                    for j in range(0, k):
                        ens_AL.append(gen(partition[j]))
                    # Construire les scénarios
                    add_scenarios(scenarios, ens_AL, V=L[i])
        return scenarios


def gen2(L):
    print('-----------')
    print("L", L)
    if len(L) == 1:
        print("single")
        print("-")
        return [L]
    else:
        scenarios = []
        for i in range(0, len(L)):  # e=L[i]
            # Calc toutes les partitions de L\{e} en L1 ... Lk
            J = L.copy()
            J.pop(i)
            partitions = calc_partitions(J)
            print("J", J)
            # liste qui contiendra des ensembles de partitions
            P = []
            for u in range(len(L)-1):
                P.append([])
            for partition in partitions:
                # P[0] ens de partitions à 1 partie
                P[len(partition)-1].append(partition)
            print("Calc P")
            for p in range(len(P)):
                print("k=", p+1, ":", P[p])
            print("")
            print("Calc scs")
            for k in range(1, len(L)):  # k = nombre de parties
                print("Pour k = ", k, "parties\n")
                for partitions in P[k-1]:  # les partitions à k parties
                    print("Pour ces partitions", partitions)
                    # Calc les ensembles d'arbres AL1 ... ALk pour la partition donnée
                    ens_AL = []  # sera un ensemble d'ensembles de scenarios
                    for partition in partitions:
                        print("Pour cette partition à k parties", partition)
                        ens_AL.append(gen2(partition))
                    # Construire les scénarios
                    print("Ajout des scs")
                    print("avant")
                    for sc in scenarios:
                        print(sc)
                    add_scenarios(scenarios, ens_AL, V=L[i])
                    print("Scs ajoutés !!!!!!! (apres)")
                    for sc in scenarios:
                        print(sc)
                    print("--")
        print("Fin de L=", L)
        for sc in scenarios:
            print(sc)
        print("------------")

        return scenarios


# scs = gen2([1, 2, 3])
# print("\nResult\n")
# for sc in scs:
#     print(sc)

def gen3(L):
    print('-----------')
    print("L", L)
    if len(L) == 1:
        print("single")
        print("-")
        return [L]
    else:
        scenarios = []
        for i in range(0, len(L)):  # e=L[i]
            # Calc toutes les partitions de L\{e} en L1 ... Lk
            J = L.copy()
            J.pop(i)
            partitions = calc_partitions(J)
            print("J", J)
            # liste qui contiendra des ensembles de partitions
            P = []
            for u in range(len(L)-1):
                P.append([])
            for partition in partitions:
                # P[0] ens de partitions à 1 partie
                P[len(partition)-1].append(partition)
            print("Calc P")
            for p in range(len(P)):
                print("k=", p+1, ":", P[p])
            print("")
            print("Calc scs")
            for k in range(1, len(L)):  # k = nombre de parties
                print("Pour k = ", k, "parties\n")
                for partitions in P[k-1]:  # les partitions à k parties
                    print("Pour ces partitions", partitions)
                    # Calc les ensembles d'arbres AL1 ... ALk pour la partition donnée
                    ens_AL = []  # sera un ensemble d'ensembles de scenarios
                    for partition in partitions:
                        print("Pour cette partition à k parties", partition)
                        ens_AL.append(gen3(partition))
                    # Construire les scénarios
                    print("Ajout des scs")
                    print("avant")
                    for sc in scenarios:
                        print(sc)
                    # add_scenarios(scenarios, ens_AL, V=L[i])
                    combs = list(
                        map(lambda x: list(x), list(it.product(*ens_AL))))
                    for comb in combs:
                        comb.insert(0, L[i])
                        scenarios.append(comb)
                    print("Scs ajoutés !!!!!!! (apres)")
                    for sc in scenarios:
                        print(sc)
                    print("--")
        print("Fin de L=", L)
        for sc in scenarios:
            print(sc)
        print("------------")

        return scenarios


scs = gen3([1, 2, 3, 4, 5])
print("\nResult\n")
for sc in scs:
    print(sc)
print(len(scs))

# Idee garder toutes les combinaisons dont la reunion est J et l'intersection vide


# P = calc_partitions([1, 2, 3, 4, 5])
# print("\nResult")
# for p in P:
#     print(p)


def calc_risque(scenario, probas, gravites, pere=None):
    # parcours en profondeur
    racine = scenario[0]
    if pere == None:
        risque = proba[racine, racine] * gravite[racine]
    else:
        risque = proba[racine, pere] * gravite[racine]
    for i in range(1, len(scenario)):
        risque += calc_risque(scenario[i], probas, gravites, racine)
    return risque


gravite = np.array([1, 2, 3, 4])
proba = np.array([[0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4],
                 [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4]])

# print(calc_risque([0, [1, [2]], [3]], proba, gravite)) # 1.3

J = [1, 2, 3, 4]
k = 2
partitions = list(map(lambda x: list(x), list(it.combinations(J, k))))

# L = [1, 2, 3, 4] k = 2 racine = 1
ens_AL = [[[2, [3]], [3, [2]]], [[4]]]
# ens_AL = [[[4]], [[3]]]
scenarios = []
# add_scenarios(scenarios, ens_AL, V=1)
# print("Result", scenarios)

# calc_partitions([1, 2, 3], 2)
# Attendu : [ [[1,2], [3]],   [[1,3], [2]],   [[3,2], [1]] ]


def cal_partitions(J, k):
    combs = []
    for m in range(1, len(J)-k+2):  # n-k+1 = taille max des parties
        comb = list(map(lambda x: set(x), list(it.combinations(J, m))))
        print(comb)
        combs.append(comb)
    partitions = []
    build_partitions(partitions, combs, k)
    # reste à sélectionner celle qui respectent ces critères :
    # union = J
    # intersection = vide
    return partitions


def build_partitions(partitions, combs, k, size=0):
    if size == 0:
        for comb in combs[size]:
            partitions.append([[], [], []])


# for m in range(1, len(J)-k+2):
#     print(list(map(lambda x: set(x), list(it.combinations(J, m)))))
