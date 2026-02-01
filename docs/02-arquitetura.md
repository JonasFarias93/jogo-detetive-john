# 📕 Arquitetura de Gameplay, Contratos de Dados & Design Narrativo

### Detetive John — Era Flet / Engine-Driven

> Documento base para desenvolvimento, expansão e versionamento do jogo **Detetive John**.

---

## Parte I — Arquitetura de Gameplay e UI (Flet)

### Visão Geral

A arquitetura do jogo é **engine-driven** e **UI-declarativa**.

A UI **não decide regras**, **não aplica efeitos** e **não interpreta narrativa**.
Ela apenas **reflete o estado atual do jogo**.

Fluxo principal:

```
Registry (capítulos)
        ↓
GameEngine
        ↓
GameState
        ↓
UI (Flet)
```

---

## Princípios Fundamentais

### 1️⃣ UI é declarativa

A UI:

* renderiza texto
* renderiza imagens
* renderiza botões

Ela **não mantém lógica de jogo**.

Toda mudança visual ocorre **após uma mudança de estado**.

---

### 2️⃣ Engine manda no fluxo

O `GameEngine` é o **orquestrador absoluto**:

* controla a cena atual
* aplica efeitos
* valida escolhas
* decide transições

A UI apenas chama:

```python
engine.start()
engine.choose(action_key)
```

---

### 3️⃣ UI não decide nada

A UI:

* não interpreta `goto`
* não aplica `effects`
* não avalia condições
* não decide se uma ação é boa ou ruim

Ela **exibe possibilidades**.

---

### 4️⃣ Capítulos são a fonte da verdade

Capítulos descrevem:

* o que acontece
* quais escolhas existem
* quais consequências são possíveis

Eles **não sabem**:

* quem é a UI
* como o texto aparece
* como o jogador clica

---

## Estrutura Conceitual da Tela

A UI deve conter **quatro regiões lógicas**, nesta ordem:

1. **Status** (topo)
2. **Narrativa** (meio-esquerda)
3. **Cena / Imagem** (meio-direita)
4. **Ações / Config / Dicas** (rodapé)

> A proporção pode variar.
> A ordem conceitual **não**.

---

## Regras de Layout

* Texto narrativo **sempre com scroll**
* Imagem da cena é **opcional**
* Ações nunca devem “pular” a UI
* Dicas (hints) devem suportar:

  * texto longo
  * quebra de linha
  * scroll
* A UI deve se adaptar a redimensionamento de tela

---

## GameEngine (Orquestrador)

### Responsabilidades

O `GameEngine` é responsável por:

* manter o estado atual (`GameState`)
* controlar:

  * cena atual
  * stats do jogador
  * ações disponíveis
* aplicar:

  * efeitos
  * transições de cena
* expor uma API simples para a UI:

  * `start()`
  * `choose(action_key)`

### Não-responsabilidades

* não renderiza UI
* não conhece Flet
* não sabe como o texto é exibido

---

## UI Flet (Camada de Apresentação)

### Responsabilidades

A UI é responsável por:

* renderizar o `GameState`
* converter estado em:

  * texto
  * imagens
  * botões
* encaminhar eventos do usuário para a engine

### Regra de Ouro

> **Toda mudança visual vem de uma mudança de estado.**

Não existe UI “esperta”.

---

## Parte II — Contratos de Dados Narrativos

### SceneData (Cena)

Campos:

* `id: str`
* `text: str`
* `image: str | ""`
* `actions: list[ActionData]`

A cena **não executa nada**.
Ela **descreve possibilidades**.

---

### ActionData (Ações)

Campos obrigatórios:

* `key: str`
* `label: str`

Campos opcionais:

* `goto: str`
* `effects: EffectsData`
* `hint: str`
* `conditions: dict` *(Sprint futura)*

> A UI não interpreta nada disso.

---

### EffectsData (Efeitos)

* `sono: int`
* `energia: int`
* `foco: int`
* `estresse: int`

**Sempre deltas**, nunca valores absolutos.

Clamp ocorre na engine.

---

## Parte III — Capítulos, Hints e Design Narrativo

### Capítulos

Um capítulo é uma pasta autocontida:

```
src/jogo/content/chapter_xx/
├─ manifest.json
├─ ascii/
└─ images/
```

Capítulos:

* não sabem da UI
* não sabem da engine
* apenas **declaram narrativa**

---

### Hints — A intuição de John

Hints:

* aparecem antes da ação
* são subjetivos
* podem mentir
* criam tensão

Nunca explicam regras.
Nunca dizem “isso é bom”.

---

### Estrutura Mental

O jogo não é uma árvore.
É um **grafo de desgaste psicológico**.

Escolher é aceitar um custo.

---

## Parte IV — Versionamento

### v0.3.0 — Nova Fundação

* UI totalmente em Flet
* Engine desacoplada
* Capítulos funcionando
* Jogo jogável de ponta a ponta

---

### Próximos Marcos

* `v0.3.1` → Typewriter + skip
* `v0.4.0` → Som e atmosfera
* `v0.5.0` → Inventário
* `v1.0.0` → Capítulo 01 completo

---

## Frase-guia (inalterada)

> **O jogador não escolhe ações.**
> **Ele escolhe narrativas internas.**
