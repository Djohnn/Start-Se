# Plataforma de Conexão entre Empreendedores e Investidores

Este projeto foi desenvolvido utilizando Python, Django. A aplicação conecta empreendedores, empresas e investidores, permitindo que empresas ofereçam partes de sua organização para investimento e que investidores possam adquirir essas ações de forma simplificada.

## Estrutura do Projeto

A aplicação é composta por três principais apps:

1. **Usuários**: 
   - Responsável pelo registro e gerenciamento de novos usuários.
   - Usuários podem ser classificados como empreendedores, clientes ou investidores.

2. **Empresários**:
   - Gerencia as empresas cadastradas, incluindo documentos e métricas relacionadas.
   - Empresários podem gerenciar suas empresas e decidir quais partes da empresa serão disponibilizadas para investimento.

3. **Investidores**:
   - Facilita a busca por empresas e a seleção de perfis de investimento.
   - Investidores podem fazer ofertas para adquirir ações das empresas cadastradas.
   - Os empresários têm o poder de decidir se aceitam ou não as propostas de investimento.

## Funcionalidades Principais

- Registro de usuários com diferentes perfis (empreendedores, clientes e investidores).
- Gestão de empresas, documentos e métricas através do app Empresários.
- Sistema de busca e propostas de investimento através do app Investidores.
- Conexão eficiente entre empreendedores e investidores para facilitar o processo de investimento.

## Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento da aplicação.
- **Django**: Framework web utilizado para estruturar a aplicação.
- **RAD (Rapid Application Development)**: Metodologia utilizada para o desenvolvimento rápido e iterativo.

## Instalação e Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/nome-do-repositorio.git

2. Navegue até o diretório do projeto:
    ```bash
    cd nome-do-repositorio
    
3. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt

5. Execulte as migrações:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver

## Uso 
   - Acesse a aplicação em http://localhost:8000.
   - Realize o registro de um novo usuário através do app Usuários.
   - Navegue pelo app Empresários para gerenciar empresas e documentos.
   - Utilize o app Investidores para buscar empresas e fazer ofertas de investimento.
   - Contribuição
   - Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença 
   - Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

