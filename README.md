# consultaCNPJ

Código feito em python que realiza uma consulta na API da receita federal brasileira para puxar alguns dados de empresas.

É necessário criar um documento .txt e salvar com o nome de "cnpjs" e dentro dele digitar apenas os números dos cnpjs desejados um abaixo do outro sem pontuações ou espaços.

Visto que a API libera apenas 3 consultas de cnpjs por minutos de graça, acrescentei um timer que faz com que o programa registre 3 consultas
aguarde o tempo e faça mais três consultas até o último cnpj do arquivo.

Ao final da consulta estarão contidos os dados que especifiquei no código, como nome da empresa, cidade, estado e etc, contudo a API é publica e da para escolher outras informações de acordo com a necessidade determinada por você.

Atualizado para criar um front-end que tenha uma barra de progresso com uma contagem regressiva para o usuário aguardar e ter noção de quanto tempo falta.

Foi criado um instalador com o inno setup para o código em um único arquivo e este estará disponível também aqui.
