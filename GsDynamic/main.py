"""
Trabalho: Otimização de Portfólio de Projetos (0/1 Knapsack)
Implementa as quatro estratégias pedidas:
  - greedy_knapsack    : Estratégia Gulosa (V/E)
  - recursive_knapsack : Solução recursiva pura (força bruta)
  - memoized_knapsack  : Recursiva + Memoização (Top-Down DP) com reconstrução
  - dp_knapsack        : Programação Dinâmica iterativa (Bottom-Up) com reconstrução

Cada função retorna: (lista_nomes_selecionados, valor_total, horas_usadas)
"""

from typing import List, Tuple

Project = Tuple[str, int, int]  # (nome, valor V, horas E)


# -----------------------------
# Fase 1: Estratégia Gulosa
# -----------------------------
def greedy_knapsack(projects: List[Project], capacity: int):
    """
    Seleciona projetos pela razão valor/horas (V/E) decrescente.
    Retorna (selected_names, total_value, used_hours).

    Complexidade: Tempo O(n log n) (ordenacao), Espaço O(n).
    Observação: Heurística — NÃO garante o ótimo para 0/1 knapsack.
    """
    sorted_projects = sorted(projects, key=lambda p: p[1] / p[2], reverse=True)
    selected = []
    used = 0
    total_value = 0
    for name, value, hours in sorted_projects:
        if used + hours <= capacity:
            selected.append(name)
            used += hours
            total_value += value
    return selected, total_value, used


# -----------------------------
# Fase 2: Solução Recursiva Pura
# -----------------------------
def recursive_knapsack(projects: List[Project], capacity: int):
    """
    Força bruta recursiva (explora todas combinações).
    Retorna (selected_names, total_value, used_hours).

    Complexidade: Tempo O(2^n), Espaço O(n) (pilha).
    """
    n = len(projects)

    def rec(i: int, rem: int) -> int:
        """
        Valor ótimo considerando itens 0..i-1 (i itens disponíveis) e capacidade rem.
        i == 0 => 0 (nenhum item)
        """
        if i == 0 or rem == 0:
            return 0
        name, val, hrs = projects[i - 1]
        # pular
        best = rec(i - 1, rem)
        # incluir
        if hrs <= rem:
            best = max(best, val + rec(i - 1, rem - hrs))
        return best

    best_value = rec(n, capacity)

    # Reconstrução (ingênua — recalcula rec muitas vezes)
    selected = []
    rem = capacity
    for i in range(n, 0, -1):
        if rem <= 0:
            break
        # se removendo item i-1 o valor cai, então o item foi escolhido
        without = rec(i - 1, rem)
        name, val, hrs = projects[i - 1]
        if hrs <= rem:
            with_item = val + rec(i - 1, rem - hrs)
        else:
            with_item = -1
        if with_item > without:
            selected.append(name)
            rem -= hrs
        # caso empate, preferimos pular (poderia escolher incluir)
    selected.reverse()
    used = capacity - rem
    return selected, best_value, used


# -----------------------------
# Fase 3: Memoização (Top-Down)
# -----------------------------
def memoized_knapsack(projects: List[Project], capacity: int):
    """
    Recursão com memoização (Top-Down).
    Usa dicionário memo[(i, rem)] = melhor valor usando i primeiros itens com rem capacidade.
    Aqui adotamos i como "número de itens considerados" (i varia 0..n).
    Retorna (selected_names, best_value, used_hours).

    Complexidade: Tempo O(n * C), Espaço O(n * C).
    """
    n = len(projects)
    memo = {}  # chave: (i, rem) -> valor ótimo

    def rec(i: int, rem: int) -> int:
        # caso base
        if i == 0 or rem == 0:
            return 0
        if (i, rem) in memo:
            return memo[(i, rem)]
        name, val, hrs = projects[i - 1]
        # pular
        best = rec(i - 1, rem)
        # incluir se couber
        if hrs <= rem:
            best = max(best, val + rec(i - 1, rem - hrs))
        memo[(i, rem)] = best
        return best

    best_value = rec(n, capacity)

    # Reconstrução usando memo preenchido (sem recalcular excessivamente)
    selected = []
    rem = capacity
    i = n
    while i > 0 and rem > 0:
        # Valor sem pegar o item i-1
        without = memo.get((i - 1, rem), rec(i - 1, rem))
        name, val, hrs = projects[i - 1]
        include = -1
        if hrs <= rem:
            include = val + memo.get((i - 1, rem - hrs), rec(i - 1, rem - hrs))
        # Se incluir produz melhor valor, incluímos
        if include > without:
            selected.append(name)
            rem -= hrs
            i -= 1
        else:
            i -= 1
    selected.reverse()
    used = capacity - rem
    return selected, best_value, used


# -----------------------------
# Fase 4: PD Iterativa (Bottom-Up)
# -----------------------------
def dp_knapsack(projects: List[Project], capacity: int):
    """
    Programação dinâmica iterativa (tabela bottom-up).
    dp[i][c] = melhor valor com os primeiros i itens (itens 0..i-1) e capacidade c.
    Retorna (selected_names, best_value, used_hours).

    Complexidade: Tempo O(n * C), Espaço O(n * C).
    """
    n = len(projects)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # preencher tabela
    for i in range(1, n + 1):
        name, val, hrs = projects[i - 1]
        for c in range(0, capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if hrs <= c:
                dp[i][c] = max(dp[i][c], val + dp[i - 1][c - hrs])

    best_value = dp[n][capacity]

    # Reconstrução
    selected = []
    c = capacity
    i = n
    while i > 0 and c >= 0:
        if dp[i][c] != dp[i - 1][c]:
            name, val, hrs = projects[i - 1]
            selected.append(name)
            c -= hrs
            i -= 1
        else:
            i -= 1
    selected.reverse()
    used = capacity - max(c, 0)
    return selected, best_value, used


# -----------------------------
# Utilitários e testes
# -----------------------------
def print_result(title: str, result):
    sel, val, used = result
    print(f"\n--- {title} ---")
    print("Selecionados:", sel)
    print("Valor total:", val)
    print("Horas usadas:", used)


def run_tests():
    """
    Executa pelo menos 4 casos de teste, incluindo um caso onde a gulosa falha.
    """

    # Caso 1: Exemplo do enunciado (C = 10)
    projetos1 = [
        ("Projeto A", 12, 4),
        ("Projeto B", 10, 3),
        ("Projeto C", 7, 2),
        ("Projeto D", 4, 3),
    ]
    cap1 = 10

    # Caso 2: Caso onde a gulosa falha
    # A(8,4) ratio=2.0 ; B(7,3) ratio≈2.333 ; C(6,2) ratio=3.0 ; cap=6
    # Greedy picks C(2) + B(3) => hours=5 value=13
    # Optimal picks A(4) + C(2) => hours=6 value=14
    projetos2 = [
        ("A", 8, 4),
        ("B", 7, 3),
        ("C", 6, 2),
    ]
    cap2 = 6

    # Caso 3: capacidade zero
    projetos3 = [
        ("X", 5, 3),
        ("Y", 10, 5),
    ]
    cap3 = 0

    # Caso 4: maior conjunto para testar DP
    projetos4 = [
        ("P1", 20, 6),
        ("P2", 30, 9),
        ("P3", 14, 4),
        ("P4", 16, 5),
        ("P5", 9, 3),
    ]
    cap4 = 15

    casos = [
        ("Enunciado (C=10)", projetos1, cap1),
        ("Gulosa Falha (demonstração)", projetos2, cap2),
        ("Capacidade Zero", projetos3, cap3),
        ("Caso Maior (C=15)", projetos4, cap4),
    ]

    for titulo, projs, cap in casos:
        print("\n" + "=" * 60)
        print("CASO:", titulo)
        print("Projetos:", projs)
        print("Capacidade:", cap)

        r_g = greedy_knapsack(projs, cap)
        r_r = recursive_knapsack(projs, cap)
        r_m = memoized_knapsack(projs, cap)
        r_d = dp_knapsack(projs, cap)

        print_result("Greedy", r_g)
        print_result("Recursiva Pura", r_r)
        print_result("Memoizada (Top-Down)", r_m)
        print_result("PD Iterativa (Bottom-Up)", r_d)

        # comparação de valores
        val_g = r_g[1]
        val_dp = r_d[1]
        if val_g != val_dp:
            print("\n>>> Observação: Gulosa NÃO encontrou o ótimo aqui.")
            print(f"    Gulosa = {val_g} vs Ótimo (DP) = {val_dp}")
        else:
            print("\n>>> Observação: Gulosa encontrou o mesmo valor ótimo neste caso.")

    # resumo das complexidades
    print("\n" + "=" * 60)
    print("ANÁLISE TEÓRICA — Complexidade:")
    print("""
    - Greedy: O(n log n) tempo (ordenacao), espaço O(n). Heurística (não-ótima em geral).
    - Recursiva pura: O(2^n) tempo, espaço O(n) pilha.
    - Memoizada (Top-Down): O(n * C) tempo, O(n * C) espaço.
    - PD Iterativa (Bottom-Up): O(n * C) tempo, O(n * C) espaço (pode ser reduzido a O(C)).
    """)


if __name__ == "__main__":
    run_tests()
