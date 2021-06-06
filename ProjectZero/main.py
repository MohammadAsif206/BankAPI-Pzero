
import logging
from flask import Flask
from routes.cust_acc_routes import create_routes

app: Flask = Flask(__name__)
create_routes(app)  # routes

logging.basicConfig(filename="record.log", level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(message)s")
# Handler methods create your WEB API layer
# They are responsible for handling HTTP requests and responses
# Parsing and generating JSON, giving back status codes as appropriate
# They SHOULD NOT be directly responsible for CRUD operations of business logics
# Your handler should use services. They SHOULD NOT use DAOs directly


if __name__ == '__main__':
    app.run()
