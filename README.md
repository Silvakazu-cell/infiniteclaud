# InfiniteClaud

**Agente autônomo completo para Claude Code** — 50x mais rápido que screenshot-based, 90% menos tokens.

## O que é

Plugin que transforma o Claude Code em um agente de automação completo com:

- **20 ferramentas MCP** — Web (Playwright), Filesystem, macOS nativo (PyAutoGUI), AppleScript, Shell
- **Orquestrador de modelos** — roteia automaticamente entre Haiku/Sonnet/Opus por complexidade
- **Dashboard web** — painel visual em localhost:8080 com modo assistente NLP
- **Telegram bot** — controle remoto do Mac com linguagem natural e aprendizado

## Instalação

```bash
claude plugin install infiniteclaud
```

Ou manualmente:

```bash
git clone https://github.com/douglaskazunari/infiniteclaud.git
cd infiniteclaud
bash setup.sh
```

## Uso

No Claude Code:

```
/InfiniteClaud
```

Depois fale naturalmente:

```
"abra o gmail e me mostre os emails"
"organize os arquivos do Desktop por tipo"
"tire um screenshot e me envie"
"pesquise sobre IA no Google"
```

## vs Claude Cowork

| Aspecto | Cowork | InfiniteClaud |
|---|---|---|
| Velocidade | 2-5s/ação | <100ms/ação |
| Tokens extras | +500/ação | 0 |
| Model routing | Fixo | Haiku/Sonnet/Opus auto |
| Acesso remoto | Nao | Telegram + Dashboard |
| Aprendizado | Nao | Memoria persistente |
| Open source | Nao | Sim |

## Componentes

```
~/.claude/automation/
├── server.py           # MCP Server
├── router/             # Orquestrador de modelos
├── tools/              # 20 ferramentas
├── dashboard/          # Web UI + API REST
└── telegram/           # Bot conversacional
```

## Requisitos

- macOS
- Python 3.10+
- Claude Code com assinatura ativa

## Licenca

MIT
