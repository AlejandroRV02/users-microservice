Users microservice

This microservice is made with Flask 2.0.3

HOST: http://0.0.0.0:6000

This RESTful API contains the following endpoints:


POST /users/signup

    @body:
        - username: String *Required
        - password: String *Required
        - name: String     *Required
        - age: Int         *Required
    
    @example:
        {
            "username": "alejandrorv",
            "password": "alejandro",
            "name": "Alejandro Rodriguez",
            "age": 22
        }
    
    @returns:
        201 CREATED
        400 BAD_REQUEST
        409 CONFLICT
        500 INTERNAL_SERVER_ERROR


POST /users/login

    @body:
        - username: String *Required
        - password: String *Required
    
    @example:
        {
            "username": "alejandrorv",
            "password": "alejandro",
        }
    
    @returns:
        200 OK - {"access_token": "token"}
        400 BAD_REQUEST
        401 UNAUTHORIZED
        500 INTERNAL_SERVER_ERROR

GET /users/profile

    @headers:
        -Authorization: As Bearer Token
    
    @example:
        Authorizationz: Bearer {token}

    @returns:
        200 OK - {"id": id, "username": username, "name": name, "age": age}
        404 NOT_FOUND
        500 INTERNAL_SERVER_ERROR

How to run

This application is allocated in Docker Hub, so you can pull by typing this command:

    - docker pull alejandrorv/users-microservice:latest

Once pulled, you need to run the next command

    - docker run -it --name users -p 6000:6000 alejandrorv/users-microservice

You can change the first option for the local port if it causes any conflict

Flag --name is also optional
