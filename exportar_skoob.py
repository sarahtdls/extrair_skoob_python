import requests
import csv

USER_ID   = '4312462'
SHELF_ID  = '1'     # <-- ajuste para o shelf_id “já li” (normalmente 1, mas confira na sua conta)
PAGE_SIZE = 1000     # skoob costuma limitar a ~200 por página

def fetch_page(user_id, shelf_id, page, limit):
    url = (
        f'https://www.skoob.com.br/v1/bookcase/books/'
        f'{user_id}/shelf_id:{shelf_id}/page:{page}/limit:{limit}'
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('response', [])

def main():
    all_books = []
    page = 1

    while True:
        books = fetch_page(USER_ID, SHELF_ID, page, PAGE_SIZE)
        if not books:
            break
        all_books.extend(books)
        print(f'Página {page}: {len(books)} livros encontrados')
        page += 1

    # grava CSV
    with open('meus_lidos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['data_leitura','paginas','nota','titulo','ano','autor'])
        for book in all_books:
            ed = book['edicao']
            paginas = book['paginas'] or ed.get('paginas','')
            writer.writerow([
                book.get('dt_leitura',''),
                paginas,
                book.get('ranking',''),
                ed.get('titulo',''),
                ed.get('ano',''),
                ed.get('autor',''),
            ])

    print(f'\nTotal de livros exportados: {len(all_books)}')

if __name__ == '__main__':
    main()
