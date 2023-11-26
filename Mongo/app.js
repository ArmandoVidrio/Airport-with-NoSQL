const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');
const mongoose = require('mongoose');

//modelo
const Vuelo = require("./flightEsquema");

const app = express();
app.use(express.json());

async function main() {
    // Función para leer y guardar datos desde un archivo CSV
    function leerYGuardarCSV(filePath) {
        const results = [];
    
        fs.createReadStream(filePath)
            .pipe(csv({
                headers: ["aerolinea", "origen", "destino", "dia", "mes", "anio", "genero", "razon", "estancia", "transporte", "conexion", "tiempoEspera"],
                skipLines: 1
            })) // Proporciona manualmente los encabezados
            .on('data', (data) => {
                results.push(data);
            })
            .on('end', () => {
                guardarEnMongo(results);
            });
    }
    
    // Función para guardar datos en MongoDB
    function guardarEnMongo(data) {
        data.forEach((row) => {

            const vueloNuevo = new Vuelo({
                aerolinea: row.aerolinea,
                origen: row.origen,
                destino: row.destino,
                conexion: row.conexion,
                tiempoEspera: row.tiempoEspera
            });
    
            vueloNuevo.save()
                .then(() => console.log('Guardado exitosamente'))
                .catch((error) => console.error('Error al guardar en MongoDB:', error));
        });
    }
    

    async function EncontrarMejoresAeropuertos() {
        try {    
            const agregacionCompleta = await Vuelo.aggregate([
                {
                    $match: {
                        tiempoEspera: { $gte: 60 },
                        conexion: "No es de conexion"
                    }
                },
                {
                    $group: {
                        _id: "$origen",
                        promedioTiempoEspera: { $avg: "$tiempoEspera" },
                        totalVuelos: { $sum: 1 }
                    }
                }
            ]);
    
            console.log("Mejores aeropuertos para abrir restaurantes:");
            console.log(agregacionCompleta);
            
        } catch (error) {
            console.error('Error al realizar la agregación:', error);
        }
        
    }

    // Establece la conexión a la base de datos
    await mongoose.connect("mongodb+srv://arlynmedina:admin@myapp.e5mj3za.mongodb.net/", { useNewUrlParser: true, useUnifiedTopology: true });

    // Llama a la función para leer y guardar datos desde el archivo CSV
    leerYGuardarCSV("./data/csvjson.csv");

    // Espera a que se completen las operaciones de guardado antes de llamar a la función para encontrar los mejores aeropuertos
    await new Promise(resolve => setTimeout(resolve, 10000)); // Pausa por 1 segundo (ajusta el tiempo según sea necesario)

    // Llama a la función para encontrar los mejores aeropuertos
    await EncontrarMejoresAeropuertos();


    // Inicia el servidor Express
    app.listen(3000, () => {
        console.log("Aplicacion corriendo con exito...");
    });
}

// Llama a la función principal
main();
