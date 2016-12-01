# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
<<<<<<< HEAD
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
=======
    session.custome_session = response.session_id
    title = "Dropshipping"
    response.flash = T("Welcome to " + title)
    return dict(message=T("Welcome to web2py!" + title))

def add_to_cart():
    product_id = str(request.vars.product_id)
    qty = str(request.vars.qty)
    user_id = get_user_id()
    cart_id = get_cart_id(user_id)
    # print 'cart_id => '+cart_id
    query = "insert into order_item (cart_id, product_id, qty) VALUES (" + cart_id + ", " + product_id + ", " + qty + ")"
    db.executesql(query)

def get_cart_id(user_id):
    query = "select cart_id from cart where user_id = '" + str(user_id) + "' and status = 'active'"
    result = db.executesql(query)
    if not result:
        cart_id = create_cart(user_id)
    else:
        cart_id = str(result[0][0])

    return cart_id


def get_number_of_items_in_cart():
    user_id = get_user_id()
    cart_id = get_cart_id(user_id)
    query = "select sum(qty) as total from order_item where cart_id = "+ cart_id
    result = db.executesql(query)
    return json.dumps({'total': int(result[0][0])})


def create_cart(user_id):
    query = "insert into cart (user_id) values('" + user_id + "')"
    db.executesql(query)
    query = "select cart_id from cart where user_id = '" + user_id + "'"
    cart_id = db.executesql(query)
    return str(cart_id[0][0])


def get_user_id():
    if auth.user_id:
        user_id = str(auth.user_id)
    else:
        user_id = session.custome_session

    return user_id

def product():
    return dict()

def checkout():
    user_id = get_user_id()
    cart_id = get_cart_id(user_id)
    query = "select * from product_order_item where cart_id = " + cart_id
    result = db.executesql(query, as_dict=True)

    return dict(location=T('Dropshiping - Checkout'),items=result)


def contact():
    return dict()
























"""


def checkout():
    return dict()

#/////////////////////
#PRODUCT PAGE
#/////////////////////
def product():
    return dict()

def get_products_by_location():
    location = request.vars.location
    query = "select * from product_location where product_location = " + location
    data = db.executesql(query, as_dict=True)
    return json.dumps(data)

#/////////////////////
#CONTACT PAGE
#/////////////////////
def contact():
    return dict()

def contact_post():
    return dict()

def contact_get():
    return dict()

#/////////////////////
#CART FUNCTIONS
#/////////////////////
def create_cart():
    user_id = get_user_id()
    query = "insert into cart (user_id) VALUES ('" + str(user_id) + "')"
    res = db.executesql(query)
    response = 1
    return response

def get_cart_id():
    user_id = get_user_id()
    query = "select cart_id from cart where user_id = '" + str(user_id) + "' and status = 'active'"
    result = db.executesql(query,as_dict=True)
    if result:
        return result[0]['cart_id']
    else:
        create_cart()
        cart_id = get_cart_id()
        return cart_id
>>>>>>> master

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


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


