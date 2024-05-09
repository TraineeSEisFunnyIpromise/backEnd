db.createUser(
        {
            username: "admin",
            password: "1234",
            roles: [
                {
                    role: "readWrite",
                    db: "db1"
                }
            ]
        }
);