# consultaCNPJ

Código feito em python que realiza uma consulta na API da receita federal brasileira para puxar alguns dados de empresas.

É necessário criar um documento .txt no mesmo repositório em que o código estiver e salvar com o nome de "cnpjs" e dentro dele colar 
e digitar apenas os números dos cnpjs desejados.

Visto que a API libera apenas 3 consultas de cnpjs por minutos de graça, acrescentei um timer que faz com que o programa registre 3 consultas
aguarde o tempo e faça mais três consultas até o último cnpj do arquivo.

Ao final da consulta sera disponibilizado no diretório um arquivo chamado resultados.txt, nele estarão contidos os dados que especifiquei na consulta, contudo a API é publica e da para brincar e escolher outras informações de acordo com a necessidade determinada por você.
