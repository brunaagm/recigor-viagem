from controller import db  # Importa a instância do banco de dados

class Viagem(db.Model):
    __tablename__ = 'Viagem'
    id = db.Column(db.Integer, primary_key=True)
    Destino = db.Column(db.String(255), nullable=False)  # Nome do destino
    Data = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    nota = db.Column(db.String(255), nullable=False) 
    def __repr__(self):
        return f'<Viagem {self.Destino} - {self.Data} - {self.descricao} - {self.nota}>'
