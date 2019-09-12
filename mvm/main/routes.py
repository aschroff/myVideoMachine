from flask import Blueprint
from flask import render_template, request
from mvm import db
from mvm.models import Item
from mvm.analytics.forms import SearchItemForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.date_posted.desc()).paginate(page=page, per_page=12)
    itemsall = Item.query.order_by(Item.date_posted.desc()).all()
    searchform = SearchItemForm()
    return render_template('home.html', items=items, itemsall=itemsall, searchform=searchform)


@main.route("/about")
def about():
    db.drop_all()
    db.create_all()
    itemsall = Item.query.order_by(Item.date_posted.desc()).all()
    searchform = SearchItemForm()
    return render_template('about.html', title='About', itemsall=itemsall, searchform=searchform)
