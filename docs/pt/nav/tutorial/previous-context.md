# Contexto Anterior

## Enviando Contexto:

Para enviar um contexto, basta retornar alguma informação na implementação da sua tarefa. Você pode retornar qualquer objeto, e ele fará parte do contexto.

{* ./docs_src/previous_context/previous_context.py hl[15,23] *}


## Recebendo Contexto

Neste exemplo, um valor de contexto anterior é recebido a partir do atributo `previous_contexto` definido na função.

{* ./docs_src/previous_context/previous_context.py hl[11,19] *}