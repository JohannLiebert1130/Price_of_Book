from flask import Blueprint, render_template, request, redirect, url_for, json, session

from src.models.crawlers.crawler import Crawler
from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route("/")
def index():
    print(session['email'])
    stores = Store.all()
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route("/store/<string:store_id>")
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.get_by_id(store_id))


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']

        store.crawler.price_tag_name = request.form['price_tag_name']
        store.crawler.price_query = json.loads(request.form['price_query'])

        store.crawler.image_tag_name = request.form['image_tag_name']
        store.crawler.image_query = json.loads(request.form['image_query'])


        # print(store.crawler.price_query)
        store.save_to_mongo()
        store.crawler.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.jinja2', store=store)


@store_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']

        price_tag_name = request.form['price_tag_name']
        price_query = json.loads(request.form['price_query'])

        image_tag_name = request.form['image_tag_name']
        image_query = json.loads(request.form['image_query'])

        crawler = Crawler(price_tag_name, price_query, image_tag_name, image_query)
        crawler.save_to_mongo()

        Store(name, url_prefix, crawler._id).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/new_store.jinja2')
