const mongoose = require("mongoose");
const mongoConnection = "mongodb+srv://arlynmedina:admin@myapp.e5mj3za.mongodb.net/";

let db = mongoose.connection;

db.on("connecting",()=>{
    console.log("Conectando a la base...");
    console.log(mongoose.connection.readyState);
});
db.on("connected",()=>{
    console.log("Conectado a la base exitosamente");
    console.log(mongoose.connection.readyState);
});

mongoose.connect(mongoConnection);
