# IASD2
Museum fire Detection

**Explain how the problem was modelled with a Bayesian network.**

A rede bayesiana é construida em "camadas" em que na mesma camada estão as variáveis referentes ao mesmo instante de tempo e o número de camadas é igual ao número de instantes de tempo diferentes do problema. Em cada camada da rede podem existir dois tipos de variáveis: tipo 1 - representa o estado de incêndio numa sala; tipo 2 - representa o estado de um sensor ativo. Nas variáveis do tipo 1, no instante inicial o estado de incêndio de cada sala (prior nodes) tem probabilidade = 0.5 (conhecimento nulo). 

As variáveis de tipo 1 dos instantes seguintes têm como "parents" as variáveis de tipo 1 correspondentes à própria sala e às salas adjacentes no instante anterior. As variáveis de tipo 2 têm como "parent" a variável de tipo 1 correspondente à sala medida pelo sensor, do mesmo instante de tempo e só aparecem nos instantes de tempo em que produziram medições. 

Para construir a tabela de probabilidades condicionais, nos casos em que a própria sala está com incêndio no instante anterior a probabilidade de estar no instante atual é igual a 1. Nos casos que não está, é igual a P caso pelo menos uma das adjacentes esteja ativa e 0 caso contrário.

No final, para calcular a sala que tem probabilidade máxima de ocorrência de incêndio no instante T, calcula-se a probabilidade para todas as salas e elege-se a que tem maior probabilidade. Para calcular a probabilidade de cada sala estar com incêndio no instante T, usa-se o algoritmo de eliminação de variável em que a variável que se pretende descobrir é a variável de tipo 1 no instante T e a evidência são todas as medições efetuadas pelos sensores.  
