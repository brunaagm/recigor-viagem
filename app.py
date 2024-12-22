from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
os.environ['FLASK_APP'] = 'controller.app'


# Inicializa o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viagens.db'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa a modificação de rastreamento de objetos

# Inicializa o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Viagem
class Viagem(db.Model):
    __tablename__ = 'Viagem'
    id = db.Column(db.Integer, primary_key=True)
    Destino = db.Column(db.String(100), nullable=False)  # Nome do destino
    Data = db.Column(db.String(120), nullable=False)  # Data de viagem

    def __repr__(self):
        return f'<Viagem {self.Destino} - {self.Data}>'

# Modelo de Descricao
class Descricao(db.Model):
    __tablename__ = 'Descricao'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), nullable=False, unique=True)

# Página de registro de viagens
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        destino_name = request.form.get('destino_name')
        data = request.form.get('date')
        descricao = request.form.get('descricao')

        if destino_name and data and descricao:
            new_viagem = Viagem(Destino=destino_name, Data=data)
            db.session.add(new_viagem)
            db.session.commit()
            flash('Viagem registrada com sucesso!', 'success')
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    viagens = Viagem.query.all()
    return render_template('cadastrar_viagem.html', viagens=viagens)

# Rota para excluir uma viagem
@app.route('/excluir/<int:id>')
def excluir_viagem(id):
    viagem_to_delete = Viagem.query.get(id)
    if viagem_to_delete:
        db.session.delete(viagem_to_delete)
        db.session.commit()
        flash('Viagem excluída com sucesso.', 'success')
    else:
        flash('Viagem não encontrada.', 'error')
    return redirect(url_for('registrar'))

# Inicialização do banco de dados
@app.before_request
def before_request():
    with app.app_context():
        db.create_all()  # Garante que as tabelas existem antes da primeira requisição

if __name__ == '__main__':
    app.run(debug=True)
