import json
import os
from uuid import uuid4

from flask import render_template
from flask import request, Response, Blueprint
from werkzeug.utils import secure_filename

from config import \
    IMAGE_UPLOAD_DIR, \
    S3_BUCKET, \
    S3_BUCKET_URL
from kizuna.models.ReactionImage import ReactionImage
from kizuna.models.ReactionImageTag import ReactionImageTag
from .extentions import aws_client, make_db_session
from .middleware import requires_auth_factory

blueprint = Blueprint('views', __name__)

requires_auth = requires_auth_factory(blueprint)


@blueprint.route("/")
def hello():
    return render_template('index.jinja2', title='Welcome')


@blueprint.route("/react/images/new")
@requires_auth
def new_reaction_image():
    return render_template('react_component.jinja2',
                           title='Upload New Reaction Image',
                           component_entry='new-reaction-image')


def allowed_image_file(type):
    return type in ['image/png', 'image/jpg', 'image/jpeg']


@blueprint.route("/react")
def gallery():
    session = make_db_session()
    images = session.query(ReactionImage).all()
    return render_template('gallery.jinja2',
                           images=images)


@blueprint.route("/api/react/images", methods=['POST'])
@requires_auth
def handle_image_upload():
    session = make_db_session()
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
        tags = [ReactionImageTag.maybe_create_tag(session, tag.lower()) for tag in tags]
        for tag in tags:
            image.tags.append(tag)
        session.commit()
        return Response(json.dumps({'ok': True, 'file': 'file'}), mimetype='application/json')
    return res


@blueprint.route("/api/react/tags")
def get_tags():
    tags = [tag.to_dict() for tag in make_db_session().query(ReactionImageTag).all()]
    return Response(json.dumps({'tags': tags}),
                    mimetype='application/json')
