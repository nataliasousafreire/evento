# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'home'), []),
    (T('Meus Eventos'), False, URL('default', 'meus_eventos'), []),
    (T('Criar Evento'), False, URL('default', 'criar_evento'), []),
    (T('Meus Perfil'), False, URL('default', 'user', 'profile'), [])
]

