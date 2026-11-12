import React, { useState } from 'react';

export default function App() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // Estado do Projeto
  const [projeto, setProjeto] = useState({
    nome: "Automação de Atendimento & RAG Enterprise",
    descricao: "Implementação de modelo LLM interno para ganho de produtividade no suporte N1 e N2",
    taxa_desconto_anual: 0.12,
    vida_util_anos: 5,
    custos: [
      { tipo: "CAPEX_INICIAL", categoria: "Hardware & GPUs", valor: 120000, ano: 0 },
      { tipo: "CAPEX_INICIAL", categoria: "Engenharia & Setup", valor: 60000, ano: 0 },
      { tipo: "OPEX_RECORRENTE", categoria: "Licenciamento e API", valor: 25000, ano: 1 },
      { tipo: "OPEX_RECORRENTE", categoria: "Licenciamento e API", valor: 25000, ano: 2 },
      { tipo: "OPEX_RECORRENTE", categoria: "Licenciamento e API", valor: 25000, ano: 3 },
      { tipo: "OPEX_RECORRENTE", categoria: "Licenciamento e API", valor: 25000, ano: 4 },
      { tipo: "OPEX_RECORRENTE", categoria: "Licenciamento e API", valor: 25000, ano: 5 },
    ],
    beneficios: [
      {
        tipo: "TANGIVEL_REDUCAO_CUSTO",
        descricao: "Redução de tempo de resolução de chamados",
        valor_estimado_anual: 95000,
        probabilidade_realizacao: 0.85,
        ano_inicio: 1,
        ano_fim: 5
      },
      {
        tipo: "TANGIVEL_AUMENTO_RECEITA",
        descricao: "Upsell proporcionado por SLA aprimorado",
        valor_estimado_anual: 30000,
        probabilidade_realizacao: 0.70,
        ano_inicio: 1,
        ano_fim: 5
      }
    ]
  });

  const [resultado, setResultado] = useState(null);

  const calcularROI = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/calculations/simulate-instant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(projeto)
      });
      const data = await response.json();
      setResultado(data);
      setStep(4);
    } catch (err) {
      alert("Aviso: Conecte o backend FastAPI na porta 8000 ou verifique as credenciais.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text text-transparent">
            ROI Engine & Decision Copilot
          </h1>
          <p className="text-sm text-slate-400">Arquitetura de Avaliação de Projetos de TI & Inovação</p>
        </div>
        <div className="flex gap-2">
          {["1. Premissas", "2. CAPEX", "3. OPEX & Benefícios", "4. Dashboard"].map((label, idx) => (
            <button
              key={idx}
              onClick={() => setStep(idx + 1)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                step === idx + 1 ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </header>

      {/* Conteúdo do Wizard */}
      <main className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-6 shadow-xl backdrop-blur">
        {step === 1 && (
          <div>
            <h2 className="text-lg font-semibold text-blue-300 mb-4">Etapa 1: Dados Básicos e Taxa de Desconto (WACC/TMA)</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Nome do Projeto</label>
                <input
                  type="text"
                  value={projeto.nome}
                  onChange={(e) => setProjeto({...projeto, nome: e.target.value})}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Horizonte de Análise (Vida Útil em Anos)</label>
                <input
                  type="number"
                  value={projeto.vida_util_anos}
                  onChange={(e) => setProjeto({...projeto, vida_util_anos: parseInt(e.target.value) || 1})}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-medium text-slate-300 mb-1">Taxa Mínima de Atratividade (TMA / WACC Anual)</label>
                <div className="flex items-center gap-3">
                  <input
                    type="range"
                    min="0.05"
                    max="0.30"
                    step="0.005"
                    value={projeto.taxa_desconto_anual}
                    onChange={(e) => setProjeto({...projeto, taxa_desconto_anual: parseFloat(e.target.value)})}
                    className="w-full accent-blue-500"
                  />
                  <span className="text-base font-bold text-teal-400 min-w-[70px]">
                    {(projeto.taxa_desconto_anual * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex gap-2 mt-2">
                  <button onClick={() => setProjeto({...projeto, taxa_desconto_anual: 0.08})} className="text-xs bg-slate-700 hover:bg-slate-600 px-2 py-1 rounded">Infra (8%)</button>
                  <button onClick={() => setProjeto({...projeto, taxa_desconto_anual: 0.12})} className="text-xs bg-slate-700 hover:bg-slate-600 px-2 py-1 rounded">Tech/IA (12%)</button>
                  <button onClick={() => setProjeto({...projeto, taxa_desconto_anual: 0.18})} className="text-xs bg-slate-700 hover:bg-slate-600 px-2 py-1 rounded">Venture/Alto Risco (18%)</button>
                </div>
              </div>
            </div>
            <div className="mt-6 flex justify-end">
              <button onClick={() => setStep(2)} className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-4 py-2 rounded-lg text-sm">
                Avançar para CAPEX →
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <h2 className="text-lg font-semibold text-blue-300 mb-4">Etapa 2: Investimento Inicial (CAPEX)</h2>
            <p className="text-xs text-slate-400 mb-4">Custos de aquisição, infraestrutura, horas de desenvolvimento e implantação no Ano 0.</p>
            <div className="space-y-3">
              {projeto.custos.filter(c => c.tipo === "CAPEX_INICIAL").map((c, i) => (
                <div key={i} className="flex gap-3 items-center bg-slate-900/80 p-3 rounded-lg border border-slate-700">
                  <input
                    type="text"
                    value={c.categoria}
                    readOnly
                    className="bg-transparent text-sm font-medium text-slate-200 flex-1"
                  />
                  <span className="text-sm font-bold text-slate-100">R$ {c.valor.toLocaleString('pt-BR')}</span>
                </div>
              ))}
            </div>
            <div className="mt-6 flex justify-between">
              <button onClick={() => setStep(1)} className="bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded-lg">← Voltar</button>
              <button onClick={() => setStep(3)} className="bg-blue-600 hover:bg-blue-500 text-white text-sm px-4 py-2 rounded-lg">Avançar para OPEX & Benefícios →</button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <h2 className="text-lg font-semibold text-blue-300 mb-4">Etapa 3: Custos Contínuos (OPEX) e Benefícios Tangíveis</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-medium text-amber-400 mb-2">Custos Recorrentes Anuais (OPEX)</h3>
                <div className="space-y-2">
                  {projeto.custos.filter(c => c.tipo === "OPEX_RECORRENTE").slice(0, 3).map((c, i) => (
                    <div key={i} className="bg-slate-900/60 p-2.5 rounded border border-slate-800 text-xs flex justify-between">
                      <span>Ano {c.ano}: {c.categoria}</span>
                      <span className="font-semibold text-amber-300">R$ {c.valor.toLocaleString('pt-BR')}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-sm font-medium text-emerald-400 mb-2">Ganhos Tangíveis Projetados</h3>
                <div className="space-y-2">
                  {projeto.beneficios.map((b, i) => (
                    <div key={i} className="bg-slate-900/60 p-2.5 rounded border border-slate-800 text-xs">
                      <div className="flex justify-between font-medium">
                        <span>{b.descricao}</span>
                        <span className="text-emerald-400">R$ {b.valor_estimado_anual.toLocaleString('pt-BR')}/ano</span>
                      </div>
                      <div className="text-[11px] text-slate-400 mt-1">
                        Probabilidade (fator de risco): {(b.probabilidade_realizacao * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="mt-8 flex justify-between">
              <button onClick={() => setStep(2)} className="bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded-lg">← Voltar</button>
              <button
                onClick={calcularROI}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold px-6 py-2 rounded-lg shadow-lg"
              >
                {loading ? "Processando..." : "Calcular Indicadores Executivos 🚀"}
              </button>
            </div>
          </div>
        )}

        {step === 4 && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-semibold text-emerald-400">Etapa 4: Dashboard de Resultados Executivos</h2>
              <button onClick={() => setStep(1)} className="text-xs bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded">Editar Parâmetros</button>
            </div>

            {resultado ? (
              <div className="space-y-6">
                {/* Cards de Métricas Principais */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-slate-900/90 border border-slate-700 p-4 rounded-xl">
                    <span className="text-xs text-slate-400 uppercase font-semibold">Valor Presente Líquido (VPL)</span>
                    <p className={`text-xl font-bold mt-1 ${resultado.vpl >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                      R$ {resultado.vpl.toLocaleString('pt-BR')}
                    </p>
                    <span className="text-[11px] text-slate-500">Descontado a {(resultado.tma_utilizada * 100).toFixed(1)}%</span>
                  </div>

                  <div className="bg-slate-900/90 border border-slate-700 p-4 rounded-xl">
                    <span className="text-xs text-slate-400 uppercase font-semibold">Taxa Interna de Retorno (TIR)</span>
                    <p className="text-xl font-bold text-teal-300 mt-1">{resultado.tir_formatada}</p>
                    <span className="text-[11px] text-slate-500">Spread: {resultado.tir ? ((resultado.tir - resultado.tma_utilizada)*100).toFixed(1) + "% vs TMA" : "N/A"}</span>
                  </div>

                  <div className="bg-slate-900/90 border border-slate-700 p-4 rounded-xl">
                    <span className="text-xs text-slate-400 uppercase font-semibold">Payback Simples</span>
                    <p className="text-xl font-bold text-amber-300 mt-1">
                      {resultado.payback_simples_anos !== null ? `${resultado.payback_simples_anos} anos` : "Superior à vida útil"}
                    </p>
                    <span className="text-[11px] text-slate-500">Fluxos nominais</span>
                  </div>

                  <div className="bg-slate-900/90 border border-slate-700 p-4 rounded-xl">
                    <span className="text-xs text-slate-400 uppercase font-semibold">Payback Descontado</span>
                    <p className="text-xl font-bold text-cyan-300 mt-1">
                      {resultado.payback_descontado_anos !== null ? `${resultado.payback_descontado_anos} anos` : "Superior à vida útil"}
                    </p>
                    <span className="text-[11px] text-slate-500">Considerando TMA</span>
                  </div>
                </div>

                {/* Tabela de Fluxo de Caixa Anual */}
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border border-slate-700 rounded-lg">
                    <thead className="bg-slate-900/90 text-slate-400 font-semibold border-b border-slate-700">
                      <tr>
                        <th className="p-2.5">Ano</th>
                        <th className="p-2.5">CAPEX</th>
                        <th className="p-2.5">OPEX</th>
                        <th className="p-2.5">Ganhos Ajustados</th>
                        <th className="p-2.5">FCL Líquido</th>
                        <th className="p-2.5">FCL Descontado</th>
                        <th className="p-2.5">Saldo Acumulado</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      {resultado.periodos.map((p) => (
                        <tr key={p.ano} className="hover:bg-slate-750/30">
                          <td className="p-2.5 font-bold text-slate-300">Ano {p.ano}</td>
                          <td className="p-2.5 text-rose-300">R$ {p.capex.toLocaleString('pt-BR')}</td>
                          <td className="p-2.5 text-amber-300">R$ {p.opex.toLocaleString('pt-BR')}</td>
                          <td className="p-2.5 text-emerald-300">R$ {p.beneficios_ajustados.toLocaleString('pt-BR')}</td>
                          <td className={`p-2.5 font-semibold ${p.fluxo_caixa_liquido >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                            R$ {p.fluxo_caixa_liquido.toLocaleString('pt-BR')}
                          </td>
                          <td className="p-2.5 text-slate-300">R$ {p.fluxo_descontado.toLocaleString('pt-BR')}</td>
                          <td className={`p-2.5 font-bold ${p.fluxo_acumulado_descontado >= 0 ? "text-teal-300" : "text-slate-400"}`}>
                            R$ {p.fluxo_acumulado_descontado.toLocaleString('pt-BR')}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-sm text-slate-400">Nenhum cálculo processado ainda.</p>
                <button onClick={calcularROI} className="mt-3 bg-blue-600 text-white text-xs px-4 py-2 rounded">
                  Calcular com Dados Exemplo
                </button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
