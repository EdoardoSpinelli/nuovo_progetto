from flask import Blueprint, request, jsonify
from src.handlers.handler_product import (
    get_all_products,
    create_product,
    get_products_count,
    update_product,
    delete_product
)

product_bp = Blueprint('products', __name__, url_prefix='/api/products')



# ── COUNT /api/products/count ───────────────────────────────────────────────────

@product_bp.route('/count', methods=['GET'])
def route_get_products_count():
    try:
        total = get_products_count()
        return jsonify({"total_products": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# ── GET /products ─────────────────────────────────────────────────────────────

@product_bp.route('', methods=['GET'])
def route_get_products():
    try:
        products = get_all_products()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── POST /products ────────────────────────────────────────────────────────────

@product_bp.route('', methods=['POST'])
def route_create_product():
    try:
        data = request.get_json()

        for field in ['name', 'quantity']:
            if field not in data:
                return jsonify({"error": f"Parametro '{field}' mancante."}), 400

        try:
            quantity = int(data['quantity'])
        except ValueError:
            return jsonify({"error": "Il parametro 'quantity' deve essere un intero."}), 400

        new_product = create_product(data['name'], quantity)
        return jsonify(new_product), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── PUT /products/<name> ────────────────────────────────────────────────────────

@product_bp.route('/<string:name>', methods=['PUT'])
def route_update_product(name):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Body JSON mancante."}), 400

        name = data.get('name')
        quantity = data.get('quantity')

        if quantity is not None:
            try:
                quantity = int(quantity)
            except ValueError:
                return jsonify({"error": "Il parametro 'quantity' deve essere un intero."}), 400

        updated = update_product(name, quantity)

        if not updated:
            return jsonify({"error": f"Prodotto con nome {name} non trovato."}), 400

        return jsonify(updated), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── DELETE /products/<name> ─────────────────────────────────────────────────────

@product_bp.route('/<string:name>', methods=['DELETE'])
def route_delete_product(name):
    try:
        deleted = delete_product(name)

        if not deleted:
            return jsonify({"error": f"Prodotto con nome {name} non trovato."}), 400

        return jsonify({"message": "Product deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
