# -*- coding: utf-8 -*-

def index():
	redirect(URL('evento','default','home'))

#mostra todos os eventos disponiveis	
def home():
	db.Evento.created_on.readable = True

	##liks paras as tabelas relacionadas
	links_t = ['Tag_Evento','Periodo','Lote']

	#campo extra de avaliacaov - campo virtual
	links_c = [dict(header='Avaliacao', body = avaliacao),
	dict(header='Ingresso', body= lambda row: A("comprar",callback=URL("default","comprar",args=[row.id]),target="_self" ))]
			   
	form = SQLFORM.smartgrid(db.Evento,deletable=False,linked_tables=links_t,
	links=links_c,create=False,csv=False,editable = False,user_signature=False,
	maxtextlength=10)

	return dict(grid=form)

def procura_tags():
	response.view = 'default/home.html'
	
	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
	
	if(form.process().accepted):
		pid = db(db.Tag.tag == form.vars.tag).select().first()
		
		links_c = [dict(header='Avaliacao', body = avaliacao),
		dict(header='Ingresso', body= lambda row: A("comprar",callback=URL("default","comprar",args=[row.id]),target="_self" ))]
		query = db.Tag_Evento.eve_id == db.Evento.id and db.Tag_Evento.tag_id == pid.id

		form = SQLFORM.grid(query,deletable=False,links=links_c,create=False,csv=False,editable = False)
		
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(grid=form)
	
@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_evento():
	msg = "Cadastrar Eventos"

	db.Evento.participantes.writable = db.Evento.org_id.writable = False
	form = SQLFORM(db.Evento,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Cadastrar Estabelecimento", _class='btn-primary', _href=URL('evento','default', "cadastro_Estabelecimento"))])
    
	Org = db(db.Organizacao.usu_id == session.auth.user.id).select().first()
	form.vars.org_id = Org.id
    
	if form.process().accepted:
		session.flash = 'Cadastro aceito!'
		Org.eventos = Org.eventos + 1
		Org.update_record()
		redirect(URL('evento','default',"cadastro_Periodo",args=[form.vars.id]))
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Estabelecimento():
    msg = "Cadastrar Estabelecimento"
    form = SQLFORM(db.Estabelecimento)
    
    if form.process().accepted:
    	print(form.vars.id)
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','default',"cadastro_evento"))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Periodo():
    msg = "Cadastrar Periodo"

    db.Periodo.eve_id.writable = False
    form = SQLFORM(db.Periodo,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Proximo", _class='btn', _href=URL('evento','default',"cadastro_Lote",args=[request.args(0)]))])

    form.vars.eve_id = request.args(0, cast=int, otherwise=URL('home'))
    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Lote():
    msg = "Cadastrar Lote"

    db.Lote.eve_id.writable = False
    
    form = SQLFORM(db.Lote)

    form.vars.eve_id = request.args(0, cast=int, otherwise=URL('home'))
    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','default',"cadastro_Tags",args=[form.vars.eve_id]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def cadastro_Tags():
	msg = "Cadastrar Tags para o Evento"

	db.Tag_Evento.eve_id.writable = db.Tag_Evento.tag.writable = False	

	form = SQLFORM(db.Tag_Evento,buttons=[BUTTON('cadastrar', _type="submit"),
	A("Criar Tag", _class='btn', _href=URL('evento','default',"criar_Tag",args=[request.args(0)])),
	A("Finalizar", _class='btn', _href=URL('evento','default',"meus_eventos"))])

	form.vars.tag = "" #gambiarra
	form.vars.eve_id = request.args(0, cast=int, otherwise=URL('home'))

	if form.process().accepted:
		session.flash = 'Cadastro aceito!'  
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

@auth.requires_login()
@auth.requires_membership("Organizacao")
def criar_Tag():
    msg = "Criar Tag"

    form = SQLFORM(db.Tag)

    if form.process().accepted:
        session.flash = 'Cadastro aceito!'
        redirect(URL('evento','default',"cadastro_Tags",args=[request.args(0)]))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        response.flash = 'Preencha o formulário!'

    return dict(msg=msg,grid=form)


##mostra os eventos que o usuario comprou
##ou eventos criados pela organizacao
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
		db.Evento.participantes.writable = db.Evento.org_id.writable = False

		org = db(session.auth.user.id == db.Organizacao.usu_id).select().first()
		query = db.Evento.org_id == org.id 

		links = [dict(header='Avaliacao', body = avaliacao)]
		form = SQLFORM.grid(query,deletable=False,create=False,csv=False,user_signature=False,links=links)

	return dict(msg=msg,rows=form)

def valida(form):
	rows = db(db.Participacao).select(db.Participacao.cli_id,db.Participacao.eve_id)
	lista = rows.as_list()
	tupla = {"cli_id":form.vars.cli_id,"eve_id":form.vars.eve_id}
	if(tupla in lista):
		form.errors.cli_id = "Cliente ja cadastrado" 

@auth.requires_login()
@auth.requires_membership("usuario")
def comprar():
	msg = "Comprar Ticket para Evento"

	form = SQLFORM.factory(Field("CPF"),
		    Field("Cartao"),Field("Numero"),
			Field("Senha","password"),
			Field("eve_id","integer",writable=False),
			Field("cli_id","integer",writable=False))

	eve_id = request.args(0, cast=int, otherwise=URL('home'))
	form.vars.eve_id = eve_id

	Cli = db(db.Cliente.usu_id == session.auth.user.id).select().first()
	form.vars.cli_id = Cli.id

	if form.process(onvalidation =valida).accepted:
		session.flash = 'Compra realizada!'

		##insere na relacao participacao e atualiza os participantes
		pid = db.Participacao.insert(cli_id= Cli.id, eve_id= eve_id)

		row = db(db.Evento.id == eve_id).select(db.Evento.id,db.Evento.participantes).first()
		row.participantes = row.participantes + 1
		row.update_record()

		#insere na relacao ticket e atualiza o lote
		Lote = db(db.Lote.eve_id == eve_id and db.Lote.quantidade > 0).select().first()
		pid = db.Ticket.insert(cli_id=Cli.id,lot_id=Lote.id)

		Lote.quantidade = Lote.quantidade - 1
		Lote.update_record()

		redirect(URL('evento','default','meus_eventos'))

	elif form.errors:
		response.flash = 'Erros no formulário ou Cliente ja possui Cadastro!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,form=form)


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
		redirect(URL('evento','default','home'))

	db.Cliente.usu_id.writable = False
	form1 = SQLFORM(db.Cliente)

	#atribuindo o usu_id igual ao do usuario
	form1.vars.usu_id = session.auth.user.id

	if form1.process().accepted:
		session.flash = 'Cadastro aceito!'
		auth.add_membership(2, session.auth.user.id) #inseri no grupo de usuarios
		redirect(URL('evento','default','home'))
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
		redirect(URL('evento','default','home'))
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

	Cli = db(db.Cliente.usu_id == pid).select(db.Cliente.id).first()
	form = SQLFORM(db.Cliente,Cli.id)
	msg = "Cliente"
	return dict(msg=msg,grid=form.process())

@auth.requires_login()
@auth.requires_membership("Organizacao")
def organizacao():
	pid = session.auth.user.id

	db.Organizacao.id.readable = False
	db.Organizacao.usu_id.writable = db.Organizacao.eventos.writable = False
	Org = db(db.Organizacao.usu_id == pid).select(db.Organizacao.id).first()
	form = SQLFORM(db.Organizacao,Org.id)

	msg = "Organizacao"
	return dict(msg=msg,grid=form.process())


def avaliacao(row):
	query = db.Participacao.eve_id == row.id 
	rows = avaliacao = db(query).select(db.Participacao.avaliacao,db.Participacao.avaliou)

	avaliacao = 0
	for row in rows:
		if(row.avaliou): 
			avaliacao += row.avaliacao
	if(len(rows) > 0):
		avaliacao = avaliacao / len(rows)
	return round(avaliacao, 2)


#Relatorios
def clientes():
	form = SQLFORM.factory(Field("Cliente","integer",requires = IS_IN_DB(db,"Cliente.id")))
	msg = "Relatorios de Cliente"
	if(form.process().accepted):
		cli_id = str(form.vars.Cliente)
		count = db.executesql('SELECT Evento.id, sum( Participacao.avaliacao)/count( Participacao.id) FROM Participacao, Evento WHERE Participacao.cli_id = '+cli_id+' and Participacao.eve_id = Evento.id GROUP BY Evento.id')

		return dict(msg=msg,grid=count) 

	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid = form)

def tag():
	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
	
	msg = "Relatorio Tag"
	if(form.process().accepted):
		tag = str(form.vars.tag)
   		tag = '\''+tag+'\''
		info = db.executesql('SELECT s.org_id, s.first_name, count( Participacao.cli_id) FROM Participacao, (auth_user inner join (Organizacao inner join (Tag_Evento inner join Evento on Evento.id = Tag_Evento.eve_id) on Organizacao.id = org_id) on auth_user.id = usu_id) as s WHERE Participacao.eve_id = s.eve_id and s.tag = '+tag+' GROUP BY s.org_id;')
		return dict(msg=msg,grid=info)
	elif form.errors:
		response.flash = 'Erros no formulário!'
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

def tag2():
	form = SQLFORM.factory(Field("tag",requires = IS_IN_DB(db,"Tag.tag","%(tag)s")))
	
	msg = "Relatorio Tag"
	if(form.process().accepted):
		tag = db(db.Tag.tag == form.vars.tag).select().first()
		query = db.Evento.id == db.Tag_Evento.eve_id and tag.id == db.Tag_Evento.tag_id
		rows = db(query).select(db.Tag_Evento.eve_id,db.Tag_Evento.tag_id,db.Evento.participantes,
		join=db.Evento.on(db.Evento.id == db.Tag_Evento.eve_id),groupby=db.Evento.org_id)
	
		return dict(msg=msg,grid=rows)
	else:
		response.flash = 'Preencha o formulário!'

	return dict(msg=msg,grid=form)

def intervalo():
    return dict()




# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

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