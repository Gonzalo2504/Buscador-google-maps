from flask import Flask, render_template, request, jsonify
from models import BuscadorFarmacias

# Instancia de la aplicación Flask
app = Flask(__name__)

# Uso de la clase
api_key = "ClAvE aPi"
buscador = BuscadorFarmacias(api_key)

@app.route("/", methods=["GET", "POST"])
def buscarFarmacias():
    if request.method == "POST":
        # Realiza la búsqueda de farmacias
        latitud, longitud = buscador.obtener_ubicacion_usuario()
        detalles_farmacias = buscador.buscar_y_obtener_detalles_farmacias(latitud, longitud)

        print("Detalles de farmacias:", detalles_farmacias)

        # Renderiza la plantilla con los resultados
        return render_template("index.html", farmacias=detalles_farmacias)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
