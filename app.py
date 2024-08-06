from flask import request, jsonify
from datetime import datetime
from database import app, db
from models import Invoice, Item, InvoiceSchema, ItemSchema

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@app.route('/invoices', methods=['POST'])
def add_invoice():
    date_str = request.json['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    items = request.json['items']
    new_invoice = Invoice(date=date)
    db.session.add(new_invoice)
    db.session.commit()

    for item in items:
        new_item = Item(
            name=item['name'],
            amount=item['amount'],
            cost=item['cost'],
            invoice_id=new_invoice.id
        )
        db.session.add(new_item)
        db.session.commit()

    return invoice_schema.jsonify(new_invoice)

@app.route('/invoices', methods=['GET'])
def get_invoices():
    all_invoices = Invoice.query.all()
    result = invoices_schema.dump(all_invoices)
    return jsonify(result)

@app.route('/invoices/<id>', methods=['GET'])
def get_invoice(id):
    invoice = Invoice.query.get(id)
    return invoice_schema.jsonify(invoice)

@app.route('/invoices/<id>', methods=['PUT'])
def update_invoice(id):
    invoice = Invoice.query.get(id)
    date_str = request.json['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    items = request.json['items']

    invoice.date = date

    for item in invoice.items:
        db.session.delete(item)

    db.session.commit()

    for item in items:
        new_item = Item(
            name=item['name'],
            amount=item['amount'],
            cost=item['cost'],
            invoice_id=invoice.id
        )
        db.session.add(new_item)

    db.session.commit()

    return invoice_schema.jsonify(invoice)

@app.route('/invoices/<id>', methods=['DELETE'])
def delete_invoice(id):
    invoice = Invoice.query.get(id)
    for item in invoice.items:
        db.session.delete(item)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice deleted'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')