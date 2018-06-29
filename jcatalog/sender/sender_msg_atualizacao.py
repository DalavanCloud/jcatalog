# coding: utf-8

# utilizar %s no lugar dos objetos que serão renderizados com str.format()
# aqui somente para title e file

body_msg = '''
<html>
<p>
    Prezado Sr(a). Editor(a) do periódico <strong>%s</strong>
</p>
<p>
    Em atenção às várias consultas que atendemos sobre a avaliação dos
    periódicos SciELO Brasil compartilhamos com todos os editores os seguintes
    esclarecimentos:
</p>
<p>
    1. A avaliação dos periódicos da coleção SciELO Brasil será realizada pelos
    pesquisadores das Coordenações de Área da FAPESP com base nos Planos de
    Desenvolvimento Editorial (PDE) apresentados pelos editores e nos dados
    sobre os periódicos mantidos pelo SciELO.
</p>
<p>
    2. O PDE deve ser enviado até o dia 10 de julho para o e-mail:
    fapesp@scielo.org
</p>
<p>
    3. Os dados atualizados do seu periódico mantidos pelo SciELO estão
    disponíveis no <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>.
</p>
<p>
    4. O formulário que os pesquisadores da FAPESP utilizarão para avaliar o
    seu periódico está disponível no <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>.
</p>
<p>
Pedimos que nos escrevam para o e-mail <u><a href="mailto:fapesp@scielo.org">fapesp@scielo.org</a></u> se houver
    qualquer dúvida ou questionamento, assim como se identificar
    inconsistências nos dados sobre o seu periódico mantidos pelo SciELO ou
    sobre o formulário de avaliação.
</p>
<p>
    Esclarecemos também sobre os seguintes critérios:
</p>
<p>
    1. <strong>Adesão ao COPE</strong> significa adesão às recomendações do
    COPE (“core practices”) que estão disponíveis em acesso aberto no website
    <u>
        <a href="https://publicationethics.org/">https://publicationethics.org/</a>
    </u>. Não se requer ser membro do COPE para aderir às recomendações do COPE.
</p>
<p>
    2. <strong>Quem acessa o periódico</strong>. Nos dados do seu periódico
    mantidos pelo SciELO no <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>
    foi agregado o indicador de porcentagem dos acessos aos artigos de 2017 nos
    servidores do SciELO vindos das diferentes regiões do mundo e de países
    selecionados, extraídos de amostragem fornecida pelo Google Analytics.
</p>
<p>
    3. <strong>Quem cita o periódico</strong>. Nos dados do seu periódico no
    <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a> é possível
    identificar número de citações recebidas de periódicos SciELO e o número de
    citações recebidas de todos os periódicos da plataforma WoS, sendo a
    diferença um indicador de visibilidade internacional do periódico
</p>
<p>
    Os editores que já enviaram seus PDEs podem atualizá-los com base nesta
    atualização se assim o desejarem.
</p>
<p>
    Atenciosamente,
</p>
<p>
    <br/>
    Abel L Packer
    <br/>
    Programa SciELO / FAPESP, Diretor
</p>
</html>
        '''
