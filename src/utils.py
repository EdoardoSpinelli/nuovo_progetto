import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.csv')


def read_products():
    """Legge il file CSV e restituisce una lista di dizionari."""
    products = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convertiamo id e quantity in interi
            row['id'] = int(row['id'])
            row['quantity'] = int(row['quantity'])
            products.append(row)
    return products


def write_products(products):
    """Scrive la lista di dizionari nel file CSV."""
    fieldnames = ['id', 'name', 'quantity']
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def get_next_id(products):
    """Genera il prossimo id incrementale."""
    if not products:
        return 1
    return max(p['id'] for p in products) + 1
