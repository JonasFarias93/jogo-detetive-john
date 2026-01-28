# Relatório — Capítulos, Ações e Hints

## Visão geral

No **Detetive John**, capítulos controlam a experiência narrativa.
A UI é apenas um meio de exibição e **nunca decide nada**.

Tudo que o jogador **vê**, **escolhe** e **sente** vem do **capítulo**.

---

## 1️⃣ O que é um Capítulo

Um capítulo é uma pasta **autocontida**, localizada em:

```
src/jogo/chapters/chapter_xx/
```

Ele contém:

* `manifest.json` (estrutura e lógica narrativa)
* arquivos de texto (`ascii/*.txt`)
* imagens (opcional)

O capítulo **não conhece a UI**, apenas descreve:

* o que acontece
* quais escolhas existem
* quais consequências são aplicadas

---

## 2️⃣ Estrutura mental de um capítulo

Pense em um capítulo como um **grafo de cenas**:

```
Cena A
 ├─ ação 1 → Cena B
 ├─ ação 2 → Cena C
 └─ ação 3 → Cena A (loop, custo psicológico)
```

Não existe **“cena correta”**.
Existe **cena alcançada**.

---

## 3️⃣ Cenas (Scene)

Cada cena define:

| Campo                | Função                      |
| -------------------- | --------------------------- |
| `text` / `text_file` | Texto narrativo exibido     |
| `image`              | Imagem ilustrativa da cena  |
| `actions`            | Lista de escolhas possíveis |

**Exemplo mental:**

> “Onde John está agora, o que ele percebe, e o que pode fazer a seguir.”

---

## 4️⃣ Ações (Action)

Uma ação representa uma **decisão do jogador**.

Cada ação pode conter:

| Campo     | Obrigatório | Função                    |
| --------- | ----------- | ------------------------- |
| `label`   | ✅           | Texto do botão            |
| `goto`    | ✅           | Próxima cena              |
| `effects` | ❌           | Impacto nos status        |
| `hint`    | ❌           | Intuição / pressentimento |

A ação **nunca executa lógica diretamente**.
Ela apenas **declara intenção**.

---

## 5️⃣ Effects — consequências numéricas

effects alteram o estado interno do jogador:

```json
"effects": {
  "sono": 15,
  "energia": -5,
  "foco": -10,
  "estresse": 5
}
```

### Regras

* valores são **deltas** (somam ou subtraem)
* o sistema faz **clamp automático (0–100)**
* o jogador **nem sempre percebe imediatamente** o custo real

👉 **Effects representam o preço invisível das escolhas.**

---

## 6️⃣ Hint — a intuição de John

### O que é

O **hint** é uma dica curta, **subjetiva e não confiável**.

Ele aparece:

* na área de “dicas” da UI
* **antes** da ação ser executada

### O que ele faz

* orienta emocionalmente
* sugere risco, **não verdade**
* cria tensão antes da escolha

### Exemplos bons

* “A rua está silenciosa demais.”
* “O corpo pede descanso. A cidade não espera.”
* “Aqui ninguém fala de graça.”

### Exemplos ruins

* “Você perderá 10 de energia.”
* “Essa é a escolha correta.”

👉 O hint **não explica regras**, ele **provoca dúvida**.

---

## 7️⃣ Como o Hint interfere na UI

### Fluxo real

```
Capítulo → Manifest → Registry → Gameplay → ActionsPanel
```

Quando o jogador clica:

1. o hint aparece
2. o jogador lê (ou ignora)
3. a ação acontece
4. a cena muda

A UI:

* não valida hint
* não interpreta hint
* apenas exibe

---

## 8️⃣ Regras de ouro para escrever capítulos

### ✅ Faça

* use hint em decisões ambíguas
* use effects sutis (não óbvios)
* permita loops (descansar, observar, hesitar)
* trate informação como **poder escasso**

### ❌ Evite

* explicar demais
* escolhas “boas vs ruins”
* consequências imediatas sempre claras
* texto didático

---

## 9️⃣ Relação com a UI (importante)

A UI é **estável e neutra**.

Isso significa:

* você pode escrever capítulos sem mexer em código
* mudar texto, imagem ou hint não quebra nada
* cenas inválidas mostram **erro narrativo**, não crash

Se algo aparece estranho na tela:

👉 o problema está no **capítulo**, não na UI

---

## 🔟 Como pensar o Capítulo 01

Para o primeiro capítulo:

* poucas cenas
* poucas ações
* hints fortes
* efeitos leves, mas **cumulativos**

### Objetivo

Ensinar o jogador que **toda escolha custa algo**, mesmo as pequenas.
