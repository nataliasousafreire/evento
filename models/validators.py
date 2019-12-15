#validacoes

db.Cliente.usu_id.requires = [IS_IN_DB(db,"auth_user.id"),IS_NOT_IN_DB(db,"Cliente.usu_id")]
db.Cliente.nascimento.requires = IS_NOT_EMPTY()
db.Cliente.sexo.requires = IS_IN_SET(['Masculino','Feminino','Outro'],zero=None)
db.Cliente.sexo.widget = SQLFORM.widgets.radio.widget
db.Cliente.nascimento.requires = IS_DATE(format='%d/%m/%Y')


db.Organizacao.usu_id.requires = [IS_IN_DB(db,"auth_user.id"),IS_NOT_IN_DB(db,"Organizacao.usu_id")]
db.Organizacao.descricao.requires = IS_NOT_EMPTY()

db.Estabelecimento.nome.requires = IS_NOT_EMPTY()
db.Estabelecimento.cep.requires = IS_NOT_EMPTY()
db.Estabelecimento.cep.requires = IS_NOT_IN_DB(db,"Estabelecimento.cep")
db.Estabelecimento.pais.requires = IS_NOT_EMPTY()
db.Estabelecimento.estado.requires = IS_NOT_EMPTY()
db.Estabelecimento.cidade.requires = IS_NOT_EMPTY()

db.Evento.org_id.requires = IS_IN_DB(db,"Organizacao.usu_id")
db.Evento.est_id.requires = IS_IN_DB(db,"Estabelecimento.id","%(nome)s")
db.Evento.titulo.requires = IS_NOT_EMPTY()
db.Evento.img.requires = IS_EMPTY_OR(IS_IMAGE())

db.Periodo.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Periodo.inicio.requires = IS_NOT_EMPTY()
db.Periodo.fim.requires = IS_NOT_EMPTY()
db.Periodo.fim.requires = IS_DATETIME(format='%d-%m-%y %H:%M:%S')
db.Periodo.inicio.requires = IS_DATETIME(format='%d-%m-%y %H:%M:%S')

db.Participacoes.cli_id.requires = IS_IN_DB(db,"Cliente.usu_id")
db.Participacoes.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")

db.Lote.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Lote.preco.requires = IS_NOT_EMPTY()
db.Lote.total.requires = IS_NOT_EMPTY()

db.Ticket.cli_id.requires = IS_IN_DB(db,"Cliente.usu_id")
db.Ticket.lot_id.requires = IS_IN_DB(db,"Lote.id")

db.Org_Est.org_id.requires = IS_IN_DB(db,"Organizacao.usu_id")
db.Org_Est.est_id.requires = IS_IN_DB(db,"Estabelecimento.id")

db.Tag.tag.requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,"Tag.tag")]

db.Eve_Tag.eve_id.requires = IS_IN_DB(db,"Evento.id","%(titulo)s")
db.Eve_Tag.tag.requires = IS_IN_DB(db,"Tag.tag","%(tag)s")

db.commit()
