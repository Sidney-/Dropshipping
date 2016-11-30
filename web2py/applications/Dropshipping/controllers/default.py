# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json
import locale
locale.setlocale( locale.LC_ALL, '' )

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    title = "Dropshipping"
    response.flash = T("Welcome to " + title)
    return dict(message=T("Welcome to web2py!" + title))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())



# Returns all of the images/information for a single product
def product():

    product_id = str(request.vars.product_id)

    query = "select * from product_view where product_id = " + product_id
    result = db.executesql(query, as_dict=True)
    format_price(result)
    return json.dumps(result)

#returns top images and info needed to build products from category
def get_products_by_category():

    category_name = request.vars.category_name

    # category_name = "Television"
    query = "select product_id, title, price, image_path from product_tag_association where tag_name = '" + str(category_name) + "'"
    result = db.executesql(query, as_dict=True)
    format_price(result)
    return json.dumps(result)

#retrieves items to populate similar items table (Selected by category)
def get_similar_items():

    product_id = str(request.vars.product_id)

    query = "select product_id, title, price, image_path from product_tag_association where product_id != " + product_id + " and tag_name in (select tag_name from product_tag_association where product_id = " + product_id + ")"
    result = db.executesql(query)
    format_price(result)

#adds an item to the cart
def add_to_cart():

    product_id = str(request.vars.product_id)
    qty = str(request.vars.qty)

    cart_id = get_cart_id()
    if cart_id != 0:
        if order_item_exists_in_cart(product_id):
            response = 0
        else:
            query = "insert into order_item (cart_id, product_id, qty) VALUES (" + cart_id + ", " + product_id + ", " + qty + ")"
            db.executesql(query)
            response = 1
    return json.dumps(dict(response=response))

#removes an item from the cart
def remove_from_cart():

    product_id = request.vars.product_id

    cart_id = get_cart_id()
    if order_item_exists_in_cart(product_id):
        query = "delete from order_item where cart_id = " + cart_id + " and product_id = " + product_id
        db.executesql(query)
        response = 1
    else:
        response = 0
    return json.dumps(dict(response=response))

#returns all items in the cart
def get_cart_items():
    cart_id = get_cart_id()
    query = "select * from product_order_item where cart_id = " + cart_id
    result = db.executesql(query, as_dict=True)
    format_price(result)
    return json.dumps(result)

#returns main categories
def get_main_categories():
    query = "select tag_name, tag_id from tag where main_category = 1"
    result = db.executesql(query, as_dict=True)
    return json.dumps(result)


def checkout():
    return dict()

def contact():
    return dict()

def create_cart():
    user_id = get_user_id()
    query = "insert into cart (user_id) VALUES ('" + user_id + "')"
    print(query)
    db.executesql(query)
    response = 1

def get_user_id():
    print (session.id)
    if auth.user_id:
        user_id = str(auth.user_id)
    elif session.id:
        user_id = str(session.id)
    else:
        session.id = response.session_id
        user_id = str(session.id)
    return user_id

def get_cart_id():
    user_id = get_user_id()
    query = "select cart_id from cart where user_id = '" + user_id + "' and status = 'active'"
    result = db.executesql(query)

    if result:
        return str(result[0][0])
    else:
        create_cart()
        cart_id = get_cart_id()
        return cart_id


def order_item_exists_in_cart(product_id):
    cart_id = get_cart_id()
    query = "select * from order_item where product_id = " + product_id + " and cart_id = " + cart_id
    result = db.executesql(query)
    if result:
        response = True
    else:
        response = False
    return response

def format_price(result):
    for i in range(len(result)):
        result[i]['price'] = locale.currency(result[i]['price'], grouping=True)



@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
