///ESQUEMA DE LOS VUELOS
const { text } = require('body-parser');
const {Schema,model} = require('mongoose');


//Esquema de los vuelos
const esquemaVuelo = new Schema({
    aerolinea:{
        type:String,
        required:true
    },
    origen:{
        type:String,
        required:true
    },
    destino:{
        type:String,
        required:true
    },
    conexion:{
        type:String,
        required:true
    },
    tiempoEspera:{
        type:Number,
        required:true
    }
    
});

//exportamos el esquema
module.exports = model("Vuelo",esquemaVuelo);