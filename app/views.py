"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route("/properties/create", methods=["GET", "POST"])
def create():
    form = PropertyForm()
    if form.validate_on_submit():
        # Get form data
        title = form.title.data
        description = form.description.data
        num_bedrooms = form.num_bedrooms.data
        num_bathrooms = form.num_bathrooms.data
        location = form.location.data
        price = form.price.data
        property_type = form.property_type.data

        # Handle file upload
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        photo.save(os.path.join(upload_folder, filename))

        # Save to database
        new_property = Property(
            title=title,
            description=description,
            num_bedrooms=num_bedrooms,
            num_bathrooms=num_bathrooms,
            location=location,
            price=price,
            property_type=property_type,
            photo=filename
        )
        db.session.add(new_property)
        db.session.commit()

        flash('Property successfully added!', 'success')
        return redirect(url_for('properties'))

    return render_template('create.html', form=form)


@app.route("/properties")
def properties():
    all_properties = Property.query.all()
    return render_template('properties.html', properties=all_properties)


@app.route("/properties/<int:propertyid>")
def property_detail(propertyid):
    prop = db.session.get(Property, propertyid)
    if prop is None:
        return render_template('404.html'), 404
    return render_template('property.html', property=prop)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404