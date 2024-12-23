import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller import app,db  # Importa a instância do Flask e o banco de dados
from flask import render_template, request, redirect, url_for, flash, session
from controller.models import Viagem  # Importa o modelo Viagem


# Página de registro de viagens
@app.route('/cadastrar', methods=['GET', 'POST'], endpoint='registro')
def registro():
    if request.method == 'POST':
        destino_name = request.form.get('destino_name')
        data = request.form.get('date')
        descricao = request.form.get('descricao')
        nota = request.form.get('descricao')
        # Verifica se todos os campos foram preenchidos
        if destino_name and data and descricao:
            new_viagem = Viagem(Destino=destino_name, Data=data, descricao=descricao, nota=nota)
            db.session.add(new_viagem)
            db.session.commit()
            flash('Viagem registrada com sucesso!', 'success')
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    viagens = Viagem.query.all()  # Exibe todas as viagens registradas
    return render_template('cadastrarViagem.html', viagens=viagens)

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
    return redirect(url_for('registro'))



if __name__ == '__main__':
    app.run(debug=True)
