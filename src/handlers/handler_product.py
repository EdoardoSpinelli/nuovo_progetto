import pandas as pd
import os


CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'products.csv')


# ── helpers ──────────────────────────────────────────────────────────────────

def _read_df():
    """Legge il CSV e restituisce un DataFrame pandas."""
    return pd.read_csv(CSV_PATH, dtype={'name': str, 'quantity': int})


def _write_df(df: pd.DataFrame):
    """Sovrascrive il CSV con il DataFrame aggiornato."""
    df.to_csv(CSV_PATH, index=False)


def _get_next_id(df: pd.DataFrame):
    """Calcola il prossimo id incrementale."""
    if df.empty:
        return 1
    return int(df['id'].max()) + 1


# ── handler functions ─────────────────────────────────────────────────────────

def get_all_products():
    """Legge tutti i prodotti dal CSV e li restituisce come lista di dizionari."""
    print(os.getenv("CSV_PATH"))

    df = _read_df()
    print(f"Prodotti trovati: {len(df)}")
    return df.to_dict(orient='records')


def create_product(name: str, quantity: int):
    """Aggiunge un nuovo prodotto al CSV con id incrementale."""
    df = _read_df()

    new_product = {
        'id': _get_next_id(df),
        'name': name,
        'quantity': quantity
    }

    df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
    _write_df(df)

    print(f"Prodotto creato: {new_product}")
    return new_product


def update_product(name: str = None, quantity: int = None):
    """
    Aggiorna nome e/o quantità del prodotto con l'id indicato.
    Restituisce il prodotto aggiornato oppure None se non trovato.
    """
    df = _read_df()
    mask = df['name'] == name

    if not mask.any():
        print(f"Prodotto con nome {name} non trovato.")
        return None

    if name is not None:
        df.loc[mask, 'name'] = name
    if quantity is not None:
        df.loc[mask, 'quantity'] = quantity

    _write_df(df)

    updated = df.loc[mask].iloc[0].to_dict()
    print(f"Prodotto aggiornato: {updated}")
    return updated


def delete_product(name: str):
    """
    Elimina il prodotto con il nome indicato.
    Restituisce True se eliminato, False se non trovato.
    """
    df = _read_df()
    mask = df['name'] == name

    if not mask.any():
        print(f"Prodotto con nome {name} non trovato.")
        return False

    df = df[~mask].reset_index(drop=True)
    _write_df(df)

    print(f"Prodotto con nome {name} eliminato.")
    return True
