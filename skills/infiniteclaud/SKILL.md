---
name: InfiniteClaud
description: Use quando quiser ativar o modo de automação InfiniteClaud — ativa o MCP Automation Server com 20 ferramentas, orquestrador inteligente de modelos (Haiku/Sonnet/Opus), dashboard web, e Telegram bot. Agente autônomo completo para executar tarefas no computador.
version: 1.0.0
---

# InfiniteClaud

Agente autônomo completo: 20 ferramentas MCP + orquestrador de modelos + dashboard web + Telegram bot.

## Ao ativar

> **InfiniteClaud ativado.** Ferramentas disponíveis:
>
> **Web (8):** web_navigate, web_click, web_type, web_extract, web_screenshot, web_wait, web_scroll, web_eval
>
> **Filesystem (5):** fs_read, fs_write, fs_list, fs_move, fs_delete
>
> **Nativo macOS (5):** mouse_click, mouse_move, keyboard_type, keyboard_hotkey, screen_screenshot
>
> **Sistema (2):** applescript_run, shell_run
>
> **Model Router:** ativo — Haiku/Sonnet/Opus automático por complexidade

## Model Router (diferencial)

Cada prompt roteado automaticamente:
- Simples → Haiku (5x econômico)
- Código/análise → Sonnet (2x econômico)
- Arquitetura → Opus (quando necessário)

Regras em `~/.claude/automation/router/rules.json`

## Modos de autonomia

- **full** — executa tudo
- **checkpoint** — pausa em ações destrutivas (padrão)
- **plan_first** — mostra plano antes

## Interfaces

- Claude Code: `/InfiniteClaud`
- Dashboard: `python3 ~/.claude/automation/dashboard/app.py` → localhost:8080
- Telegram: `python3 ~/.claude/automation/telegram/bot.py`
