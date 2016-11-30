# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json

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

def checkout():
    return dict()

def product():
    return dict()

def get_products_by_location():
    location = request.vars.location
    query = "select * from product_location where product_location = " + location
    data = db.executesql(query, as_dict=True)
    return json.dumps(data)


def contact():
    return dict()

def create_cart():

    if result:
        response = 0
    else:
        query = "insert into cart (user_id) VALUES (" + str(user_id) + ")"
        db.executesql(query)
        response = 1

    return dict(response=response)

def get_cart_id():
    user_id = str(auth.user_id)
    query = "select cart_id from cart where user_id = " + user_id  + "status = active"
    result = db.executesql(query)
    if result:
        return str(result[0])
    else:
        return str(0)


def add_to_cart():
    product_id = request.vars.product_id
    qty = request.vars.qty
    user_id = str(auth.user_id)

    cart_id = get_cart_id()
    if cart_id != 0:
        query = "select * from order_item where user_id = " + user_id + " and cart_id = " + cart_id
        result = db.executesql(query)
        if result:
            response = 0
        else:
            query = "insert into order_item (cart_id, product_id, qty) VALUES (" + str(cart_id) + ", " + str(product_id) + ", "+ str(qty) + ")"
            db.executesql(query)
            response = 1
    return dict(response=response)


def get_cart_items():


def remove_from_cart():
    product_id = request.vars.product_id
    user_id = str(auth.user_id)



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
