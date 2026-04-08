# ✅ Checklist: Lançamento em App Stores

Guia prático para não esquecer nenhuma etapa antes de publicar seu app Lovable.

---

## Fase 1: Preparação (Semana 1-2)

### Desenvolvimento & Testes

- [ ] App clonado/exportado do Lovable
- [ ] Capacitor instalado e configurado
- [ ] Build iOS e Android rodando localmente
- [ ] Testado em emulador Android (min API 24)
- [ ] Testado em simulador iOS (min iOS 13)
- [ ] Sem erros ou warnings no console
- [ ] Performance aceitável (< 3s load)
- [ ] Responsive em diferentes tamanhos

### Funcionalidade

- [ ] Todos os links internos funcionam
- [ ] Formulários validam e submetem corretamente
- [ ] APIs externas testadas (backend, APIs terceiros)
- [ ] Notificações/alerts funcionando
- [ ] Teste de fluxo completo do usuário
- [ ] Comportamento offline (se aplicável)
- [ ] Testes em WiFi e dados móveis

### Assets & Conteúdo

- [ ] Logo em alta qualidade (500×500px+)
- [ ] Icon da app 512×512px PNG (transparente ou sólido)
- [ ] Screenshots (mín 2, recomendado 5)
- [ ] Feature graphic/banner para Play Store (1024×500px)
- [ ] Video demo/preview (máx 30s) para App Store
- [ ] Descrição clara e atrativa
- [ ] Palavras-chave/tags relevantes
- [ ] Screenshots em português (se Brasil)

### Documentação Legal

- [ ] Política de Privacidade redigida
- [ ] Privacy Policy em URL pública (HTTPS)
- [ ] Termos de Serviço (se aplicável)
- [ ] Documentação de permissões utilizadas
- [ ] Aviso de coleta de dados (se analytics/ads)
- [ ] Atribuições de open source (Capacitor, React, etc)

---

## Fase 2: Contas & Certificados (Semana 1-3)

### Google Play Store

- [ ] Google Account criada
- [ ] Developer Account criada (US$ 25 pago)
- [ ] 2-Step Verification ativado
- [ ] Google Play Console acessível
- [ ] Perfil de desenvolvedor completo
- [ ] Keystore `.jks` gerado
- [ ] **Keystore armazenado de forma segura** (backup externo)
- [ ] Senha do keystore anotada (em local seguro)

### Apple App Store

- [ ] Apple ID criada com email válido
- [ ] 2-Factor Authentication ativado
- [ ] Developer Program enrollado (US$ 99/ano pago)
- [ ] Apple Agreement & Policies aceito
- [ ] App Store Connect acessível
- [ ] Identidade verificada na Apple
- [ ] Certificados gerados (via Xcode ou App Store Connect)
- [ ] Provisioning Profiles criados
- [ ] **Certificados salvos de forma segura**

---

## Fase 3: Setup App Store (Semana 2-3)

### Google Play Store Setup

- [ ] App criada no Play Console
- [ ] Nome do app finalizado
- [ ] Categoria selecionada
- [ ] Descrição curta (< 80 caracteres)
- [ ] Descrição longa (até 4000 caracteres)
- [ ] Icon 512×512px enviada
- [ ] Screenshots (2-8) enviados
- [ ] Feature graphic enviada
- [ ] Política de Privacidade URL adicionada
- [ ] Email de contato configurado
- [ ] País/região de distribuição selecionado

### Apple App Store Setup

- [ ] App criado no App Store Connect
- [ ] Bundle ID registrado (deve corresponder ao certificado)
- [ ] SKU gerado
- [ ] Nome do app finalizado
- [ ] Subtítulo adicionado (máx 30 caracteres)
- [ ] Categoria primária selecionada
- [ ] Descrição preenchida (até 4000 caracteres)
- [ ] Palavras-chave adicionadas
- [ ] Support URL adicionada
- [ ] Privacy URL adicionada
- [ ] Preço definido (grátis ou valor)
- [ ] Disponibilidade em países selecionada

---

## Fase 4: Compilação & Assinatura (Semana 3)

### Android - APK/AAB Build

- [ ] Versionado incrementado (versionCode++)
- [ ] `build.gradle` configurado corretamente
- [ ] `gradlew bundleRelease` executado com sucesso
- [ ] `app-release.aab` gerado e testado
- [ ] Assinatura verificada: `jarsigner -verify app-release.aab`
- [ ] Backup do keystore feito
- [ ] APK/AAB < 100MB (ou justificado)
- [ ] Nenhum aviso ou erro no build

### iOS - IPA Build

- [ ] Versão incrementada em Info.plist
- [ ] Bundle ID correto em Xcode
- [ ] Equipe/Team selecionada (Apple Developer)
- [ ] Certificado de distribuição selecionado
- [ ] Provisioning Profile válido
- [ ] `xcodebuild archive` executado com sucesso
- [ ] `xcodebuild exportArchive` completou
- [ ] `App.ipa` gerado
- [ ] IPA < 300MB
- [ ] Sem avisos de segurança

---

## Fase 5: Testes Finais (Semana 3-4)

### Android - Teste APK/AAB

- [ ] Instalado em dispositivo/emulador Android real
- [ ] App abre sem crashes
- [ ] Todas funções testadas
- [ ] Botões e navegação funcionam
- [ ] Teclado virtual funciona
- [ ] Performance aceitável
- [ ] Teste em múltiplas versões Android (5.0, 8.0, 12.0, 14.0)
- [ ] Teste em múltiplos dispositivos (phone + tablet)

### iOS - Teste IPA via TestFlight

- [ ] IPA enviada para App Store Connect
- [ ] TestFlight build processado (aguardar 5-20 min)
- [ ] Convites TestFlight enviados (min 5 betatesters)
- [ ] 24h de testes com usuários reais
- [ ] Nenhum crash reportado
- [ ] Feedback positivo recebido
- [ ] App abre sem erros
- [ ] Todas funções verificadas
- [ ] Teste em iPhone + iPad (se aplicável)

### Compliance & Segurança

- [ ] Sem dados sensíveis logados
- [ ] Sem hardcoded credentials/API keys
- [ ] Permissões apenas as necessárias
- [ ] Privacy Policy acessível dentro do app (link)
- [ ] Aviso de coleta de dados (se aplicável)
- [ ] GDPR compliant (se EU/Brasil)
- [ ] Verificação de injeção SQL/XSS

---

## Fase 6: Submissão (Semana 4)

### Google Play Store - Final

- [ ] Todo conteúdo em português (se Brasil)
- [ ] Screenshots alinhados com descrição
- [ ] Screenshots mostram diferencial
- [ ] Nenhuma informação confidencial em screenshots
- [ ] Versão Content Rating completa
- [ ] Permissões justificadas
- [ ] Data de lançamento definida (imediato ou futuro)
- [ ] Clique "Review release" → "Start rollout"
- [ ] Submissão confirmada (vai aparecer em "Under review")

### Apple App Store - Final

- [ ] Todo conteúdo em português (se Brasil)
- [ ] Screenshots em resolução correta (1242×2688 ou 2048×1536)
- [ ] Preview/video demo presente e atrativo
- [ ] Age Rating Questionnaire completo
- [ ] License info preenchido
- [ ] IPA foi testada em TestFlight com sucesso
- [ ] Signingconfig usando Distribution Certificate
- [ ] Clique "Submit for Review"
- [ ] Selecione "Automatic Release" ou "Manual Release"
- [ ] Submissão confirmada

---

## Fase 7: Acompanhamento (Semana 4-6)

### Google Play Store

- [ ] Checkar status diariamente: https://play.google.com/console
- [ ] Fila: "Under review" (4-24h típico)
- [ ] Status atualizado para "Published"? ✓ Sucesso!
- [ ] Rejeitado? Leia feedback, corrija, resubmita
- [ ] 24h após publicação: verificar reviews
- [ ] Primeira semana: monitorar crash rate

### Apple App Store

- [ ] Checkar status diariamente: App Store Connect
- [ ] Status: "Waiting for Review" → "In Review" → "Ready for Sale"
- [ ] Notificação por email quando aprovado
- [ ] Se rejeitado: ler detalhes, corrigir, resubmeter
- [ ] 24h após aprovação: app aparece na loja
- [ ] Primeira semana: monitorar ratings/reviews

### Post-Launch (Primeiras 2 Semanas)

- [ ] Google Play: 500+ installs alcançado?
- [ ] Apple Store: 50+ installs alcançado?
- [ ] Rating médio > 3.5 stars?
- [ ] Responder reviews negativos educadamente
- [ ] Monitorar crash reports (Firebase/App Center)
- [ ] Bug fixes críticos? Deploy imediatamente
- [ ] Analytics configurados (Firebase/Mixpanel)?
- [ ] Promo codes distribuídos para review?

---

## Fase 8: Manutenção Contínua

### Atualizações & Bug Fixes

- [ ] Bug critical → Update ASAP (< 1 dia)
- [ ] Feature request → Próxima versão
- [ ] Cada update: incrementar versionCode (Android) + versionName
- [ ] Cada update: incrementar version em Info.plist (iOS)
- [ ] Changelog escrito e atualizado
- [ ] Release notes preparadas em português

### Monitoramento Contínuo

- [ ] Analytics ativo e monitorado
- [ ] Firebase/Crashlytics configurado
- [ ] Crash rate mantido < 1%
- [ ] Reviews respondidas dentro de 48h
- [ ] User retention metricado
- [ ] Performance monitorada (load time, battery usage)
- [ ] Security updates aplicados (dependências)

### Legal & Compliance

- [ ] Privacy Policy atualizada quando necessário
- [ ] GDPR/LGPD compliance mantido
- [ ] Age rating revisada (se conteúdo muda)
- [ ] Certificados renovados quando próximos de expirar
- [ ] Developer account renovado anualmente (Apple)

---

## ⏰ Timeline Recomendada

```
SEMANA 1-2:  Desenvolvimento, testes locais, assets
SEMANA 2-3:  Contas dev, certificados, setup lojas
SEMANA 3:    Build final, assinatura
SEMANA 3-4:  Testes com TestFlight (iOS), beta testers
SEMANA 4:    Submissão play Store + App Store
SEMANA 4-6:  Aguardando aprovação, acompanhamento
SEMANA 6+:   Post-launch, monitoramento, updates
```

---

## 🚨 Red Flags & Erros Comuns

### Comum no Android

- ❌ APK < não assinado → ✅ Use keystore correto
- ❌ Versão duplicada publicada → ✅ Sempre incrementar versionCode
- ❌ Permissões não utilizadas → ✅ Remova do `AndroidManifest.xml`
- ❌ App crashes em versões antigas → ✅ Teste Android 5.0+
- ❌ Feature graphic errada → ✅ 1024×500px exato

### Comum no iOS

- ❌ Bundle ID mismatch → ✅ Deve ser igual ao certificado
- ❌ Certificado expirado → ✅ Regenere antes de vencer
- ❌ Video preview faltando → ✅ Obrigatório
- ❌ Screenshots erradas → ✅ 1242×2688 ou 2048×1536
- ❌ Sem 2FA no Apple ID → ✅ Ativar antes de começar

### Comum em Ambas

- ❌ Privacy Policy inválida/404 → ✅ URL pública e acessível
- ❌ App funciona apenas com internet → ✅ Deve ter offline support
- ❌ Screenshots genéricas → ✅ Mostre features específicas
- ❌ Description genérica ("my app") → ✅ Ser descritivo e atrativo
- ❌ Sem testes antes de submeter → ✅ TestFlight/Beta testers obrigatório

---

## 📞 Suporte & Help

**Quando rejeitado:**
1. Leia feedback **completamente** da Apple/Google
2. Identifique exatamente qual guideline violou
3. Corrija **apenas** o problema identificado
4. Resubmeta sem aguardar fila (vai pra frente)

**Contatos:**
- Google Play: https://support.google.com/googleplay
- Apple Support: https://developer.apple.com/contact/

**FAQ:**
- "Quanto tempo até aprovação?" - 4-24h Play Store, 24-48h App Store
- "Posso mudar versão entre testes?" - Sim, versões diferentes no TestFlight/beta
- "Quantas tentativas?" - Ilimitado! Resubmeta sem custo
- "Quanto gasto?" - $25 Play + $99 Apple/ano + comissões de vendas (15-30%)
