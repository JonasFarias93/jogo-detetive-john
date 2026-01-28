# 📕 BÍBLIA NARRATIVA — HOLLOWAY: O MAL MENOR

> Este documento define as **regras psicológicas, narrativas e estruturais** do jogo.
> Qualquer capítulo, crime, escolha ou hint **deve respeitar estas diretrizes**.

---

## 1️⃣ PRINCÍPIOS FUNDAMENTAIS DO JOGO

### 🎭 Princípio 1 — O jogador nunca “erra”

O jogador sempre age com **boa intenção**.
Se algo dá errado, **não é punição, é consequência**.

O desconforto nasce do **atraso entre escolha e efeito**.

---

### 🩸 Princípio 2 — John nunca é herói

* Ele pode fazer o bem
* Sempre perde algo em troca
* Nunca é recompensado emocionalmente

Isso é intencional e deve entrar na mente do jogador:

> “Eu tentei fazer o certo… por que tudo piorou?”

Trocar a escolha “errada” **nunca melhora o mundo** —
apenas muda **quem paga o preço**.

---

### ⚖️ Princípio 3 — Não existe escolha limpa

Nunca escreva:

* bem vs mal
* certo vs errado

Sempre escreva:

* **duas formas de se justificar**

O jogador não escolhe ações.
Ele escolhe **narrativas internas**.

---

### 🧠 Princípio 4 — Informação é punição

* Descobrir tudo → custo psicológico
* Ignorar detalhes → o mundo piora

Saber demais **não salva John**.
Às vezes só o destrói mais rápido.

---

### 🕳️ Princípio 5 — Memória não é verdade

* Memórias são fragmentadas
* Podem ser desbloqueadas ou perdidas
* Algumas só aparecem em estados alterados

O jogo **nunca confirma** se uma memória é real.

---

## 2️⃣ SANIDADE COMO FILTRO NARRATIVO (REGRA DE OURO)

Sanidade **não altera eventos**.
Ela altera **a forma como eles são apresentados**.

### Estados narrativos

#### 🟢 Sanidade Alta

* Descrições objetivas
* Crimes parecem claros
* NPCs coerentes
* Dúvidas sutis

#### 🟡 Sanidade Média

* Contradições em diálogos
* Detalhes que “não batem”
* Jogador questiona decisões passadas

#### 🔴 Sanidade Baixa

* Cenas variam conforme escolhas antigas
* NPCs lembram eventos inexistentes
* Um mesmo fato tem múltiplas versões

⚠️ **Nunca explique isso ao jogador.**

---

## 3️⃣ LOOP PSICOLÓGICO DO JOGO

```
ESCOLHA
 → JUSTIFICATIVA MORAL
   → CONSEQUÊNCIA ATRASADA
     → CULPA ou NEGAÇÃO
       → NOVA ESCOLHA (PIOR INFORMADA)
```

Esse loop:

* prende o jogador
* cria dissonância cognitiva
* gera apego emocional

O jogo **nunca permite corrigir totalmente o passado**.

---

## 4️⃣ O ASSASSINO — REGRAS PSICOLÓGICAS

### Visão do assassino

* John é seu igual
* Os crimes são mensagens
* Tudo é um jogo compartilhado

> “Eu não estou te machucando, John.
> Estou te acordando.”

### Regras fixas

* Nunca mata alguém “importante demais”
* Nunca repete padrões de forma óbvia
* Sempre deixa algo que John poderia perceber
* Nunca se revela se John não “jogar”

### Relação simbiótica

* John resiste → o assassino pressiona
* John se corrompe → o assassino se aproxima
* John quebra → o assassino valida

**Pergunta central:**

> *Eu te enlouqueço antes… ou você me pega primeiro?*

---

## 5️⃣ CAPÍTULOS — REGRAS ESTRUTURAIS

### O que é um capítulo

Unidade narrativa **autocontida**, localizada em:

```
src/jogo/chapters/chapter_xx/
```

Ele **não conhece a UI**.
Ele **define a experiência**.

### Estrutura mental

Um capítulo é um **grafo de cenas**:

```
Cena A
 ├─ ação 1 → Cena B
 ├─ ação 2 → Cena C
 └─ ação 3 → Cena A (loop psicológico)
```

Não existe cena correta.
Existe **cena alcançada**.

### Cena (Scene)

Define:

* onde John está
* o que percebe
* o que pode fazer

Campos:

* `text` / `text_file`
* `image`
* `actions`

### Ação (Action)

Uma ação:

* declara intenção
* nunca executa lógica
* nunca explica consequência

Campos:

* `label`
* `goto`
* `effects` (opcional)
* `hint` (opcional)

### Effects

* representam **preço invisível**
* são **deltas (±)**
* impacto pode ser tardio

O jogador não percebe tudo na hora.

### Hint — a intuição de John

* subjetivo
* não confiável
* aparece antes da ação

O hint:

* não explica
* não orienta moral
* provoca dúvida

---

## 6️⃣ MAPA MACRO DA HISTÓRIA

```
          [ MORTE DA FAMÍLIA ]
                   |
     --------------------------------
     |                              |
[ ASSASSINO ]                 [ JOHN ]
"estamos brincando"     "estou enlouquecendo?"
     |                              |
     -----------[ CASOS ]------------
                  |
   ---------------------------------
   |               |               |
Ignorar        Resolver        Distorcer
   |               |               |
Crime maior   Sanidade ↓     Memória ↑↓
```

Nada é linear.
Tudo reage ao jogador.

---

## 7️⃣ CAPÍTULO 01 — REGISTRO CANÔNICO

### 📖 Título

**O Mal Menor**

### 🎯 Função narrativa

* Ensinar que não existe escolha limpa
* Introduzir memória fragmentada
* Mostrar que ignorar também é escolher

### 🔪 Crime

* **Vítima:** porteiro, 42 anos
* **Cena:** apartamento simples
* **Versão oficial:** suicídio

**Detalhes:**

* relógio parado às **03:17**
* porta trancada por fora
* bilhete:

> “Eu fiz o que achei certo.”

### 🧠 Paralelo psicológico

* 03:17 = horário da ligação da morte da família (talvez)

Fragmento:

* telefone tocando
* John demora
* corte brusco

### ⚖️ Dilema central

* Ele encobriu um crime para proteger uma criança
* Se falar → família destruída
* Se morrer → verdade enterrada

### 🎮 Escolhas

**A — Arquivar**

* Verdade enterrada
* Padrão silencioso começa
* John dorme melhor… por enquanto

**B — Reabrir**

* Família exposta
* Memória desbloqueada
* Sanidade ↓

**C — Forjar**

* John cruza uma linha
* Chefia desconfia
* Portas se fecham

### 🧠 Reação do assassino

* Ajusta o jogo
* Testa limites
* O jogador só sente depois

### 🧠 Frase final

> “Às vezes o mal menor só é o mal…
> que a gente aprende a suportar.”

---

## 8️⃣ REGRA FINAL (A MAIS IMPORTANTE)

Se o jogador **não se questionar depois da escolha**,
o capítulo **falhou**.
