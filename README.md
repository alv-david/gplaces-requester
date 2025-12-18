# gplaces-requester

Ferramenta em Python para **auditoria de exposição de API Keys da Google Maps Platform**, com execução de chamadas reais e **mensuração de impacto financeiro** baseada nos preços oficiais do Google.

O objetivo é permitir, a partir de um único script:
- Identificação de **APIs acessíveis sem restrição**
- Validação prática de **API Keys expostas**
- Execução controlada de requisições reais
- **Cálculo de custo financeiro estimado ou efetivo**
- Geração de evidência técnica para relatórios de segurança

---

## Funcionalidades

### 1. Validação de API Key
- Testa automaticamente múltiplos endpoints da Google Maps Platform
- Considera a API **ativa** quando a resposta é `HTTP 200`
- APIs ativas são tratadas como exploráveis
- A API Key nunca é exibida em texto claro (sanitizada no output)

---

### 2. Identificação Automática de APIs
O script identifica o tipo de API com base no endpoint acessado, incluindo:

- Geocoding API
- Find Place From Text
- Place Autocomplete
- Elevation API
- Timezone API
- Place Details (Basic)
- Nearby Search
- Text Search

Essa identificação é usada para:
- Classificação do resultado
- Aplicação do preço correto
- Cálculo do custo financeiro

---

### 3. Execução de Requisições Reais

O script **não simula chamadas**. Todas as requisições são reais.

Existem três modos principais de execução:

#### Modo PoC (`--poc`)
- Executa **1 request por API ativa**
- Serve apenas para comprovação de acesso
- Impacto financeiro mínimo
- Recomendado para validação inicial

#### Modo Normal
- Executa múltiplas requisições por API
- Quantidade definida por `--rpurl`
- **Gera custo real na conta Google**

#### Modo Controle de Custo (`--target-cost`)
- Recebe um valor máximo em USD
- Divide o custo entre as APIs ativas
- Calcula automaticamente quantas requisições executar por API
- **Gera custo real controlado**

---

### 4. Controle de Ritmo (Delay)
- Permite definir intervalo entre requisições
- Reduz risco de rate limit ou alertas automáticos

O delay é definido em segundos (ex.: `0.05` = 50ms).

---

### 5. Cálculo de Impacto Financeiro
- O custo é calculado com base no número de requisições executadas
- Utiliza os preços públicos da Google Maps Platform (USD / 1.000 requests)
- O relatório final apresenta custo por API e custo total

Tabela utilizada:

| API | USD / 1.000 |
|----|-------------|
| Geocode | 5.00 |
| Autocomplete | 2.83 |
| Find Place From Text | 17.00 |
| Place Details (Basic) | 17.00 |
| Elevation | 5.00 |
| Timezone | 5.00 |
| Nearby Search | 32.00 |
| Text Search | 32.00 |

---

### 6. Relatórios e Evidências

#### Output em Terminal
- APIs ativas são listadas
- APIs vulneráveis são marcadas com `[ALERT]`
- Estatísticas de requisições e custo são exibidas ao final

#### Exportação CSV
- Nome da API
- Status
- Total de requisições
- Requisições com HTTP 200
- Preço unitário
- Custo calculado

---

### 7. Logging
- Log opcional em arquivo
- Registra:
  - Data e hora
  - API testada
  - Status HTTP
  - Erros de conexão

---

## Parâmetros Disponíveis

| Parâmetro | Descrição |
|----------|-----------|
| `--api-key` | API Key da Google Maps Platform |
| `--rpurl` | Número de requisições por API |
| `--poc` | Executa 1 request por API |
| `--target-cost` | Define custo máximo em USD |
| `--delay` | Delay entre requisições (segundos) |
| `--csv` | Exporta relatório CSV |
| `--log` | Arquivo de log |

---

## Exemplos de Uso

```bash
python3 google-requests.py --api-key SUA_CHAVE --target-cost=5
