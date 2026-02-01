import Header from "@/components/Header";

export default function PrivacidadePage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <Header />
      <main className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">
          Politica de Privacidade
        </h1>

        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 space-y-6 text-sm text-slate-700 dark:text-slate-300 leading-relaxed">

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              1. Introducao
            </h2>
            <p>
              O NutriOffshore AI esta comprometido com a protecao dos dados pessoais de seus usuarios,
              em conformidade com a Lei Geral de Protecao de Dados Pessoais (LGPD - Lei 13.709/2018).
              Esta politica descreve como coletamos, utilizamos, armazenamos e protegemos suas informacoes.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              2. Dados Coletados
            </h2>
            <p className="mb-2">Coletamos os seguintes tipos de dados pessoais e dados pessoais sensiveis:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li><strong>Dados de identificacao:</strong> nome, matricula, data de nascimento, sexo</li>
              <li><strong>Dados fisicos:</strong> altura, peso, circunferencia abdominal, percentual de gordura</li>
              <li><strong>Dados de saude:</strong> glicemia, colesterol, pressao arterial, condicoes de saude, medicamentos</li>
              <li><strong>Dados nutricionais:</strong> planos alimentares, registros de refeicoes, metas caloricas</li>
              <li><strong>Dados de interacao:</strong> historico de conversas com o agente de IA, preferencias alimentares</li>
              <li><strong>Dados profissionais:</strong> cargo, turno de trabalho, regime de embarque</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              3. Finalidade do Tratamento
            </h2>
            <p className="mb-2">Seus dados sao utilizados exclusivamente para:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Gerar orientacoes nutricionais personalizadas atraves de inteligencia artificial</li>
              <li>Calcular necessidades caloricas e distribuicao de macronutrientes</li>
              <li>Monitorar evolucao de indicadores de saude (peso, IMC, exames)</li>
              <li>Gerar alertas medicos quando indicadores estiverem fora da faixa normal</li>
              <li>Adaptar planos alimentares ao contexto offshore (turno, funcao, disponibilidade)</li>
              <li>Melhorar continuamente o servico de orientacao nutricional</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              4. Base Legal
            </h2>
            <p>
              O tratamento de dados pessoais sensiveis (dados de saude) e realizado com base no
              consentimento explicito do titular (Art. 11, I da LGPD). O tratamento de dados pessoais
              nao sensiveis baseia-se no consentimento do titular e na execucao do servico contratado.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              5. Compartilhamento de Dados
            </h2>
            <p>
              Seus dados pessoais <strong>nao sao compartilhados</strong> com terceiros, exceto quando
              necessario para o funcionamento do servico (provedores de infraestrutura em nuvem) ou
              quando exigido por determinacao legal ou regulatoria. Todos os provedores de servico
              estao sujeitos a acordos de confidencialidade.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              6. Retencao de Dados
            </h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Dados de saude e medicoes sao retidos enquanto o cadastro estiver ativo</li>
              <li>Historico de conversas com a IA e retido por 12 meses para continuidade do atendimento</li>
              <li>Planos nutricionais sao retidos enquanto estiverem ativos ou para historico medico</li>
              <li>Apos a exclusao da conta, todos os dados sao removidos em ate 30 dias</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              7. Direitos do Titular
            </h2>
            <p className="mb-2">Conforme a LGPD (Art. 18), voce tem direito a:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li><strong>Acesso:</strong> solicitar copia de todos os seus dados pessoais armazenados</li>
              <li><strong>Correcao:</strong> solicitar a correcao de dados incompletos, inexatos ou desatualizados</li>
              <li><strong>Eliminacao:</strong> solicitar a exclusao dos seus dados pessoais</li>
              <li><strong>Portabilidade:</strong> solicitar a transferencia dos seus dados para outro servico</li>
              <li><strong>Revogacao do consentimento:</strong> revogar o consentimento a qualquer momento</li>
              <li><strong>Informacao:</strong> ser informado sobre o compartilhamento dos seus dados</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              8. Seguranca dos Dados
            </h2>
            <p>
              Adotamos medidas tecnicas e organizacionais para proteger seus dados, incluindo:
              criptografia em transito (HTTPS/TLS), controle de acesso baseado em funcoes,
              monitoramento de acessos e logs de auditoria. Os dados de saude recebem protecao
              adicional conforme sua natureza sensivel.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">
              9. Contato
            </h2>
            <p>
              Para exercer seus direitos, esclarecer duvidas ou registrar reclamacoes sobre o
              tratamento dos seus dados pessoais, entre em contato com o Encarregado de Protecao
              de Dados (DPO):
            </p>
            <p className="mt-2">
              <strong>E-mail:</strong>{" "}
              <a href="mailto:privacidade@nutrioffshore.com.br" className="text-ocean-600 dark:text-ocean-400 underline">
                privacidade@nutrioffshore.com.br
              </a>
            </p>
          </section>

          <section className="border-t border-slate-200 dark:border-slate-700 pt-4">
            <p className="text-xs text-slate-400 dark:text-slate-500">
              Esta politica de privacidade foi atualizada em janeiro de 2026 e esta em conformidade
              com a Lei Geral de Protecao de Dados Pessoais (Lei 13.709/2018).
            </p>
          </section>

        </div>
      </main>
    </div>
  );
}
