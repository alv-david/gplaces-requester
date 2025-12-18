import requests
import argparse
import math
import csv
import re
import time
import sys
import os
from datetime import datetime

# ===================== LIMPAR TERMINAL =====================
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# ===================== CORES =====================
AZUL_CLARO = "\033[1;94m"
VERMELHO = "\033[1;31m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ===================== URLS =====================
urls_vulneraveis = [
    "https://maps.googleapis.com/maps/api/geocode/json?latlng=40,30&key=CHAVE",
    "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=CHAVE",
    "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Bingh&types=%28cities%29&key=CHAVE",
    "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=CHAVE",
    "https://maps.googleapis.com/maps/api/timezone/json?location=39.6034810,-119.6822510&timestamp=1331161200&key=CHAVE",
    "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key=CHAVE",
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=100&types=food&name=harbour&key=CHAVE",
    "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Sydney&key=CHAVE"
]

# ===================== PREÇOS =====================
precos_api = {
    "geocode": 5.00,
    "findplacefromtext": 17.00,
    "autocomplete": 2.83,
    "elevation": 5.00,
    "timezone": 5.00,
    "placedetails_basic": 17.00,
    "nearbysearch": 32.00,
    "textsearch": 32.00
}

# ===================== FUNÇÕES =====================
def identificar_api(url):
    if "geocode" in url: return "geocode"
    if "findplacefromtext" in url: return "findplacefromtext"
    if "autocomplete" in url: return "autocomplete"
    if "elevation" in url: return "elevation"
    if "timezone" in url: return "timezone"
    if "details" in url: return "placedetails_basic"
    if "nearbysearch" in url: return "nearbysearch"
    if "textsearch" in url: return "textsearch"
    return "desconhecida"

def sanitize_url(url):
    return re.sub(r'key=[^&]+', 'key=[REDACTED]', url)

def log_message(log_file, message):
    if log_file:
        with open(log_file, 'a', encoding='utf-8') as lf:
            lf.write(f"{datetime.now().isoformat()} - {message}\n")

def filtrar_apis_validas(urls, delay, log_file):
    urls_validas = []
    status_map = {}
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                urls_validas.append(url)
                status_map[identificar_api(url)] = "Ativa"
            else:
                status_map[identificar_api(url)] = "Não vulnerável"
            log_message(log_file, f"Testada {url} - Status {r.status_code}")
        except Exception as e:
            status_map[identificar_api(url)] = "Não vulnerável"
            log_message(log_file, f"Erro ao testar {url}: {e}")
        if delay:
            time.sleep(delay)
    return urls_validas, status_map

def testar_urls(urls, status_map, requests_por_url, delay, log_file):
    resultados = {}
    vulneraveis_resumo = []

    print(f"{BOLD}Iniciando testes...{RESET}\n")
    for url in urls:
        api_name = identificar_api(url)
        clean_url = sanitize_url(url)
        print(f"{AZUL_CLARO}{BOLD}[INFO]{RESET} Testando {api_name}: {clean_url}")
        log_message(log_file, f"Iniciando teste para {api_name} - {clean_url}")

        chamadas = 0
        status_200 = 0
        for _ in range(requests_por_url):
            chamadas += 1
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    status_200 += 1
            except Exception as e:
                log_message(log_file, f"Erro request {chamadas} {api_name}: {e}")
            if delay:
                time.sleep(delay)

        if status_200 > 0:
            vulneraveis_resumo.append(api_name)
            status_map[api_name] = "Ativa"
        else:
            status_map[api_name] = "Não vulnerável"

        resultados[api_name] = {
            "chamadas": chamadas,
            "status_200": status_200
        }

    if vulneraveis_resumo:
        print("\nResumo das APIs vulneráveis:")
        print("---------------------------------------")
        for api in vulneraveis_resumo:
            print(f"{VERMELHO}[ALERT]{RESET} {api} está vulnerável!")
        print("---------------------------------------")

    return resultados

def relatorio_final(resultados, status_map, csv_filename, log_file):
    print("\n=== RELATÓRIO FINAL ===")
    total_custo = 0.0
    rows = []

    for api, stats in resultados.items():
        preco = precos_api.get(api, 0)
        custo = round((stats['chamadas'] / 1000) * preco, 4)
        total_custo += custo

        print(f"[{api}]")
        print(f"  Total chamadas: {stats['chamadas']}")
        print(f"  Sucesso (200): {stats['status_200']}")
        print(f"  Preço unitário: US$ {preco:.2f} / 1.000 requests")
        print(f"  Custo estimado: US$ {custo:.4f}")
        print("------------------------------------------------------------")

        rows.append([
            api,
            status_map.get(api, ''),
            stats['chamadas'],
            stats['status_200'],
            preco,
            custo
        ])

        log_message(log_file, f"{api} | Chamadas: {stats['chamadas']} | Sucesso: {stats['status_200']} | Custo: {custo}")

    print(f"TOTAL GERAL ESTIMADO: US$ {total_custo:.4f}")

    if csv_filename:
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["API", "Status", "Total Chamadas", "Sucesso (200)", "Preço Unitário USD/1000", "Custo USD"])
            writer.writerows(rows)
            writer.writerow(["TOTAL", "", "", "", "", total_custo])
        print(f"\n[INFO] CSV salvo em: {csv_filename}")
        log_message(log_file, f"CSV salvo em {csv_filename}")

    print("\n* APIs marcadas com [ALERT] podem gerar custo direto se exploradas.")
    print("* Custos baseados na tabela pública do Google Maps Platform.")

# ===================== MAIN =====================
if __name__ == "__main__":
    limpar_terminal()

    if len(sys.argv) == 1:
        print(f"""
{BOLD}Google Places API Requester - Uso:{RESET}

python3 google-requests.py [PARÂMETROS]

--api-key        Chave da API Google
--rpurl          Requests por URL
--target-cost    Custo máximo USD
--poc            1 request por endpoint
--delay          Delay entre requests
--csv            Exportar CSV
--log            Arquivo de log
""")
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Scanner Google APIs com cálculo de custo")
    parser.add_argument("--rpurl", type=int, default=1)
    parser.add_argument("--target-cost", type=float)
    parser.add_argument("--poc", action="store_true")
    parser.add_argument("--delay", type=float, default=0)
    parser.add_argument("--api-key", type=str)
    parser.add_argument("--csv", type=str)
    parser.add_argument("--log", type=str)
    args = parser.parse_args()

    if args.api_key:
        urls_vulneraveis = [url.replace("CHAVE", args.api_key) for url in urls_vulneraveis]

    urls_ativas, status_map = filtrar_apis_validas(urls_vulneraveis, args.delay, args.log)

    reqs = args.rpurl if not args.poc else 1
    resultados = testar_urls(urls_ativas, status_map, reqs, args.delay, args.log)
    relatorio_final(resultados, status_map, args.csv, args.log)
