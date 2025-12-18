# gplaces-requester

Este projeto é um script em Python que executa chamadas reais às APIs da Google Maps Platform com o objetivo de:

- Verificar se uma API Key está ativa
- Identificar quais APIs estão acessíveis sem restrições
- Contabilizar requisições aceitas
- Calcular impacto financeiro com base nos preços oficiais

O script **não é um simulador**. Ele realiza requisições reais.

---

## Funcionamento Geral

O script recebe uma API Key como parâmetro e executa requisições HTTP em múltiplos endpoints da Google Maps Platform.

Para cada endpoint:

1. É feita uma chamada inicial para verificar se a API responde com HTTP 200
2. Endpoints ativos são considerados exploráveis
3. O script executa chamadas adicionais conforme o modo de execução
4. As respostas HTTP 200 são contabilizadas
5. O custo é calculado com base no preço por 1.000 requisições

A API Key nunca é exibida em texto claro no output.

---

## APIs Testadas

O script testa os seguintes serviços:

- Geocoding API
- Find Place From Text
- Place Autocomplete
- Elevation API
- Timezone API
- Place Details (Basic)
- Nearby Search
- Text Search

---

## Precificação Utilizada

O cálculo de custo utiliza os valores públicos da Google Maps Platform (USD por 1.000 requisições):

| API | USD |
|-----|-----|
| Geocode | 5.00 |
| Autocomplete | 2.83 |
| Find Place From Text | 17.00 |
| Place Details (Basic) | 17.00 |
| Elevation | 5.00 |
| Timezone | 5.00 |
| Nearby Search | 32.00 |
| Text Search | 32.00 |

---

## Modos de Execução

O comportamento do script muda conforme os parâmetros utilizados.

### Modo PoC

Ativado com `--poc`.

- Executa exatamente 1 requisição por API ativa
- Serve apenas para comprovar que a API está acessível
- Impacto financeiro mínimo

Exemplo:
```bash
python3 google-requests.py --api-key SUA_CHAVE --poc
