# Projeto de Pesquisa: Servidor de Diálogos

## Membros do Grupo

| **Matrícula** | **Aluno** |
| :--: | :--: |
| 20/0018167 |  Gabriel Mariano da Silva |
| 19/0088257 |  Guilherme Keyti Cabral Kishimoto |
| 15/0141629 | Matheus Leal Pimentel |
| 19/0117401 | Thalisson Alves G. de Jesus |

## Como executar?

Para executar a plataforma, primeiramente é necessário instalar os softwares utilizados na mesma. Os passos para a instalação destes estão melhor descritos no [**Relatório do Projeto**](/docs/Relatorio_TrabalhoFinal_FRC_2023_2.pdf).

Tendo estes instalados e os arquivos dos diretórios "*/etc*", "*/var*" devidamente localizados no diretório *root* de sua máquina *Linux*, é necessário instalar as dependências necessárias para o projeto. Para isto, execute o seguinte comando:

```
pip3 install -r code/requirements.txt
```

Feito isso, agora execute o código *python* referente ao *back-end* da plataforma com o seguinte comando:

```
python3 code/src/server.py
```

Pronto! Agora a plataforma já pode ser acessada através de sua *URL* em seu *browser* de preferência. Abaixo, algumas possibilidades (utilizando *HTTP* e *HTTPS*, respectivamente) a serem acessadas em seu *browser*:

#### Utilizando *HTTP*:

```
http://projetofrc.com
```

#### Utilizando *HTTPS*:

```
https://projetofrc.com
```

É importante ressaltar que, ao acessar a plataforma pela primeira vez, é provável que apareça uma página informando que "este *site* não é seguro". Todavia, basta clicar na opção de "continuar o acesso" (ou algo similar) para acessar a plataforma!

## Apresentação do Projeto

A apresentação do projeto está disponível no [**YouTube**](www.google.com). Os slides utilizados na apresentação estão disponíveis no [**Repositório do GitHub**](/docs/Slides_TrabalhoFinal_FRC_2023_2.pdf).

## Relatório do Projeto

O relatório do projeto está disponível no [**Repositório do GitHub**](/docs/Relatorio_TrabalhoFinal_FRC_2023_2.pdf).