# Template-struktur

  - index
  - auth
      - login, logout, register, forgot-password, reset-password
  - user
      - me
  - pages
      - about, privacy, accessability, contact, how-tos...
  - search/adv. search
  - resource
      - collection, entity, record...
        - core metadata, files, relations, series, thumbnails...
  - admin


# Et par indledende overvejelser.

Software:

Pluggy (https://pluggy.readthedocs.io/en/stable/):

https://kracekumar.com/post/build_plugins_with_pluggy/

https://dev.to/waylonwalker/a-minimal-pluggy-example-3mp0

Blinker (https://blinker.readthedocs.io/en/stable/)

Pyemitter (https://pypi.org/project/pymitter/)


Hooks/signals: 
before_entity_insert 
after_entity_insert 
after_entity_get 
before_entity_revert 
after_entity_revert 
before_entity_update 
after_entity_update 
after_entity_delete 

before_render_template (GUI-response) x
    context object / 

before_json_response (Data-response) 

before_search_query x
after_search_results x
before_next_results 

# Todo

Register: Man bliver altid verificeret. 
OK: redirect ikke til login når man forsøger at logge ind uden at det lykkes. 



token: 

dennis.iversen+asdf@gmail.com

Test token:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTM2MzA5YjMtYTY3YS00NDBhLTk0ZTctNDQzOTRkY2NhOGVlIiwiZW1haWwiOiJkZW5uaXMuaXZlcnNlbithc2RmQGdtYWlsLmNvbSIsImF1ZCI6ImZhc3RhcGktdXNlcnM6dmVyaWZ5IiwiZXhwIjoxNjc3NzQ3ODQyfQ.m-4Q-Ted2CS7x-nRuqVvrU5a5-227Yd05emkK4a_4Ew
