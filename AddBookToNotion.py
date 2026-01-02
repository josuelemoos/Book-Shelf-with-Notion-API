
import requests
import sys

# --- CONFIGURAÇÕES / DEFINIÇÕES DO BD E API KEY ---
NOTION_TOKEN = "cole aqui" #API KEY da integration
#acesse https://www.notion.so/profile/integrations , crie uma integration, e pegue sua INTEGRATION SECRET 
DATABASE_ID = "cole aqui" #BD ID
#No link do Notion onde esta a sua tabela de livros, copie o que esta entre www.notion.so/ e ?...

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_page(title, author, tags_string, review_text):
    create_url = "https://api.notion.com/v1/pages"

    # 1. Tratamento das Tags
    tags_list = []
    if tags_string:
        tags_list = [{"name": tag.strip()} for tag in tags_string.split(",")]

    # 2. Montagem do JSON
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": { "title": [{"text": {"content": title}}] },
            "Autor": { "rich_text": [{"text": {"content": author}}] },
            "Tags": { "multi_select": tags_list }
        },
        # 3. AQUI ENTRA O CONTEÚDO DA PÁGINA (A REVIEW)
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Minha Review"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text", 
                            "text": {
                                "content": review_text 
                            }
                        }
                    ]
                }
            }
        ]
    }

    res = requests.post(create_url, headers=headers, json=data)

    if res.status_code == 200:
        print(f"✅ Livro '{title}' e review salvos com sucesso!")
    else:
        print(f"❌ Erro: {res.status_code}")
        print(res.json())

if __name__ == "__main__":
    # Modo interativo (Se rodar sem argumentos)
    if len(sys.argv) < 2:
        print("--- Adicionar Livro + Review ---")
        titulo = input("Nome do Livro: ")
        autor = input("Autor: ")
        tags = input("Tags (separadas por vírgula): ")
        review = input("Escreva sua review: ") 
        
        create_page(titulo, autor, tags, review)
    
    # Modo direto via terminal
    # python AddBookToNotion.py "Titulo" "Autor" "Tag1,Tag2" "Review aqui"
    elif len(sys.argv) == 5:
        create_page(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('Uso: python AddBookToNotion.py "Titulo" "Autor" "Tags" "Review"')