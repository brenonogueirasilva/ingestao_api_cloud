# Projeto de Engenharia de Dados: Ingestão de Dados por API em ambiente Cloud (GCP)

## Introdução

O objetivo deste projeto é desenvolver uma automação que colete dados governamentais por meio de uma API e armazene esses dados. O projeto será implementado em um ambiente de nuvem, especificamente na Google Cloud Platform (GCP). Utilizaremos Cloud Functions como local de execução do código, que será desenvolvido em Python, seguindo os princípios da programação orientada a objetos (POO) e as melhores práticas de programação.

Após a coleta dos dados da API, as respostas serão salvas no formato JSON no Cloud Storage e, posteriormente, serão inseridas no BigQuery. O gatilho de execução será configurado por meio do Cloud Scheduler. Toda a infraestrutura será provisionada utilizando o Terraform, que permite a criação da infraestrutura como código.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação utilizada para o desenvolvimento da pipeline.
- **Cloud Functions:** O ambiente na nuvem que executará o código Python, fornecendo escalabilidade e flexibilidade.
- **Cloud Storage:** Um ambiente na nuvem que permitirá armazenar os arquivos JSON, incluindo as respostas da API de forma segura e escalável.
- **Cloud Scheduler:** Uma ferramenta na nuvem que permite agendar a execução das Cloud Functions, possibilitando automação e programação de tarefas.
- **BigQuery:** Um sistema de armazenamento na nuvem que não apenas permite salvar os dados no formato JSON, mas também facilita consultas e análises avançadas, atuando como uma espécie de banco de dados em nuvem.
- **Terraform:** Uma ferramenta que possibilita a provisionamento eficiente de toda a infraestrutura necessária, seguindo a metodologia de infraestrutura como código (IaC).
  
<p align="left">
<img src="/img/python-logo.png" alt="python" height="50" /> 
<img src="/img/postgres-logo.png" alt="postgres" height="50" /> 
<img src="/img/docker-logo.png" alt="docker" height="50"/> 
</p>

## Arquitetura

![Diagrama de Arquitetura](img/arquitetura_ingestao_por_api.png)

## Etapas do Projeto

### 1. Estudo da Documentação da API

Realização de um estudo da documentação da API, no caso a Brasil API (https://brasilapi.com.br/docs) para o entendimento de como utilizá-la e realizar as requisições. No caso desta API, as requisições são unicamente do tipo GET, sendo necessário apenas passar parâmetros e, para alguns endpoints, mudar os paths dependendo do estado na qual se queria a informação, por exemplo.

### 2. Desenvolvimento da Lógica para Realizar a Requisição à API

Desenvolvimento da classe BrasilApi para lidar com a interação com a API, incluindo requisições e tratamento de erros. Essa classe possibilita a criação de requisições à API e a geração de nomes de arquivos que posteriormente salvarão o conteúdo da resposta para facilitar a identificação. Além disso, a classe também retorna um dicionário denominado "envelope," o qual contém informações cruciais sobre a requisição. 

Isso se torna necessário devido à natureza das respostas da API, que geralmente não incluem detalhes relacionados à solicitação em si. Por exemplo, ao solicitar informações sobre os municípios do estado de São Paulo, a resposta pode conter todos os municípios de São Paulo, mas não fornece informações específicas sobre o estado. Isso pode dificultar a identificação do estado ao inserir informações de vários estados no banco de dados. Portanto, o "envelope" é um dicionário que é incorporado à resposta em formato JSON, servindo como uma espécie de metadados da requisição. 

Além disso, foi desenvolvida a classe "cloud_storage" para possibilitar a interação com o Cloud Storage da Google, que será o repositório na nuvem usado para armazenar as respostas da API no formato JSON. Paralelamente, também foi criada a classe "big_query" para interagir com o BigQuery da Google, permitindo a inserção de tabelas originadas dos dados em formato JSON, bem como a consulta dessas tabelas. O BigQuery servirá como o local de armazenamento principal para os dados coletados pela API, oferecendo a capacidade de armazenar e consultar esses dados de forma eficiente. 
no qual será salva as repostas da API em arquivos json

### 3. Automação de Várias Requisições

Quando é necessário obter informações sobre municípios de diferentes estados, várias requisições devem ser feitas, o que pode exigir a criação de inúmeros objetos "BrasilAPI". Para simplificar o processo de requisições com diversos parâmetros, foi desenvolvido a classe OrquestratorAPI . Essa classe aceita um dicionário de parâmetros contendo listas de parâmetros e/ou caminhos, permitindo a iteração nessas listas. Isso possibilita a realização de várias requisições e o armazenamento dos retornos em arquivos JSON. Com essa classe, abstraímos a necessidade de criar múltiplos objetos "BrasilAPI," tornando simples a criação de parâmetros e/ou paths que contenham a lista de estados desejados. A própria classe cuida de realizar as várias requisições.

Essa lógica nos permitiu efetuar inúmeras requisições à API e salvar os resultados na Cloud Storage e posteriormente inserir estes dados no BigQuery.

### 4. Provisionamento da infraestrutura na Nuvem

Até o momento, todo o código foi executado em um ambiente local. Para permitir a interação com as ferramentas mencionadas, foi criada uma conta de serviço no Google Cloud Platform (GCP) com permissões para acessar o Cloud Storage e o BigQuery. Chaves de acesso foram geradas para que o código pudesse interagir com essas ferramentas. Os testes de desenvolvimento foram conduzidos nesse ambiente local.

Além disso, foi utilizada a biblioteca "framework," que possibilita simular a execução de uma Cloud Function localmente. Posteriormente, para provisionar a infraestrutura na nuvem, será empregado o Terraform, uma poderosa ferramenta que permite a implementação da infraestrutura como código (IaC), considerada uma boa prática em DevOps.

Nesse contexto, foram criados diversos arquivos:
- "variables.tf": Define variáveis que serão utilizadas em várias partes do código, simplificando a alteração de parâmetros quando necessário.
- "provider.tf": Contém o código que permite a conexão com o GCP, lendo um arquivo JSON associado às chaves de uma conta de serviço que possui todas as credenciais necessárias para implantar a infraestrutura.
- "outputs.tf": Retorna informações essenciais após a execução do código, como o URL do gatilho da Cloud Function.
- "main.tf": Contém vários recursos, incluindo a criação de um bucket no Cloud Storage (usado para armazenar o código da Cloud Function), a definição do objeto do bucket (que é um arquivo zip da pasta "src" contendo todo o código) e a criação da Cloud Function com as configurações necessárias.
    
Com os arquivos corretos e configurados, basta executar os comandos do Terraform para implantar a infraestrutura na nuvem e executar o código automaticamente.

Por fim, foi configurado no Cloud Scheduler um agendamento para a execução periódica da Cloud Function, garantindo a automação de acordo com a periodicidade necessária.


## Pré-Requisitos

Para execução do codigo é necessário possuir terraform instalado na máquina local, uma conta no GCP com criação de um usuário de serviço com acesso a todos os servicos mencionados no projeto.

## Executando o Projeto

Siga os passos abaixo para executar este projeto:

1. Copie o diretório do projeto para uma pasta local em seu computador.
2. Abra o terminal do seu computador e mova até o diretório do projeto.
3. Crie uma conta de servico no GCP com a credencias a todos os serviços mencionados e baixe uma chave em um arquivo json e coloque o arquivo no diretório raiz com nome apt-theme-402300-32506a51a70d
4. Execute o comando: `terraform init`
5. Execute o comando: `terraform plan`
6. Execute o comando: `terraform apply`

