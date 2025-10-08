import QueryData
import requests
import json
from bs4 import BeautifulSoup

def retrieve_parties(names):
    
    search_results = []

    for i, name in enumerate(names):
        print(f"\n[+] Searching for: {name} ({i+1}/{len(names)})", end="", flush=True)
        
        form_data = {
            "txtStrParte": name,
            "sbmNovo": "Consultar"
        }
        
        response = requests.post("https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica", data=form_data)
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup.prettify())
            
            #div = soup.find("div", class_="infraAreaTabela")
            #if div:
            #    print(div.get_text())

            table = soup.find("table", class_="infraTable")
            if table:
                
                search = QueryData.Search(name)
                
                for row in table.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) == 0:
                        continue
                
                    party = cols[0].get_text(strip=True) if len(cols) > 0 else ''
                    doc = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                    params = cols[0].find('a')['href'] if len(cols) > 0 else ''
                    
                    data = QueryData.Party(party, doc, params)
                    #print(data)
                    search.add_party(data)
                    print(".", end="", flush=True)
                    #print(search)
                    
                search_results.append(search)
                #print(search)
        #break
                
    return search_results
                
                
def retrieve_party_processes(search_results):
    print("\n[+] Retrieving processes", end="", flush=True)        
    if search_results:
        for search in search_results:
            for party in search.parties:
                if len(party.params) > 0:
                    #print(data)
                    get_url = f"https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/{party.params}"
                    #print(get_url)
                    response = requests.get(get_url)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        #print(soup.prettify())
                        table = soup.find("table", class_="infraTable")
                        if table:
                            for row in table.find_all("tr"):
                                cols = row.find_all("td")
                                if len(cols) == 0:
                                    continue
                                number = cols[0].get_text(strip=True) if len(cols) > 0 else ''
                                params = cols[0].find('a')['href'] if len(cols) > 0 else ''
                                author = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                                defendant = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                                subject = cols[3].get_text(strip=True) if len(cols) > 3 else ''
                                last_event = cols[4].get_text(strip=True) if len(cols) > 4 else ''
                                
                                process = QueryData.Process(number, author, defendant, subject, last_event, params)
                                party.add_process(process)
                                print(".", end="", flush=True)
                                #print(process)                    
                    #break
        
def enrich_processes_with_details(search_results):        
    print("\n[+] Enriching processes with details", end="", flush=True)    
    if search_results:
        for search in search_results:
            for party in search.parties:
                for process in party.processes:
                    if len(process.params) > 0:
                        #print(process)
                        get_url = f"https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/{process.params}"
                        #print(get_url)
                        response = requests.get(get_url)
                        
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            print(soup.prettify())
                            
                            #Assuntos
                            fieldsets = soup.find_all("fieldset", class_="infraFieldset", id="fldAssuntos")
                            #print(fieldsets)
                            for fieldset in fieldsets:
                                #print(fieldset)
                                table = fieldset.find("table", class_="infraTable")
                                if table:
                                    for row in table.find_all("tr"):
                                        cols = row.find_all("td")
                                        if len(cols) == 0:
                                            continue
                                        code = cols[0].get_text(strip=True) if len(cols) > 0 else ''
                                        description = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                                        principal = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                                        
                                        subject = QueryData.Subject(code, description, principal)
                                        process.add_subject(subject)
                                        print(".", end="", flush=True)
                                        #print(subject)
                                        
                                    #break
                                    
                            #Partes e Representantes
                            fieldset = soup.find("fieldset", class_="infraFieldset", id="fldPartes")
                            #print(fieldset)
                            table = fieldset.find("table", class_="infraTable")
                            if table:
                                #print(table)
                                for row in table.find_all("tr"):
                                    cols = row.find_all("td")
                                    if len(cols) == 0:
                                        continue
                                    
                                    author = cols[0].get_text(strip=True) if len(cols) > 0 else ''
                                    defendant = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                                    
                                    process.add_authors_and_defendants(author, defendant)
                                    print(".", end="", flush=True)


                            #Informações Adicionais
                            fieldset = soup.find("fieldset", class_="infraFieldset", id="fldInformacoesAdicionais")
                            #print(fieldset)
                            table = fieldset.find("table")
                            if table:
                                #print(table)
                                key = ""
                                value = ""
                                for i, label in enumerate(table.find_all("label")):
                                    #print(label)
                                    if i % 2 == 0:
                                        key = label.get_text(strip=True)
                                    else:
                                        value = label.get_text(strip=True)
                                        
                                    if key and value:
                                        process.add_additional_info(key, value)
                                        print(".", end="", flush=True)
                                        #print(f"{key}: {value}")
                                        key = ""
                                        value = ""
                                    
                            #Eventos
                            tables = soup.find_all("table", class_="infraTable")
                            for table in tables:
                                if table and "Evento" in table.get_text():
                                    for row in table.find_all("tr"):
                                        cols = row.find_all("td")
                                        if len(cols) == 0:
                                            continue
                                        number = cols[0].get_text(strip=True) if len(cols) > 0 else ''
                                        date = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                                        description = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                                        user = cols[3].get_text(strip=True) if len(cols) > 3 else ''
                                        documents = cols[4].get_text(strip=True) if len(cols) > 4 else ''
                                        
                                        event = QueryData.Event(number, date, description, user, documents)
                                        process.add_event(event)
                                        print(".", end="", flush=True)
                                        #print(event)
                            
                        #break

def export_json(query_results):
    print("\n[+] Exporting JSON file")
    if query_results:
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump([data for data in query_results], f, ensure_ascii=False, indent=4, default=QueryData.serialize_to_dict)


def main():
    
    print("\n[+] Initiating...", end="", flush=True)
    
    #search_results = retrieve_parties(["ADILSON DA SILVA", "JOÂO DA SILVA MORAES","RICARDO DE JESUS","SERGIO FIRMINO DA SILVA","HELENA FARIAS DE LIMA","PAULO SALIM MALUF","PEDRO DE SÁ"])
    search_results = retrieve_parties(["RICARDO DE JESUS"])

    retrieve_party_processes(search_results)

    enrich_processes_with_details(search_results)

    export_json(search_results)


if __name__ == "__main__":
    main()
