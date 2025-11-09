from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def get_embedding(text):
    return model.encode(text)

padroes = {
    "monolitico": (
        "A arquitetura monolítica concentra toda a aplicação em um único bloco. "
        "Todos os módulos — interface, lógica de negócio e acesso a dados — estão integrados no mesmo código-base e são implantados juntos. "
        "É simples de desenvolver e testar, mas de difícil escalabilidade e manutenção, pois qualquer mudança exige o redeploy completo do sistema."
    ),

    "camadas": (
        "A arquitetura em camadas (ou em tiers) organiza o sistema em níveis lógicos, geralmente compostos por apresentação, negócio e dados. "
        "Cada camada se comunica apenas com a imediatamente inferior ou superior, promovendo separação de responsabilidades e modularidade. "
        "É comum em aplicações web tradicionais e facilita manutenção e testes, embora possa introduzir acoplamento entre camadas."
    ),

    "microservicos": (
        "A arquitetura de microserviços divide a aplicação em serviços pequenos, independentes e executáveis separadamente. "
        "Cada serviço possui sua própria lógica e banco de dados, comunicando-se via APIs, filas ou mensagens assíncronas. "
        "Essa abordagem aumenta a escalabilidade e a tolerância a falhas, mas adiciona complexidade operacional e necessidade de observabilidade e orquestração."
    ),

    "orientada_a_servicos": ( 
        "A arquitetura orientada a serviços (SOA) é baseada em serviços que expõem funcionalidades por meio de interfaces padronizadas. "
        "Diferente dos microserviços, os serviços SOA tendem a ser maiores e centralizados em um barramento de integração (ESB), "
        "favorecendo reuso, mas com menor independência e maior acoplamento entre módulos."
    ),

    "event_driven": (
        "A arquitetura orientada a eventos é centrada em produtores e consumidores de eventos. "
        "Os componentes reagem a mudanças de estado publicando ou escutando eventos através de um barramento assíncrono. "
        "Esse modelo reduz o acoplamento e melhora a escalabilidade, sendo útil em sistemas distribuídos e aplicações em tempo real."
    ),

    "serverless": (
        "Na arquitetura serverless, o código é executado sob demanda em funções hospedadas por provedores de nuvem, sem gerenciamento de servidores. "
        "Cada função é acionada por eventos específicos, permitindo escalabilidade automática e cobrança por uso. "
        "Ideal para workloads variáveis, mas depende fortemente do provedor e pode introduzir latência no cold start."
    ),

    "microlithico": (
        "A arquitetura microlítica (ou monólito modular) combina características de microserviços e monólitos. "
        "Os módulos são bem definidos e independentes dentro de um mesmo deploy, compartilhando o mesmo ambiente de execução. "
        "Facilita desenvolvimento e manutenção modular sem a complexidade operacional dos microserviços."
    ),

    "hexagonal": (
        "A arquitetura hexagonal (ou ports and adapters) separa a lógica central do sistema das interfaces externas, como banco de dados e APIs. "
        "A aplicação comunica-se com o mundo externo por meio de portas (interfaces) e adaptadores (implementações). "
        "Esse padrão facilita testes, substituição de dependências e manutenção de regras de negócio puras."
    ),

    "limpa": (
        "A arquitetura limpa (Clean Architecture) organiza o código em círculos concêntricos, onde a lógica de negócio é o núcleo e as dependências externas estão nas camadas mais externas. "
        "O fluxo de dependência é sempre de fora para dentro, mantendo o domínio independente de frameworks e infraestrutura."
    ),

    "mvc": (
        "O padrão MVC (Model-View-Controller) separa a aplicação em três componentes: Model (dados e regras), View (interface do usuário) e Controller (controle do fluxo). "
        "Esse padrão é amplamente utilizado em aplicações web e desktop, facilitando organização e reutilização de código."
    ),
    "pipe_and_filter": (
        "A arquitetura Pipe and Filter (tubos e filtros) organiza o processamento de dados como uma sequência de etapas independentes (filtros), "
        "onde cada filtro recebe uma entrada, processa-a e envia a saída para o próximo filtro através de um canal (pipe). "
        "Cada filtro é responsável por uma transformação específica, e os pipes servem apenas para transmitir dados entre eles. "
        "Essa arquitetura é útil em sistemas que realizam processamento de fluxo de dados contínuos, como compiladores, pipelines de dados e sistemas de processamento multimídia. "
        "Ela favorece a reutilização e a composição de componentes, já que filtros podem ser facilmente substituídos ou rearranjados."
    ),
    "plugin_modular": (
        "A arquitetura de plugins e modularidade permite que funcionalidades sejam adicionadas ou removidas dinamicamente através de módulos ou plugins independentes. "
        "O núcleo da aplicação fornece uma infraestrutura básica, enquanto os plugins estendem suas capacidades sem alterar o código principal. "
        "Esse padrão é comum em sistemas extensíveis, como IDEs, CMSs e plataformas de software que suportam customizações pelos usuários."
    ),
}


entrada = """
O projeto utiliza uma arquitetura modular organizada em três subprojetos — frontend, server e collector — configurados como um monorepo. Cada módulo pode ser executado independentemente, mas há integração entre eles, evidenciada pelo uso de scripts centralizados e compartilhamento de build no Docker. O servidor usa Prisma ORM, indicando um banco de dados relacional, e é compatível com MySQL, PostgreSQL e SQL Server. O frontend utiliza Vite e bibliotecas de reconhecimento e síntese de voz, caracterizando uma SPA com processamento local de IA. O collector realiza pré-processamento de dados multimodais (texto, imagem, som e vídeo), convertendo-os para formatos compreensíveis pela IA. A presença de múltiplas integrações com LLMs (OpenAI, Anthropic, Cohere, Ollama, AWS Bedrock, Transformers locais) indica suporte híbrido a modelos locais e em nuvem. O Dockerfile confirma compatibilidade com ARM64 e AMD64, além de unir os módulos frontend e server em uma mesma imagem, reforçando o padrão de monólito modular ou microlítico. A infraestrutura suporta múltiplos provedores de nuvem (AWS e GCP), sugerindo implantação distribuída e escalável. Portanto, a arquitetura geral é microlítica: composta por módulos independentes e bem definidos, mas implantados de forma unificada, com características híbridas entre monólito e microserviços.
"""

print("Gerando embeddings...\n")

emb_entrada = get_embedding(entrada)
emb_padroes = {nome: get_embedding(texto) for nome, texto in padroes.items()}

print("Resultados de similaridade:")
resultados = []
for nome, emb in emb_padroes.items():
    sim = cosine_similarity([emb_entrada], [emb])[0][0]
    resultados.append((nome, sim))

resultados.sort(key=lambda x: x[1], reverse=True)
for nome, score in resultados:
    print(f"{nome:20s} -> Similaridade: {score:.4f}")

print("\nPadrão mais provável:", resultados[0][0])
