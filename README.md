## To run this application

### Create virtual environment and activate it

    Windows machine:
    virtualenv venv

    Activate the virtual env:
    venv\Scripts\activate

### Install all the dependencies

    poetry install

### Run the application

    poetry run python manage.py runserver

### To migrate the applicaiton

    poetry run python manage.py makemigrations
    poetry run python manage.py migrate

### Tables

    what we have
    Post - /nodes, name: serverA; reponse: id:1, name
    Post - /edges, source:serverA, destination: serverB, latency; reponse: id
    Get - /routes/shortest/, source:serverA, destination: ServerD; reponse: "total_latency":23.4, path:["ServerA",serverB, serverD] or no path between nodes

    Get - /route/history - filter by source, destination, limit(number of records), date_from/date_to(timestamp)
    Response:
        "id": 1,
        "source": "ServerA",
        "destination": "ServerD",
        "total_latency": 23.4,
        "path": ["ServerA", "ServerB", "ServerD"],
        "created_at": "2026-02-20T14:32:00Z"

    Plan of action:
    In the models.py create 2 tables
        Nodes: id, name: serverA, created_at, modified_at
        Edges: id, source:Foreignkey of node, destination:Foreignkey of node, latency, created_at, modified_at


    Next we create app name as api and create endpoints /nodes, edges, /routes/shortest/

    optional;
    Get /nodes, Delete/nodes/{id}/
    Get /edges, Delete /edges/id/

    History api needs this
        /routes/history
         {
            "id": 1,
            "source": "ServerA",
            "destination": "ServerD",
            "total_latency": 23.4,
            "path": ["ServerA", "ServerB", "ServerD"],
            "created_at": "2026-02-20T14:32:00Z"
        },
