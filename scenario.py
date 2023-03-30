import itertools as it
import numpy as np


J = [1, 2, 3, 4]
k = 2
partitions = list(map(lambda x: set(x), list(it.combinations(J, k))))


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
                    # Calc les ensembles d'arbres AL1 ... ALk
                    ens_AL = []
                    for j in range(0, k):
                        ens_AL.append(gen(partition[j]))
                    # Construire les scénarios
                    add_scenario(scenarios, ens_AL, k, L[i])
        return scenarios


def add_scenario(scenarios, ens_AL, k, V):
    # for sc1 in ens_AL[0]:
    #     for sc2 in ens_AL[1]:
    #         # ...
    #         for sck in ens_AL[k-1]:
    #             scenarios.append([V, sc1, sc2, ..., sck])
    if len(scenario) == 0:
        scenarios.append([V])
    else:
        scs_to_add = []  # eviter une boucle infinie
        for scenario in scenarios:
            j = len(scenario)
            if j == k+1:
                return scenarios
            for sous_sc in ens_AL[j]:
                # ajouter len(ens_AL[k]) nouveaux scenarios
                sc_to_add = scenario.copy()
                sc_to_add.add(sous_sc)
        for scenario in scs_to_add:
            scenarios.append(scenario)
        add_scenario(scenarios, ens_AL, k, V)


def calc_partitions(J, k):
    for m in range(1, len(J)-k+2):
        print(list(map(lambda x: list(x), list(it.combinations(J, m)))))


# calc_partitions([1, 2, 3, 4], 2)


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


def partitions(ensemble, k):
    n = len(ensemble)
    if k == 1:
        return [ensemble]
    if n < k:
        return []
    resultat = []
    for i in range(n):
        premier = ensemble[i:i+1]
        partitions_restes = partitions(ensemble[:i] + ensemble[i+1:], k-1)
        for partition in partitions_restes:
            resultat.append([premier] + partition)
    return resultat


print(partitions([1, 2, 3, 4], 2))
