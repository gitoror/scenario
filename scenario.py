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


def gen(L):
    if len(L) == 1:
        return [L]
    else:
        scenarios = []
        for i in range(0, len(L)):  # e=L[i]
            # Calc toutes les partitions de L\{e} en L1 ... Lk
            J = L.copy()
            J.pop(i)
            partitions = calc_partitions(J)
            # liste qui contiendra des ensembles de partitions
            P = []
            for u in range(len(L)-1):
                P.append([])
            for partition in partitions:
                # P[0] ens de partitions à 1 partie
                P[len(partition)-1].append(partition)
            for k in range(1, len(L)):  # k = nombre de parties
                for partitions in P[k-1]:  # les partitions à k parties
                    # Calc les ensembles d'arbres AL1 ... ALk pour la partition donnée
                    ens_AL = []  # sera un ensemble d'ensembles de scenarios
                    for partition in partitions:
                        ens_AL.append(gen(partition))
                    # Construire les scénarios
                    combs = list(
                        map(lambda x: list(x), list(it.product(*ens_AL))))
                    for comb in combs:
                        comb.insert(0, L[i])
                        scenarios.append(comb)
        return scenarios


# scs = gen([1, 2, 3])
# print("\nResult\n")
# for sc in scs:
#     print(sc)
# print(len(scs))

def draw_tree(node, depth):
    if node is None:
        return
    # Imprimer l'indentation pour aligner le nœud avec ses parents et frères
    print('   ' * depth, end='')
    # Imprimer le caractère pour représenter la branche de l'arbre
    if depth > 0:
        print('|-- ', end='')
    # Imprimer le contenu du nœud
    print(node[0])
    # Appeler la fonction récursive pour chaque enfant du nœud
    if len(node) > 1:
        for child in node[1:]:
            draw_tree(child, depth + 1)


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


def pires_scenarios(evenements, probas, gravites, nb_scenarios=1):
    scenarios = gen(evenements)
    for s in range(len(scenarios)):
        scenarios[s] = {'s': scenarios[s], 'r': round(calc_risque(
            scenarios[s], probas, gravites), 3)}
    sorted_scenario = sorted(scenarios, key=lambda x: x['r'], reverse=True)
    # retourner les nb_scenarios premiers 's'
    # return list(map(lambda x: x['s'], sorted_scenario[:nb_scenarios]))
    S = sorted_scenario[:nb_scenarios]
    for s in S:
        draw_tree(s['s'], 0)
        print("")
    return S


print(pires_scenarios([1, 2, 3], proba, gravite, 3))
