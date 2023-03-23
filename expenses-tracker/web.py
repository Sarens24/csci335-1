from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:password@127.0.0.1:3306/shared_expenses"
db = SQLAlchemy(app)

class GroupRecord(db.Model):
  __tablename__ = "groups"

  id = db.Column(db.Integer, primary_key=True)
  person1 = db.Column(db.String(255), nullable=False)
  person2 = db.Column(db.String(255), nullable=False)
  person3 = db.Column(db.String(255), nullable=False)
  
class ExpenseRecord(db.Model):
  __tablename__ = "expenses"

  id = db.Column(db.Integer, primary_key=True)
  person = db.Column(db.String(255), nullable=False)
  amount = db.Column(db.Integer, nullable=False)


@app.route("/groups", methods=["POST"])
def create_group():
  person1 = request.json.get("person1")
  person2 = request.json.get("person2")
  person3 = request.json.get("person3")
  if (person1 and person2 and person3):
    group = GroupRecord(person1=person1, person2=person2, person3=person3)
    db.session.add(group)
    db.session.commit()
    return jsonify({ "group_id": group.id })
  return jsonify({ "error": "A field is missing" })

@app.route("/groups/<group_id>/expenses", methods=["POST"])
def create_expense(group_id):
  person = request.json.get("person")
  amount = request.json.get("amount")
  group = GroupRecord.query.filter(GroupRecord.id == group_id).first()
  if (not person):
    return jsonify({ "error": "Person is missing or blank" })
  if (not amount or amount < 0):
    return jsonify({ "error": "Amount is missing or <= 0" })
  if (not group):
    return jsonify({ "error": "Group ID does not exist" })
  if (group.person1 != person and group.person2 != person and group.person3 != person):
    return jsonify({ "error": "Person is not part of the group" })
  expense = ExpenseRecord(person=person, amount=amount)
  db.session.add(expense)
  db.session.commit()
  return jsonify({})

@app.route("/groups/<group_id>/settle_up", methods=["POST"])
def settle_up(group_id):
  group = GroupRecord.query.filter(GroupRecord.id == group_id).first()
  if (not group):
    return jsonify({ "error": "Group ID does not exist" })
  expense1 = ExpenseRecord.query.filter(ExpenseRecord.person == group.person1).first()
  expense2 = ExpenseRecord.query.filter(ExpenseRecord.person == group.person2).first()
  expense3 = ExpenseRecord.query.filter(ExpenseRecord.person == group.person3).first()
  if (not expense1 and not expense2 and not expense3):
    return jsonify({ "error": "No expenses have been tracked yet" })

  expenses = [expense1, expense2, expense3]
  new_list = sorted(expenses, key=lambda x: x.amount)
  shared = (expense1.amount + expense2.amount + expense3.amount) / 3

  # if two people overpaid
  if new_list[1].amount > shared:
    return jsonify({ "shared_amount": shared, "transactions": [
      {
        "from": new_list[0].person,
        "to": new_list[2].person,
        "amount": new_list[2].amount - shared
      },
      {
        "from": new_list[0].person,
        "to": new_list[1].person,
        "amount": new_list[1].amount - shared
      }
    ] })
  # if two people underpaid
  elif new_list[1].amount < shared:
    return jsonify({ "shared_amount": shared, "transactions": [
      {
        "from": new_list[0].person,
        "to": new_list[2].person,
        "amount": shared - new_list[0].amount
      },
      {
        "from": new_list[1].person,
        "to": new_list[2].person,
        "amount": shared - new_list[1].amount
      }
    ] })
  # if someone paid the same as shared amount
  else:
    return jsonify({ "shared_amount": shared, "transactions": [
      {
        "from": new_list[0].person,
        "to": new_list[2].person,
        "amount": shared - new_list[0].amount
      }
    ] })

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
