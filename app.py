from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogadores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * \
    1024 


class Jogador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    gols = db.Column(db.Integer, nullable=False)
    jogos = db.Column(db.Integer, nullable=False)
    temporada = db.Column(db.String(10), nullable=False)
    foto = db.Column(db.String(100), nullable=True)
    altura = db.Column(db.String(10), nullable=True)  
    peso = db.Column(db.Float, nullable=True)          
    nascimento = db.Column(db.String(10), nullable=True) 
    nacionalidade = db.Column(db.String(50), nullable=True)  

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    jogadores = Jogador.query.all()
    print("Jogadores:", jogadores)
    return render_template('index.html', jogadores=jogadores)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        time = request.form['time']
        gols = request.form['gols']
        jogos = request.form['jogos']
        temporada = request.form['temporada']
        altura = request.form['altura']
        peso = request.form['peso']
        nascimento = request.form['nascimento']
        nacionalidade = request.form['nacionalidade']

        foto = request.files['foto']
        if foto and foto.filename != '':
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            caminho_foto = filename
        else:
            caminho_foto = None

        novo_jogador = Jogador(
            nome=nome, time=time, gols=gols, jogos=jogos, temporada=temporada,
            foto=caminho_foto, altura=altura, peso=peso, nascimento=nascimento, nacionalidade=nacionalidade
        )
        db.session.add(novo_jogador)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    jogador = Jogador.query.get_or_404(id)
    if request.method == 'POST':
        jogador.nome = request.form['nome']
        jogador.time = request.form['time']
        jogador.gols = request.form['gols']
        jogador.jogos = request.form['jogos']
        jogador.temporada = request.form['temporada']
        jogador.altura = request.form['altura']
        jogador.peso = request.form['peso']
        jogador.nascimento = request.form['nascimento']
        jogador.nacionalidade = request.form['nacionalidade']
        
        nova_foto = request.files.get('foto')
        if nova_foto:
            filename = secure_filename(nova_foto.filename)
            caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            nova_foto.save(caminho_foto)
            jogador.foto = filename

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', jogador=jogador)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        jogador = Jogador.query.get_or_404(id)
        db.session.delete(jogador)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Erro ao excluir jogador: {e}")
        return "Erro ao excluir jogador."


@app.route('/jogadores')
def lista_jogadores():
    jogadores = Jogador.query.all()
    return render_template('lista_jogadores.html', jogadores=jogadores)


@app.route('/teste')
def teste():
    return "A rota /teste está funcionando!"


if __name__ == '__main__':
    app.run(debug=True, port=4000)
