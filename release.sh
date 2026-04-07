#!/bin/bash
# InfiniteClaud — Auto Release Script
# Uso: bash release.sh patch|minor|major "descrição da mudança"
# Gera changelog, bump versão, commit e push automaticamente.

set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_JSON="$PLUGIN_DIR/.claude-plugin/plugin.json"
CHANGELOG="$PLUGIN_DIR/CHANGELOG.md"

# Cores
GOLD='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# --- Validação ---
if [[ $# -lt 2 ]]; then
  echo -e "${RED}Uso: bash release.sh <patch|minor|major> \"descrição\"${NC}"
  echo "  patch = bug fix (1.0.0 → 1.0.1)"
  echo "  minor = nova feature (1.0.0 → 1.1.0)"
  echo "  major = breaking change (1.0.0 → 2.0.0)"
  exit 1
fi

BUMP_TYPE="$1"
DESCRIPTION="$2"

# --- Ler versão atual ---
CURRENT_VERSION=$(jq -r '.version' "$PLUGIN_JSON")
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# --- Calcular nova versão ---
case "$BUMP_TYPE" in
  patch) PATCH=$((PATCH + 1)) ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  *) echo -e "${RED}Tipo inválido: $BUMP_TYPE (use patch, minor ou major)${NC}"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
DATE=$(date +"%Y-%m-%d")

echo -e "${GOLD}⚡ InfiniteClaud Release${NC}"
echo -e "  Versão: ${RED}$CURRENT_VERSION${NC} → ${GREEN}$NEW_VERSION${NC}"
echo -e "  Tipo: $BUMP_TYPE"
echo -e "  Descrição: $DESCRIPTION"
echo ""

# --- Atualizar plugin.json ---
echo -e "${GOLD}1. Atualizando versão em plugin.json...${NC}"
tmp=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"

# --- Gerar changelog ---
echo -e "${GOLD}2. Gerando changelog...${NC}"

# Buscar commits desde último tag (ou todos se não houver tag)
LAST_TAG=$(git -C "$PLUGIN_DIR" describe --tags --abbrev=0 2>/dev/null || echo "")

if [[ -n "$LAST_TAG" ]]; then
  COMMITS=$(git -C "$PLUGIN_DIR" log "$LAST_TAG"..HEAD --oneline --no-merges 2>/dev/null || echo "")
else
  COMMITS=$(git -C "$PLUGIN_DIR" log --oneline --no-merges -20 2>/dev/null || echo "")
fi

# Categorizar commits
FEATURES=""
FIXES=""
OTHER=""

while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  hash=$(echo "$line" | cut -d' ' -f1)
  msg=$(echo "$line" | cut -d' ' -f2-)

  if echo "$msg" | grep -qiE "^feat"; then
    FEATURES="$FEATURES\n- $msg"
  elif echo "$msg" | grep -qiE "^fix"; then
    FIXES="$FIXES\n- $msg"
  else
    OTHER="$OTHER\n- $msg"
  fi
done <<< "$COMMITS"

# Montar entrada do changelog
ENTRY="## [$NEW_VERSION] — $DATE\n\n**$DESCRIPTION**\n"

[[ -n "$FEATURES" ]] && ENTRY="$ENTRY\n### Features\n$FEATURES\n"
[[ -n "$FIXES" ]] && ENTRY="$ENTRY\n### Fixes\n$FIXES\n"
[[ -n "$OTHER" ]] && ENTRY="$ENTRY\n### Other\n$OTHER\n"

# Criar ou atualizar CHANGELOG.md
if [[ ! -f "$CHANGELOG" ]]; then
  echo -e "# InfiniteClaud Changelog\n\n$ENTRY" > "$CHANGELOG"
else
  # Inserir nova entrada após o título
  tmp=$(mktemp)
  echo -e "# InfiniteClaud Changelog\n\n$ENTRY" > "$tmp"
  tail -n +3 "$CHANGELOG" >> "$tmp"
  mv "$tmp" "$CHANGELOG"
fi

echo -e "${GREEN}  Changelog atualizado${NC}"

# --- Sync para ~/.claude/automation (instalação local) ---
echo -e "${GOLD}3. Sincronizando com instalação local...${NC}"
INSTALL_DIR="$HOME/.claude/automation"
if [[ -d "$INSTALL_DIR" ]]; then
  cp "$PLUGIN_DIR/scripts/server.py" "$INSTALL_DIR/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/state.py" "$INSTALL_DIR/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/config.json" "$INSTALL_DIR/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/tools/"*.py "$INSTALL_DIR/tools/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/router/"* "$INSTALL_DIR/router/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/dashboard/app.py" "$INSTALL_DIR/dashboard/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/dashboard/api/"*.py "$INSTALL_DIR/dashboard/api/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/dashboard/static/"* "$INSTALL_DIR/dashboard/static/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/telegram/bot.py" "$INSTALL_DIR/telegram/" 2>/dev/null || true
  cp "$PLUGIN_DIR/scripts/telegram/memory.py" "$INSTALL_DIR/telegram/" 2>/dev/null || true
  echo -e "${GREEN}  Instalação local sincronizada${NC}"
fi

# --- Git commit + tag + push ---
echo -e "${GOLD}4. Commit + tag + push...${NC}"
cd "$PLUGIN_DIR"
git add -A
git commit -m "release: v$NEW_VERSION — $DESCRIPTION"
git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION: $DESCRIPTION"
git push origin master
git push origin "v$NEW_VERSION"

echo ""
echo -e "${GREEN}✅ Release v$NEW_VERSION publicada!${NC}"
echo ""
echo -e "  📦 Plugin: v$NEW_VERSION"
echo -e "  📝 Changelog: $CHANGELOG"
echo -e "  🏷️  Tag: v$NEW_VERSION"
echo -e "  🚀 Push: origin/master"
echo ""
echo -e "  Usuários atualizam com: ${GOLD}claude plugin update infiniteclaud${NC}"
