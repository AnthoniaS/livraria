from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    autor = db.Column(db.String(30), nullable=False)
    edicao = db.Column(db.String(30), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    paginas = db.Column(db.Integer, nullable=False)
    

    def to_json(self):
        json_livros = {
            'id': self.id,
            'nome': self.nome,
            'autor': self.autor,
            'edicao': self.edicao,
            'ano': self.ano,
            'paginas': self.paginas
            
        }
        return json_livros

    @staticmethod
    def from_json(json_livros):
        nome = json_livros.get('nome')
        autor = json_livros.get('autor')
        edicao = json_livros.get('edicao')
        ano = json_livros.get('ano')
        paginas = json_livros.get('paginas')
        return Livro(nome=nome, autor=autor, edicao=edicao, ano=ano, paginas=paginas)


@app.route('/livros')
@cross_origin()
def cadastro():
    # obtém todos os registros da tabela livros em ordem de titulo
    livros = Livro.query.order_by(Livro.nome).all()
    # converte a lista de livros para o formato JSON
    # list comprehensions
    return jsonify([livro.to_json() for livro in livros])


@app.route('/livros', methods=['POST'])
@cross_origin()
def inclusao():
    livro = Livro.from_json(request.json)

    # se campo tiver algum conteúdo
    # if !livro.titulo or !livro.genero or !livro.duracao or !livro.nota

    # if '' or 0 in livro.to_json().values()

    # list comprehensions
    erros = [campo for campo, valor in livro.to_json().items()
             if valor == '' or valor == 0]

    # em Python, JS... 0 => False; qualquer valor (exceto 0) => True
    if len(erros):
        return jsonify({'id': 0, 'message': ','.join(erros) + ' deve(m) ser preenchido(s)'}), 400

    db.session.add(livro)
    db.session.commit()
    return jsonify(livro.to_json()), 201


@app.route('/livros/<int:id>')
@cross_origin()
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.to_json()), 200


@app.errorhandler(404)
@cross_origin()
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@app.route('/livros/<int:id>', methods=['PUT'])
@cross_origin()
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    livro = Livro.query.get_or_404(id)

    # recupera os dados enviados na requisição
    livro.nome = request.json['nome']
    livro.autor = request.json['autor']
    livro.edicao = request.json['edicao']
    livro.ano = request.json['ano']
    livro.paginas = request.json['paginas']

    # altera (pois o id já existe)
    db.session.add(livro)
    db.session.commit()
    return jsonify(livro.to_json()), 204


@app.route('/livros/<int:id>', methods=['DELETE'])
@cross_origin()
def exclui(id):
    Livro.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Livro excluído com sucesso'}), 200


@app.route('/livros/pesq/<palavra>')
@cross_origin()
def pesquisa(palavra):
    # obtém todos os registros da tabela livros em ordem de nome
    livros = Livro.query.order_by(Livro.nome).filter(
        Livro.nome.like(f'%{palavra}%')).all()
    # converte a lista de livros para o formato JSON (list comprehensions)
    return jsonify([livro.to_json() for livro in livros])


@app.route('/')
def teste():
    return '<h1>Cadastro de Livros</h1>'


if __name__ == '__main__':
    app.run(debug=True)
