# AvaliadorREspostasLLM

# Avaliação de Respostas de LLMs

Este projeto demonstra como usar a API do Google Gemini e o OpenRouter para gerar respostas a uma pergunta e, em seguida, avaliar a qualidade dessas respostas usando outro LLM via OpenRouter.

## Pré-requisitos

*   **Python 3.6 ou superior:** Certifique-se de ter o Python instalado em seu sistema.
*   **Chaves de API:** Você precisará das seguintes chaves de API:
    *   `OPENROUTER_API_KEY`: Obtida no [OpenRouter](https://openrouter.ai/).
    *   `GOOGLE_APII_KEY`: Obtida no [Google AI Studio](https://makersuite.google.com/app/apikey).
*   **Bibliotecas Python:** As seguintes bibliotecas são necessárias:
    *   `openai`
    *   `google.generativeai`
    *   `requests`
    *   `python-dotenv`

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate.bat  # No Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    Se você não tiver um arquivo `requirements.txt`, pode instalar as dependências individualmente:

    ```bash
    pip install openai google-generativeai requests python-dotenv
    ```

## Configuração

1.  **Crie um arquivo `.env`:**

    Na raiz do projeto, crie um arquivo chamado `.env` e adicione suas chaves de API da seguinte forma:

    ```
    OPENROUTER_API_KEY=SUA_CHAVE_OPENROUTER
    GOOGLE_APII_KEY=SUA_CHAVE_GOOGLE_AI
    ```

    **Importante:** Não inclua este arquivo `.env` no seu repositório Git (ele já deve estar no `.gitignore`).

## Execução

1.  **Execute o script Python:**

    ```bash
    python seu_script.py  # Substitua seu_script.py pelo nome do seu arquivo python
    ```

    No caso deste código, o comando seria:

    ```bash
    python nome_do_arquivo.py
    ```

    (Substitua `nome_do_arquivo.py` pelo nome real do arquivo.)

## Explicação do Código

O código realiza as seguintes etapas:

1.  **Carrega as variáveis de ambiente:**  Usa a biblioteca `dotenv` para carregar as chaves de API do arquivo `.env`.
2.  **Define uma pergunta:** Define a pergunta que será enviada aos LLMs.
3.  **Gera respostas com diferentes LLMs:**
    *   Usa a API do Google Gemini para gerar uma resposta.
    *   Usa o OpenRouter para gerar respostas com o ChatGPT e o Mistral.
4.  **Avalia as respostas:**
    *   Usa o OpenRouter e o modelo `google/palm-2-codechat-bison` para avaliar a qualidade de cada resposta com base em critérios como clareza, coerência, precisão, criatividade e gramática.
5.  **Imprime as respostas e as avaliações:**  Exibe as respostas geradas pelos LLMs e as avaliações correspondentes.

## Observações

*   **Limites de Taxa:** As APIs do OpenRouter e do Google Gemini podem ter limites de taxa. O código inclui um tratamento básico para o erro 429 (limite de taxa atingido) no OpenRouter, esperando um curto período e tentando novamente.  Você pode precisar ajustar esse tempo de espera dependendo dos seus limites e do uso.
*   **Custos:** O uso das APIs do OpenRouter e do Google Gemini pode incorrer em custos.  Consulte as páginas de preços de cada serviço para obter informações detalhadas.
*   **Erros:** O código inclui algum tratamento de erros básico, mas pode ser necessário aprimorá-lo para lidar com diferentes tipos de erros e situações.
*   **Formato da Resposta:** O código espera que a resposta do OpenRouter esteja em um formato específico (JSON com uma lista de `choices` contendo um `message` com um campo `content`). Se o formato da resposta for diferente, o código pode não funcionar corretamente.
*   **Modelo de Avaliação:** O modelo `google/palm-2-codechat-bison` usado para avaliação foi escolhido como um exemplo. Você pode experimentar com outros modelos para obter diferentes perspectivas de avaliação.
*   **Melhorias:**  Este código pode ser aprimorado adicionando mais tratamento de erros, logs, opções de configuração (como a pergunta, os modelos a serem usados, os critérios de avaliação), e uma interface mais amigável.
*   **Arquivo `requirements.txt`:** Inclua um arquivo `requirements.txt` com as dependências do seu projeto.  Para gerar este arquivo, você pode usar o comando:

    ```bash
    pip freeze > requirements.txt
    ```

    Isso listará todas as bibliotecas instaladas no seu ambiente e as salvará no arquivo `requirements.txt`.
