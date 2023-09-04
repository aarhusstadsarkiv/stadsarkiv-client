from stadsarkiv_client.core.logging import get_log
import typing

log = get_log()

settings_facets: dict[str, typing.Any] = {
    "content_types": {
        "label": "Materialetype",
        "multiple": True,
        "hierarchical": True,
        "content": [
            {"id": "99", "label": "Andet materiale"},
            {
                "children": [
                    {
                        "id": "66",
                        "icon": "far fa-image",
                        "label": "Afbildning af arkitektur og bygning",
                    },
                    {
                        "id": "65",
                        "icon": "far fa-image",
                        "label": "Afbildning af kunst",
                    },
                    {"id": "73", "icon": "far fa-image", "label": "Arkitekturtegning"},
                    {
                        "id": "64",
                        "icon": "far fa-image",
                        "label": "By- og gadebilleder",
                    },
                    {"id": "70", "icon": "far fa-image", "label": "Collage"},
                    {"id": "71", "icon": "far fa-image", "label": "Illustrationer"},
                    {
                        "id": "100",
                        "icon": "far fa-image",
                        "label": "Landskabs- og naturbilleder",
                    },
                    {"id": "62", "icon": "far fa-image", "label": "Luftfoto"},
                    {"id": "68", "icon": "far fa-image", "label": "Maleri"},
                    {"id": "67", "icon": "far fa-image", "label": "Plakat"},
                    {"id": "69", "icon": "far fa-image", "label": "Planche"},
                    {"id": "63", "icon": "far fa-image", "label": "Portræt"},
                    {"id": "74", "icon": "far fa-image", "label": "Postkort"},
                    {"id": "72", "icon": "far fa-image", "label": "Tekniske tegninger"},
                ],
                "id": "61",
                "icon": "far fa-image",
                "label": "Billeder",
            },
            {
                "children": [
                    {"id": "98", "icon": "fas fa-laptop", "label": "Hjemmesider"},
                    {"id": "96", "icon": "fas fa-laptop", "label": "Software"},
                    {"id": "97", "icon": "fas fa-laptop", "label": "Spil"},
                ],
                "id": "95",
                "icon": "fas fa-laptop",
                "label": "Elektronisk materiale",
            },
            {
                "children": [
                    {
                        "description": "Skøder, pantebreve, forpagtningskontrakter, m.m.",
                        "id": "13",
                        "icon": "fas fa-gavel",
                        "label": "Ejendomspapirer",
                    },
                    {"id": "12", "icon": "fas fa-gavel", "label": "Kontrakter"},
                    {"id": "16", "icon": "fas fa-gavel", "label": "Love og cirkulærer"},
                    {"id": "15", "icon": "fas fa-gavel", "label": "Regulativer"},
                    {"id": "11", "icon": "fas fa-gavel", "label": "Retningslinier"},
                    {
                        "id": "17",
                        "icon": "fas fa-gavel",
                        "label": "Standarder og specifikationer",
                    },
                    {"id": "14", "icon": "fas fa-gavel", "label": "Vedtægter"},
                ],
                "id": "10",
                "icon": "fas fa-gavel",
                "label": "Forskrifter og vedtægter",
            },
            {
                "children": [
                    {"id": "5", "icon": "far folder-open", "label": "Borgersager"},
                    {
                        "id": "2",
                        "icon": "far folder-open",
                        "label": "Bygge- og ejendomssager",
                    },
                    {
                        "id": "8",
                        "icon": "far folder-open",
                        "label": "By- og lokalplaner",
                    },
                    {
                        "id": "7",
                        "icon": "far folder-open",
                        "label": "Byråds- og udvalgssager",
                    },
                    {"id": "4", "icon": "far folder-open", "label": "Emnesager"},
                    {"id": "9", "icon": "far folder-open", "label": "Kommunalplaner"},
                    {"id": "6", "icon": "far folder-open", "label": "Personalesager"},
                    {
                        "id": "3",
                        "icon": "far folder-open",
                        "label": "Vej og område, kulturmiljøsager",
                    },
                ],
                "id": "1",
                "icon": "far folder-open",
                "label": "Kommunale sager og planer",
            },
            {
                "children": [
                    {"id": "80", "icon": "far fa-map", "label": "Diagram"},
                    {"id": "76", "icon": "far fa-map", "label": "Matrikelkort"},
                    {"id": "79", "icon": "far fa-map", "label": "Tekniske kort"},
                    {"id": "77", "icon": "far fa-map", "label": "Topografiske kort"},
                    {"id": "78", "icon": "far fa-map", "label": "Økonomiske kort"},
                ],
                "id": "75",
                "icon": "far fa-map",
                "label": "Kortmateriale",
            },
            {
                "description": "upubliceret",
                "children": [
                    {
                        "description": "upubliceret",
                        "id": "51",
                        "icon": "far file-alt",
                        "label": "Afhandlinger og disputatser",
                    },
                    {
                        "description": "upubliceret",
                        "id": "53",
                        "icon": "far file-alt",
                        "label": "Eksamensopgaver",
                    },
                    {
                        "description": "upubliceret",
                        "id": "50",
                        "icon": "far file-alt",
                        "label": "Erindringer og dagbøger",
                    },
                    {
                        "description": "upubliceret",
                        "id": "52",
                        "icon": "far file-alt",
                        "label": "Forelæsningspapirer og -noter",
                    },
                    {
                        "description": "upubliceret",
                        "id": "56",
                        "icon": "far file-alt",
                        "label": "Håndbøger og manualer",
                    },
                    {
                        "description": "upubliceret, email, chat, breve, interviews",
                        "id": "60",
                        "icon": "far file-alt",
                        "label": "Korrespondance",
                    },
                    {
                        "description": "upubliceret, skudsmålsbøger, eksamenspapirer, anbefalinger, attester, m.m.",
                        "id": "58",
                        "icon": "far file-alt",
                        "label": "Personlige papirer",
                    },
                    {
                        "description": "upubliceret, arkivalske registranter",
                        "id": "59",
                        "icon": "far file-alt",
                        "label": "Registranter",
                    },
                    {
                        "description": "upubliceret, festtaler, oratoriske taler, politiske taler m.m.",
                        "id": "54",
                        "icon": "far file-alt",
                        "label": "Taler",
                    },
                    {
                        "description": "upubliceret",
                        "id": "57",
                        "icon": "far file-alt",
                        "label": "Tweets, online posts, blogs",
                    },
                    {
                        "description": "upubliceret",
                        "id": "55",
                        "icon": "far file-alt",
                        "label": "Udklip og småtryk",
                    },
                ],
                "id": "49",
                "icon": "far file-alt",
                "label": "Manuskripter",
            },
            {
                "description": "tv, radio og internet",
                "children": [
                    {
                        "description": "tv, radio og internet",
                        "id": "93",
                        "icon": "fas fa-film",
                        "label": "Animation",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "89",
                        "icon": "fas fa-film",
                        "label": "Dokumentarer",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "90",
                        "icon": "fas fa-film",
                        "label": "Eksperimental videokunst",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "92",
                        "icon": "fas fa-film",
                        "label": "Fiktion og kortfilm",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "91",
                        "icon": "fas fa-film",
                        "label": "Magasin- og nyhedsprogrammer",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "94",
                        "icon": "fas fa-film",
                        "label": "Oplæsninger",
                    },
                    {
                        "description": "tv, radio og internet",
                        "id": "88",
                        "icon": "fas fa-film",
                        "label": "Reportager",
                    },
                ],
                "id": "87",
                "icon": "fas fa-film",
                "label": "Medieproduktioner",
            },
            {
                "children": [
                    {"id": "86", "label": "Ikke-musikalsk lyd"},
                    {"id": "85", "label": "Live-opførelser"},
                    {"id": "82", "label": "Musikudgivelser"},
                    {"id": "83", "label": "Noder"},
                    {"id": "84", "label": "Sange og salmer"},
                ],
                "id": "81",
                "label": "Musik og lydoptagelser",
            },
            {
                "children": [
                    {
                        "description": "inkl. anmeldelser, nekrologer, opiniods, m.m.",
                        "id": "41",
                        "icon": "fas fa-book",
                        "label": "Artikler og essays",
                    },
                    {
                        "description": "inkl. diskografi, filmografi og andre værkfortegnelse",
                        "id": "40",
                        "icon": "fas fa-book",
                        "label": "Bibliografier",
                    },
                    {
                        "id": "44",
                        "icon": "fas fa-book",
                        "label": "Detailkataloger, reklamer, propaganda",
                    },
                    {"id": "37", "icon": "fas fa-book", "label": "Faglitteratur"},
                    {
                        "description": "Vejvisere, telefonbøger, m.m.",
                        "id": "46",
                        "icon": "fas fa-book",
                        "label": "Fortegnelser",
                    },
                    {
                        "id": "45",
                        "icon": "fas fa-book",
                        "label": "Kataloger og programmer for diverse",
                    },
                    {
                        "id": "47",
                        "icon": "fas fa-book",
                        "label": "Nyhedsbreve og medlemsblade",
                    },
                    {"id": "43", "icon": "fas fa-book", "label": "Pjecer, pamfletter"},
                    {"id": "48", "icon": "fas fa-book", "label": "Rapporter"},
                    {
                        "description": "encyklopædier, ordbøger, m.m.",
                        "id": "39",
                        "icon": "fas fa-book",
                        "label": "Reference- og opslagsværker",
                    },
                    {
                        "description": "inkl. autobiografier",
                        "id": "38",
                        "icon": "fas fa-book",
                        "label": "Skønlitteratur, dramatik og poesi",
                    },
                    {
                        "description": "magasiner, årspublikationer, periodica, m.m.",
                        "id": "42",
                        "icon": "fas fa-book",
                        "label": "Tidsskrifter og aviser",
                    },
                ],
                "id": "36",
                "icon": "fas fa-book",
                "label": "Publikationer",
            },
            {
                "children": [
                    {
                        "id": "27",
                        "icon": "fab fa-leanpub",
                        "label": "Andre registre og protokoller",
                    },
                    {
                        "id": "22",
                        "icon": "fab fa-leanpub",
                        "label": "Brandtaksationsprotokoller",
                    },
                    {
                        "description": "Lister, medlemsfortegnelser, adressefortegnelser, navnelister, m.m.",
                        "id": "28",
                        "icon": "fab fa-leanpub",
                        "label": "Diverse fortegnelser",
                    },
                    {
                        "id": "20",
                        "icon": "fab fa-leanpub",
                        "label": "Dødsattester og -journaler",
                    },
                    {"id": "24", "icon": "fab fa-leanpub", "label": "Folketællinger"},
                    {"id": "25", "icon": "fab fa-leanpub", "label": "Kirkebøger"},
                    {
                        "id": "19",
                        "icon": "fab fa-leanpub",
                        "label": "Mødereferater og forhandlingsprotokoller",
                    },
                    {"id": "23", "icon": "fab fa-leanpub", "label": "Realregistre"},
                    {
                        "id": "21",
                        "icon": "fab fa-leanpub",
                        "label": "Skattemandtalslister",
                    },
                    {
                        "id": "26",
                        "icon": "fab fa-leanpub",
                        "label": "Skifteprotokoller",
                    },
                ],
                "id": "18",
                "icon": "fab fa-leanpub",
                "label": "Registre og protokoller",
            },
            {
                "children": [
                    {"id": "34", "icon": "far chart-bar", "label": "Database"},
                    {
                        "id": "31",
                        "icon": "far chart-bar",
                        "label": "Regnskaber og budgetmateriale",
                    },
                    {
                        "id": "30",
                        "icon": "far chart-bar",
                        "label": "Spørgeskemaundersøgelser",
                    },
                    {
                        "id": "32",
                        "icon": "far chart-bar",
                        "label": "Statistisk materiale",
                    },
                    {
                        "id": "33",
                        "icon": "far chart-bar",
                        "label": "Statistisk undersøgelse",
                    },
                    {"id": "35", "icon": "far chart-bar", "label": "Tabelværk"},
                ],
                "id": "29",
                "icon": "far chart-bar",
                "label": "Statistisk og økonomisk materiale",
            },
        ],
    },
    "subjects": {
        "label": "Emnekategori",
        "multiple": True,
        "hierarchical": True,
        "content": [
            {
                "id": "17",
                "label": "Erhverv",
                "children": [
                    {
                        "id": "53",
                        "label": "Banker og Sparekasser",
                    },
                    {
                        "id": "14",
                        "label": "Detailhandel og service",
                    },
                    {
                        "id": "13",
                        "label": "Fagforeninger",
                    },
                    {
                        "id": "66",
                        "label": "Fiskeri og jagt",
                    },
                    {
                        "id": "15",
                        "label": "Håndværk og industri",
                    },
                    {
                        "id": "57",
                        "label": "Kooperation",
                    },
                    {
                        "id": "54",
                        "label": "Kost og logi",
                    },
                    {
                        "id": "16",
                        "label": "Land- og skovbrug",
                    },
                    {
                        "id": "55",
                        "label": "Turistvæsen",
                    },
                ],
            },
            {
                "id": "29",
                "label": "Historiske perioder og temaer",
                "children": [
                    {
                        "id": "4",
                        "label": "Myter og sagn",
                    },
                    {
                        "id": "28",
                        "label": "Oldtid",
                    },
                    {
                        "id": "51",
                        "label": "Vikingetiden",
                    },
                    {
                        "id": "30",
                        "label": "Indtil 1536",
                    },
                    {
                        "id": "72",
                        "label": "1536-1660",
                    },
                    {
                        "id": "69",
                        "label": "1660-1814",
                    },
                    {
                        "id": "68",
                        "label": "Det 19. århundrede",
                    },
                    {
                        "id": "31",
                        "label": "Det 20. århundrede",
                    },
                    {
                        "id": "70",
                        "label": "Besættelsen",
                    },
                    {
                        "id": "7",
                        "label": "Det 21. århundrede",
                    },
                ],
            },
            {
                "id": "37",
                "label": "Kultur og fritid",
                "children": [
                    {
                        "id": "34",
                        "label": "Arkitektur",
                    },
                    {
                        "id": "33",
                        "label": "Arrangementer og festtraditioner",
                    },
                    {
                        "id": "56",
                        "label": "Folkekultur og dagligdagsliv",
                    },
                    {
                        "id": "35",
                        "label": "Forlystelser, spil og idræt",
                    },
                    {
                        "id": "76",
                        "label": "Kulturinstitutioner",
                    },
                    {
                        "id": "74",
                        "label": "Kunst og litteratur",
                    },
                    {
                        "id": "73",
                        "label": "Mad og drikke",
                    },
                    {
                        "id": "36",
                        "label": "Musik",
                    },
                    {
                        "id": "75",
                        "label": "Skulpturer og offentlig kunst",
                    },
                    {
                        "id": "1",
                        "label": "Teater, film, radio og tv",
                    },
                ],
            },
            {
                "id": "62",
                "label": "Natur",
                "children": [
                    {
                        "id": "59",
                        "label": "Kilder",
                    },
                    {
                        "id": "58",
                        "label": "Skove",
                    },
                    {
                        "id": "61",
                        "label": "Strand og bugt",
                    },
                    {
                        "id": "60",
                        "label": "Søer",
                    },
                    {
                        "id": "12",
                        "label": "Åer og bække",
                    },
                ],
            },
            {
                "id": "42",
                "label": "Personer",
                "children": [
                    {
                        "id": "39",
                        "label": "Arkitekter og bygmestre",
                    },
                    {
                        "id": "38",
                        "label": "Embedsmænd",
                    },
                    {
                        "id": "41",
                        "label": "Erhvervsfolk",
                    },
                    {
                        "id": "21",
                        "label": "Gejstlige",
                    },
                    {
                        "id": "40",
                        "label": "Historiske personer",
                    },
                    {
                        "id": "22",
                        "label": "Journalister og pressefotografer",
                    },
                    {
                        "id": "19",
                        "label": "Kulturpersoner",
                    },
                    {
                        "id": "18",
                        "label": "Politikere",
                    },
                    {
                        "id": "20",
                        "label": "Undervisere og forskere",
                    },
                ],
            },
            {
                "id": "3",
                "label": "Samfund",
                "children": [
                    {
                        "id": "71",
                        "label": "Beskæftigelse og arbejdsløshed",
                    },
                    {
                        "id": "5",
                        "label": "Bolig, byggeri og byplanlægning",
                    },
                    {
                        "id": "47",
                        "label": "Foreninger",
                    },
                    {
                        "id": "44",
                        "label": "Kommunal forvaltning",
                    },
                    {
                        "id": "43",
                        "label": "Kommunikation og medier",
                    },
                    {
                        "id": "6",
                        "label": "Lovgivning og jura",
                    },
                    {
                        "id": "45",
                        "label": "Militær",
                    },
                    {
                        "id": "27",
                        "label": "Penge og økonomi",
                    },
                    {
                        "id": "24",
                        "label": "Politi, brand og redning",
                    },
                    {
                        "id": "23",
                        "label": "Politik",
                    },
                    {
                        "id": "46",
                        "label": "Religion og kirke",
                    },
                    {
                        "id": "25",
                        "label": "Socialpolitik og velfærd",
                    },
                    {
                        "id": "67",
                        "label": "Sundhedsvæsen",
                    },
                    {
                        "id": "64",
                        "label": "Trafik og transport",
                    },
                    {
                        "id": "53",
                        "label": "Ud- og indvandring",
                    },
                    {
                        "id": "26",
                        "label": "Undervisning og uddannelse",
                    },
                    {
                        "id": "65",
                        "label": "Videnskab og forskning",
                    },
                ],
            },
            {
                "id": "9",
                "label": "Steder",
                "children": [
                    {
                        "id": "8",
                        "label": "Byer og bydele",
                    },
                    {
                        "id": "10",
                        "label": "Ejendomme og bygningsværker",
                    },
                    {
                        "id": "52",
                        "label": "Gader og veje",
                    },
                    {
                        "id": "49",
                        "label": "Kirker",
                    },
                    {
                        "id": "48",
                        "label": "Parker og anlæg",
                    },
                    {
                        "id": "11",
                        "label": "Slotte og herregårde",
                    },
                    {
                        "id": "50",
                        "label": "Sogne",
                    },
                    {
                        "id": "32",
                        "label": "Torve og pladser",
                    },
                ],
            },
            {
                "id": "2",
                "label": "Andet",
            },
        ],
    },
    "availability": {
        "label": "Tilgængelighed",
        "multiple": False,
        "hierarchical": False,
        "content": [
            {
                "id": "2",
                "label": "På magasin",
            },
            {
                "id": "3",
                "label": "Kan ses på læsesalen",
            },
            {
                "id": "4",
                "label": "Kan ses online",
            },
        ],
    },
    "usability": {
        "label": "Brug af materialer",
        "multiple": False,
        "hierarchical": False,
        "content": [
            {
                "id": "1",
                "label": "I offentlig eje",
            },
            {
                "id": "2",
                "label": "CC Navngivelse",
            },
            {
                "id": "3",
                "label": "CC Navngivelse-IkkeKommerciel",
            },
            {
                "id": "4",
                "label": "Alle rettigheder forbeholdes",
            },
        ],
    },
}
