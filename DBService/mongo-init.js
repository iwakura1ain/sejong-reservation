db.createUser(
    {
        user: "testusr",
        pwd: "1234",
        roles: [
            {
                role: "readWrite",
                db: "exampledb"
            }
        ]
    }
);
