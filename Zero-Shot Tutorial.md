# **🧠 Arquitecture Recommender: Semantic Similarity Engine**

Este projeto implementa um motor de recomendação de **arquiteturas de software** baseado em **similaridade semântica**. Utilizando o *Sentence Transformers* e a similaridade de cosseno, ele compara uma descrição de sistema fornecida pelo usuário com as descrições de arquiteturas de software predefinidas para sugerir as opções mais adequadas.

## **🚀 Como Funciona**

1. **Embeddings**: Um modelo pré-treinado (all-MiniLM-L6-v2) transforma a descrição do sistema (texto de entrada) e todas as descrições de arquitetura pré-definidas em vetores numéricos de alta dimensão (*embeddings*).  
2. **Similaridade de Cosseno**: O código calcula a similaridade do cosseno entre o vetor da descrição de entrada e o vetor de cada arquitetura.  
3. **Ranking**: As arquiteturas são ranqueadas com base na similaridade, sendo as mais altas as mais semanticamente próximas à descrição do sistema.

## **⚙️ Pré-requisitos**

Para executar este código, você precisa do Python instalado e das seguintes bibliotecas:

Bash  
pip install sentence-transformers torch

## **📂 Estrutura do Código**

O script é dividido em três seções principais:

### **1\. Dicionário de Arquiteturas (ARCHITECTURE\_DESCRIPTIONS)**

Este é o **banco de conhecimento** do sistema. Contém pares de **Nome da Arquitetura**: **Descrição Detalhada**.

| Arquitetura | Descrição |
| :---- | :---- |
| **MVC** | Padrão que separa a aplicação em Model, View e Controller. |
| **Microservices** | Divide a aplicação em serviços pequenos, independentes e implantáveis separadamente. |
| **Layered architecture** | Organiza o sistema em níveis de abstração distintos (apresentação, negócio, dados). |
| **Event-driven architecture** | Baseada na emissão, detecção e reação a eventos de forma assíncrona. |
| ... | E mais 8 arquiteturas clássicas (Serverless, Hexagonal, CQRS, etc.). |

---

### **2\. Funções Utilitárias**

* load\_embedding\_model(model\_name): Carrega o modelo de *embedding* do SentenceTransformer. Por padrão, usa **all-MiniLM-L6-v2** por ser eficiente e performático.  
* get\_embedding(text, model): Recebe um texto e retorna seu respectivo vetor (**torch.Tensor**) de *embedding*.  
* compute\_semantic\_similarity(...): A função central.  
  * Carrega o modelo.  
  * Calcula o *embedding* da descrição de entrada.  
  * Itera sobre todas as arquiteturas, calcula seus *embeddings* e a similaridade de cosseno.  
  * Retorna os resultados classificados da maior para a menor similaridade.  
* pretty\_print(result, top\_k): Exibe o resultado de forma legível, mostrando as arquiteturas com as maiores pontuações.

---

### **3\. Execução Principal (if \_\_name\_\_ \== "\_\_main\_\_":)**

Esta seção demonstra o uso do motor.

1. Uma variável description é definida com a descrição detalhada do sistema a ser analisado.  
2. A função compute\_semantic\_similarity é chamada para processar a descrição.  
3. O resultado é impresso na tela usando pretty\_print.

## **▶️ Exemplo de Uso**

Para executar a análise com a descrição de exemplo:

Python  
if \_\_name\_\_ \== "\_\_main\_\_":  
    description \= """  
    Linguagem dominante é o JS.  
    ...  
    Backend dividido em dois serviços NodeJS/Express:  
      \- Server: gerencia interações com DB.  
      \- Collector: coleta e processa documentos enviados.  
    """

    result \= compute\_semantic\_similarity(description)  
    pretty\_print(result, top\_k=10)

### **Saída Esperada:**

A saída mostrará as arquiteturas mais recomendadas e suas pontuações de similaridade. Note que a descrição de exemplo (com "Backend dividido em **dois serviços**") provavelmente resultará em alta pontuação para arquiteturas distribuídas:

Texto analisado:  
 Linguagem dominante é o JS.  
    Frontend: ViteJs \+ React.  
    Backend: NodeJs \+ Express (JS).  
    Permite rodar localmente (Desktop) e em servidores (Docker).  
    Funcionalidade principal: RAG (Geração Aumentada por Recuperação).  
    Objetivo: construtor no-code de IAs.  
    Suporta múltiplos modelos LLM (Gemini, OpenAI, Ollama, etc.).  
    Permite escolher Vector DB (LanceDB, PGVector, Pinecone, etc.).  
    Backend dividido em dois serviços NodeJS/Express:  
      \- Server: gerencia interações com DB.  
      \- Collector: coleta e processa documentos enviados. ...

Top 10 arquiteturas mais semelhantes (label : similaridade):  
  \- Microservices                 : 0.7012  \# Alta similaridade com 'serviços separados'  
  \- Serverless                    : 0.6125  
  \- Event-driven architecture     : 0.5987  
  \- Service-oriented architecture : 0.5540  
  \- Client-server                 : 0.5402  
  \- ...

## **✍️ Personalização**

Para usar com suas próprias descrições:

1. **Edite a descrição:** Modifique a string da variável description no bloco if \_\_name\_\_ \== "\_\_main\_\_":.  
2. **Adicione arquiteturas:** Você pode estender o dicionário ARCHITECTURE\_DESCRIPTIONS com novas arquiteturas e suas descrições.  
3. **Mude o modelo:** Altere o parâmetro model\_name na função load\_embedding\_model para experimentar outros modelos do **Sentence-Transformers**, como all-mpnet-base-v2.

