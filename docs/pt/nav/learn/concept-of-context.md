# Conceito de Contexto

Quando é falado sobre **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** dentro da biblioteca Dotflow estamos falando de como os dados são trafegados dentro das tarefas. O **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** é basicamente uma classe embutida em todo retorna de uma tarefa, essa classe é padronizada e você pode acessar o valor dela com o objeto `storage`.

/// note

O padrão da classe **[Contexto](https://dotflow-io.github.io/dotflow/nav/reference/context/)** é atribuido ao **Contexto Incial** e **Contexto Anterior** de uma tarefa. 

///

## Acessando os dados do Contexto

{* ./docs_src/context/context.py hl[10] *}

Para detalhes sobre a implementação da classe, você pode acessar [aqui](https://dotflow-io.github.io/dotflow/nav/reference/context/ "Classe Contexto").
