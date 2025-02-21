import openai
import google.generativeai as genai
import requests
import json
import time
import os
from dotenv import load_dotenv 

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GOOGLE_APII_KEY = os.environ.get("GOOGLE_APII_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("A variável de ambiente OPENROUTER_API_KEY não está definida.")
if not GOOGLE_APII_KEY:
    raise ValueError("A variável de ambiente GOOGLE_APII_KEY não está definida.")

PERGUNTA = "Qual é a importacia da inteligência artificial na área da saúde?"

def avalia_resposta_llm(resposta, llm_nome):
    try:
        promt_avaliacao = f"""
        A seguinte resposta foi gerada pelo modelo {llm_nome}
        para a pergunta: {PERGUNTA}

        Resposta:
        {resposta}
        
        Por favor, avalie a qualidade desta resposta com base nos critérios de clareza, coerência, precisão da informação, criatividade e consistência gramatical.
        """
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            },
            data=json.dumps({
                "model": "google/palm-2-codechat-bison",
                "messages": [
                    {
                        "role": "user",
                        "content": promt_avaliacao
                    }
                ]
            })
        )
        if response.status_code == 200:
            try:
                response_json = response.json()
                if 'choices' in response_json and len(response_json['choices']) > 0 and 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                    return response_json['choices'][0]['message']['content'].strip()
                else:
                    print(f"Erro: Resposta do OpenRouter em formato inesperado: {response_json}")
                    return None
            except json.JSONDecodeError:
                print(f"Erro: Resposta do OpenRouter não é um JSON válido: {response.text}")
                return None

        elif response.status_code == 429: 
            print("Erro: Limite de taxa atingido. Aguardando e tentando novamente.")
            time.sleep(2) 
            return avalia_resposta_llm(resposta, llm_nome) 
        else:
            print(f"Erro ao avaliar resposta com OpenRouter: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao avaliar resposta do {llm_nome}: {e}")
        return "Não foi possivel avaliar a resposta."

def gera_resposta_gemini(pergunta):
    try: 
        genai.configure(api_key=GOOGLE_APII_KEY)
        model = genai.GenerativeModel('gemini-pro')
        resposta = model.generate_content(pergunta)
        return resposta.text
    except Exception as e:
        print(f"Erro ao gerar resposta do Gemini: {e}")
        return None

def gera_resposta_openrouter(pergunta, modelo, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    },
                    data=json.dumps({
                        "model": modelo,
                        "messages": [
                            {
                                "role": "user",
                                "content": pergunta
                            }
                        ]
                    })
                )
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    if 'choices' in response_json and len(response_json['choices']) > 0 and 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                        return response_json['choices'][0]['message']['content'].strip()
                    else:
                        print(f"Erro: Resposta do OpenRouter em formato inesperado: {response_json}")
                        return None
                except json.JSONDecodeError:
                    print(f"Erro: Resposta do OpenRouter não é um JSON válido: {response.text}")
                    return None


            elif response.status_code == 429: 
                retries += 1
                wait_time = (2 ** retries)  
                print(f"Erro: Limite de taxa atingido. Aguardando {wait_time} segundos e tentando novamente (tentativa {retries}/{max_retries}).")
                time.sleep(wait_time)

            else:
                print(f"Erro ao gerar resposta com OpenRouter ({modelo}): {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Erro ao gerar resposta com OpenRouter ({modelo}): {e}")
            return None

    print(f"Falha ao gerar resposta com OpenRouter ({modelo}) após {max_retries} tentativas.") 
    return None  

def main():
    print("Enviando a pergunta para os LLMs...")

    resposta_gemini = gera_resposta_gemini(PERGUNTA)
    resposta_openrouter_chatgpt = gera_resposta_openrouter(PERGUNTA, "openai/gpt-3.5-turbo")
    resposta_openrouter_mistral = gera_resposta_openrouter(PERGUNTA, "mistralai/Mistral-7B-Instruct-v0.1") 

    print("\nRespostas dos LLMs:\n")
    print("Google Gemini:", resposta_gemini)
    print("OpenRouter (ChatGPT):", resposta_openrouter_chatgpt)
    print("OpenRouter (Mistral):", resposta_openrouter_mistral)

    print("\nAvaliando as respostas...\n")
    avaliacao_gemini = avalia_resposta_llm(resposta_gemini, "Google Gemini")
    avaliacao_chatgpt = avalia_resposta_llm(resposta_openrouter_chatgpt, "OpenRouter (ChatGPT)") 
    avaliacao_mistral = avalia_resposta_llm(resposta_openrouter_mistral, "OpenRouter (Mistral)")

    print("Avaliações das Respostas:\n")
    print("Avaliação Google Gemini:", avaliacao_gemini)
    print("Avaliação OpenRouter (ChatGPT):", avaliacao_chatgpt) 
    print("Avaliação OpenRouter (Mistral):", avaliacao_mistral)

    print("\nProcesso concluído.")


if __name__ == "__main__":
    main()