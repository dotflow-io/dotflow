# Conceito de Contexto

Quando é referido sobre **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** dentro da biblioteca Dotflow estamos falando de como os dados sao trafegados dentro das tarefas. O **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** é basicamente uma classe embutida em todo retorna de uma tarefa, essa classe é padronizada e voce pode acessar o valor dela com o objeto `storage`.

/// note

O padrao da classe **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** é atribuido ao **Contexto Incial** e **Contexto Anterior** de uma tarefa. 

///

## Acesssando os dados do Contexto

{* ./docs_src/context/context.py hl[10] *}

Para detalhes sobre a implementação da classe, você pode acessar [aqui](https://dotflow-io.github.io/dotflow/nav/reference/context/ "Classe Contexto").