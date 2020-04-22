from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/filmes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)
    autor = db.Column(db.String(30), nullable=False)
    

    def to_json(self):
        json_filmes = {
            'id': self.id,
            'titulo': self.titulo,
            'categoria': self.categoria,
            'autor': self.autor
            
        }
        return json_filmes

    @staticmethod
    def from_json(json_filmes):
        titulo = json_filmes.get('titulo')
        categoria = json_filmes.get('categoria')
        autor = json_filmes.get('autor')
        return Filme(titulo=titulo, categoria=categoria, autor=autor)


@app.route('/filmes')
@cross_origin()
def cadastro():
    # obtém todos os registros da tabela filmes em ordem de titulo
    filmes = Filme.query.order_by(Filme.titulo).all()
    # converte a lista de filmes para o formato JSON
    # list comprehensions
    return jsonify([filme.to_json() for filme in filmes])


@app.route('/filmes', methods=['POST'])
@cross_origin()
def inclusao():
    filme = Filme.from_json(request.json)

    # se campo tiver algum conteúdo
    # if !filme.titulo or !filme.genero or !filme.duracao or !filme.nota

    # if '' or 0 in filme.to_json().values()

    # list comprehensions
    erros = [campo for campo, valor in filme.to_json().items()
             if valor == '' or valor == 0]

    # em Python, JS... 0 => False; qualquer valor (exceto 0) => True
    if len(erros):
        return jsonify({'id': 0, 'message': ','.join(erros) + ' deve(m) ser preenchido(s)'}), 400

    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.to_json()), 201


@app.route('/filmes/<int:id>')
@cross_origin()
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    filme = Filme.query.get_or_404(id)
    return jsonify(filme.to_json()), 200


@app.errorhandler(404)
@cross_origin()
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@app.route('/filmes/<int:id>', methods=['PUT'])
@cross_origin()
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    filme = Filme.query.get_or_404(id)

    # recupera os dados enviados na requisição
    filme.titulo = request.json['titulo']
    filme.genero = request.json['categoria']
    filme.autor = request.json['autor']

    # altera (pois o id já existe)
    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.to_json()), 204


@app.route('/filmes/<int:id>', methods=['DELETE'])
@cross_origin()
def exclui(id):
    Filme.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Livro excluído com sucesso'}), 200


@app.route('/filmes/pesq/<palavra>')
@cross_origin()
def pesquisa(palavra):
    # obtém todos os registros da tabela filmes em ordem de titulo
    filmes = Filme.query.order_by(Filme.titulo).filter(
        Filme.titulo.like(f'%{palavra}%')).all()
    # converte a lista de filmes para o formato JSON (list comprehensions)
    return jsonify([filme.to_json() for filme in filmes])


@app.route('/')
def teste():
    return '<h1>Cadastro de Livros</h1>'


if __name__ == '__main__':
    app.run(debug=True)
