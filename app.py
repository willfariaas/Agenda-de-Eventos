

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/evento'

db = SQLAlchemy(app)

class Evento(db.Model):

	__tablename__= 'evento'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	titulo = db.Column(db.String)
	descricao = db.Column(db.String)
	local = db.Column(db.String)
	data = db.Column(db.String)

	def __init__(self, titulo, descricao, local, data):
		self.titulo = titulo
		self.descricao = descricao
		self.local = local
		self.data = data

db.create_all()

@app.route("/index", methods=['GET', 'POST'])
def index():
	eventos = Evento.query.all()
	return render_template("index.html",eventos=eventos)

@app.route("/cadastrar")
def cadastrar():
	action = request.args.get("action")
	if action == "edit":
		_id=request.args.get("id")
		eventos = Evento.query.filter_by(_id=_id)
		return render_template("cadastro.html", eventos=eventos, disabled='disabled')
	return render_template("cadastro.html", eventos=[""], disabled="")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		titulo = request.form.get("titulo")
		descricao = request.form.get("descricao")
		local = request.form.get("local")
		data = request.form.get("data")

		if titulo and descricao and local and data:
			p = Evento(titulo, descricao, local, data)
			db.session.add(p)
			db.session.commit()

	return redirect(url_for("index"))

@app.route("/lista")
def lista():
	_id=request.args.get("id")
	eventos = Evento.query.filter_by(_id=_id)
	return render_template("lista.html", eventos=eventos)

if __name__ == '__main__':
	app.run(debug=True)