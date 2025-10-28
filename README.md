## Demo HBr - MCP Server

![status](https://img.shields.io/badge/status-active-brightgreen)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![ollama](https://img.shields.io/badge/ollama-required-yellow)
![mysql](https://img.shields.io/badge/mysql-required-orange)
![license](https://img.shields.io/badge/license-TODO-lightgrey)

Descrição
---------

Este repositório contém um servidor MCP (Model-Chain-Provider) simples feito com FastMCP para expor tools que interagem com uma base MySQL. O projeto usa Llama Index para construir agentes que consomem essas tools e Ollama como provedor local de LLM (modelo local).

Principais componentes
- `servidor.py` — servidor MCP que registra ferramentas (tools) para adicionar, ler e apagar dados da tabela `tomografo`.
- `cliente_ollama.ipynb` — notebook com exemplo de cliente que consome as tools via Llama Index e cria um agente usando Ollama.

Funcionalidades
- Ferramentas MCP para INSERT/SELECT/DELETE em uma tabela de exemplo (`tomografo`).
- Integração com Llama Index para construir um agente baseado em funções.
- Execução local de modelos via Ollama (ex.: `qwen3:4b`).

Requisitos
- Python 3.8+
- MySQL Server (com um banco `hbr_demo_db` disponível ou criar manualmente)
- Ollama instalado e com o(s) modelo(s) necessários (ex.: `qwen3:4b`)
- Dependências Python listadas em `requirements.txt`

Configurações relevantes
- Em `servidor.py`, a função `init_db()` usa por padrão:
  - user: `root`
  - password: `pass123`
  - host: `127.0.0.3`
  - database: `hbr_demo_db`

  Obs: esses valores podem ser alterados diretamente no arquivo ou adaptados para usar variáveis de ambiente se preferir. Se o banco de dados não existir, crie-o antes de iniciar o servidor:

  ```sql
  CREATE DATABASE IF NOT EXISTS hbr_demo_db;
  ```

Como executar
--------------

1) Instale dependências Python

```powershell
python -m pip install -r requirements.txt
```

2) Configure MySQL

- Certifique-se que o MySQL está rodando e que a base `hbr_demo_db` existe. Atualize as credenciais/host em `servidor.py` se necessário.

3) Garanta que o Ollama e o modelo local estejam prontos

- Instale e carregue o modelo desejado no Ollama (ex.: `qwen3:4b`). Consulte a documentação do Ollama para os comandos de instalação/carregamento.

4) Inicie o servidor MCP

```powershell
python servidor.py --server_type=sse
```

5) Execute o cliente (notebook)

- Abra `cliente_ollama.ipynb` e execute as células. O notebook se conecta ao endpoint SSE padrão `http://127.0.0.1:8000/sse` (confirme a URL/porta do servidor se necessário).

Uso rápido
-----------

- O notebook demonstra:
  - criação das tools a partir do servidor MCP (via `BasicMCPClient`).
  - construção de um agente `FunctionAgent` usando Llama Index com `Ollama` como LLM.
  - loop interativo para enviar mensagens ao agente, que pode chamar as tools do servidor.

Notas de troubleshooting
-----------------------
- Erro de conexão MySQL: verifique usuário/senha/host/porta e se o serviço do MySQL está ativo.
- Banco de dados não existe: criar `hbr_demo_db` manualmente.
- Problemas com Ollama: confirme que o modelo indicado no notebook (`qwen3:4b`) está instalado e disponível localmente.
- Endpoint MCP: se o servidor não estiver em `127.0.0.1:8000`, atualize o notebook para apontar para a URL correta.

Segurança e privacidade
-----------------------

- Este projeto é um exemplo/demo. Não armazene credenciais sensíveis no repositório. Use variáveis de ambiente ou um arquivo de configuração seguro para credenciais em produção.

Próximos passos sugeridos
-------------------------
- Adicionar um `LICENSE` apropriado.
- Incluir CI (ex.: GitHub Actions) para lint/testes.
- Adicionar exemplos automatizados e testes unitários para as ferramentas MCP.

Contribuição
------------

Sinta-se à vontade para abrir issues e pull requests. Para mudanças maiores, descreva o caso de uso e inclua testes reproduzíveis.

Contato
-------

Projeto mantido pela equipe HBr - CIIA.
