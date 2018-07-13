# coding: utf-8

# utilizar %s no lugar dos objetos que serão renderizados com str.format()
# aqui somente para title e file

body_msg = '''
<html>
<p>
    Prezado Sr(a) Editor(a) do periódico <strong>%s</strong>
</p>
<p>
    Como informamos anteriormente, a avaliação dos periódicos da coleção SciELO
    Brasil será realizada pelos pesquisadores das Coordenações de Área da
    FAPESP com base nos Planos de Desenvolvimento Editorial (PDE) apresentados
    pelos editores e nos dados sobre os periódicos mantidos pelo SciELO.
</p>
<p>
    A avaliação será realizada com o apoio de um formulário com dados
    individualizados para cada periódicos. As métricas utilizadas no formulário
    são apresentados em três versões: o valor nominal para o periódico, a
    posição relativa do valor nominal (entre 0 e 1) entre todos os periódicos
    da coleção SciELO Brasil e a posição relativa do valor nominal entre os
    periódicos da área temática do periódico.
</p>
<p>
    O formulário de avaliação individualizado para o seu periódico está no
    link: <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>
</p>
<p>
    Os dados atualizados do seu periódico mantidos pelo SciELO estão
    disponíveis no link <a href="http://static.scielo.org/fapesp_evaluation/%s">link</a>.
</p>
<p>
    Pedimos que nos escrevam para o e-mail <a href="mailto:fapesp@scielo.org">fapesp@scielo.org</a>
    se houver qualquer dúvida ou questionamento, assim como se identificar
    inconsistências nos dados sobre o seu periódico mantidos pelo SciELO ou
    sobre o formulário de avaliação. No caso de erros ou inconsistências dos
    dados os dados do seu periódico e do formulário serão atualizados.
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
