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

def menu():
    print("\n--- 📥 CENTRAL DE MÍDIA ---")
    print("1. 📚 Livro")
    print("2. 🎬 Filme")
    print("3. 📺 Série")
    
    escolha = input(">> Opção: ").strip()
    
    if escolha not in DBS:
        print("Opção inválida.")
        return

    config = DBS[escolha]
    
    print(f"\nAdicionando em {config['tipo']}...")
    titulo = input("Título: ")
    
    nome_criador = input("Autor/Diretor: ") 
    tags = input("Tags: ")
    review = input("Review: ")

    enviar_notion(config, titulo, nome_criador, tags, review)

if __name__ == "__main__":
    menu()