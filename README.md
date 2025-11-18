<h1 align="center"> Sistema Produtiva - Aplicação web para gerenciamento de tarefas e controle de tempo, desenvolvida com Django</h1>
<img width="344" height="108" alt="logo" src="https://github.com/user-attachments/assets/97476068-a9e4-4606-9b2c-3135cbeb3ab7" />

## Índice 
* [Descrição do Projeto](#descrição-do-projeto)
* [Funcionalidades e Demonstração da Aplicação](#funcionalidades-e-demonstração-da-aplicação)
* [Manual de instalação](#manual-de-instalação)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Banco de Dados](#banco-de-dados)
* [Pessoas Desenvolvedoras do Projeto](#pessoas-desenvolvedoras)
* [Conclusão](#conclusão)

## Descrição do Projeto
Este sistema concilia o controle de tarefas e o registro de horas trabalhadas, buscando também manter o histórico das atividades concluídas e gerar relatórios de comparação entre a expectativa e a realização real das tarefas, permitindo maior produtividade para profissionais em trabalho remoto.
# :hammer: Funcionalidades do projeto
- `1`: O sistema é dividido em dois tipos de usuários: Administrador, que tem acesso a todas as funcionalidades do sistema, e Usuário comum, que pode gerenciar as próprias tarefas e apontamentos.
- `2`: Os usuários comuns têm acesso apenas aos projetos dos quais participam e podem visualizar os outros participantes envolvidos nesses mesmos projetos.
- `3`: Apenas os administradores podem criar novos projetos e delegá-los aos participantes.
- `4`: O sistema conta com categorização de tarefas com base na Matriz de Eisenhower.
- `5`: Os apontamentos podem ser iniciados e dado uma descrição (opcional) o status do ver/lançar na página de tarefas mudará para ˜em andamento˜ até que o apontamento seja parado.
- `6`: O apontamento quando registrado ficará visivel o usuário responsável, o tempo inicial e final (com a data) e a descrição se houver. 
- `7`: Projetos e tarefas podem ser criados, cancelados, restaurados e excluídos definitivamente.
- `8`: O relatório do projeto estará disponível para visualização por ambos os tipos de usuários apenas quando o projeto for marcado como concluído.

## Manual de Instalação 
`Passo a passo da instalação`
1. Clonar o repositório e entar na pasta do projeto
```bash
git clone https://github.com/anacstralioti/pi-ifsc.git
cd <pi-ifsc>
```
2. Criar e ativar um ambiente virtual (venv)
Linux / macOS:
 ```bash
 python -m venv venv
 source venv/bin/activate
```
Windows (PowerShell):
```bash
 python -m venv venv
 venv\Scripts\Activate.ps1
```
Windows (cmd):
```bash
 python -m venv venv
 venv\Scripts\activate
```
3. Instalar dependências
instale as dependências utilizando pip:
```bash
 pip install Django 
 pip install python-decouple 
 python -m pip install Pillow
```
Se preferir instalar todas de uma vez utilize o arquivo requirements.txt:
```bash
 pip install -r requirements.txt
 ```
4. Crie um arquivo .env na raiz do projeto com a SECRET_KEY. Exemplo:
Dentro de .env:
```bash
SECRET_KEY='sua_chave_secreta_aqui'
DEBUG=True
 ```
Para gerar uma SECRET_KEY você pode usar o próprio Django (from django.core.management.utils import get_random_secret_key) ou um gerador online confiável.

5. Preparar o banco de dados
Para criar um superusuário (acesso ao admin):
```bash
 python manage.py createsuperuser
```
6. Iniciar o servidor de desenvolvimento
```bash
python manage.py runserver
```
Acesse o sistema em: http://127.0.0.1:8000/

- Uso básico
* Abra o navegador e acesse: http://127.0.0.1:8000/
* Faça login com um usuário cadastrado ou acesse o painel administrativo em http://127.0.0.1:8000/admin/.
* Navegue pelos módulos: Projetos, Tarefas e Apontamentos e Relatório.

## Tecnologias Utilizadas
-  `Back-end`: `Python`
- `Framework`: `Django`
- `Banco de dados`: `SQLite`
- `Front-end`: `HTML`, `Tailwind CSS`, `JavaScript`
- `IDE recomendada`: `Visual Studio Code` (opcional)

## Banco de dados
- Nome do arquivo padrão: db.sqlite3
- Arquivo de importação: db.sqlite3
- Aplicação em execução local padrão: http://127.0.0.1:8000/
  
## Pessoas Desenvolvedoras 
* Ana Stralioti - https://github.com/anacstralioti
* Stephane Vale - https://github.com/Stephanevale
  
## Conclusão
A aplicação “Produtiva” buscará capacitar profissionais a ter um controle aprimorado de rotina, refletindo diretamente em sua produtividade, e, de forma secundária, oferecerá um meio de demonstrar o tempo trabalhado, recurso particularmente importante para trabalhadores em regime remoto.


