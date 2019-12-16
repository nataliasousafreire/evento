# -*- coding: utf-8 -*-

def home():
	response.flash = T("Hello World")

	db.Evento.created_on.readable = True
	links_t = ['Tag_Evento','Periodo','Lote']
	links_c = [dict(header='Ingresso', body= lambda row: A("comprar",callback=URL("default","comprar",args=[row.id]),target="_self" ))]
	
	form = SQLFORM.smartgrid(db.Evento,deletable=False,showbuttontext=False,
			linked_tables=links_t,links=links_c,create=False,
			csv=False,editable = False,user_signature=False)

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

@auth.requires_login()
def meus_eventos():
	msg = "Meus Eventos"

	##usuario ou organizacao
	usu = db(db.Cliente.usu_id == session.auth.user.id).select()
	
	if(usu):
		db.Participacao.cli_id.writable = db.Participacao.eve_id.writable = False
		query = db.Evento.id == db.Participacao.eve_id and session.auth.user.id == db.Participacao.cli_id
		form = SQLFORM.grid(query,deletable=False,create=False,csv=False,user_signature=False)
	
	else:
		db.Evento.created_on.readable = True
		db.Evento.participantes.writable = False
		db.Evento.org_id.writable = False
		org = db(session.auth.user.id == db.Organizacao.usu_id).select()
		query = db.Evento.org_id ==org[0].id
		form = SQLFORM.grid(query,deletable=False,create=False,csv=False,user_signature=False)

	
	return dict(msg=msg,rows=form)

@auth.requires_login()
@auth.requires_membership("usuario")
def comprar():
	##response.flash = T("Comprar")
	msg = request.args(0)
	return dict(msg=msg)


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

@auth.requires_login()
@auth.requires_membership("usuario")
def cliente():
	pid = session.auth.user.id
	db.Cliente.id.readable = False
	db.Cliente.usu_id.writable = False

	form = SQLFORM(db.Cliente,pid)
	msg = "Cliente"
	return dict(msg=msg,grid=form.process())

@auth.requires_login()
@auth.requires_membership("Organizacao")
def organizacao():
	pid = session.auth.user.id
	sel = db(db.Organizacao.usu_id == pid).select(db.Organizacao.id)

	db.Organizacao.id.readable = False
	db.Organizacao.usu_id.writable = db.Organizacao.eventos.writable = False

	form = SQLFORM(db.Organizacao,sel[0].id)

	msg = "Organizacao"
	return dict(msg=msg,grid=form.process())

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


def intervalo():
    return dict()


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