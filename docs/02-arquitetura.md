# Arquitetura Gameplay & Contratos de Dados

> Base para desenvolvimento, expansão e versionamento do jogo.

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

* **conditions: dict | None (Sprint 2+)**
  Regras para mostrar/bloquear ação.

**Regra:** UI não interpreta `goto` nem `effects`. Isso é responsabilidade do `GameplayScreen`.

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
* Carregam textos (ex: `ascii/intro.txt`)
* Definem imagens, ações e efeitos

## GameplayScreen (orquestrador)

* Mantém `player_stats` e `current_scene_id`
* Solicita `SceneData` ao registry
* Atualiza UI via APIs dos painéis
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

# Critérios de pronto — Tag 0.2.0

A tag **0.2.0** pode ser criada quando:

* Gameplay abre e fecha sem duplicar UI.
* Status atualiza corretamente quando stats mudam.
* Cena atualiza texto e imagem sem rebuild completo.
* Ações renderizam corretamente e disparam callbacks funcionais.
