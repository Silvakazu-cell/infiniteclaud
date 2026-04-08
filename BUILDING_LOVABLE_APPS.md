# 🎯 Guia: Usando InfiniteClaud para Construir Apps com Lovable

Este documento explica como usar o **InfiniteClaud** e seus exemplos para criar e publicar um app Lovable nas App Stores.

---

## ⚠️ Clarificação Importante

**Este repositório (InfiniteClaud) é:**
- ✅ Um plugin/MCP server para automação no Claude Code
- ✅ Um guia completo de publicação em app stores
- ✅ Exemplos prontos de configuração (gradle, plist, Capacitor)
- ❌ NÃO é um app final para publicar direto nas lojas

**Para publicar um app:**
1. Criar um novo repositório com sua app Lovable
2. Usar este repositório como **referência e template**
3. Seguir o checklist em `docs/app-store-checklist.md`
4. Usar exemplos em `examples/` como base

---

## 📋 Passo 1: Entender a Estrutura

### Este Repositório (InfiniteClaud)
```
infiniteclaud/
├── README.md                    # Plugin documentation + Launch Guide
├── .gitignore                   # Security rules (obrigatório)
├── LICENSE                      # MIT license
├── examples/                    # Exemplo de configurações
│   ├── gradle-config.example    # Android build
│   ├── plist-config.example     # iOS config
│   ├── capacitor.config.json    # Capacitor setup
│   ├── firebase-setup.js        # Analytics integration
│   └── sign-and-deploy.sh       # Build automation
├── docs/
│   └── app-store-checklist.md   # 80+ item checklist
├── scripts/                     # InfiniteClaud implementation
└── skills/                      # Claude skills
```

### Seu Novo App (criar novo repositório)
```
my-lovable-app/
├── src/                         # Your React/Lovable code
├── public/                      # Static assets
├── package.json
├── capacitor.config.json        # ← copiar de examples/
├── android/                     # ← npx cap add android
├── ios/                         # ← npx cap add ios
├── docs/
│   └── app-store-checklist.md   # ← copiar de infiniteclaud/
├── .gitignore                   # ← copiar de infiniteclaud/
└── LICENSE
```

---

## 🚀 Passo 2: Criar Novo App

### Opção A: Do Zero com Vite + React

```bash
# Criar novo projeto
npm create vite@latest my-lovable-app -- --template react
cd my-lovable-app

# Instalar dependências
npm install

# Adicionar Capacitor
npm install @capacitor/core @capacitor/cli
npm install @capacitor/android @capacitor/ios

# Build inicial
npm run build

# Inicializar Capacitor
npx cap init com.yourcompany.myapp "My Lovable App"

# Adicionar plataformas
npx cap add android
npx cap add ios

# Sincronizar
npx cap sync
```

### Opção B: Clonar seu Projeto Lovable

```bash
# Se você tem um projeto Lovable exportado
git clone <seu-repo-lovable> my-lovable-app
cd my-lovable-app

# Seguir os mesmos passos acima (instalar Capacitor, etc)
```

---

## 📝 Passo 3: Copiar Configurações do InfiniteClaud

### 1. Copiar .gitignore
```bash
cp ../infiniteclaud/.gitignore ./
```

### 2. Copiar Checklist
```bash
mkdir -p docs
cp ../infiniteclaud/docs/app-store-checklist.md ./docs/
```

### 3. Copiar Exemplos
```bash
cp ../infiniteclaud/examples/capacitor.config.json ./
cp ../infiniteclaud/examples/sign-and-deploy.sh ./scripts/
chmod +x ./scripts/sign-and-deploy.sh
```

### 4. Copiar Firebase Setup
```bash
mkdir -p src/config
cp ../infiniteclaud/examples/firebase-setup.js ./src/config/
```

### 5. Personalizar capacitor.config.json
```json
{
  "appId": "com.yourcompany.myapp",        // ← seu app ID
  "appName": "Meu App Incrível",           // ← seu nome
  "webDir": "dist",
  "plugins": {
    "FirebaseMessaging": {
      "senderId": "YOUR_SENDER_ID"         // ← seu Firebase ID
    }
  }
}
```

---

## ⚙️ Passo 4: Configurar Build

### Android: build.gradle

Copiar estrutura de `examples/gradle-config.example`:

```gradle
android {
    namespace "com.yourcompany.myapp"    // ← seu app ID
    compileSdk 34
    
    defaultConfig {
        applicationId "com.yourcompany.myapp"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }
}
```

### iOS: Info.plist

Usar como referência `examples/plist-config.example`:

```xml
<key>CFBundleName</key>
<string>Meu App</string>
<key>CFBundleIdentifier</key>
<string>com.yourcompany.myapp</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
```

---

## 🔐 Passo 5: Segurança

### Criar .env para credenciais

```bash
# .env (nunca commitar!)
REACT_APP_FIREBASE_API_KEY=xxxxx
REACT_APP_FIREBASE_PROJECT_ID=xxxxx
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=xxxxx
KEYSTORE_PASSWORD=sua_senha_segura
KEY_ALIAS=release-key
KEY_PASSWORD=sua_senha_segura
```

### Adicionar ao .gitignore
```bash
echo ".env" >> .gitignore
echo "keystore.jks" >> .gitignore
echo "*.p8" >> .gitignore
```

---

## 📦 Passo 6: Gerar Keystores & Certificados

### Android Keystore

```bash
keytool -genkey -v -keystore keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key \
  -storepass $KEYSTORE_PASSWORD \
  -keypass $KEY_PASSWORD \
  -dname "CN=Seu Nome, O=Sua Empresa, L=Cidade, ST=Estado, C=BR"

# Backup em local seguro (fora do repo!)
cp keystore.jks ~/.local/backup/keystore-myapp.jks.bak
```

### Apple Certificates

Seguir as instruções em `README.md` seção **Apple App Store - Passo 2**.

---

## 🧪 Passo 7: Testar Localmente

### Android Emulator
```bash
npx cap open android
# No Android Studio: Run → Run 'App'
```

### iOS Simulator
```bash
npx cap open ios
# No Xcode: Product → Run
```

### Sync de Mudanças
```bash
npm run build
npx cap sync
```

---

## ✅ Passo 8: Pre-Launch Checklist

Usar `docs/app-store-checklist.md`:

- [ ] Fase 1: Desenvolvimento & Testes (Semana 1-2)
- [ ] Fase 2: Contas & Certificados (Semana 1-3)
- [ ] Fase 3: Setup App Store (Semana 2-3)
- [ ] Fase 4: Compilação & Assinatura (Semana 3)
- [ ] Fase 5: Testes Finais (Semana 3-4)
- [ ] Fase 6: Submissão (Semana 4)
- [ ] Fase 7: Acompanhamento (Semana 4-6)
- [ ] Fase 8: Manutenção Contínua

---

## 🚀 Passo 9: Build para Produção

### Android AAB (recomendado)

```bash
./scripts/sign-and-deploy.sh android 1.0.0
# Resultado: app/build/outputs/bundle/release/app-release.aab
```

### iOS IPA

```bash
./scripts/sign-and-deploy.sh ios 1.0.0
# Resultado: build/ipa/App.ipa
```

---

## 📤 Passo 10: Submeter nas Lojas

### Google Play Store

1. Acesse: https://play.google.com/console
2. Create App
3. Upload `app-release.aab`
4. Preencher descrição, screenshots, etc
5. Submeter para review (4-24h)

### Apple App Store

1. Acesse: https://appstoreconnect.apple.com
2. My Apps → New App
3. Upload `App.ipa` via Transporter ou Xcode
4. Preencher descrição, screenshots, video
5. Submeter para review (24-48h)

Veja instruções detalhadas em `README.md` - seção **🚀 Lançamento de Apps Lovable**.

---

## 🆘 Troubleshooting

### "Module not found: Capacitor"
```bash
npm install @capacitor/core @capacitor/cli
npm install @capacitor/android @capacitor/ios
npm run build
npx cap sync
```

### "Versão de gradle incompatível"
```bash
# Atualizar gradle wrapper
./gradlew wrapper --gradle-version=latest
```

### "iOS deployment target mismatch"
```bash
# No Xcode:
# Build Settings → iOS Deployment Target → 13.0+
```

### "Firebase initialization error"
```bash
# Verificar .env file
# Copiar credenciais corretas de Firebase Console
```

---

## 📚 Referências Rápidas

| Recurso | Link |
|---------|------|
| Capacitor Docs | https://capacitorjs.com/ |
| React Guide | https://react.dev/ |
| Firebase Docs | https://firebase.google.com/docs |
| Play Store Console | https://play.google.com/console |
| App Store Connect | https://appstoreconnect.apple.com |
| Android Studio | https://developer.android.com/studio |
| Xcode | https://developer.apple.com/xcode/ |

---

## 💡 Tips & Tricks

### Usar InfiniteClaud para Automação

```bash
/InfiniteClaud
"Valide o app-store-checklist.md do meu projeto"
"Faça o build Android e prepare para submissão"
"Verifique se há vulnerabilidades em node_modules"
```

### Monitoramento Contínuo

```bash
# Acompanhar download/reviews
/InfiniteClaud
"Acesse Play Console e verifique o status da minha app"
"Mostre o últimos reviews no App Store"
```

---

## 📋 Próximos Passos

1. ✅ Criar novo repositório
2. ✅ Inicializar com Lovable/React code
3. ✅ Adicionar Capacitor
4. ✅ Copiar configs do InfiniteClaud
5. ✅ Criar contas developer (Play + Apple)
6. ✅ Gerar keystores & certificados
7. ✅ Testar em emuladores
8. ✅ Preencher app store details
9. ✅ Submeter para aprovação
10. ✅ Monitorar & manter

---

**Dúvidas?** Veja `README.md` seção **🚀 Lançamento de Apps Lovable** para instruções detalhadas!
