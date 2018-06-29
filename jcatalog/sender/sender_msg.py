# coding: utf-8

# utilizar %s no lugar dos objetos que serão renderizados com str.format()
# aqui somente para title e file

body_msg = '''
<html>
<p align="justify">
    Prezado Sr(a). Editor(a) do periódico: <strong>%s</strong>
</p>
<p align="justify">
    Por ocasião do vigésimo aniversário do Programa SciELO, a FAPESP fará uma
    avaliação dos periódicos ativos na coleção SciELO Brasil há dois ou mais
    anos.
</p>
<p align="justify">
    Para essa avaliação, solicitamos aos editores de cada periódico apresentar,
    até 10 de julho, um Plano de Desenvolvimento Editorial (PDE) do periódico,
    conforme o esquema sugerido abaixo.
</p>
<p align="justify">
    Os dados mantidos pelo SciELO sobre o desempenho do seu periódico podem ser
    obtidos neste <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>.
</p>
<p align="justify">
    A avaliação será realizada com o auxílio dos pesquisadores que participam
    das Coordenações de Área da Fapesp e com base nos Planos de Desenvolvimento
    Editorial apresentados.
</p>
<p align="justify">
    O resultado da avaliação será comunicado aos editores-chefes dos periódicos
    e apresentado no evento de aniversário do SciELO.
</p>
<p align="justify">
O plano deverá ser encaminhado ao diretor do SciELO através do e-mail <u><a href="mailto:fapesp@scielo.org">fapesp@scielo.org</a></u> até 10 de
    julho de 2018. O acesso ao plano será reservado aos avaliadores.
</p>
<p align="justify">
    Agradecemos desde já sua colaboração.
</p>
<p align="justify">
    Cordialmente,
</p>
<p align="left">
    <strong>Abel L. Packer</strong><br/>
    Diretor do Programa SciELO / FAPESP<br/>


<br/>
</p>
<p align="justify">
    <strong>
        Esquema sugerido para a apresentação do Plano de Desenvolvimento
        Editorial de Periódicos da Coleção SciELO Brasil ativos na coleção
        desde janeiro de 2016
    </strong>
</p>
<p align="justify">
    O Plano de Desenvolvimento Editorial (PDE) deve expressar os avanços
    almejados para o periódico até o final de 2021. Espera-se um documento de
    até 5 páginas com análises do estado atual e propostas de evolução até o
    final de 2021 em torno das questões listadas a seguir além de outras que o
    editor considere relevante para o futuro desempenho do periódico.
</p>
<p align="justify">
    <strong>
        Questões relevantes para o PDE – situação atual e proposta de evolução
        até o final de 2021:
    </strong>
</p>
<ol>
    <li>
        <p align="justify">
            Institucionalidade do periódico:
        </p>
    </li>
</ol>
<ol>
    <ol type="a">
        <li>
            <p align="justify">
                Instituição diretamente responsável e dependências
                hierárquicas, se houver – nome e tipo de instituição (sociedade
                científica, associação profissional, universidade, etc.).
            </p>
        </li>
        <li>
            <p align="justify">
                Alinhamento da missão e objetivos do periódico e da instituição
                diretamente responsável.
            </p>
        </li>
        <li>
            <p align="justify">
                Periódico regido por estatuto?
            </p>
        </li>
        <li>
            <p align="justify">
                Política de composição do corpo editorial.
            </p>
        </li>
    </ol>
</ol>
<ol start="2">
    <li>
        <p align="justify">
            Singularidade do periódico:
        </p>
        <ol type="a">
            <li>
                <p align="justify">
                    Na comunicação da pesquisa do Brasil.
                </p>
            </li>
            <li>
                <p align="justify">
                    Frente aos periódicos da mesma área já existentes no Brasil
                    e globalmente.
                </p>
            </li>
            <li>
                <p align="justify">
                    Quem publica no periódico.
                </p>
            </li>
            <li>
                <p align="justify">
                    Quem acessa o periódico.
                </p>
            </li>
            <li>
                <p align="justify">
                    Quem cita o periódico.
                </p>
            </li>
        </ol>
    </li>
</ol>
<ol start="3">
    <li>
        <p align="justify">
            Sustentabilidade econômica:
        </p>
        <ol type="a">
            <li>
                <p align="justify">
                    Orçamento anual estimado, indicando os itens de custeio
                    considerados. Custo médio por artigo estimado.
                </p>
            </li>
            <li>
                <p align="justify">
                    Modelo de financiamento atual.
                </p>
            </li>
            <li>
                <p align="justify">
                    Política em relação a cobrança de APC (“Article Processing
                    Charge”).
                </p>
            </li>
        </ol>
    </li>
</ol>
<ol start="4">
    <li>
        <p align="justify">
            Adesão a Boas Práticas Editoriais, incluindo o processo editorial e
            integridade da pesquisa:
        </p>
        <ol type="a">
            <li>
                <p align="justify">
                    Modalidade e política de avaliação de manuscritos utilizada
                    pelo periódico. Sistema de gestão de manuscritos, volume de
                    transações, índice de rejeição imediato e após avaliação
                    dos manuscritos, tempos médios de processamento (da
                    recepção à rejeição imediata ou aceite para avaliação, do
                    início da avaliaçãoaté a aprovação ou rejeição e até a
                    publicação online no SciELO.
                </p>
            </li>
            <li>
                <p align="justify">
                    Política de encomenda de manuscritos e de artigos de
                    revisão (“reviews”).
                </p>
            </li>
            <li>
                <p align="justify">
                    Política de publicação de números especiais e dossiês.
                </p>
            </li>
            <li>
                <p align="justify">
                    Boas práticas em ética acadêmica:
                </p>
                <ol type="i">
                    <li>
                        <p align="justify">
                            Política e procedimentos para detecção e resolução
                            de violações éticas especificadas nas instruções
                            aos autores.
                        </p>
                    </li>
                    <li>
                        <p align="justify">
                            Uso de sistema de detecção de plagio.
                        </p>
                    </li>
                    <li>
                        <p align="justify">
                            Critérios de autoria e exigência de registro da
                            contribuição de cada autor no final do artigo.
                        </p>
                    </li>
                    <li>
                        <p align="justify">
                            Adesão ao COPE.
                        </p>
                    </li>
                </ol>
            </li>
            <li>
                <p align="justify">
                    Exigência de ORCID dos autores.
                </p>
            </li>
        </ol>
    </li>
</ol>
<ol start="5">
    <li>
        <p align="justify">
            Evolução e projeção futura da visibilidade e impacto do periódico:
        </p>
        <ol type="a">
            <li>
                <p align="justify">
                    Visibilidade internacional: idioma dos artigos, autoria,
                    coautoria, composição do corpo editorial, da assessoria
                    usada, das citações recebidas e das citações feitas.
                </p>
            </li>
            <li>
                <p align="justify">
                    Bibliometria.
                </p>
            </li>
            <li>
                <p align="justify">
                    Acessos e downloads.
                </p>
            </li>
            <li>
                <p align="justify">
                    Presença e influência nas Redes Sociais.
                </p>
            </li>
            <li>
                <p align="justify">
                    Outras métricas.
                </p>
            </li>
        </ol>
    </li>
</ol>
<ol start="6">
    <li>
        <p align="justify">
            Aspectos considerados fundamentais nas análises e propostas de
            metas do PDE:
        </p>
        <ol type="a">
            <li>
                <p align="justify">
                    Metas editoriais relacionadas à preservação e aumento da
                    visibilidade e do impacto acadêmico (não necessariamente apenas
                    bibliométrico) do periódico com destaque para o fortalecimento da
                    sua singularidade.
                </p>
            </li>
            <li>
                <p align="justify">
                    Meios para realizar as metas: compromisso da instituição
                    diretamente responsável e hierarquicamente superior,
                    sustentabilidade, fontes de recursos, estrutura operacional, etc.
                </p>
            </li>
            <li>
                <p align="justify">
                    <a name="_GoBack"></a>
                    Ações e liderança para busca das metas: responsabilidade e
                    liderança das autoridades da instituição responsável, dos
                    editores-chefes e demais membros do corpo editorial, ações
                    planejadas, profissionalização, etc.
                </p>
            </li>
            <li>
                <p align="justify">
                    Sempre que aplicável as metas, meios e responsabilidades devem ser
                    qualificadas com indicadores ou fontes de verificação assim como de
                    premissas ou restrições.
                </p>
            </li>
        </ol>
    </li>
</ol>
</html>
        '''
