#!/bin/bash
# InfiniteClaud Model Router — Orquestrador inteligente de modelos
# Classifica o prompt por complexidade e roteia para Haiku/Sonnet/Opus automaticamente.
# Parte integrada do plugin InfiniteClaud.

LOG_FILE="$HOME/.claude/automation/router/route-log.jsonl"
SETTINGS_FILE="$HOME/.claude/settings.json"
RULES_FILE="$HOME/.claude/automation/router/rules.json"

input=$(cat)
prompt_raw=$(echo "$input" | jq -r '.prompt // ""')
prompt=$(echo "$prompt_raw" | tr '[:upper:]' '[:lower:]')

# --- Carregar regras customizáveis ---
# Se rules.json existir, carrega patterns customizados
# Caso contrário, usa os padrões hardcoded
OPUS_PATTERNS="(cod[eo]|program(ar|ação|ming)?|implement|função|function|bug|debug|desenvolv|script|\bapi\b|database|banco de dados|framework|refactor|refatorar|testes?|deploy|\bgit\b|docker|kubernetes|typescript|javascript|python|\brust\b|\bjava\b|react|vue|angular|método|method|algoritmo|algorithm|syntax|lint|\bpackage\b|\bmodule\b|library|biblioteca|\bclass\b|variavel|variable|endpoint|backend|frontend|servidor|server|commit|pull request|\bpr\b|repositorio|repository)"

SONNET_PATTERNS="(anali[sz]|compar|explica|estrateg|plane[jg]|avali|decisão|raciocin|complex|arquitetura|pesquis|investig|filosof|histor|economi|politic|científic|research|design system|argumen|justif|ponderar|pros e contras|vantagens|desvantagens|detalhad|aprofund)"

if [[ -f "$RULES_FILE" ]]; then
  custom_opus=$(jq -r '.opus_patterns // empty' "$RULES_FILE" 2>/dev/null)
  custom_sonnet=$(jq -r '.sonnet_patterns // empty' "$RULES_FILE" 2>/dev/null)
  [[ -n "$custom_opus" ]] && OPUS_PATTERNS="$custom_opus"
  [[ -n "$custom_sonnet" ]] && SONNET_PATTERNS="$custom_sonnet"
fi

# --- Classificação ---
if echo "$prompt" | grep -qE "$OPUS_PATTERNS"; then
  model="opus"
  confidence="0.85"
  reason="tarefa de programação/desenvolvimento"
elif echo "$prompt" | grep -qE "$SONNET_PATTERNS"; then
  model="sonnet"
  confidence="0.80"
  reason="análise/raciocínio complexo"
else
  model="haiku"
  confidence="0.75"
  reason="tarefa simples/conversacional"
fi

# --- Atualizar settings.json ---
tmp=$(mktemp)
if jq --arg model "$model" '.model = $model' "$SETTINGS_FILE" > "$tmp" 2>/dev/null; then
  mv "$tmp" "$SETTINGS_FILE"
else
  rm -f "$tmp"
fi

# --- Log ---
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
prompt_preview="${prompt_raw:0:80}"

log_entry=$(jq -nc \
  --arg ts "$timestamp" \
  --arg preview "$prompt_preview" \
  --arg model "$model" \
  --argjson confidence "$confidence" \
  --arg reason "$reason" \
  '{
    ts: $ts,
    prompt_preview: $preview,
    model_selected: $model,
    confidence: $confidence,
    reason: $reason,
    classified_by: "infiniteclaud-router"
  }' 2>/dev/null) || true

if [[ -n "$log_entry" ]]; then
  mkdir -p "$(dirname "$LOG_FILE")"
  echo "$log_entry" >> "$LOG_FILE"
fi

# --- Resposta ao Claude Code ---
echo "{\"systemMessage\": \"⚡ InfiniteClaud Router → $model ($reason)\"}"
