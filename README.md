# PPGEE-lucy

## Motivação:

O PPGEE-Lucy é um fork do `lucyLattes`[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2591748.svg)](https://doi.org/10.5281/zenodo.2591748), O objetivo é adaptar o `lucylattes` às necessidades do Programa de Pós-Graduação em Engenharia Elétrica da UFMG (PPGEE-UFMG). Estamos desenvolvendo rotinas para:

- Classificação automática dos autores dos artigos gerados pela comunidade do PPGEE-UFMG em um determinado ano. Isto é importante para o preenchimento do relatório Sucupira, especialmente devido à necessidade de identificar se determinado autor é discente ou egresso do programa (PRONTO!);
- Geração automática de indicadores de produtividade, compatíveis com os utilizados pela área de Engenharias IV da CAPES, com a finalidade de auxílio na avaliação do desempenho do programa;
- Auxílio no processo de credenciamento/recredenciamento dos docentes do PPGEE-UFMG, gerando os indicadores utilizados;
- Detecção de anomalias nos dados do PPGEE-UFMG

## O que faz:

- Extração, compilação, e organização dos dados dos currículos da plataforma *Lattes* em planilhas, e geração de um relátório simplificado (funcionalidades herdadas do `lucyLattes`).
- Geração de planilhas com os dados organizados para auxiliar na avaliação do programa, credenciamento de docentes e preenchimento correto do relatório Sucupira.

## Requisitos:
  
- Sistema operacional Linux ou Windows;
- Python 3.8 ou superior;
- Navegador (Firefox ou Chromium) para visualizar o relatório.

## Instalação no Linux

1. Faça o Download do PPGEE-Lucy. 
Download aqui: [https://github.com/rencmbr/lucylattes/](https://github.com/rencmbr/lucylattes/). Vá na opção "Code". Se você trabalha com o git, escolha a opção "Clone". Se não for este o caso, escolha a opção `.zip` para fazer o download dos arquivos.

2. Se a opção foi o .zip, descompacte o arquivo em um diretório de sua preferência. 

3. Copie os *curriculos Lattes* desejados no diretório `xml_zip`. NÃO altere o nome e nem o formato dos arquivos baixados, e *NÃO DESCOMPACTE OS ARQUIVOS*. O nome do arquivo é composto por *16* caracteres e a extensão `.zip`, e.g. `3275865819287843.zip`. Dentro de cada arquivo .zip existirá um arquivo denominado curriculo.xml.

**Python**

- Se não possuir *Python3*  ou superior instalado no *DEBIAN, UBUNTU ou derivados*:

```
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-tk
```
**Ambiente virtual python** (virtual environments) no Linux

Para saber mais sobre *ambiente virtual* em `Python`, clique aqui [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html). O autor do `lucyLattes`, Rafael Tieppo, fez um post resumido sobre o assunto [AQUI](https://rafatieppo.github.io/post/2021_07_27_python_env/).

De forma resumida, sugiro a seguinte instalação do ambiente virtual:

1. Crie uma pasta (diretório) na pasta de instalação do PPGEE-Lucy com o nome .venv. Crie o ambiente virtual:

```
 mkdir .venv
 
 python3 -m venv .venv
 ```

2. Para ativar o ambiente virtual:

```
source .venv/bin/activate

(.venv) renato@renato-mint:~/my-lucylattes/ppgeelucy$  
```
(note o (.venv) no início do "prompt" de comando, indicando que o ambiente virtual está ativado.

3. Para Desativar o ambiente virtual:

```
(.venv) renato@renato-mint:~/my-lucylattes/ppgeelucy$ deactivate
renato@renato-mint:~/my-lucylattes/ppgeelucy$ 
```
note que (.venv) no início do "prompt" de comando desapareceu, indicando que o ambiente virtual foi desativado.

**Pacotes Python**

Para instalar os pacotes python necessários, acesse o **Terminal**, ative o ambiente virtual e instale os pacotes que estão listados no arquivo `requirements_lucyLattes.txt`. Para isso, use o `pip`, executando o comando

```
pip install -r requirements_lucyLattes.txt
```

o que instalará os pacotes necessários no ambiente virtual. 
## Como executar o programa

Pelo terminal, com o **ambiente virtual ATIVADO**, acesse o diretório onde o PPGEE-Lucy foi instalado e digite:

```
python3 app_ppgeelucy.py
```

Se a instalação estiver correta, o programa iniciará sua execução e, ao seu final, gravará os dados de saída do PPGEE no diretório `ppgee_data` O relatório gerado pelo `lucylattes` original estará no diretório `relatório`.

## Configurações:

1. As configurações originais para a execução do `lucylattes`estão no arquivo config_tk.txt. Estas configurações continuam a ser utilizadas pelo PPGEE-lucy e podem ser modificadas editando o arquivo. As linhas do arquivo devem ser mantidas na ordem em que se encontram e são as seguintes:
- ano inicial:2021
- ano final:2024
- qualis:qualis_todasareas_periodicos_2020.csv
- pg:Programa de Pós Graduação em Engenharia Elétrica - UFMG
- apagar csv_producao:0
- calcular indcapes:0
- calcular hwebsci:0

Onde ano inicial e ano final são os anos do período para o qual o relatório será gerado; 
qualis é o arquivo que será usado para a classificação Qualis dos artigos publicados (os arquivos de classificação estão na pasta jcr_qualis). Uma observação é que para as Engenharias IV o arquivo a ser usado atualmente é o qualis_todasareas_periodicos_2020.csv;
pg é o nome do programa de pós graduação em análise;
apagar_csv_producao indica, caso igual a 1, que os arquivos .csv gerados durante a execução do programa devem ser apagados ao final da execução (tenho sempre mantido ele igual a 0 (zero));
calcular indcapes indica, caso igual a 1, que os indicadores da capes devem ser calculados. Na realidade, esses indicadores ainda estão em fase de testes, não são calculados pelo lucylattes;
calcular hwebsci indica, caso igual a 1, que o "índice h" deve ser calculado.

2. As configurações para o PPGEE-Lucy estão no arquivo config_ppgee.txt. Assim como no caso anterior, as linhas do arquivo devem ser mantidas na ordem em que se encontram e são as seguintes:

- run_html_report: 1
- run_authors_classification: 1
- authors_classification_year: 2020

Onde run_html_report indica, caso igual a 1, que o relatório html original do script lucylattes deve ser gerado;
run_authors_classification indica, caso igual a 1, que a classificação dos autores de artigos (se docentes, discentes, egressos) deve ser gerada;
authors_classification_year é o ano que deve ser usado para a classificação dos autores de artigos. Isto é necessário porque classificação dos autores depende do ano (um discente neste ano pode se transformar em um egresso no ano seguinte, por exemplo).

## Arquivos de dados:

O PPGEE-Lucy utiliza os arquivos gerados pelos scripts do `lucylattes` e que são armazenados no diretório csv_producao. Ao rodar o app_ppgeelucy.py esses arquivos são automaticamente gerados a partir dos currículos Lattes armazenados no diretório xml_zip.
Além desses arquivos, o PPGEE-Lucy utiliza os seguintes arquivos de dados que devem ser colocados no diretório ppgee_data:

- Discentes-PPGEE-ano.csv : arquivo csv com os discentes do PPGEE no ano específico - por exemplo Discentes-PPGEE-2020.csv para o ano de 2020 e Discentes-PPGEE-2022.csv para o ano de 2022. Formato do arquivo: arquivo de texto, com os nomes do discente e do orientador separados por virgula e cada par de discente/orientador separado do seguinte por fim-de-linha. Caso um discente tenha mais de uma forma como o nome aparece nas publicacoes, basta incluir na lista as varias formas.
- Egressos-PPGEE-ano.csv: arquivo csv com os egressos do PPGEE: por exemplo Egressos-PPGEE-2020.csv, que contém os egressos do ano de 2020 e, pelo menos, dos cinco anos anteriores (2015 a 2019). Formato do arquivo: arquivo de texto, com o nome do egresso, seu CPF, Nível (se Mestrado ou Doutorado), nome do orientador e ano de defesa, separados por virgula. Caso um egresso tenha mais de uma forma como o nome aparece nas publicacoes, basta incluir na lista as varias formas, uma em cada linha.
- Docentes-PPGEE-NomesAlternativos-ano.csv: por exemplo, Docentes-PPGEE-NomesAlternativos-2020.csv para o ano de 2020. Arquivo csv com nomes alternativos para os docentes do PPGEE. Os nomes "oficiais", completos, dos docentes são gerados a partir da leitura dos currículos Lattes presentes no diretório xml_zip. Porém, existem situações (como, por exemplo, o caso em que o docente tem o sobrenome "FILHO", ou então "JUNIOR") em que versões alternativas dos nomes devem ser utilizadas. Nesse caso, basta incluir as versões (uma em cada linha) nesse arquivo.

## Arquivos de saida:

- Os arquivos no diretório csv_producao podem ser usados diretamente para análise da produção do programa;
- Os arquivos no diretório relatorio contêm uma síntese da produção do programa. Abra o arquivo relatorio_producao.html com um navegador para visualizar;
- Os arquivos artigosclassificados-PPGEE-ano.csv e eventosclassificados-PPGEE-ano.csv, no diretório ppgee_data, contêm a classificação (se docentes, discentes ou egressos) dos autores dos artigos em periódicos ou em eventos publicados no ano específico.

## Observações:

- No PPGEE-Lucy ainda há a possibilidade de rodar o `lucylattes` original. Basta executar, com o python3, o aplicativo app_lucy-Lattes,py ao invés do app_ppgeelucy.py. Maiores detalhes sobre o app_lucylattes, ver a documentação no site original do `lucylattes` - https://github.com/rafatieppo/lucylattes ;
- Os arquivos do PPGEE-Lucy estão bem separados dos arquivos do `lucylattes` original. Código de funções no diretório ppgee_resources (os do `lucylattes`estão no diretório resources) e arquivos de dados e saída de resultados no diretório ppgee_data. Os arquivos app_ppgeelucy.py e ppgeelucy.py, presentes no diretório de instalação do PPGEE-Lucy, não interferem nos arquivos originais do `lucylattes`também presentes neste diretório (app_lucyLattes.py, lucyLattes.py)

## A fazer:

- Incluir a identificação de autores que sejam alunos de graduação. Isso não parece complicado, basta usar a mesma lógica de identificação de discentes ou de egressos. No caso do PPGEE-UFMG a maior dificuldade parece estar na obtenção dos dados dos alunos da graduação;
- Gerar os indicadores utilizados pela Comissão de Área das Engenharias IV;
- Incluir o algoritmo utilizado no PPGEE-UFMG no credenciamento/recredenciamento de docentes;
- Incluir ferramentas para a detecção de anomalias nos dados do PPGEE-UFMG.

## Autores:
- Renato Cardoso Mesquita (PPGEE-Lucy)
- rencmbr@gmail.com
- https://github.com/rencmbr

Baseado nos trabalhos de:
- Rafael Tieppo (autor do `lucylattes`)
- rafaeltieppo@yahoo.com.br
- https://rafatieppo.github.io/

E no de Ricardo Hiroshi Caldeira Takahashi (classificação de autores)

## xml schemas


- general data

```
<CURRICULO-VITAE
    <DADOS-GERAIS
        <RESUMO-CV
        <ENDERECO
            <ENDERECO-PROFISSIONAL
        </ENDERECO>
    </DADOS-GERAIS>
```


- ppe
```
<CURRICULO-VITAE
    <ATUACOES-PROFISSIONAIS>
        <ATUACAO-PROFISSIONAL
            <ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO>
                <PARTICIPACAO-EM-PROJETO
                    <PROJETO-DE-PESQUISA
                        <EQUIPE-DO-PROJETO>
                        </EQUIPE-DO-PROJETO>
                    </PROJETO-DE-PESQUISA>
                </PARTICIPACAO-EM-PROJETO>
            </ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO>
        </ATUACAO-PROFISSIONAL>
    </ATUACOES-PROFISSIONAIS>
```

- books

```
<CURRICULO-VITAE
    <PRODUCAO-BIBLIOGRAFICA>
        <LIVROS-E-CAPITULOS>
            <LIVROS-PUBLICADOS-OU-ORGANIZADOS>
                <LIVRO-PUBLICADO-OU-ORGANIZADO>
                    <DADOS-BASICOS-DO-LIVRO />
                    <AUTORES />
                </LIVRO-PUBLICADO-OU-ORGANIZADO
            </LIVROS-PUBLICADOS-OU-ORGANIZADOS>
        </LIVROS-E-CAPITULOS
    </PRODUCAO-BIBLIOGRAFICA>
```

- chapters

```
<CURRICULO-VITAE
    <PRODUCAO-BIBLIOGRAFICA>
        <LIVROS-E-CAPITULOS>
            <CAPITULOS-DE-LIVROS-PUBLICADOS>
                <CAPITULO-DE-LIVRO-PUBLICADO>
                    <DADOS-BASICOS-DO-CAPITULO />
                    <AUTORES />
                </CAPITULO-DE-LIVRO-PUBLICADO
            </CAPITULOS-DE-LIVROS-PUBLICADOS>
        </LIVROS-E-CAPITULOS
    </PRODUCAO-BIBLIOGRAFICA>
```

- advising finished

```
<CURRICULO-VITAE
    <OUTRA-PRODUCAO>
        <ORIENTACOES-CONCLUIDAS>
            <ORIENTACOES-CONCLUIDAS-PARA-MESTRADO
            </ORIENTACOES-CONCLUIDAS-PARA-MESTRADO>
            <ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO
            </ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO>
            <ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO
            </ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO>
            <OUTRAS-ORIENTACOES-CONCLUIDAS
            </OUTRAS-ORIENTACOES-CONCLUIDAS>
        </ORIENTACOES-CONCLUIDAS
    </OUTRA-PRODUCAO>
```

- advising running

```
<CURRICULO-VITAE
    <DADOS-COMPLEMENTARES>
        <ORIENTACOES-EM-ANDAMENTO>
            <ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO>
            </ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO>
            <ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO>
            </ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO>
            <ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO>
            </ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO>
            <ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA>
            </ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA>
            <OUTRAS-ORIENTACOES-EM-ANDAMENTO>
            </OUTRAS-ORIENTACOES-EM-ANDAMENTO>
        </ORIENTACOES-EM-ANDAMENTO
    </DADOS-COMPLEMENTARES>
</CURRICULUM-VITAE>

```

- teaching

```
<CURRICULO-VITAE
    <ATUACOES-PROFISSIONAIS>
        <ATUACAO-PROFISSIONAL
            <ATIVIDADES-DE-ENSINO>
                <ENSINO
                    <DISCIPLINA
                    </DISCIPLINA>
                </ENSINO
            </ATIVIDADES-DE-ENSINO>
        </ATUACAO-PROFISSIONAL>
    </ATUACOES-PROFISSIONAIS>
```

- courses

```
<CURRICULO-VITAE
    <PRODUCAO-TECNICA>
        <DEMAIS-TIPOS-DE-PRODUCAO-TECNICA>
            <CURSO-DE-CURTA-DURACAO-MINISTRADO
            </CURSO-DE-CURTA-DURACAO-MINISTRADO>
        </DEMAIS-TIPOS-DE-PRODUCAO-TECNICA>
    </PRODUCAO-TECNICA>
```

- papers

```
<CURRICULO-VITAE
    <PRODUCAO-BIBLIOGRAFICA>
        <ARTIGOS-PUBLICADOS
            <ARTIGO-PUBLICADO>
                <DADOS-BASICOS-DO-ARTIGO />
                <AUTORES />
            </ARTIGO-PUBLICADO>
        </ARTIGOS-PUBLICADOS>
    </PRODUCAO-BIBLIOGRAFICA>
```

- worksevents

```
<CURRICULO-VITAE
    <PRODUCAO-BIBLIOGRAFICA>
        <TRABALHOS-EM-EVENTOS>
            <TRABALHO-EM-EVENTOS>
                <DADOS-BASICOS-DO-EVENTO />
            </TRABALHO-EM-EVENTOS>
                <AUTORES />
        </TRABALHOS-EM-EVENTOS>
    </PRODUCAO-BIBLIOGRAFICA>
```
