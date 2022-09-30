from flask import Flask,url_for,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jcp_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "jcp_helper233445"

db=SQLAlchemy(app)

class Prueba(db.Model):
    __tablename__="Preguntas"
    idPregunta=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    enunciado=db.Column(db.String(500),nullable=False)
    autor=db.Column(db.String(200))
    fecha=db.Column(db.String(20),nullable=False)#2022-06-18
    tema=db.Column(db.String(250))
    tipo_pregunta=db.Column(db.String(100),nullable=False)
    lenguaje=db.Column(db.String(50),nullable=False)
    opciones=db.Column(db.String(800))
    respuesta=db.Column(db.String(800),nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

#db.create_all()


@app.route("/preguntas", methods=["GET"])
def preguntas():
    query_lenguaje=request.args.get("lenguaje")

    #sí se ingresa un lenguaje se realiza la busqueda en base a ese lenguaje
    if query_lenguaje:
        preguntas=db.session.query(Prueba).filter_by(lenguaje=query_lenguaje).all()
        if preguntas:
            return jsonify(preguntas=[pregunta.to_dict() for pregunta in preguntas])
        else:
            return jsonify(response={"Not found": "No hay resultados para ese lenguaje."})
    else:
        #sí no, se muestran todos los datos de los preguntas
        preguntas = db.session.query(Prueba).all()
        if preguntas:
            return jsonify(preguntas=[pregunta.to_dict() for pregunta in preguntas])
        else:
            return jsonify(response={"Not found": "Aún no hay preguntas registradas."})


# @app.route("/colonias", methods=["GET"])
# def colonias():
#     cp_col=request.args.get("codigop")
#     query_colonia=request.args.get("colonia")

#     if cp_col:
#         colonias=db.session.query(Colonia).filter_by(codigop=cp_col).all()
#         if colonias:
#             return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
#         else:
#             return jsonify(response={"Not found": "No hay resultados para ese código postal."})
#     elif query_colonia:
#         colonias=db.session.query(Colonia).filter_by(colonia=query_colonia).all()
#         if colonias:
#             return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
#         else:
#             return jsonify(response={"Not found": "No hay resultados para esa colonia."})
#     else:
#         colonias = db.session.query(Colonia).all()
#         if colonias:
#             return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
#         else:
#             return jsonify(response={"Not found": "Aún no hay colonias registradas."})


@app.route("/nueva_pregunta", methods=["POST"])
def pregunta_post():
    try:
        now=datetime.datetime.now()
        nueva_pregunta = Prueba(
            enunciado=request.args.get("enunciado"),
            autor=request.args.get("autor"),
            fecha=now.date(),
            tema= request.args.get("tema"),
            tipo_pregunta= request.args.get("tipo_pregunta"),
            lenguaje= request.args.get("lenguaje"),
            opciones= request.args.get("opciones"),
            respuesta=request.args.get("respuesta")
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        return jsonify(response={"success": "Pregunta agregada con éxito."})
    except:
        return jsonify(response={"error": "Ha ocurrido un error al agregar la pregunta."})

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000,debug=True)