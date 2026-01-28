# Arquitetura Gameplay, Contratos de Dados & Design Narrativo

> Base para desenvolvimento, expansão e versionamento do jogo **Detetive John**.

---

## Parte I — Arquitetura de Gameplay e UI

# Princípios

**KV manda no layout**
A hierarquia visual e “slots” ficam no `.kv`.

**Python manda no estado e eventos**
O `GameplayScreen` mantém estado (player, cena atual, ações) e chama APIs dos módulos.

**Módulos não recriam a tela**
Eles atualizam UI via `refresh()` / `set_*()`, sem `clear_widgets()` no fluxo normal.

**Módulos são independentes**
Status não sabe de Cena, Cena não sabe de Ações. Apenas o `GameplayScreen` orquestra.

---

# Estrutura da tela (layout obrigatório)

O `gameplay.kv` deve fornecer **3 áreas (slots)** na tela, **nesta ordem**:

1. **Status Area** (topo)
2. **Scene Area** (meio)
3. **Actions Area** (rodapé)

---

## Regras de layout

* A altura relativa pode mudar, mas a **ordem não**.
* Deve suportar redimensionamento sem quebrar o texto nem “estourar” componentes.
* O **scroll do texto da cena é obrigatório**.

---

# Contrato do GameplayScreen (orquestrador)

## Responsabilidades

* Controlar o ciclo de vida da tela (`enter` / `leave`) sem duplicar widgets.
* Manter o estado do jogo:

  * `player_stats`
  * `scene_text`
  * `scene_image_path`
  * `actions` (lista de ações)
* Conectar eventos (cliques) às mudanças de estado.
* Chamar as APIs dos módulos para refletir mudanças na UI.

## Não-responsabilidades

* Não montar manualmente toda a UI (evitar construir a tela inteira em `on_enter`).
* Não deve conter lógica de layout detalhada (isso é do KV).

---

# Módulo 1 — StatusPanel (STATUS)

## Responsabilidades

* Renderizar e atualizar os indicadores:

  * Sono
  * Energia
  * Foco
  * Estresse
* Exibir **label + barra (0–100)**.
* Atualizar valores **sem reconstruir widgets**.

## API pública (contrato)

* `set_stats(stats)` → recebe objeto/estrutura com os 4 valores.
* `refresh()` → força re-render dos números/barras a partir do estado atual.

## Regras

* Valores devem ser **clampados em 0..100** (se necessário, pode ser feito no orquestrador).
* Não dispara eventos de jogo; **apenas exibe**.

---

# Módulo 2 — ScenePanel (CENA)

## Responsabilidades

* Renderizar:

  * Texto da cena (com `ScrollView`)
  * Imagem da cena (opcional)
* Atualizar texto e imagem **sem reconstruir o layout**.

## API pública (contrato)

* `set_text(text: str)`
* `set_image(path: str | None)`

  * `None` ou `""` significa “sem imagem”
* (opcional) `refresh()` caso mantenha estado interno

## Regras

* Texto deve quebrar e respeitar área disponível.
* **Scroll vertical obrigatório**.
* Imagem deve manter proporção.

---

# Módulo 3 — ActionsPanel (AÇÕES)

## Responsabilidades

* Renderizar lista de ações como botões.
* Disparar callback do jogo quando uma ação for selecionada.

## API pública (contrato)

* `set_actions(actions)` onde `actions` é uma lista de itens:

  * `label: str`
  * `callback: callable`
* `clear_actions()` (opcional)

## Regras

* Este módulo **não decide o efeito da ação**. Apenas executa callback.
* Botões devem suportar múltiplas ações sem “vazar binds” antigos.

---

# Teclado (fora da Sprint 1 / Sprint 2+)

* Suporte a “1..9” pode ser adicionado depois.
* Contrato futuro: `bind_keys(enabled=True)` ou suporte via `GameplayScreen`.

---

# Contrato KV (ids e encaixe)

## Obrigatório no `gameplay.kv`

* Deve existir um container raiz com **3 regiões**, com **ids estáveis** para injeção/lookup:

  * `status_area`
  * `scene_area`
  * `actions_area`

**Regra:** o `GameplayScreen` injeta/instancia os módulos nessas áreas **ou** referencia widgets já declarados no KV.

---

## Parte II — Contrato de Dados Narrativos

# Contrato de Dados — Cena (SceneData)

## Objetivo

Padronizar o que um capítulo deve fornecer para renderizar uma cena: **texto, imagem, ações e efeitos**.

Esse contrato permite:

* UI modular (`ScenePanel` / `StatusPanel` / `ActionsPanel`)
* capítulos independentes de UI
* evolução incremental (inventário, flags, sanidade, memória etc.)

---

# Estrutura mínima (Sprint 1)

Uma cena deve ser representada por um **objeto/dict**.

## Campos obrigatórios

* **id: str**
  Identificador único dentro do capítulo. Ex: `intro`, `street_01`.

* **text: str**
  Texto já pronto para exibição (pode ser carregado de arquivo `.txt`).

## Campos opcionais

* **image: str | ""**
  Caminho da imagem da cena. Vazio significa “sem imagem”.

* **actions: list[ActionData]**
  Lista de ações exibidas no `ActionsPanel`.

* **effects: EffectsData**
  Alterações nos status aplicadas ao escolher uma ação.

* **next: str | None**
  Próxima cena padrão em fluxo linear.

---

# ActionData (ações)

Cada ação é um item com:

## Campos obrigatórios

* **key: str**
  Tecla/atalho lógico (futuro teclado 1..9).

* **label: str**
  Texto do botão exibido ao jogador.

## Campos opcionais

* **goto: str | None**
  ID da cena destino.

* **effects: EffectsData | None**
  Efeitos aplicados ao escolher a ação.

* **hint: str | None**
  Intuição subjetiva apresentada antes da escolha.

* **conditions: dict | None (Sprint 2+)**
  Regras para mostrar/bloquear ação.

**Regra:** UI não interpreta `goto`, `effects` nem `hint`. Isso é responsabilidade do `GameplayScreen`.

---

# EffectsData (efeitos)

Efeitos são **deltas**, nunca valores absolutos:

* `sono: int`
* `energia: int`
* `foco: int`
* `estresse: int`

**Regra:** clamp `0..100` ocorre no `GameplayScreen`.

---

# Fluxo de responsabilidades

## Chapters (fonte de verdade)

* Definem e retornam `SceneData`
* Carregam textos (`ascii/*.txt`)
* Definem imagens, ações, hints e efeitos

## GameplayScreen (orquestrador)

* Mantém `player_stats` e `current_scene_id`
* Solicita `SceneData` ao registry
* Atualiza UI via APIs dos painéis
* Exibe hint antes da execução da ação
* Aplica efeitos e transições de cena

## UI Widgets

* Apenas exibem conteúdo
* Não conhecem capítulos nem regras

---

# Contrato de Manifest (alinhado ao manifest.json)

Estrutura sugerida:

* `id`
* `text_file` (opcional)
* `text` (opcional)
* `image` (opcional)
* `actions`

O `registry.py`:

* lê o manifest
* carrega textos
* retorna `SceneData` pronto

---

## Parte III — Design Narrativo, Ações e Hints

# Capítulos, Ações e Hints

## Visão geral

No **Detetive John**, capítulos controlam a experiência narrativa.
A UI é apenas um meio de exibição e **nunca decide nada**.

Tudo que o jogador **vê**, **escolhe** e **sente** vem do **capítulo**.

---

## O que é um Capítulo

Um capítulo é uma pasta **autocontida**:

```
src/jogo/chapters/chapter_xx/
```

Contém:

* `manifest.json`
* textos (`ascii/*.txt`)
* imagens (opcional)

O capítulo descreve:

* o que acontece
* quais escolhas existem
* quais consequências são aplicadas

---

## Estrutura mental

Um capítulo é um **grafo de cenas**:

```
Cena A
 ├─ ação 1 → Cena B
 ├─ ação 2 → Cena C
 └─ ação 3 → Cena A (loop, custo psicológico)
```

Não existe cena correta.
Existe **cena alcançada**.

---

## Hint — a intuição de John

O **hint** é uma dica curta, subjetiva e não confiável.

Ele:

* aparece antes da ação
* orienta emocionalmente
* cria tensão

Exemplos:

* “A rua está silenciosa demais.”
* “O corpo pede descanso. A cidade não espera.”

O hint **não explica regras**. Ele **provoca dúvida**.

---

## Regras de ouro

### Faça

* use hints em decisões ambíguas
* use efeitos sutis e cumulativos
* permita loops e hesitação

### Evite

* escolhas boas vs ruins
* consequências óbvias
* texto didático

---

# Versionamento e Critérios de Pronto

## Tag 0.2.0 — UI Estável

A tag **0.2.0** representa a estabilização da UI:

* Gameplay abre e fecha sem duplicar UI
* Layout KV consolidado
* Status, Cena e Ações renderizam corretamente

---

## Tag 0.2.1 — Ajustes e Refinamentos

A tag **0.2.1** representa ajustes incrementais:

* Correções visuais e de layout
* Ajustes de fluxo interno
* Pequenas melhorias sem quebra de contrato

---

## Tag 0.2.2 — Consolidação de Contratos

A tag **0.2.2** pode ser criada quando:

* Status reflete mudanças corretamente
* Cena atualiza texto e imagem sem rebuild
* Ações executam fluxo completo (**hint → efeito → transição**)
* Contratos de dados (SceneData, ActionData, EffectsData) estão estáveis
