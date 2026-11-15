// scripts/init_mongo.js
db = db.getSiblingDB('tienda');

// Insertar usuarios de prueba
db.usuarios.insertMany([
  { username: "admin", password: "SuperSecretPassword123", role: "admin" },
  { username: "user1", password: "password123", role: "client" }
]);



//COMIENZO DE LA MODIFICACIÓN 
//Creación de usuario con permisos de lectura y escritura
db.createUser({
  user: "app_user",
  pwd: "AppPasswordSegura456!",
  roles: [
    { role: "readWrite", db: "pedidos_db" }
  ]
});
//FIN DE LA MODIFICACIÓN



// Insertar un pedido inicial de prueba
db.pedidos.insertOne({
  producto: "Laptop Gaming",
  cantidad: 1
});

print("Base de datos 'tienda' inicializada correctamente con datos de prueba.");
