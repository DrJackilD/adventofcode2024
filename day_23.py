from collections import defaultdict
from itertools import combinations
from typing import DefaultDict

INPUT_FILE = "input_23.txt"


def bron_kerbosch(
    graph: DefaultDict[str, set[str]],
    to_explore: set[str],
    seen: set | None = None,
    explored: set | None = None,
) -> list[set[str]]:
    seen = seen or set()
    explored = explored or set()

    if not to_explore and not seen:
        return [explored]

    cliques = []
    for v in list(to_explore):
        cliques.extend(
            bron_kerbosch(graph, to_explore & graph[v], seen & graph[v], explored | {v})
        )
        to_explore.remove(v)
        seen.add(v)
    return cliques


def get_party_password(graph: DefaultDict[str, set[str]]) -> str:
    cliques = bron_kerbosch(graph, set(graph.keys()))
    cliques.sort(key=len, reverse=True)
    return ",".join(sorted(cliques[0]))


def party_of_three(graph: DefaultDict[str, set[str]]) -> int:
    triples = set()
    for node in graph:
        if not node.startswith("t"):
            continue

        for nei1, nei2 in combinations(graph[node], 2):
            if nei1 in graph[nei2]:
                triples.add(frozenset([node, nei1, nei2]))
    return len(triples)


if __name__ == "__main__":
    deps = defaultdict(set)
    with open(INPUT_FILE) as f:
        nodes = set()
        for line in f:
            a, b = line.strip().split("-")
            deps[a].add(b)
            deps[b].add(a)

    print(party_of_three(deps))  # part 1
    print(get_party_password(deps))  # part 2
