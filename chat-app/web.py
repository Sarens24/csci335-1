from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:password@127.0.0.1:3306/chat_app"
db = SQLAlchemy(app)

class UserRecord(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)


@app.route("/users", methods=["POST"])
def create_user():
  username = request.json.get("username")
  if username:
    count = UserRecord.query.filter(UserRecord.name == username).count()
    if count > 0:
      return jsonify({ "error": "User already exists" })
    user = UserRecord(name=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({})
  else:
    return jsonify({ "error": "Username field is missing" })

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
