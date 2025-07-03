# Sistema de Recomendação:
por João Pedro de Castro, Vinícius Tormin, Bruno Moreira, Cleiver Júnior, Samuel Lopes e Igor Aguiar

## Resumo:
Repositório focado no desenvolvimento do trabalho final da matéria "Pensamento Analítico de Dados" (PAD) do Bacharelado em Inteligência Artificial (BIA) da UFG. Iremos desenvolver, com originalidade em relação ao Projeto FMF, indicado pelo Professor Fernando Marques Federson, um sistema de recomendação. O projeto que nos serve de inspiração pode ser encontrado em [Recommendation Systems](https://github.com/PrateekCoder/Recommendation-Systems).

## AGEMC do nosso projeto:

### A (ASK/PERGUNTA):
- Com base no último filme que a pessoa asssitiu e gostou, quais filmes ela gostaria de asssitir também?

### G (OBTER OS DADOS):
- Dados de filmes já lançados ou em produção: [Dataset Movies TMDB](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)

### E (EXPLORAR OS DADOS):
- Análise das distribuição dos dados numéricos do nosso dataset (se a distribuição é normal ou não) e análise de correlação entre as variáveis por meio de testes estatísticos. 

### M (MODELAR OS DADOS):
- Combinação das colunas com as informações que vamos utilizar em uma coluna. Nessa coluna tratamento dos nulos dessa coluna. Após isso, tokenização e vetorização das features. No final, foi feita uma busca por similaridade para descobrir os filmes mais semelhantes à escolha da pessoa.

### C (COMUNICAR OS RESULTADOS):
- Interface interativa, feita em React, com os filmes para que a pessoa possa escolher o filme e veja quais são os filmes semelhantes a esse filme. 

![Imagem exemplo front](imgs\image.png "Imagem que ilustra a tela da interface interativa.")