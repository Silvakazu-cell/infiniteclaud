#!/bin/bash
# sign-and-deploy.sh
# Script para assinar e fazer deploy automático de apps Android/iOS
# Uso: ./sign-and-deploy.sh [android|ios] [version]
# Variáveis de ambiente necessárias (não commitar - adicionar a .env):
#   - KEYSTORE_PASSWORD
#   - KEY_ALIAS
#   - KEY_PASSWORD

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funções auxiliares
print_info() {
  echo -e "${GREEN}ℹ${NC} $1"
}

print_error() {
  echo -e "${RED}✗${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

# Validar argumentos
if [ $# -lt 1 ]; then
  print_error "Uso: ./sign-and-deploy.sh [android|ios] [version]"
  echo "  android - Assinar e preparar APK/AAB para Play Store"
  echo "  ios     - Preparar IPA para App Store"
  exit 1
fi

PLATFORM=$1
VERSION=${2:-"1.0.0"}

# Validar plataforma
if [[ ! "$PLATFORM" =~ ^(android|ios)$ ]]; then
  print_error "Plataforma inválida: $PLATFORM"
  exit 1
fi

# Verificar se o keystore existe (apenas Android)
if [ "$PLATFORM" = "android" ] && [ ! -f "keystore.jks" ]; then
  print_error "keystore.jks não encontrado!"
  print_info "Crie um keystore com: keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias release-key"
  exit 1
fi

# ==================== ANDROID ====================
if [ "$PLATFORM" = "android" ]; then
  print_info "Iniciando build Android versão $VERSION..."

  # Verificar variáveis de ambiente
  if [ -z "$KEYSTORE_PASSWORD" ] || [ -z "$KEY_ALIAS" ] || [ -z "$KEY_PASSWORD" ]; then
    print_error "Variáveis de ambiente não definidas!"
    print_info "Defina: KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD"
    exit 1
  fi

  # Limpar build anterior
  print_info "Limpando build anterior..."
  ./gradlew clean

  # Build release
  print_info "Compilando APK assinado..."
  ./gradlew assembleRelease

  # Build AAB (recomendado para Play Store)
  print_info "Compilando AAB assinado..."
  ./gradlew bundleRelease

  # Encontrar arquivos gerados
  APK="app/build/outputs/apk/release/app-release.apk"
  AAB="app/build/outputs/bundle/release/app-release.aab"

  if [ -f "$APK" ]; then
    print_info "✓ APK gerado: $APK"
  else
    print_error "APK não encontrado!"
    exit 1
  fi

  if [ -f "$AAB" ]; then
    print_info "✓ AAB gerado: $AAB"
  else
    print_warning "AAB não encontrado"
  fi

  # Verificar assinatura
  print_info "Verificando assinatura do APK..."
  jarsigner -verify -verbose -certs "$APK" > /dev/null && \
    print_info "✓ APK assinado corretamente" || \
    print_error "Erro na assinatura"

  # Output final
  echo ""
  print_info "Build Android concluído!"
  echo "  Arquivo pronto para submissão:"
  echo "  → $AAB (recomendado para Play Store)"
  echo "  → $APK (alternativa)"

# ==================== iOS ====================
elif [ "$PLATFORM" = "ios" ]; then
  print_info "Preparando build iOS versão $VERSION..."

  # Verificar se Xcode está disponível
  if ! command -v xcodebuild &> /dev/null; then
    print_error "Xcode não encontrado!"
    exit 1
  fi

  # Atualizar versão no Info.plist
  print_info "Atualizando versão para $VERSION..."
  /usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VERSION" ios/App/App/Info.plist

  # Build para Archive
  print_info "Compilando IPA assinado..."
  xcodebuild -workspace ios/App/App.xcworkspace \
    -scheme App \
    -configuration Release \
    -derivedDataPath build \
    -destination generic/platform=iOS \
    -archivePath build/App.xcarchive \
    archive

  # Exportar IPA
  print_info "Exportando IPA..."
  xcodebuild -exportArchive \
    -archivePath build/App.xcarchive \
    -exportOptionsPlist ios/export-options.plist \
    -exportPath build/ipa

  IPA="build/ipa/App.ipa"

  if [ -f "$IPA" ]; then
    print_info "✓ IPA gerado: $IPA"
  else
    print_error "IPA não encontrado!"
    exit 1
  fi

  # Output final
  echo ""
  print_info "Build iOS concluído!"
  echo "  Arquivo pronto para submissão:"
  echo "  → $IPA"
  echo "  Próximo passo: Fazer upload via App Store Connect"
fi

# ==================== PÓS-BUILD ====================
print_info "Processo concluído com sucesso!"
print_info "Próximas ações:"
echo "  1. Revisar arquivo gerado"
echo "  2. Fazer upload na loja respectiva (Play Store / App Store Connect)"
echo "  3. Submeter para revisão"
echo "  4. Acompanhar status de aprovação"
