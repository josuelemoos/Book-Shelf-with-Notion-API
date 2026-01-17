import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()


DBS = {
    "1": { "tipo": "Livro", "id": os.getenv("DB_LIVROS_ID"), "icon": "📚" },
    "2": { "tipo": "Filme", "id": os.getenv("DB_FILMES_ID"), "icon": "🎬" },
    "3": { "tipo": "Série", "id": os.getenv("DB_SERIES_ID"), "icon": "📺" }
}


COLUNA_AUTOR_PADRAO = "Autor" 

TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def enviar_notion(db_config, titulo, criador, tags, review):
    url = "https://api.notion.com/v1/pages"
    
    tags_list = [{"name": tag.strip()} for tag in tags.split(",")] if tags else []

    data = {
        "parent": {"database_id": db_config["id"]},
        "properties": {
            "Name": { "title": [{"text": {"content": titulo}}] },
            
            
            COLUNA_AUTOR_PADRAO: { 
                "rich_text": [{"text": {"content": criador}}] 
            },
            
            "Tags": { "multi_select": tags_list }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": { "rich_text": [{"text": {"content": "Review"}}] }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": { "rich_text": [{"text": {"content": review}}] }
            }
        ]
    }

    res = requests.post(url, headers=HEADERS, json=data)
    
    if res.status_code == 200:
        print(f"\n✅ Sucesso! {db_config['icon']} '{titulo}' salvo em {db_config['tipo']}.")
    else:
        print(f"\n❌ Erro {res.status_code}:")
        
        print(res.json().get('message', res.text))

def consultar_notion(db_config, filtro=None, limit=10):
    url = f"https://api.notion.com/v1/databases/{db_config['id']}/query"
    
    
    payload = {
        "page_size": limit,
        
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }

    
    if filtro:
        payload["filter"] = filtro

    res = requests.post(url, headers=HEADERS, json=payload)
    
    if res.status_code == 200:
        dados = res.json()
        itens = dados.get("results", [])
        
        print(f"\n--- 🔍 Resultados em {db_config['tipo']} ---")
        for item in itens:
            
            
            try:
                nome = item["properties"]["Name"]["title"][0]["plain_text"]
            except IndexError:
                nome = "Sem Título"
            
           
            nota_texto = ""
            if "Tags" in item["properties"]:

                lista_tags = item["properties"]["Tags"]["multi_select"]
                

                nomes_das_tags = [tag["name"] for tag in lista_tags]
                
                if nomes_das_tags:
                    nota_texto = f" | Tags/Nota: {', '.join(nomes_das_tags)}"
            
            print(f"- {nome}{nota_texto}")

def menu():
    print("\n--- 📥 CENTRAL DE MÍDIA ---")
    print("1. 📚 Adicionar Livro")
    print("2. 🎬 Adicionar Filme")
    print("3. 📺 Adicionar Série")
    print("4. 📋 Ver últimos itens salvos")
    print("5. 🌟 Buscar por Nota ou Tags")
    
    escolha = input(">> Opção: ").strip()
    
    if escolha in ["1", "2", "3"]:
        config = DBS[escolha]
        
        
    elif escolha == "4":
        tipo = input("De qual DB (1-Livro, 2-Filme, 3-Série)? ")
        if tipo in DBS:
            consultar_notion(DBS[tipo])
            
    elif escolha == "5":
        tipo = input("Buscar em qual DB (1-Livro, 2-Filme, 3-Série)? ")
        
        if tipo in DBS:
            
            valor_busca = input("Qual tag ou nota você procura? ")

            
            filtro_tags = {
                "property": "Tags",
                "multi_select": {
                    "contains": valor_busca 
                }
            }
            
            consultar_notion(DBS[tipo], filtro=filtro_tags)

if __name__ == "__main__":
    menu()