# klient-generator. 

"Hvad der skal gøres, hvornår det skal gøres, hvad hver trin eller milepæl afhænger af" 

1. Ordrer
   1. Datamodel
      1. "orders". Ny tabel.  
      2. "records" (Arkivalier). Husk at placering skal fremgå af den enkelte 'record' (arkivalie). 
   2. Endpoints (API - webservice)
      1. GET /orders - kræver "admin". Skal hente alle brugerens ordrer. 
      2. PUT/DELETE /orders/{id} - kræver "admin". Opdater eller slet en ordre. 
      3. GET /users/me/orders - kræver "user". Hent alle aktive ordrer.
         1. Klient: /user/orders. Vis brugerens ordrer.  
      4. DELETE /users/me/orders/{order_id}
         1. Klient: /user/orders/delete/{id}
   3. Adgangskontrol
      1. Test af adgangskontrol. Benyt "endpoints" og brugere. 
   4. Mail-funktioner
      1. Konfirmations-mail vedrørende bestilling til brugerne
      2. Statusændrings-mail angående bestilling til brugerne
   5. GUI-elementer (brugere):
      1. Tabel med ordrer på profil-side, desuden slet funktion
   6. GUI-elementer (admin):
      1. Tabel med alle ordrer på "admin" side, incl. "update", "delete", "filter", "sort" funktionalitet. 

2. Brugere
   1. Endpoints
      1. Mangler endpoint til at slette "rettigheder". Vi kan oprette rettigheder
      2. Endpoint til at slette bruger for admin
      3. Endpoint til at slette bruger for brugeren
   3. FLyt brugere til nyt system. 
      1. FLyt bookmarks
      2. FLyt søgeresultater. 

3. Entiteter
   1. Flytning af entiteter (Afventer denne i første omgang)
   2. Mulighed for at rette entiteter. 

4. GUI elementer på aarhusarkiv v2.
   1. Aarhus Arkivet
      1. OK Tjek om elementer er identiske med eksisterende arkiv.
         1. Opret automatisk test til dette. 
      2. Manglende sider
         1. OK Forside.
         2. OK. Undersider
            1. OK Vejledning
            2. OK Om samlingerne
            3. OK Og andre. 
      3. Footer
         1. OK Kopiere "footer" information.
         2. OK Link til nyhedsbrev
      4. OK Logo
   2. Teater Arkivet
      1. OK "Add / Edit / Delete" relationer
      2. GUI-elements
         1. OK Tjek om sidernes elementer er identiske i forhold til eksisterende arkiv
            1. Automatisk test af dette.

5. Servere.
   1. Udvikling
      1. OK client.openaws.dk (aarhusarkivet)
      2. OK teater.openaws.dk (teaterarkivet)
         1. Opret ny demo. DNS opsætning. 
   2. Produktion
      1. aarhusarkivet.dk
      2. Find domæne navn til teaterarkivet. Fx: teater.aarhusarkivet.dk

6. E-mail
   1. DNS opsætning. Fix afsendelse af e-mails 
      1. OK Se: Opsætning "spf-dkim-dmarc" (https://www.brevo.com/blog/understanding-spf-dkim-dmarc/)