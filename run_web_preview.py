#!/usr/bin/env python3
"""
Servidor Web Leve para Demonstração do ROI Calculator & Decision Copilot
Permite visualizar e interagir com a aplicação diretamente no navegador sem Docker ou Node.js.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Adiciona o backend ao path para importar os motores financeiros
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.services.financial_engine import FinancialEngine
from app.services.monte_carlo import MonteCarloEngine

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ROI Calculator & Decision Copilot</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <div class="max-w-6xl mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8 border-b border-slate-800 pb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent">
          ROI Engine & Decision Copilot
        </h1>
        <p class="text-sm text-slate-400 mt-1">Simulador Financeiro de Precisão & Análise Estocástica de Monte Carlo</p>
      </div>
      <div class="flex gap-2">
        <button onclick="setStep(1)" id="tab-1" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 text-white">1. Premissas</button>
        <button onclick="setStep(2)" id="tab-2" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:bg-slate-700">2. CAPEX</button>
        <button onclick="setStep(3)" id="tab-3" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:bg-slate-700">3. OPEX & Ganhos</button>
        <button onclick="setStep(4)" id="tab-4" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:bg-slate-700">4. Dashboard</button>
      </div>
    </header>

    <!-- Card Principal -->
    <main class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-2xl backdrop-blur">
      
      <!-- ETAPA 1 -->
      <section id="step-1" class="step-content">
        <h2 class="text-lg font-bold text-blue-400 mb-4 flex items-center gap-2">
          <span>📊</span> Etapa 1: Premissas do Projeto & Taxa Mínima de Atratividade (WACC / TMA)
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Nome do Projeto</label>
            <input type="text" id="proj-nome" value="Automação de Atendimento & IA Enterprise" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Horizonte de Vida Útil (Anos)</label>
            <input type="number" id="proj-vida" value="5" min="1" max="20" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
          </div>
          <div class="md:col-span-2">
            <label class="block text-xs font-medium text-slate-300 mb-1">Taxa de Desconto Anual / TMA (WACC ex: 0.12 para 12% a.a.)</label>
            <input type="number" step="0.01" id="proj-tma" value="0.12" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <button onclick="setStep(2)" class="bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm px-5 py-2 rounded-lg transition">Avançar para CAPEX →</button>
        </div>
      </section>

      <!-- ETAPA 2 -->
      <section id="step-2" class="step-content hidden">
        <h2 class="text-lg font-bold text-teal-400 mb-4 flex items-center gap-2">
          <span>💰</span> Etapa 2: Investimento Inicial (CAPEX - Ano 0)
        </h2>
        <div class="space-y-3" id="capex-list">
          <div class="flex items-center gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <input type="text" value="Servidores & Infraestrutura GPU" class="bg-transparent flex-1 text-sm text-slate-200 outline-none">
            <span class="text-xs text-slate-400">R$</span>
            <input type="number" value="120000" class="capex-val w-32 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-right text-sm text-white">
          </div>
          <div class="flex items-center gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
            <input type="text" value="Engenharia, Setup & Fine-Tuning" class="bg-transparent flex-1 text-sm text-slate-200 outline-none">
            <span class="text-xs text-slate-400">R$</span>
            <input type="number" value="60000" class="capex-val w-32 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-right text-sm text-white">
          </div>
        </div>
        <div class="mt-6 flex justify-between">
          <button onclick="setStep(1)" class="bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded-lg">← Voltar</button>
          <button onclick="setStep(3)" class="bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm px-5 py-2 rounded-lg transition">Avançar para OPEX & Ganhos →</button>
        </div>
      </section>

      <!-- ETAPA 3 -->
      <section id="step-3" class="step-content hidden">
        <h2 class="text-lg font-bold text-emerald-400 mb-4 flex items-center gap-2">
          <span>📈</span> Etapa 3: Custos Recorrentes (OPEX) & Benefícios Ponderados por Risco
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
            <h3 class="text-sm font-semibold text-rose-400 mb-3">Custos Operacionais Anuais (OPEX)</h3>
            <div class="space-y-2">
              <label class="block text-xs text-slate-400">Licenciamento & APIs por ano (R$)</label>
              <input type="number" id="opex-anual" value="25000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white">
            </div>
          </div>
          <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-800">
            <h3 class="text-sm font-semibold text-emerald-400 mb-3">Benefícios Anuais Estimados</h3>
            <div class="space-y-2">
              <label class="block text-xs text-slate-400">Redução de Custos de Suporte (R$ / ano)</label>
              <input type="number" id="benef-1-val" value="95000" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white">
              <label class="block text-xs text-slate-400">Probabilidade de Realização (ex: 0.85 = 85%)</label>
              <input type="number" step="0.05" id="benef-1-prob" value="0.85" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white">
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-between items-center">
          <button onclick="setStep(2)" class="bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded-lg">← Voltar</button>
          <button onclick="executarCalculo()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm px-6 py-2.5 rounded-lg shadow-lg hover:shadow-emerald-500/20 transition flex items-center gap-2">
            <span>⚡</span> Calcular ROI & Simulação
          </button>
        </div>
      </section>

      <!-- ETAPA 4 (DASHBOARD) -->
      <section id="step-4" class="step-content hidden">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-teal-400 flex items-center gap-2">
            <span>🎯</span> Resultados Executivos do Projeto
          </h2>
          <span id="badge-status" class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            [APROVADO] Viável
          </span>
        </div>

        <!-- KPI Cards Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <span class="text-xs text-slate-400">Valor Presente Líquido (VPL)</span>
            <div id="kpi-vpl" class="text-xl font-bold text-emerald-400 mt-1">R$ 0,00</div>
          </div>
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <span class="text-xs text-slate-400">Taxa Interna de Retorno (TIR)</span>
            <div id="kpi-tir" class="text-xl font-bold text-blue-400 mt-1">0,0%</div>
          </div>
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <span class="text-xs text-slate-400">Payback Descontado</span>
            <div id="kpi-payback" class="text-xl font-bold text-amber-400 mt-1">0 anos</div>
          </div>
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <span class="text-xs text-slate-400">Retorno s/ Investimento (ROI)</span>
            <div id="kpi-roi" class="text-xl font-bold text-purple-400 mt-1">0%</div>
          </div>
        </div>

        <!-- Monte Carlo Box -->
        <div class="bg-slate-900/90 p-5 rounded-xl border border-indigo-900/50 mb-6 shadow-inner">
          <h3 class="text-sm font-semibold text-indigo-300 mb-3 flex items-center gap-2">
            <span>🎲</span> Simulação Estocástica de Monte Carlo (1.000 Iterações)
          </h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
            <div class="p-3 bg-slate-800/60 rounded-lg">
              <span class="text-xs text-slate-400 block">Probabilidade de VPL > 0</span>
              <span id="mc-prob" class="text-lg font-bold text-emerald-400">93.3%</span>
            </div>
            <div class="p-3 bg-slate-800/60 rounded-lg">
              <span class="text-xs text-slate-400 block">Pessimista (P10)</span>
              <span id="mc-p10" class="text-sm font-bold text-rose-400">R$ 0</span>
            </div>
            <div class="p-3 bg-slate-800/60 rounded-lg">
              <span class="text-xs text-slate-400 block">Mediana / Base (P50)</span>
              <span id="mc-p50" class="text-sm font-bold text-blue-400">R$ 0</span>
            </div>
            <div class="p-3 bg-slate-800/60 rounded-lg">
              <span class="text-xs text-slate-400 block">Otimista (P90)</span>
              <span id="mc-p90" class="text-sm font-bold text-emerald-400">R$ 0</span>
            </div>
          </div>
        </div>

        <!-- Projeção Anual Table -->
        <div class="overflow-x-auto rounded-xl border border-slate-800">
          <table class="w-full text-xs text-left text-slate-300">
            <thead class="bg-slate-900/80 text-slate-400 uppercase tracking-wider">
              <tr>
                <th class="p-3">Período</th>
                <th class="p-3">CAPEX</th>
                <th class="p-3">OPEX</th>
                <th class="p-3">Ganhos Ajustados</th>
                <th class="p-3">FCL Líquido</th>
                <th class="p-3">Saldo Descontado</th>
              </tr>
            </thead>
            <tbody id="periodos-tbody" class="divide-y divide-slate-800 bg-slate-900/40">
            </tbody>
          </table>
        </div>

        <div class="mt-6 flex justify-between">
          <button onclick="setStep(3)" class="bg-slate-700 hover:bg-slate-600 text-white text-sm px-4 py-2 rounded-lg">← Alterar Premissas</button>
          <button onclick="executarCalculo()" class="bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm px-4 py-2 rounded-lg">Recalcular</button>
        </div>
      </section>

    </main>
  </div>

  <script>
    function setStep(s) {
      for (let i = 1; i <= 4; i++) {
        document.getElementById('step-' + i).classList.add('hidden');
        const btn = document.getElementById('tab-' + i);
        btn.className = 'tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-slate-400 hover:bg-slate-700';
      }
      document.getElementById('step-' + s).classList.remove('hidden');
      document.getElementById('tab-' + s).className = 'tab-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 text-white';
    }

    async function executarCalculo() {
      const vida = parseInt(document.getElementById('proj-vida').value) || 5;
      const tma = parseFloat(document.getElementById('proj-tma').value) || 0.12;
      const opexVal = parseFloat(document.getElementById('opex-anual').value) || 25000;
      const benefVal = parseFloat(document.getElementById('benef-1-val').value) || 95000;
      const benefProb = parseFloat(document.getElementById('benef-1-prob').value) || 0.85;

      let capexTotal = 0;
      document.querySelectorAll('.capex-val').forEach(el => capexTotal += (parseFloat(el.value) || 0));

      const payload = {
        taxa_desconto_anual: tma,
        vida_util_anos: vida,
        custos: [
          { tipo: "CAPEX_INICIAL", categoria: "Investimento", valor: capexTotal, ano: 0 }
        ],
        beneficios: [
          {
            tipo: "TANGIVEL_REDUCAO_CUSTO",
            descricao: "Benefício",
            valor_estimado_anual: benefVal,
            probabilidade_realizacao: benefProb,
            ano_inicio: 1,
            ano_fim: vida
          }
        ]
      };

      for (let y = 1; y <= vida; y++) {
        payload.custos.push({ tipo: "OPEX_RECORRENTE", categoria: "Operação", valor: opexVal, ano: y });
      }

      try {
        const res = await fetch('/api/calculations/simulate-instant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        renderResultados(data);
        setStep(4);
      } catch (err) {
        alert("Erro ao calcular: " + err);
      }
    }

    function renderResultados(data) {
      const calc = data.calculo;
      const mc = data.monte_carlo;

      document.getElementById('kpi-vpl').innerText = 'R$ ' + calc.vpl.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
      document.getElementById('kpi-tir').innerText = calc.tir_formatada;
      document.getElementById('kpi-payback').innerText = calc.payback_descontado_anos ? calc.payback_descontado_anos.toFixed(2) + ' anos' : 'Não recupera';
      document.getElementById('kpi-roi').innerText = calc.roi_percentual.toFixed(1) + '%';

      const badge = document.getElementById('badge-status');
      if (calc.eh_viavel) {
        badge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        badge.innerText = '[APROVADO] Projeto Viável';
      } else {
        badge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-rose-500/20 text-rose-300 border border-rose-500/30';
        badge.innerText = '[REPROVADO] Projeto Inviável';
      }

      document.getElementById('mc-prob').innerText = mc.probabilidade_vpl_positivo.toFixed(1) + '%';
      document.getElementById('mc-p10').innerText = 'R$ ' + mc.vpl_percentis.P10.toLocaleString('pt-BR', { minimumFractionDigits: 0 });
      document.getElementById('mc-p50').innerText = 'R$ ' + mc.vpl_percentis.P50.toLocaleString('pt-BR', { minimumFractionDigits: 0 });
      document.getElementById('mc-p90').innerText = 'R$ ' + mc.vpl_percentis.P90.toLocaleString('pt-BR', { minimumFractionDigits: 0 });

      const tbody = document.getElementById('periodos-tbody');
      tbody.innerHTML = '';
      calc.periodos.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-200">Ano ${p.ano}</td>
          <td class="p-3 text-rose-400">R$ ${p.capex.toLocaleString('pt-BR')}</td>
          <td class="p-3 text-amber-400">R$ ${p.opex.toLocaleString('pt-BR')}</td>
          <td class="p-3 text-emerald-400">R$ ${p.beneficios_ajustados.toLocaleString('pt-BR')}</td>
          <td class="p-3 font-bold ${p.fluxo_caixa_liquido >= 0 ? 'text-teal-300' : 'text-rose-400'}">R$ ${p.fluxo_caixa_liquido.toLocaleString('pt-BR')}</td>
          <td class="p-3 font-bold ${p.fluxo_acumulado_descontado >= 0 ? 'text-teal-300' : 'text-slate-400'}">R$ ${p.fluxo_acumulado_descontado.toLocaleString('pt-BR')}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    // Carrega cálculo padrão ao abrir
    window.onload = executarCalculo;
  </script>
</body>
</html>
"""

class ROIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/calculations/simulate-instant":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                tma = float(data.get("taxa_desconto_anual", 0.12))
                vida = int(data.get("vida_util_anos", 5))
                custos = data.get("custos", [])
                beneficios = data.get("beneficios", [])

                # Executa motor financeiro
                metricas = FinancialEngine.analyze_project(tma, vida, custos, beneficios)
                
                # Executa Monte Carlo
                mc = MonteCarloEngine.simulate(tma, vida, custos, beneficios, iteracoes=1000)

                response_data = {
                    "calculo": metricas,
                    "monte_carlo": mc
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silencia logs excessivos
        pass

def run():
    port = 8080
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, ROIRequestHandler)
    print(f"[*] Servidor ROI Copilot iniciado na porta {port}!")
    print(f"[*] Acesse: http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run()
