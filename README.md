# Projeto: Otimização de Portfólio de Projetos

## Integrantes

* **Heitor Anderson Prestes de Oliveira Filho **– RM: **554823**
* **Lucca Ribeiro Cardinale** – RM: **556668**

---

## Descrição do Projeto

Este projeto implementa a **Otimização de Portfólio de Projetos** utilizando o clássico problema da **Mochila 0/1 **. O objetivo é selecionar o conjunto ótimo de projetos que maximize o valor total entregue sem ultrapassar o limite de horas disponível.

O código inclui **quatro abordagens distintas**, conforme solicitado:

1. **Estratégia Gulosa (Greedy)** — Seleciona projetos pela melhor razão Valor/Horas.
2. **Solução Recursiva Pura (Força Bruta)** — Explora todas as combinações possíveis.
3. **Solução com Memoização (Top-Down)** — Recursiva com cache, mais eficiente.
4. **Programação Dinâmica Iterativa (Bottom-Up)** — Método clássico usando tabela DP.

Cada método retorna:

* Lista de projetos selecionados
* Valor total obtido
* Total de horas utilizadas

O script também contém um módulo de testes automáticos que executa diferentes cenários, incluindo casos onde a estratégia gulosa não encontra a solução ótima.

---

## Estrutura do Arquivo

```
├── main.py     # Código-fonte completo com as quatro abordagens
├── README.md       # Este documento
```

---

## 🧠 Lógica do Problema

O problema da mochila 0/1 consiste em:

* Dado um conjunto de itens (projetos) com **valor (V)** e **custo em horas (E)**,
* Selecionar um subconjunto cujo valor total seja **máximo**, desde que a soma das horas não ultrapasse a **capacidade disponível**.

A diferença entre as abordagens está no nível de eficiência e garantia de encontrar o ótimo.

---

## 🚀 Instruções de Uso

### 1. Requisitos

* Python **3.8+**

### 2. Execução

Basta rodar o arquivo principal:

```bash
python main.py
```

A saída exibirá:

* Projetos disponíveis em cada caso
* Capacidade testada
* Resultados de cada método
* Comparação entre resultados

---

## 📦 Dependências

Não há dependências externas. Todo o programa utiliza apenas bibliotecas padrão do Python.

---

## 🧪 Casos de Teste Inclusos

O script executa automaticamente quatro cenários:

1. **Exemplo padrão** do enunciado.
2. **Caso onde a estratégia gulosa falha**.
3. **Capacidade zero**, validando bordas.
4. **Caso maior**, demonstrando eficiência da DP.

---

## 📈 Análise de Complexidade

* **Greedy:** O(n log n) — rápido, mas não garante solução ótima.
* **Recursiva pura:** O(2ⁿ) — extremamente lenta para muitos projetos.
* **Memoização (Top-Down):** O(n × C)
* **DP Iterativa (Bottom-Up):** O(n × C) — método mais robusto e recomendado.

---

## 📜 Observações Finais

Este projeto demonstra diferentes estratégias algorítmicas para o mesmo problema, permitindo comparar trade-offs entre desempenho, complexidade e qualidade de solução.

Ideal para fins didáticos e estudos de Análise de Algoritmos, Estruturas de Dados e tomada de decisão baseada em otimização.

---

## ✨ Licença

Uso acadêmico e educacional.
