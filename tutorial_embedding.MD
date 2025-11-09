## Tutorial da Análise de Similaridade de Padrões Arquiteturais

Nesta atividade, foi escolhida a abordagem de *feature extraction* para realizar a análise semântica entre diferentes descrições de padrões de arquitetura.  
O modelo utilizado foi o **Qwen/Qwen3-Embedding-0.6B**, disponível no Hugging Face. Esse modelo foi carregado no script Python por meio da biblioteca `sentence-transformers`, que permite gerar *embeddings* — representações vetoriais de textos — para posterior cálculo de similaridade.

A primeira etapa consistiu em obter e resumir a entrada de dependências do projeto **AnythingLLM**.  
Esse resumo serviu como base de comparação, representando o conteúdo a ser analisado.

Em seguida, foram criadas descrições curtas e objetivas de diversos **padrões de arquitetura de software**, como:

- *Camadas*  
- *Monolítico*  
- *Microserviços*  
- *Pipe and Filter*  
- *Service Oriented*  
- *Plugin/Modular*  
- *Hexagonal*  
- *Limpa*  
- *Event-Driven*

Cada descrição foi estruturada em formato JSON para facilitar o processamento automatizado.

Com o modelo carregado e os textos definidos, o script gerou *embeddings* tanto para a descrição das dependências do AnythingLLM quanto para cada padrão arquitetural.  
Depois, foi calculada a similaridade entre esses vetores usando o **cosseno** como métrica.  
O resultado final exibiu, em ordem decrescente, quais padrões de arquitetura apresentavam maior relação semântica com o texto de entrada.

Assim, foi possível identificar, de forma quantitativa, qual padrão arquitetural mais se assemelha à estrutura e funcionamento do AnythingLLM.
