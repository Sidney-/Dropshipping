# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json

#/////////////////////
#GENERAL SUBROUTINES
#/////////////////////
def get_user_id():
    if auth.user_id:
        user_id = str(auth.user_id)
    else:
        user_id = str(response.session_id)
    return user_id

#/////////////////////
#INDEX PAGE
#/////////////////////
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
    query = "insert into cart (user_id) VALUES ('" + user_id + "')"
    print(query)
    db.executesql(query)
    response = 1

    return dict(response=response)

def get_cart_id():
    user_id = get_user_id()
    query = "select cart_id from cart where user_id = '" + user_id + "' and status = 'active'"
    print(query)
    result = db.executesql(query,as_dict=True)
    print(int(result['cart_id']))
    if result:
        return str(result[0])
    else:
        create_cart()
        cart_id = get_cart_id()
        return cart_id

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
    return dict(response=response)

def get_cart_items():
    cart_id = get_cart_id()
    query = "select * from order_items where cart_id = " + cart_id
    data = db.executesql(query, as_dict=True)
    return json.dumps(data)

def order_item_exists_in_cart(product_id):
    cart_id = get_cart_id()
    query = "select * from order_item where product_id = " + product_id + " and cart_id = " + cart_id
    result = db.executesql(query)
    if result:
        response = True
    else:
        response = False
    return response

def remove_from_cart():
    product_id = request.vars.product_id
    cart_id = get_cart_id()

    if order_item_exists_in_cart(product_id):
        query = "delete from order_item where cart_id = " + cart_id + " and product_id = " + product_id
        response = 1
    else:
        response =0
    return dict(response)

#/////////////////////
#DEFAULT PY FUNCTIONS
#/////////////////////
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