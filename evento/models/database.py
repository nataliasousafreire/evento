#Definicao do schema

db.define_table("Cliente",
			    Field("usu_id","reference auth_user",unique=True,notnull=True,label= "Usuario"),
			    Field("nascimento","date",notnull=True,label = "Data de nascimento"),
			    Field("sexo","string",length = 1,label = "Sexo"),
			    Field("profissao","string",length = 50,label = "Profissão"),
			   )


db.define_table("Organizacao",
				Field("usu_id","reference auth_user",unique=True,notnull=True,label= "Usuario"),
				Field("eventos","integer",default = 0,label = "Eventos realizados"),
				Field("descricao","text",notnull=True,length = 1000,label = "Descrição"),
				Field("site","string",length = 30,label = "Site"),
				Field("avaliacao","decimal(3,1)",default = 0.0,label= "Avaliação")
			   )

db.define_table("Estabelecimento",
				Field("nome","string",notnull=True,length = 30,label="Nome"),
				Field("cep","string",notnull=True,unique=True,length = 8,label ="CEP"),
				Field("pais","string",notnull=True,length = 30,label ="Pais"),
				Field("estado","string",notnull=True,length = 2,label="Estado(sigla)"),
				Field("cidade","string",notnull=True,length = 30,label="Cidade")
			   )

db.define_table("Evento",
				Field("org_id", "reference Organizacao",notnull=True,label="Organizacao"),
				Field("est_id", "reference Estabelecimento",notnull=True,label = "Estabelecimento"),
				Field("img","upload",label="Imagem"),
				Field("titulo","string",notnull=True,length = 50,label="Titulo"),
				Field("descricao","text",length = 1000,label="Descrição"),
				Field("avaliacao","decimal(3,1)",default = 0.0,label="Avaliação"),
				Field("participantes","integer",default = 0,label= "Total Participantes"),
				auth.signature
			   )

db.define_table("Periodo",
				Field("inicio","datetime",notnull=True,label = "Inicio"),
				Field("fim","datetime",notnull=True,label = "Termino"),
				Field("eve_id","reference Evento",notnull=True,label = "Evento"),
				)

db.define_table("Participacoes",
				Field("cli_id","reference Cliente",notnull=True,label = "Usuario"),
				Field("eve_id","reference Evento",notnull=True,label= "Evento"),
				Field("avaliacao","decimal(3,1)",default = 0.0,label = "Avaliação"),
				Field("avaliou","boolean",default=False,label="Avaliou"),
				)

db.define_table("Lote",
				Field("eve_id","reference Evento",notnull=True,label="Evento"),
				Field("preco","double",notnull=True,default = 0.0,label="Preço"),
				Field("total","integer",notnull=True,label="Total"),
				Field("quantidade",compute = lambda L: L["total"]),
				auth.signature
				)

db.define_table("Ticket",
				Field("cli_id","reference Cliente",notnull=True,label="Usuario"),
				Field("lot_id","reference Lote",notnull=True,label ="Estabelecimento")
				)
				
db.define_table("Org_Est",
				Field("org_id","reference Organizacao",notnull=True,label = "Organizacao"),
				Field("est_id","reference Estabelecimento",notnull=True,label="Estabelecimento"),
				)

db.define_table("Tag",
				Field("tag","string",notnull=True,length = 30,label="Tag"),
				auth.signature
				)

db.define_table("Eve_Tag",
				Field("tag_id","reference Tag",notnull=True),
				Field("tag","string",notnull=True,length = 30),
				Field("eve_id","reference Evento",notnull=True,label="Evento")
			    )


#db.auth_group.truncate()
#auth.add_group('admin', 'pode fazer qualquer coisa')
#auth.add_group('usuario', 'acesso restrito nas funções importantes, nao pode criar ou modificar eventos\
#				,pode comprar Tickets para eventos e avaliar')
#auth.add_group('Organizacao', 'acesso restrito nas funções importantes, pode criar e modificar eventos,\
#				nao pode comprar ingressos')

#auth.enable_record_versioning(db)