# Metacash 💸 - Gerenciamento Financeiro

## 🚀 Visão Geral
Metacash é uma aplicação para gerenciamento de finanças pessoais, projetado com uma arquitetura de software moderna e limpa em Python. Este sistema serve como o "cérebro" para uma futura interface gráfica, lidando com toda a lógica de negócio, gerenciamento de usuários e persistência de dados.

## ✨ Funcionalidades

-   **Gerenciamento Completo de Usuários (CRUD):** Cadastro, Login, Atualização e Deleção.
-   **Segurança:** Login com Autenticação de Dois Fatores (2FA) via e-mail e gerenciamento seguro de credenciais.
-   **Perfil Financeiro:** Registro de salário, gastos fixos e definição de preferências de gastos (escala 1-5).
-   **Gerenciamento de Metas:** Criação, atualização e acompanhamento de metas financeiras.
-   **Relatório de gastos:** Gráfico de pizza que mostra como estão distribuidos seus gastos.
-   **Diagnóstico de gastos:** Fala se seu gasto está de acordo ou não com suas preferências.
-   **Dicas de economia diarias:** Da uma dica baseada em trasnporte, alimentação ou lazer todo dia.

## 🚀 Guia de Instalação e Execução

Para configurar e rodar este projeto em uma nova máquina, abra seu terminal (PowerShell no Windows, ou Terminal no macOS/Linux) e siga os passos abaixo.

**Certifique-se de ter [Python 3.10+](https://www.python.org/downloads/) e [Git](https://git-scm.com/downloads) instalados.**

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/metacash.git](https://github.com/seu-usuario/metacash.git)
cd metacash
```

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

Isso cria um ambiente isolado para as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\activate
# No macOS/Linux (Bash/Zsh):
source venv/bin/activate
```
Após a ativação, você verá `(venv)` no início do seu terminal.

### 3. Instalar as Dependências

Com o ambiente ativo, instale todas as bibliotecas necessárias de uma só vez usando o arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

Para que o envio de e-mail da verificação de dois fatores funcione, você precisa criar um arquivo `.env` com suas credenciais.

1.  **Crie uma Senha de App** para sua conta do Gmail seguindo as [instruções do Google](https://support.google.com/accounts/answer/185833). Isso irá gerar uma senha segura de 16 letras.

2.  Crie o arquivo de exemplo `.env.example` para criar seu arquivo de configuração local.
    ```bash
    # No Windows:
    copy .env.example .env
    # No macOS/Linux:
    cp .env.example .env
    ```

3.  Abra o arquivo `.env` que você acabou de criar e preencha com suas credenciais:
    ```
    EMAIL_REMETENTE=seu_email_remetente@gmail.com
    SENHA_APP_EMAIL=sua_senha_de_app_de_16_letras
    ```

### 5. Executar a Aplicação (Simulação)

Com tudo configurado, execute o arquivo `main.py` para ver a simulação da lógica da aplicação em ação.
```bash
python interface.py
```
## Fluxogramas do projeto
- Clicando nesse link você vai ser redirecionado para um drive com os principais fluxos do MetaCash (https://drive.google.com/drive/folders/1cc7KhsOQPP752RGZlG_YJhrb04sT5AXg)
