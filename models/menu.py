# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'home'), []),
    (T('Meus Eventos'), False, URL('default', 'meus_eventos'), []),
    (T('Criar Evento'), False, URL('default', 'cadastro_evento'), []),
    (T('Meus Perfil'), False, URL(), [
    	(T('Usuario'), False, URL('default', 'user', 'profile'), []),
   		(T('Cliete'), False, URL('default', 'cliente'), []),
   		(T('Organizacao'), False, URL('default', 'organizacao'), [])
    	]),

    
    (T('Relatorios'), False, URL(),[
    	(T('Relatorio Tags'), False, URL('default', 'tag'), []),
    	(T('Relatorio Clientes'), False, URL('default', 'cliente'), []),
    	(T('Relatorio Intervalos'), False, URL('default', 'intevalo'), [])
    	])
]

