import os
import sys
from flask import Flask, render_template, request
from werkzeug.debug import DebuggedApplication
from models import *


# Flask quickstart:
# https://flask.palletsprojects.com/en/3.0.x/quickstart/
# Flask factory pattern:
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/

def create_app():
    
    # Static files (e.g. css, js, images) will be stored one level up, in the ~/public_html directory
    STATIC_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public_html'))


    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False,
                static_folder=STATIC_FOLDER,
                static_url_path='/static'
    )


    # Load config from file config.py
    app.config.from_pyfile('config.py')


    # Keep static files path in app config
    app.config["STATIC_FOLDER"] = STATIC_FOLDER


    # Enable debug mode - you will see beautiful error messages later :)
    # https://flask.palletsprojects.com/en/3.0.x/debugging/
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)


    # Ensure the instance folder exists - nothing interesting now
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#configure-the-extension
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/app/instance/database.sqlite"
    db.init_app(app)

    with app.app_context():
        db.create_all()



    # Setup custom "Not found" page
    # https://flask.palletsprojects.com/en/3.0.x/errorhandling/#custom-error-pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    # Register blueprints (views)
    # https://flask.palletsprojects.com/en/3.0.x/blueprints/
    # from .views.index import bp as bp_index
    # app.register_blueprint(bp_index)

    #####################
    # TODO: remove
    # TESTING
    ###############
    # Create a remote server
    with app.app_context():
        remote = Remote(
            address="192.168.1.100",
            port=8080,
            secret="supersecret123",
            name="BackupNode1"
        )
        db.session.add(remote)
        db.session.commit()
        remote1 = Remote(
            address="192.168.1.113",
            port=8080,
            secret="superseawqwe3",
            name="SAMANGo"
        )
        db.session.add(remote1)
        db.session.commit()


        # Create a document
        document = Document(
            file_hash="abc123def456",
            local_file_path="/var/data/doc1.txt",
            is_local=True,
        )
        db.session.add(document)
        db.session.commit()

        # Link the metadata to the document (backref)
        metadata = DocumentMetadata(
            document_Id=document.local_Id  # Will be set after document is created
        )
        db.session.add(metadata)
        db.session.commit()

        # Create a mirror relationship (Document <-> Remote)
        mirror = DocumentMirror(
            document_Id=document.local_Id,
            remote_Id=remote.Id
        )

        mirror = DocumentMirror(
            document_Id=document.local_Id,
            remote_Id=remote1.Id
        )
        db.session.add(mirror)
        db.session.commit()

        print("Example entries created!")

        from sqlalchemy import select
        q = select(Remote).where(Remote.Id == 2)
        r = db.session.execute(q)
        for row in r.all():
            print(row)
            print(row.Remote.Id)
            db.session.delete(row.Remote)

        q = select(Remote).where(Remote.Id == 2)
        r = db.session.execute(q)
        for row in r.all():
            print(row)

    return app


