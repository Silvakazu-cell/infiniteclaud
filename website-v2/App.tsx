import { useState, useEffect } from 'react'
import './App.css'

export default function App() {
  const [scrollY, setScrollY] = useState(0)
  const [tokensNormal, setTokensNormal] = useState(0)
  const [tokensOptimized, setTokensOptimized] = useState(0)
  const [selectedUseCase, setSelectedUseCase] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'costs' | 'speed'>('overview')
  const [speedNormal, setSpeedNormal] = useState(0)
  const [speedOptimized, setSpeedOptimized] = useState(0)
  const [selectedSetupStep, setSelectedSetupStep] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    const duration = 2000
    const startTime = Date.now()
    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      setTokensNormal(Math.floor(progress * 125000))
      setTokensOptimized(Math.floor(progress * 5000))
      setSpeedNormal(Math.floor(progress * 8.2 * 100) / 100)
      setSpeedOptimized(Math.floor(progress * 0.16 * 100) / 100)
      if (progress < 1) requestAnimationFrame(animate)
    }
    animate()
  }, [])

  const useCases = [
    { id: 'analyst', icon: '📊', title: 'Analista de Dados', company: 'Startup Tech', challenge: 'Processava 500K tokens/dia', solution: 'InfiniteClaud + Model Router', results: ['⏱️ 47min → 56s', '💰 -$18k/mês', '🚀 50 análises/dia', '📈 20 arquivos paralelos'], metrics: { speed: '50x', tokens: '-96%', cost: '-$18k' } },
    { id: 'content', icon: '✍️', title: 'Creator de Conteúdo', company: 'Agência Digital', challenge: 'Criava 50 posts/mês manualmente', solution: 'MCP Search + Web Extract', results: ['🎯 300 posts/mês', '⚡ 2h → 2min', '📱 Multi-plataforma', '💡 1.5M impressões'], metrics: { speed: '60x', content: '6x', reach: '1.5M' } },
    { id: 'developer', icon: '👨‍💻', title: 'Engenheiro', company: 'SaaS', challenge: 'Code review = 2.5k tokens/arquivo', solution: 'Model Router Haiku→Sonnet', results: ['🔍 100 reviews/dia', '💎 -87% custo', '✅ 99.2% accuracy', '📚 Docs automática'], metrics: { reviews: '5x', accuracy: '99.2%', cost: '-87%' } },
    { id: 'researcher', icon: '🔬', title: 'Pesquisador', company: 'Universidade', challenge: '500 papers/mês = 1.2M tokens', solution: 'Web Extract + Paralelo', results: ['📖 50 papers/3min', '🎓 Padrões automáticos', '💰 0 custo de curadoria', '📊 Relatórios auto'], metrics: { papers: '50x', time: '-97%', cost: '-100%' } },
    { id: 'pm', icon: '📋', title: 'Product Manager', company: 'Fintech', challenge: 'Roadmap + feedback = 800 tokens/dia', solution: 'MCP Jira/Slack/GitHub', results: ['📅 Roadmap auto-semanal', '💬 1k mensagens/10s', '🎯 Priorização auto', '⚙️ Sincronização real-time'], metrics: { features: '3x', time: '-80%', churn: '-15%' } },
    { id: 'translator', icon: '🌍', title: 'Localização', company: 'Global', challenge: '100k strings/mês para traduzir', solution: 'Model Router + Batch', results: ['🌐 45 idiomas', '⚡ 20x mais rápido', '🎨 98% contexto', '💰 -72% custo profissional'], metrics: { languages: '3.7x', speed: '20x', cost: '-72%' } }
  ]

  const setupSteps = [
    { step: 1, icon: '📥', title: 'Instalar Plugin', cmd: 'npm install infiniteclaud-plugin', desc: 'Baixar do npm registry' },
    { step: 2, icon: '🔗', title: 'Clonar Repositório', cmd: 'git clone https://github.com/infiniteclaud/infiniteclaud.git', desc: 'Código-fonte completo' },
    { step: 3, icon: '⚙️', title: 'Configurar Environment', cmd: 'cp .env.example .env\n# Editar com suas chaves API', desc: 'Definir CLAUDE_API_KEY' },
    { step: 4, icon: '📊', title: 'Dashboard Inicial', cmd: 'npm run dev\n# Abrir http://localhost:3000', desc: 'Interface de configuração' },
    { step: 5, icon: '✅', title: 'Testar Agentes', cmd: 'npm run test:agents\n# Rodar suite de testes', desc: 'Validar instalação' },
    { step: 6, icon: '🚀', title: 'Telegram + Automação', cmd: '/start\n# Ativar bot do Telegram', desc: 'Conexão com canal' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0F0F0F] via-[#1A1A1A] to-[#0F0F0F] text-[#F5F0E8]">
      {/* Navbar Sticky */}
      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-[rgba(15,15,15,0.9)] border-b border-[rgba(212,168,67,0.1)]">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-black bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">∞Claud</div>
          <div className="flex gap-6 text-sm">
            <a href="#features" className="text-[#A0A0A0] hover:text-[#D4A843] transition">Features</a>
            <a href="#tokens" className="text-[#A0A0A0] hover:text-[#D4A843] transition">Tokens</a>
            <a href="#usecases" className="text-[#A0A0A0] hover:text-[#D4A843] transition">Casos</a>
            <a href="#architecture" className="text-[#A0A0A0] hover:text-[#D4A843] transition">Arquitetura</a>
          </div>
          <button className="px-6 py-2 bg-gradient-to-r from-[#D4A843] to-[#A07C2A] rounded-lg text-black font-bold text-sm">Instalar</button>
        </div>
      </nav>

      {/* ========== SECTION 1: HERO + TOKEN MOTION ========== */}
      <section className="min-h-screen flex items-center justify-center relative pt-20 overflow-hidden">
        <div className="absolute w-96 h-96 rounded-full opacity-20 blur-3xl" style={{ background: 'linear-gradient(135deg, #D4A843, #06B6D4)', left: '10%', top: '20%', animation: 'float 20s ease-in-out infinite' }} />
        <div className="absolute w-80 h-80 rounded-full opacity-15 blur-3xl" style={{ background: 'linear-gradient(135deg, #06B6D4, #A855F7)', right: '10%', bottom: '20%', animation: 'float 25s ease-in-out infinite', animationDelay: '2s' }} />

        <div className="relative z-10 max-w-4xl mx-auto px-6 text-center">
          <div className="mb-6 inline-block px-4 py-2 bg-[rgba(6,182,212,0.1)] border border-[rgba(6,182,212,0.3)] rounded-full">
            <p className="text-[#06B6D4] text-sm font-bold uppercase">Automação 50x Mais Rápida</p>
          </div>

          <h1 className="text-6xl md:text-7xl font-black mb-6 leading-tight">
            <span className="bg-gradient-to-r from-[#F2D275] via-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">InfiniteClaud</span>
            <br />
            <span className="text-[#F5F0E8]">Plugin Oficial Claude</span>
          </h1>

          <p className="text-lg md:text-xl text-[#A0A0A0] max-w-2xl mx-auto mb-8">Automação 50x mais rápida, 96% menos tokens, 20 ferramentas MCP nativas e Model Router inteligente</p>

          <div className="flex gap-4 justify-center mb-12">
            <button className="px-8 py-4 bg-gradient-to-r from-[#D4A843] to-[#A07C2A] rounded-lg font-bold text-black hover:shadow-2xl transition transform hover:-translate-y-1">↓ Baixar Agora</button>
            <button className="px-8 py-4 bg-[rgba(6,182,212,0.1)] border-2 border-[#06B6D4] text-[#06B6D4] rounded-lg font-bold hover:bg-[rgba(6,182,212,0.2)] transition">Ver Demo</button>
          </div>

          <div className="grid grid-cols-3 gap-6">
            <div className="p-4 bg-[rgba(212,168,67,0.05)] border border-[rgba(212,168,67,0.2)] rounded-lg"><p className="text-[#D4A843] text-3xl font-black">50x</p><p className="text-[#A0A0A0] text-sm mt-2">Mais Rápido</p></div>
            <div className="p-4 bg-[rgba(6,182,212,0.05)] border border-[rgba(6,182,212,0.2)] rounded-lg"><p className="text-[#06B6D4] text-3xl font-black">96%</p><p className="text-[#A0A0A0] text-sm mt-2">Menos Tokens</p></div>
            <div className="p-4 bg-[rgba(168,85,247,0.05)] border border-[rgba(168,85,247,0.2)] rounded-lg"><p className="text-[#A855F7] text-3xl font-black">20+</p><p className="text-[#A0A0A0] text-sm mt-2">Ferramentas MCP</p></div>
          </div>
        </div>
      </section>

      {/* ========== SECTION 2: TOKEN COMPARISON ========== */}
      <section id="tokens" className="min-h-screen flex items-center py-20 relative">
        <div className="max-w-6xl mx-auto px-6 w-full">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black mb-4"><span className="bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">Economia de Tokens</span><br /><span className="text-[#F5F0E8]">em Tempo Real</span></h2>
            <p className="text-[#A0A0A0] text-lg mt-4 max-w-2xl mx-auto">Veja como o InfiniteClaud reduz drasticamente o consumo em cada operação</p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="relative h-96 flex items-center justify-center">
              <div className="w-full space-y-12">
                <div className="space-y-2">
                  <div className="text-sm font-bold text-[#A0A0A0]">Uso Normal</div>
                  <div className="relative h-16 bg-[rgba(255,255,255,0.05)] rounded-xl overflow-hidden border border-[rgba(212,168,67,0.2)]">
                    <div className="h-full bg-gradient-to-r from-[#D4A843] via-[#EC4899] to-[#D4A843] rounded-xl opacity-80 flex items-center justify-end pr-4 transition-all duration-2000 ease-out" style={{ width: `${(tokensNormal / 125000) * 100}%`, boxShadow: '0 0 20px rgba(212, 168, 67, 0.5)' }}>
                      {tokensNormal > 10000 && <span className="text-white font-bold text-sm">{tokensNormal.toLocaleString('pt-BR')}</span>}
                    </div>
                  </div>
                  <div className="text-right text-xs text-[#6B6B6B]">125.000 tokens</div>
                </div>

                <div className="space-y-2">
                  <div className="text-sm font-bold text-[#06B6D4]">Com InfiniteClaud</div>
                  <div className="relative h-16 bg-[rgba(255,255,255,0.05)] rounded-xl overflow-hidden border border-[rgba(6,182,212,0.2)]">
                    <div className="h-full bg-gradient-to-r from-[#06B6D4] via-[#00E5CC] to-[#06B6D4] rounded-xl opacity-80 flex items-center justify-end pr-4 transition-all duration-2000 ease-out" style={{ width: `${(tokensOptimized / 125000) * 100}%`, boxShadow: '0 0 20px rgba(6, 182, 212, 0.5)' }}>
                      {tokensOptimized > 100 && <span className="text-white font-bold text-sm">{tokensOptimized.toLocaleString('pt-BR')}</span>}
                    </div>
                  </div>
                  <div className="text-right text-xs text-[#6B6B6B]">5.000 tokens</div>
                </div>
              </div>
            </div>

            <div className="space-y-8">
              <div className="p-8 bg-[rgba(212,168,67,0.05)] border border-[rgba(212,168,67,0.2)] rounded-2xl hover:bg-[rgba(212,168,67,0.1)] transition">
                <h3 className="text-[#D4A843] font-black text-lg mb-2">📊 Redução de 96%</h3>
                <p className="text-[#A0A0A0]">De 125k para apenas 5k tokens por operação padrão</p>
              </div>
              <div className="p-8 bg-[rgba(6,182,212,0.05)] border border-[rgba(6,182,212,0.2)] rounded-2xl hover:bg-[rgba(6,182,212,0.1)] transition">
                <h3 className="text-[#06B6D4] font-black text-lg mb-2">⚡ 50x Mais Rápido</h3>
                <p className="text-[#A0A0A0]">Latência reduzida com processamento otimizado</p>
              </div>
              <div className="p-8 bg-[rgba(168,85,247,0.05)] border border-[rgba(168,85,247,0.2)] rounded-2xl hover:bg-[rgba(168,85,247,0.1)] transition">
                <h3 className="text-[#A855F7] font-black text-lg mb-2">💰 Economia Real</h3>
                <p className="text-[#A0A0A0]">Reduza custos de API em até 96% mantendo qualidade</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========== SECTION 3: FEATURES GRID ========== */}
      <section id="features" className="py-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-black mb-4"><span className="text-[#F5F0E8]">20+ Ferramentas</span><br /><span className="bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">MCP Nativas</span></h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[{ icon: '🔗', title: 'Model Router', desc: 'Roteamento inteligente Haiku/Sonnet/Opus' }, { icon: '🌐', title: 'Web Extract', desc: 'Extração otimizada sem screenshots' }, { icon: '📊', title: 'Data Processing', desc: 'Processamento paralelo em larga escala' }, { icon: '🔍', title: 'Search', desc: 'Busca semântica avançada' }, { icon: '🎨', title: 'Image Gen', desc: 'Geração e edição de imagens' }, { icon: '📝', title: 'Document AI', desc: 'Análise de documentos' }].map((f, i) => (
              <div key={i} className="p-6 bg-gradient-to-br from-[rgba(212,168,67,0.05)] to-[rgba(6,182,212,0.05)] border border-[rgba(212,168,67,0.1)] rounded-xl hover:border-[rgba(212,168,67,0.4)] transition group" style={{ animation: `slideInUp 0.6s ease-out forwards`, opacity: 0, animationDelay: `${i * 100}ms` }}>
                <div className="text-4xl mb-3 group-hover:scale-125 transition">{f.icon}</div>
                <h3 className="text-[#D4A843] font-bold mb-2">{f.title}</h3>
                <p className="text-[#A0A0A0] text-sm">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== SECTION 4: CASOS DE USO ========== */}
      <section id="usecases" className="py-20 px-6 border-t border-[rgba(212,168,67,0.1)]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-black text-center mb-12"><span className="bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">Casos de Uso Reais</span></h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {useCases.map((useCase) => (
              <button key={useCase.id} onClick={() => setSelectedUseCase(useCase.id)} className={`p-6 rounded-xl border-2 transition text-left ${selectedUseCase === useCase.id ? 'bg-gradient-to-br from-[rgba(212,168,67,0.2)] to-[rgba(6,182,212,0.1)] border-[#D4A843]' : 'bg-[rgba(15,15,15,0.5)] border-[rgba(212,168,67,0.2)] hover:border-[#D4A843]'}`}>
                <div className="text-5xl mb-3">{useCase.icon}</div>
                <h3 className="text-[#D4A843] font-black text-lg mb-1">{useCase.title}</h3>
                <p className="text-[#A0A0A0] text-sm">{useCase.company}</p>
              </button>
            ))}
          </div>

          {selectedUseCase && (() => {
            const useCase = useCases.find(u => u.id === selectedUseCase)!
            return (
              <div className="p-8 bg-gradient-to-br from-[rgba(212,168,67,0.1)] to-[rgba(6,182,212,0.05)] border-2 border-[#D4A843] rounded-2xl">
                <div className="flex items-center gap-4 mb-8">
                  <div className="text-6xl">{useCase.icon}</div>
                  <div>
                    <h2 className="text-4xl font-black text-[#D4A843] mb-2">{useCase.title}</h2>
                    <p className="text-[#A0A0A0]">{useCase.company}</p>
                  </div>
                </div>
                <div className="grid md:grid-cols-2 gap-8 mb-8">
                  <div><h3 className="text-[#06B6D4] font-black mb-3">🎯 Desafio</h3><p className="text-[#F5F0E8]">{useCase.challenge}</p></div>
                  <div><h3 className="text-[#D4A843] font-black mb-3">⚡ Solução</h3><p className="text-[#F5F0E8]">{useCase.solution}</p></div>
                </div>
                <h3 className="text-[#06B6D4] font-black mb-4">✨ Resultados</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  {useCase.results.map((r, i) => (
                    <div key={i} className="p-4 bg-[rgba(6,182,212,0.1)] border border-[rgba(6,182,212,0.3)] rounded-lg text-[#F5F0E8] text-sm">{r}</div>
                  ))}
                </div>
              </div>
            )
          })()}
        </div>
      </section>

      {/* ========== SECTION 5: ARQUITETURA ========== */}
      <section id="architecture" className="py-20 px-6 border-t border-[rgba(212,168,67,0.1)]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-black text-center mb-12"><span className="bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">Arquitetura de Agentes</span></h2>

          <div className="bg-[rgba(15,15,15,0.7)] border border-[rgba(212,168,67,0.2)] rounded-2xl p-8 mb-8">
            <svg viewBox="0 0 1000 500" className="w-full h-auto">
              <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                  <polygon points="0 0, 10 3, 0 6" fill="#06B6D4" />
                </marker>
              </defs>

              {/* Input */}
              <rect x="50" y="50" width="150" height="80" fill="rgba(212,168,67,0.2)" stroke="#D4A843" strokeWidth="2" rx="8" />
              <text x="125" y="85" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#D4A843">📥 INPUT</text>

              {/* Arrow */}
              <line x1="200" y1="90" x2="270" y2="90" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" />

              {/* Router */}
              <rect x="270" y="30" width="150" height="120" fill="rgba(6,182,212,0.2)" stroke="#06B6D4" strokeWidth="2" rx="8" />
              <text x="345" y="60" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#06B6D4">🤖 ROUTER</text>
              <rect x="280" y="75" width="40" height="25" fill="rgba(212,168,67,0.3)" stroke="#D4A843" rx="3" />
              <text x="300" y="93" textAnchor="middle" fontSize="9" fill="#D4A843">H</text>
              <rect x="325" y="75" width="40" height="25" fill="rgba(168,85,247,0.3)" stroke="#A855F7" rx="3" />
              <text x="345" y="93" textAnchor="middle" fontSize="9" fill="#A855F7">S</text>
              <rect x="370" y="75" width="40" height="25" fill="rgba(236,72,153,0.3)" stroke="#EC4899" rx="3" />
              <text x="390" y="93" textAnchor="middle" fontSize="9" fill="#EC4899">O</text>

              {/* Arrows to agents */}
              <line x1="295" y1="150" x2="200" y2="220" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" strokeDasharray="5,5" />
              <line x1="345" y1="150" x2="345" y2="220" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" strokeDasharray="5,5" />
              <line x1="395" y1="150" x2="490" y2="220" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" strokeDasharray="5,5" />

              {/* Agents */}
              <rect x="100" y="220" width="130" height="80" fill="rgba(212,168,67,0.15)" stroke="#D4A843" strokeWidth="2" rx="6" />
              <text x="165" y="250" textAnchor="middle" fontSize="12" fontWeight="bold" fill="#D4A843">Agent 1</text>
              <text x="165" y="270" textAnchor="middle" fontSize="10" fill="#A0A0A0">5k tokens</text>

              <rect x="280" y="220" width="130" height="80" fill="rgba(6,182,212,0.15)" stroke="#06B6D4" strokeWidth="2" rx="6" />
              <text x="345" y="250" textAnchor="middle" fontSize="12" fontWeight="bold" fill="#06B6D4">Agent 2</text>
              <text x="345" y="270" textAnchor="middle" fontSize="10" fill="#A0A0A0">2k tokens</text>

              <rect x="460" y="220" width="130" height="80" fill="rgba(168,85,247,0.15)" stroke="#A855F7" strokeWidth="2" rx="6" />
              <text x="525" y="250" textAnchor="middle" fontSize="12" fontWeight="bold" fill="#A855F7">Agent 3</text>
              <text x="525" y="270" textAnchor="middle" fontSize="10" fill="#A0A0A0">3k tokens</text>

              {/* Arrows to output */}
              <line x1="165" y1="300" x2="345" y2="350" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" />
              <line x1="345" y1="300" x2="345" y2="350" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" />
              <line x1="525" y1="300" x2="345" y2="350" stroke="#06B6D4" strokeWidth="2" markerEnd="url(#arrowhead)" />

              {/* Output */}
              <rect x="270" y="350" width="150" height="80" fill="rgba(212,168,67,0.2)" stroke="#D4A843" strokeWidth="2" rx="8" />
              <text x="345" y="385" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#D4A843">📤 OUTPUT</text>
              <text x="345" y="410" textAnchor="middle" fontSize="10" fill="#A0A0A0">10k tokens</text>
            </svg>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[{ name: 'Agentes Simultâneos', limit: '∞ Ilimitado', desc: 'Processamento paralelo' }, { name: 'Model Router', limit: 'H/S/O', desc: 'Seleção inteligente' }, { name: 'MCP Integradas', limit: '20+ nativas', desc: 'Sem setup adicional' }].map((item, i) => (
              <div key={i} className="p-6 bg-gradient-to-br from-[rgba(212,168,67,0.1)] to-[rgba(6,182,212,0.05)] border border-[rgba(212,168,67,0.2)] rounded-xl">
                <h3 className="text-[#D4A843] font-black mb-2">{item.name}</h3>
                <p className="text-2xl font-black bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent mb-2">{item.limit}</p>
                <p className="text-[#A0A0A0] text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== FINAL CTA ========== */}
      <section className="py-20 px-6 border-t border-[rgba(212,168,67,0.1)]">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-black mb-6">Pronto para<br /><span className="bg-gradient-to-r from-[#D4A843] to-[#06B6D4] bg-clip-text text-transparent">Revolucionar seu Workflow?</span></h2>
          <p className="text-[#A0A0A0] text-lg mb-8">Instale o InfiniteClaud agora e economize até 96% em tokens</p>
          <button className="px-12 py-4 bg-gradient-to-r from-[#D4A843] to-[#A07C2A] rounded-lg font-bold text-black text-lg hover:shadow-2xl transition transform hover:-translate-y-1">Instalar Plugin →</button>
        </div>
      </section>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@400;500;600;700&display=swap');
        * { font-family: 'DM Sans', system-ui, -apple-system, sans-serif; }
        h1, h2, h3, h4 { font-family: 'Playfair Display', serif; font-weight: 900; letter-spacing: -0.02em; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-30px); } }
        @keyframes slideInUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
      `}</style>
    </div>
  )
}
