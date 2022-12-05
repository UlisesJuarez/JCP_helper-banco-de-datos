from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jcp_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "jcp_helper233445"

db=SQLAlchemy(app)

class Prueba(db.Model):
    __tablename__="Cuestionarios"

    idCuestionario=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    titulo=db.Column(db.String(100),nullable=False)
    autor=db.Column(db.String(200),)
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

#db.create_all()


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


@app.route("/cuestionario_titulo",methods=["GET"])
def cuestionario_titulo():
    query_titulo=request.args.get("titulo").lower()
    search=f"%{query_titulo}%"

    if query_titulo:
        cuestionarios=db.session.query(Prueba).filter(Prueba.titulo.like(search)).all()
        if cuestionarios:
            return jsonify(cuestionarios=[cuestionario.to_dict() for cuestionario in cuestionarios])
        else:
            return jsonify(response={"Not found":"No hay cuestionarios para ese criterio de busqueda"})
    else:
        return jsonify(response={"Error":"Ho haz ingresado un criterio de busqueda"})


@app.route("/cuestionario_id",methods=["GET"])
def cuestionario_id():
    query_id=request.args.get("id")
    
    if query_id:
        cuestionario=db.session.query(Prueba).filter_by(idCuestionario=query_id).all()
        if cuestionario:
            return jsonify(cuestionario=[item.to_dict() for item in cuestionario])
        else:
            return jsonify(response={"Not found":"No existe un cuestionario con ese id"})
    else:
        return jsonify(response={"Error":"No haz ingresado un criterio de busqueda"})


@app.route("/nuevo_cuestionario", methods=["POST"])
def cuestionario_post():
    try:
        now=datetime.datetime.now()
        nuevo_cuestionario = Prueba(
            titulo=request.args.get("titulo"),
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