from flask import Flask,url_for,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jcp_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "jcp_helper233445"

db=SQLAlchemy(app)

class Prueba(db.Model):
    __tablename__="Cuestionarios"
    # idPregunta=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    # enunciado=db.Column(db.String(500),nullable=False)
    # autor=db.Column(db.String(200))
    # fecha=db.Column(db.String(20),nullable=False)#2022-06-18
    # tema=db.Column(db.String(250))
    # tipo_pregunta=db.Column(db.String(100),nullable=False)
    # lenguaje=db.Column(db.String(50),nullable=False)
    # opciones=db.Column(db.String(800))
    # respuesta=db.Column(db.String(800),nullable=False)

    idCuestionario=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    autor=db.Column(db.String(200))
    temas=db.Column(db.String(100),nullable=False)
    fecha=db.Column(db.String(20),nullable=False)#2022-06-18
    tipo=db.Column(db.String(50),nullable=False)
    lenguaje=db.Column(db.String(50),nullable=False)
    preguntas=db.Column(db.String(20000),nullable=False)



    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

db.create_all()


@app.route("/cuestionarios", methods=["GET"])
def cuestionarios():
    query_lenguaje=request.args.get("lenguaje")

    #sí se ingresa un lenguaje se realiza la busqueda en base a ese lenguaje
    if query_lenguaje:
        cuestionarios=db.session.query(Prueba).filter_by(lenguaje=query_lenguaje).all()
        if cuestionarios:
            return jsonify(cuestionarios=[cuestionario.to_dict() for cuestionario in cuestionarios])
        else:
            return jsonify(response={"Not found": "No hay resultados para ese lenguaje."})
    else:
        #sí no, se muestran todos los datos de los cuestionarios
        cuestionarios = db.session.query(Prueba).all()
        if cuestionarios:
            return jsonify(cuestionarios=[cuestionario.to_dict() for cuestionario in cuestionarios])
        else:
            return jsonify(response={"Not found": "Aún no hay cuestionarios registradas."})




@app.route("/nuevo_cuestionario", methods=["POST"])
def cuestionario_post():
    try:
        now=datetime.datetime.now()
        nuevo_cuestionario = Prueba(
            autor=request.args.get("autor"),
            temas= request.args.get("temas"),
            fecha=now.date(),
            tipo= request.args.get("tipo"),
            lenguaje= request.args.get("lenguaje"),
            preguntas=request.args.get("preguntas")
        )
        db.session.add(nuevo_cuestionario)
        db.session.commit()
        return jsonify(response={"success": "Cuestionario agregado con éxito."})
    except:
        return jsonify(response={"error": "Ha ocurrido un error al agregar el cuesntionario."})

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000,debug=True)