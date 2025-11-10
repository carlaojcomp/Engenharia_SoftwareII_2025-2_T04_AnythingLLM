from sentence_transformers import SentenceTransformer
import torch
from typing import List, Dict, Any
from torch.nn.functional import cosine_similarity

# ===============================================================
# 🔹 Dicionário de arquiteturas com descrições detalhadas
# ===============================================================
ARCHITECTURE_DESCRIPTIONS = {
    "MVC": (
        "Model-View-Controller (MVC) é um padrão arquitetural que separa "
        "a aplicação em três camadas: Model (lógica de dados e regras de negócio), "
        "View (interface com o usuário) e Controller (coordena a interação entre "
        "modelos e visões). É muito usado em frameworks web como Django, Rails e Spring MVC."
    ),
    "Microservices": (
        "Arquitetura de Microservices divide a aplicação em serviços pequenos, "
        "independentes e implantáveis separadamente. Cada serviço é responsável por uma "
        "função específica e se comunica com outros via APIs. Facilita escalabilidade, "
        "resiliência e implantação contínua."
    ),
    "Layered architecture": (
        "A arquitetura em camadas organiza o sistema em níveis de abstração distintos, "
        "como apresentação, lógica de negócio e acesso a dados. Cada camada depende apenas "
        "da camada imediatamente inferior. É um modelo clássico de sistemas corporativos."
    ),
    "Monolithic": (
        "Arquitetura monolítica é aquela em que toda a lógica de aplicação está agrupada "
        "num único bloco implantável. É mais simples de desenvolver inicialmente, mas "
        "dificulta a escalabilidade e manutenção em sistemas grandes."
    ),
    "Event-driven architecture": (
        "Arquitetura orientada a eventos é baseada na emissão, detecção e reação a eventos. "
        "Os componentes são fracamente acoplados e se comunicam de forma assíncrona via filas "
        "ou brokers como Kafka e RabbitMQ. Ideal para sistemas altamente reativos e escaláveis."
    ),
    "Plugin/modular architecture": (
        "Arquitetura modular ou de plugins permite estender funcionalidades do sistema "
        "sem alterar seu núcleo. Cada módulo ou plugin pode ser adicionado ou removido "
        "de forma independente. Usada em IDEs, jogos e plataformas extensíveis."
    ),
    "Serverless": (
        "Arquitetura Serverless executa funções sob demanda na nuvem, sem que o desenvolvedor "
        "precise gerenciar servidores. Cada função é acionada por eventos e escala automaticamente. "
        "Usada em plataformas como AWS Lambda e Google Cloud Functions."
    ),
    "CQRS": (
        "Command Query Responsibility Segregation (CQRS) separa operações de escrita (commands) "
        "e leitura (queries) em modelos distintos, otimizando desempenho e consistência. "
        "É comum em sistemas com alta carga de leitura e necessidade de eventos consistentes."
    ),
    "Hexagonal architecture": (
        "Arquitetura Hexagonal (ou Ports and Adapters) separa o núcleo da aplicação "
        "das interfaces externas (banco de dados, UI, APIs) por meio de portas e adaptadores. "
        "Facilita testes e independência de infraestrutura."
    ),
    "Onion architecture": (
        "Arquitetura Onion é uma variação da Hexagonal, com camadas concêntricas "
        "em torno do domínio central. Cada camada depende apenas da camada mais interna. "
        "Promove alta coesão e baixo acoplamento."
    ),
    "Client-server": (
        "Arquitetura cliente-servidor separa o sistema em dois papéis principais: "
        "o cliente (interface que solicita recursos) e o servidor (componente que os fornece). "
        "Modelo clássico da web moderna."
    ),
    "Service-oriented architecture": (
        "Arquitetura orientada a serviços (SOA) organiza o sistema como um conjunto de serviços "
        "reutilizáveis e interoperáveis que se comunicam por protocolos padronizados, "
        "como SOAP e REST. É um precursor dos microserviços."
    ),
}

# ===============================================================
# 🔹 Funções utilitárias
# ===============================================================
def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """Carrega modelo de embedding Sentence-Transformers."""
    # Carrega o modelo de forma otimizada
    model = SentenceTransformer(model_name)
    # Retornamos o modelo. O tokenizer está embutido nele
    return model

# NOVO MÉTODO DE EMBEDDING
def get_embedding(text: str, model) -> torch.Tensor:
    """Retorna embedding da sentença usando o método otimizado do S-T."""
    embedding_list = model.encode([text], convert_to_tensor=True, show_progress_bar=False)
    return embedding_list[0] # Retorna o tensor do primeiro (e único) item da lista

# Ajuste o 'compute_semantic_similarity' para usar o novo 'load_embedding_model'
def compute_semantic_similarity(description: str,
                            architecture_descriptions: Dict[str, str] = ARCHITECTURE_DESCRIPTIONS,
                            model_name: str = "all-MiniLM-L6-v2") -> Dict[str, Any]:
    """Calcula similaridade entre a descrição do sistema e embeddings das arquiteturas."""

    # O S-T agora retorna apenas o modelo, não o tokenizer separadamente
    model = load_embedding_model(model_name)

    # Passe apenas o modelo para get_embedding
    desc_emb = get_embedding(description, model)

    results = []
    for label, desc in architecture_descriptions.items():
        label_emb = get_embedding(desc, model)
        sim = cosine_similarity(desc_emb.unsqueeze(0), label_emb.unsqueeze(0)).item()
        results.append((label, sim))

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return {
        "sequence": description,
        "labels_scores": results
    }

def pretty_print(result: Dict[str, Any], top_k: int = 5):
    print("Texto analisado:\n", result["sequence"][:800], "...\n")
    print(f"Top {top_k} arquiteturas mais semelhantes (label : similaridade):")
    for label, score in result["labels_scores"][:top_k]:
        print(f"  - {label:<30} : {score:.4f}")

# ===============================================================
# 🔹 Execução principal
# ===============================================================
if __name__ == "__main__":
    description = """
    Linguagem dominante é o JS.
    Frontend: ViteJs + React.
    Backend: NodeJs + Express (JS).
    Permite rodar localmente (Desktop) e em servidores (Docker).
    Funcionalidade principal: RAG (Geração Aumentada por Recuperação).
    Objetivo: construtor no-code de IAs.
    Suporta múltiplos modelos LLM (Gemini, OpenAI, Ollama, etc.).
    Permite escolher Vector DB (LanceDB, PGVector, Pinecone, etc.).
    Backend dividido em dois serviços NodeJS/Express:
      - Server: gerencia interações com DB.
      - Collector: coleta e processa documentos enviados.
    """

    result = compute_semantic_similarity(description)
    pretty_print(result, top_k=10)
