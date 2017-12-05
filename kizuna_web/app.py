import os
import urllib.parse
from uuid import uuid4
from flask import Flask
from flask import render_template
from flask import Flask, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
import json
import boto3
from kizuna.Kizuna import Kizuna
from raven import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kizuna.models.ReactionImage import ReactionImage
from kizuna.models.ReactionImageTag import ReactionImageTag

from config import \
    AWS_ACCESS_KEY_ID,\
    AWS_SECRET_ACCESS_KEY,\
    DATABASE_URL,\
    IMAGE_UPLOAD_DIR,\
    KIZUNA_ENV,\
    S3_BUCKET,\
    S3_BUCKET_URL,\
    SENTRY_URL

DEV_INFO = Kizuna.read_dev_info('./.dev-info.json')

sentry = Client(SENTRY_URL,
                release=DEV_INFO.get('revision'),
                environment=KIZUNA_ENV) if SENTRY_URL else None

app = Flask(__name__, static_folder='../static')

db_engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=db_engine)

aws_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


@app.route("/")
def hello():
    return render_template('index.jinja2', title='Welcome')


@app.route("/react/images/new")
def new_reaction_image():
    return render_template('react_component.jinja2',
                           title='Upload New Reaction Image',
                           component_entry='new-reaction-image')


def allowed_image_file(type):
    return type in ['image/png', 'image/jpg', 'image/jpeg']


@app.route("/react")
def gallery():
    return render_template('gallery.jinja2',
                           images=Session().query(ReactionImage).all())


@app.route("/api/react/images", methods=['POST'])
def handle_image_upload():
    session = Session()
    res = Response(json.dumps({'ok': True}), status=200, mimetype='application/json')

    title = request.values.get('title')
    tags = json.loads(request.values.get('tags'))
    file = request.files.get('file')
    if file.filename == '':
        return Response(json.dumps({'ok': False}), status=400, mimetype='application/json')
    if file and allowed_image_file(type=file.content_type):
        ext = os.path.splitext(file.filename)[1]
        filename = secure_filename(uuid4().hex + ext)
        image_path = os.path.join(IMAGE_UPLOAD_DIR, filename)
        aws_client.put_object(Body=file, Key=image_path, Bucket=S3_BUCKET)
        image_url = S3_BUCKET_URL + '/' + image_path
        image = ReactionImage(name=title, url=image_url)
        session.add(image)
        tags = [ReactionImageTag.maybe_create_tag(session, tag) for tag in tags]
        for tag in tags:
            image.tags.append(tag)
        session.commit()
        return Response(json.dumps({'ok': True, 'file': 'file'}), mimetype='application/json')
    return res


@app.route("/api/react/tags")
def get_tags():
    tags = [tag.to_dict() for tag in Session().query(ReactionImageTag).all()]
    return Response(json.dumps({'tags': tags}),
                    mimetype='application/json')
