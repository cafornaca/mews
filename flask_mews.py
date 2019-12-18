from os.path import abspath, dirname, join

from flask import flash, Flask, Markup, redirect, render_template, url_for
<<<<<<< HEAD
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
=======
import sqlalchemy
from wtforms import Form
>>>>>>> Figuring out issues with
=======
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
>>>>>>> Got Flask app UI to workgit add .
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

_cwd = dirname(abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-mews.db')
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    application_name = db.Column(db.String)
    connection_string = db.Column(db.String)
    models = db.relationship('Models', backref='mews', lazy='select')
    resources = db.relationship('Resources', backref='mews', lazy='select')

    def __repr__(self):
        return '<Project %r>' % (self.base_url)

    def __str__(self):
        return self.base_url


class Models(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String)
    table_name = db.Column(db.String)
    init_model = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    columns = db.relationship('Columns', backref='mews', lazy='select')
    
    def __repr__(self):
        return '<Model %r - %r>' % (self.url, self.date)

class Columns(db.Model):
    __tablename__ = 'columns'

    id = db.Column(db.Integer, primary_key=True)
    column_name = db.Column(db.String)
    column_type = db.Column(db.String)
    column_additional = db.Column(db.String)
    primary_key = db.Column(db.Boolean)
    foreign_key = db.Column(db.Boolean)
    unique = db.Column(db.Boolean)
    content = db.Column(db.String)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))

    def __repr__(self):
        return '<Column %r - %r>' % (self.url, self.date)

class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String)
    on_get = db.Column(db.Boolean)
    on_post = db.Column(db.Boolean)
    on_put = db.Column(db.Boolean)
    on_del = db.Column(db.Boolean)
    on_get_by_identifier = db.Column(db.Boolean)
    identifier = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    Routes = db.relationship('Routes', backref='mews', lazy='select')

    def __repr__(self):
        return '<Resource %r - %r>' % (self.url, self.date)

class Routes(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String)
    data_object_exists = db.Column(db.Boolean)
    data_object = db.Column(db.String)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))

    def __repr__(self):
        return '<Route %r - %r>' % (self.url, self.date)


class ProjectForm(Form):
    project_name = fields.StringField()
    application_name = fields.StringField()
    connection_string = fields.StringField()

class ModelsForm(Form):
    model_name = fields.StringField()
    table_name = fields.StringField()
    init_model = fields.StringField()
    project_id = fields.IntegerField()
    project = QuerySelectField(query_factory=Project.query.all)

class ColumnsForm(Form):    
    column_name = fields.StringField()
    column_type = fields.StringField()
    column_additional = fields.StringField()
    primary_key = fields.BooleanField()
    foreign_key = fields.BooleanField()
    unique = fields.BooleanField()
    content = fields.StringField()
    model_id = QuerySelectField(query_factory=Models.query.all)

class ResourcesForm(Form): 
    resource_name = fields.StringField()
    on_get = fields.BooleanField()
    on_post = fields.BooleanField()
    on_put = fields.BooleanField()
    on_del = fields.BooleanField()
    on_get_by_identifier = fields.BooleanField()
    identifier = fields.StringField()
    project_id = QuerySelectField(query_factory=Project.query.all)

class RoutesForm(Form):
    route_name = fields.StringField()
    data_object_exists = fields.BooleanField()
    data_object = fields.StringField()
    resource_id = QuerySelectField(query_factory=Resources.query.all)


@app.route("/")
def index():
    project_form = ProjectForm()
    models_form = ModelsForm()
    columns_form = ColumnsForm()
    resources_form = ResourcesForm()
    routes_form = RoutesForm()
    return render_template("index.html",
        project_form = project_form,
        models_form = models_form,
        columns_form = columns_form,
        resources_form = resources_form,
        routes_form = routes_form)

@app.route("/project", methods=("POST", ))
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project()
        form.populate_obj(project)
        db.session.add(project)
        db.session.commit()
        flash("Added project")
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

@app.route("/model", methods=("POST", ))
def add_model():
    form = ModelsForm()
    if form.validate_on_submit():
        model = Models()
        form.populate_obj(model)
        model.project_id = form.project.data.id
        db.session.add(model)
        db.session.commit()
        flash("Added model for project " + form.project.data.project_name)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

@app.route("/column", methods=("POST", ))
def add_column():
    form = ColumnsForm()
    if form.validate_on_submit():
        column = Columns()
        form.populate_obj(column)
        column.model_id = form.models.data.id
        db.session.add(column)
        db.session.commit()
        flash("Added column for model " + form.project.data.model_name)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

@app.route("/resource", methods=("POST", ))
def add_resource():
    form = ResourcesForm()
    if form.validate_on_submit():
        resource = Resources()
        form.populate_obj(resource)
        resource.project_id = form.project.data.id
        db.session.add(resource)
        db.session.commit()
        flash("Added resource for project " + form.project.data.project_name)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

@app.route("/route", methods=("POST", ))
def add_route():
    form = RoutesForm()
    if form.validate_on_submit():
        route = Routes()
        form.populate_obj(route)
        route.resource_id = form.resources.data.id
        db.session.add(route)
        db.session.commit()
        flash("Added route for resource " + form.resource.data.model_name)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)


# @app.route("/sites")
# def view_sites():
#     query = Site.query.filter(Site.id >= 0)
#     data = query_to_list(query)
#     data = [next(data)] + [[_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)] for row in data]
#     return render_template("data_list.html", data=data, type="Sites")


# _LINK = Markup('<a href="{url}">{name}</a>')


# def _make_link(site_id):
#     url = url_for("view_site_visits", site_id=site_id)
#     return _LINK.format(url=url, name=site_id)


# @app.route("/site/<int:site_id>")
# def view_site_visits(site_id=None):
#     site = Site.query.get_or_404(site_id)
#     query = Visit.query.filter(Visit.site_id == site_id)
#     data = query_to_list(query)
#     title = "visits for " + site.base_url
#     return render_template("data_list.html", data=data, type=title)


def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]

if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run()