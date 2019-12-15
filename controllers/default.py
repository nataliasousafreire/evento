# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# ---- API (example) -----

@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

def home():
    response.flash = T("Hello World")
 
    form = SQLFORM.grid(db.Evento,create=False,csv=False)
    msg = "Home de Eventos"
    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def criar_evento():
    msg = "Criar Eventos"
    form = SQLFORM(db.Evento)

    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
    elif form.errors:
         response.flash = 'Erros no formulário!'
    else:
         response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

def show():
    grid = SQLFORM.smartgrid(db.Cliente, linked_tables=['auth_user'])
    return dict(grid=grid,field_id= "usu_id")	

@auth.requires_login()
@auth.requires_membership("usuario")
def meus_eventos():
    msg = "Meus Eventos"

    query1 = session.auth.user.id == db.Participacoes.cli_id
    query2 = db.Evento.id == db.Participacoes.eve_id
    form = db(query1 and query2 and db.Evento.org_id == db.Organizacao.usu_id).select(db.Evento.titulo,db.Organizacao.usu_id)
    
    return dict(msg=msg,rows=form)


# ---- Action for login/register/etc (required for auth) -----
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

@auth.requires_login()
def registro():
	##impede que seja de 2 grupos
	if  auth.has_membership(2, session.auth.user.id) or auth.has_membership(3, session.auth.user.id):
		redirect(URL('home'))

	db.Cliente.usu_id.writable = False
	form1 = SQLFORM(db.Cliente)

	#atribuindo o usu_id igual ao do usuario
	form1.vars.usu_id = session.auth.user.id

	if form1.process().accepted:
		session.flash = 'Cadastro aceito!'
		auth.add_membership(2, session.auth.user.id) #inseri no grupo de usuarios
		redirect(URL('home'))
	elif form1.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	db.Organizacao.usu_id.writable = False
	db.Organizacao.eventos.writable = False
	form2 = SQLFORM(db.Organizacao)

	#atribuindo o usu_id igual ao do usuario
	form2.vars.usu_id = session.auth.user.id

	if form2.process().accepted:
		session.flash = 'Formulário aceito!'
		auth.add_membership(3, session.auth.user.id) #inseri no grupo de organizacao
		redirect(URL('home'))
	elif form2.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	msg = "Registro- Cliente ou Organizacao"
	return dict(msg=msg,form1=form1,form2=form2)

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

#Relatorios
def tag():
    return dict()

def cliente():
    return dict()

def intervalo():
    return dict()