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

## 🚀 Lançamento de Apps Lovable em App Stores

**Guia completo para publicar aplicativos construídos com Lovable no Google Play Store e Apple App Store**

### 📋 Resumo Executivo

Este guia fornece instruções profissionais para transformar um projeto Lovable em um aplicativo nativo publicado nas lojas de apps. 

**Timeline esperada:** 2-6 semanas (incluindo desenvolvimento, testes, certificados e aprovações)

**Custos:**
- **Google Play Store:** US$ 25 (taxa única de registro)
- **Apple App Store:** US$ 99/ano (Apple Developer Program)
- **Comissões:** 30% na Play Store | 30% na App Store (ambas com opções de redução a 15% para pequenos negócios)

---

### ⚠️ Importante: Lovable → Nativo

**Limitação crítica:** Lovable gera aplicativos web (React DOM/HTML/CSS), não código nativo. Para publicar na Play Store/App Store, você **precisa empacotar** seu app web em um wrapper nativo.

**Soluções recomendadas:**

1. **Capacitor** (Recomendado)
   - Converte seu app Lovable em APK/IPA
   - Mantém performance de web app
   - Acesso a APIs nativas (câmera, GPS, notificações)
   - Documentação: [https://capacitorjs.com/](https://capacitorjs.com/)

2. **Alternativas (True Native)**
   - **Newly** - "O Lovable para Mobile" com React Native
   - **Natively** - Cria apps nativos via IA
   - **Median** - Converte websites em apps nativos

Para este guia, usaremos **Capacitor** por ser a mais flexível e bem documentada.

---

### ✅ Pré-Requisitos (Obrigatório)

Antes de começar, tenha pronto:

| Item | Play Store | App Store |
|------|-----------|-----------|
| **Conta Developer** | Google Account | Apple Account com 2FA |
| **Taxa Inicial** | US$ 25 | US$ 99/ano |
| **Identidade Legal** | ID válido | Legal binding authority |
| **Certificados** | Keystore `.jks` | Provisioning profiles (.p8) |
| **Dispositivo Teste** | Android 5.0+ | iPhone/iPad com iOS 13+ |
| **Código-fonte** | Lovable + Capacitor wrapper | Lovable + Capacitor wrapper |
| **Documentos** | Política de Privacidade, Termos | Privacy Policy, EULA |
| **Imagens** | 512x512 icon, screenshots | App icon, previews, screenshots |

**Documentação necessária (ambas lojas):**
- ✅ Política de Privacidade (URL pública)
- ✅ Termos de Serviço
- ✅ Descrição clara do app
- ✅ Screenshots em português (se BR)

---

### 🔧 Configuração Inicial com Capacitor

#### Passo 1: Configurar Projeto

```bash
# Instalar Capacitor globalmente
npm install -g @capacitor/cli

# No seu projeto Lovable clonado/exportado:
npm install @capacitor/core @capacitor/cli

# Inicializar Capacitor
npx cap init com.yourcompany.lovableapp "Lovable App"
```

#### Passo 2: Configurar Plataformas

```bash
# Adicionar plataformas
npx cap add android
npx cap add ios

# Build seu projeto Lovable (gera /dist)
npm run build

# Sincronizar com plataformas nativas
npx cap sync
```

#### Passo 3: Configurar `capacitor.config.json`

Veja exemplo completo em `examples/capacitor.config.json`. Configurações essenciais:

```json
{
  "appId": "com.yourcompany.lovableapp",
  "appName": "Lovable App",
  "webDir": "dist",
  "plugins": {
    "FirebaseMessaging": {
      "senderId": "YOUR_SENDER_ID"
    }
  }
}
```

---

### 📱 Google Play Store - Passo a Passo

#### 1. Criar Conta Google Play Developer

1. Acesse [Google Play Console](https://play.google.com/console)
2. Clique em **"Create account"**
3. Pague taxa única de **US$ 25**
4. Complete o perfil do desenvolvedor
5. Ative 2-Step Verification na Google Account

#### 2. Preparar APK/AAB Assinado

```bash
# Gerar keystore (GUARDE BEM - precisa para updates)
keytool -genkey -v -keystore keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key

# Build APK assinado (via Gradle)
./gradlew bundleRelease

# Resultado: app/build/outputs/bundle/release/app-release.aab
```

**Arquivo a usar:** `app-release.aab` (Android App Bundle - formato moderno obrigatório)

Ver configuração completa em `examples/gradle-config.example`

#### 3. Criar App no Play Console

1. Clique **"Create App"**
2. Digite nome do app
3. Escolha categoria (e.g., Produtividade)
4. Tipo de app: **"Application"**
5. Confirme se tem acesso a device testing

#### 4. Preencher Detalhes da Loja

**Aba: App details**
- App name: "Meu App Lovable"
- Short description: Máx 80 caracteres
- Full description: Máx 4000 caracteres
- URL Homepage (link ao site/Lovable)

**Aba: Graphics**
- App icon: 512×512px PNG
- Feature graphic: 1024×500px
- Screenshots: Mín 2, máx 8 (1080×1920px)

**Aba: Categorias & Conteúdo**
- Categoria principal
- Classificação etária
- Permissões solicitadas (câmera, localização, etc)

#### 5. Configurar Privacidade & Políticas

- URL Política Privacidade: `https://yoursite.com/privacy`
- Email contato: seu@email.com
- Declarar dados coletados (analytics, ads, etc)

#### 6. Setup Preços & Distribuição

**Aba: Pricing & distribution**
- País/região (escolha onde vender)
- Preço: Gratuito ou pago
- Conteúdo: Escolha apropriado para idade

#### 7. Submeter para Revisão

1. Na aba **"Release"** → **"Create new release"**
2. Upload `app-release.aab`
3. Nota interna (para suas referências)
4. Clique **"Review release"** → **"Start rollout to production"**

**Tempo de aprovação:** 4-24 horas geralmente

---

### 🍎 Apple App Store - Passo a Passo

#### 1. Criar Conta Apple Developer

1. Acesse [Apple Developer Program](https://developer.apple.com/programs/)
2. Clique **"Enroll"**
3. Use Apple ID com 2-Factor Authentication **obrigatório**
4. Complete verificação de identidade
5. Pague **US$ 99/ano**
6. Aceite Developer Agreement & Policies

#### 2. Gerar Certificados & Provisioning Profiles

**Via Xcode (recomendado):**

1. Abra Xcode → Preferences → Accounts
2. Clique seu Apple ID → Manager Certificates
3. Clique **"+"** → **"iOS App Development"** ou **"iOS Distribution"**

**Via App Store Connect (alternativa):**

1. Acesse [App Store Connect](https://appstoreconnect.apple.com/)
2. Certificates, Identifiers & Profiles
3. Crie certificado `.p8` (válido 5 anos)

#### 3. Preparar IPA Assinado

```bash
# Atualizar versão em Info.plist
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString 1.0.0" \
  ios/App/App/Info.plist

# Build para archive
xcodebuild -workspace ios/App/App.xcworkspace \
  -scheme App -configuration Release \
  -archivePath build/App.xcarchive archive

# Exportar IPA
xcodebuild -exportArchive \
  -archivePath build/App.xcarchive \
  -exportOptionsPlist ios/export-options.plist \
  -exportPath build/ipa
```

Ver configuração completa em `examples/plist-config.example`

**Arquivo resultante:** `build/ipa/App.ipa`

#### 4. Criar Aplicativo no App Store Connect

1. Acesse [App Store Connect](https://appstoreconnect.apple.com/)
2. **My Apps** → **"+"** → **"New App"**
3. Platform: **iOS**
4. Nome do bundle: `com.yourcompany.lovableapp` (deve corresponder ao certificado)
5. SKU: Código único (ex: `LOVABLE_APP_001`)

#### 5. Preencher Informação do App

**Aba: App Information**
- Nome do app
- Subtítulo (máx 30 caracteres)
- Categoria primária
- Texto de privacidade

**Aba: Pricing & Availability**
- Grátis ou pago (preço em USD → converte para outras moedas)
- Disponibilidade em países
- Data de lançamento

**Aba: App Preview & Screenshots**
- Videos demo (máx 30s, obrigatório)
- Screenshots (2-5 por dispositivo: iPhone 6.5", iPhone 5.5", iPad)
- Tamanho: 1242×2688px ou 2048×1536px (iPad)

**Aba: Description**
- Descrição (máx 4000 caracteres)
- Palavras-chave (máx 100 caracteres)
- Support URL
- Privacy URL
- Homepage URL

#### 6. Configurar Avaliações & Conteúdo

- Age Rating: Responda questionário
- Permissões (câmera, localização, etc)
- Completude do app (funciona offline?)

#### 7. Fazer Upload do IPA

**Opção A: Xcode (recomendado)**
```bash
xcodebuild -exportArchive \
  -archivePath build/App.xcarchive \
  -exportOptionsPlist ios/export-options.plist \
  -exportPath . \
  -allowProvisioningUpdates
```

**Opção B: Transporter (via App Store Connect)**
1. Download: [Apple Transporter](https://apps.apple.com/app/transporter/id1450874784)
2. Login com Apple ID
3. Arraste IPA na janela
4. Upload automático

#### 8. Submeter para Revisão

1. **Version Release** → Escolha **"Automatic release"** ou **"Manual release"**
2. Clique **"Submit for Review"**
3. Responda pergunta final sobre compliance

**Tempo de aprovação:** 24-48 horas (às vezes até 5 dias)

---

### 🤖 Automação com /InfiniteClaud

Use o plugin InfiniteClaud para automatizar todo o processo:

```bash
# Usar o script de assinatura
/InfiniteClaud execute ./examples/sign-and-deploy.sh android 1.0.0
/InfiniteClaud execute ./examples/sign-and-deploy.sh ios 1.0.0

# Validação automática
/InfiniteClaud "Verifique se todos os assets estão pronto para submissão"

# Upload assistido
/InfiniteClaud "Me guie pelo upload do AAB no Play Store"
```

---

### 📊 Integração com Firebase (Opcional mas Recomendado)

Para analytics e push notifications:

```javascript
// Veja: examples/firebase-setup.js

import { initializeApp } from 'firebase/app';
import { getAnalytics, logEvent } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  // ... outras chaves em variáveis de ambiente
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Rastrear eventos
logEvent(analytics, 'app_open');
logEvent(analytics, 'user_signup');
```

---

### ❌ Troubleshooting & Rejeições Comuns

#### Play Store

| Problema | Solução |
|----------|---------|
| "App contém permissões não utilizadas" | Remova permissões não necessárias do `AndroidManifest.xml` |
| "Política de privacidade faltando" | Adicione URL válida e acessível de Privacy Policy |
| "App crashes ao abrir" | Teste em múltiplos dispositivos Android (5.0 a 14.0) |
| "Rejeição: Conteúdo sexual implícito" | Revise imagens/texto; defina classificação correta |
| "Teste de funcionalidade falhou" | Certifique que app funciona offline; testes em WiFi + dados |

#### App Store

| Problema | Solução |
|----------|---------|
| "Guideline 4.2 - Spam" | Remova conteúdo genérico; customize para seu nicho |
| "Guideline 2.1 - Funcionalidade" | App deve ter funcionalidade clara e funcionante |
| "Guideline 5.1 - Conformidade Legal" | Adicione Privacy Policy; respeite GDPR se EU |
| "IPA inválido ou assinatura errada" | Regenere certificados; verifique Bundle ID |
| "Tela branca/crash ao abrir" | Teste em TestFlight com 10+ testers antes de submeter |

**Rejeição? Não se preocupe:**
1. Leia detalhadamente o feedback da Apple/Google
2. Corrija conforme indicado
3. Resubmeta (grátis, sem fila de espera)
4. Contato: support@apple.com ou play-developer-support@google.com

---

### 📋 Checklist Pré-Lançamento

#### Antes de Qualquer Submissão

- [ ] App funciona em múltiplos idiomas (se aplicável)
- [ ] Sem crashes ou bugs críticos
- [ ] Testes completos (links, formulários, APIs)
- [ ] Performance: tempo de abertura < 3s
- [ ] Responsive: testa em tablets e phones
- [ ] Offline: funciona sem internet (estrutura)

#### Antes de Submeter Play Store

- [ ] APK/AAB assinado com keystore válido
- [ ] Versão code incrementada (versionCode++)
- [ ] Screenshots em português (se Brasil)
- [ ] Política de privacidade em URL acessível
- [ ] 3+ screenshots (recomendado 5)
- [ ] Icon 512×512px em PNG
- [ ] Descrição clara em português

#### Antes de Submeter App Store

- [ ] IPA assinado com certificado válido
- [ ] Bundle ID corresponde ao certificado criado
- [ ] Teste em TestFlight com 5+ pessoas
- [ ] Screenshots em 1242×2688px ou 2048×1536px
- [ ] Video preview (máx 30s) ou screenshots
- [ ] Todos os campos preenchidos (nome, descrição, categoria)
- [ ] Privacy Policy em HTTPS público
- [ ] Age rating concluído

#### Documentação

- [ ] Direitos autorais incluídos (Open Source, assets, etc)
- [ ] Licenças de dependências (React, Capacitor, etc)
- [ ] Aviso de coleta de dados (se usar analytics)
- [ ] Contato de suporte válido

---

### 📚 Referências & Recursos

**Documentação Oficial:**
- [Google Play Console Help](https://support.google.com/googleplay)
- [App Store Connect Help](https://help.apple.com/app-store-connect)
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Developer Docs](https://developer.android.com/)
- [Apple Developer Docs](https://developer.apple.com/documentation/)

**Guias Úteis:**
- [Play Store Review Policy](https://play.google.com/about/developer-content-policy/)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Capacitor Android Setup](https://capacitorjs.com/docs/android)
- [Capacitor iOS Setup](https://capacitorjs.com/docs/ios)

**Ferramentas Recomendadas:**
- [Capacitor CLI](https://capacitorjs.com/docs/cli/) - Scaffolding automático
- [Android Studio](https://developer.android.com/studio) - Development Android
- [Xcode](https://developer.apple.com/download/) - Development iOS
- [Firebase Console](https://console.firebase.google.com/) - Analytics & Messaging
- [App Annie](https://www.appannie.com/) - Market Intelligence

**Comunidades:**
- [Capacitor Discord](https://discord.com/invite/4dZx6HBs3z)
- [Stack Overflow - lovable-app](https://stackoverflow.com/questions/tagged/lovable-app)
- [r/AppDev](https://reddit.com/r/AppDev) - Subreddit
- [Dev.to - Mobile](https://dev.to/t/mobile)

---

### 🔐 Segurança - Confidencialidade

⚠️ **IMPORTANTE:** Nunca commite em repositório público:
- `keystore.jks` (Android)
- `.p8` certificates (iOS)
- `.env` com credenciais Firebase/APIs
- Senhas ou API keys

**Use `.gitignore`:**
```
keystore.jks
*.p8
*.env
*.key
ios/export-options.plist
```

---

## Licenca

MIT
