# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mEZMX6Y1Vr4PdIcVm5667NZVQXxvafmi

**Task 06: Modifying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""Read the RDF file as shown in class"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph() # Creamos un grafo y asignamos namespaces
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class)) # Sujeto = Researcher + predicado = type + Objeto = Class (vocabulario)
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**

"""

ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDFS.subClassOf , ns.Person))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smithers"**"""

ns = Namespace("http://somewhere#")                   # Estoy creando datos con # y no con /
g.add((ns.JaneSmithers, RDF.type, ns.Researcher))     # sujeto JaneSmithers + predicado = type + objeto = Researcher

for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmithers the email address, fullName, given and family names. Use the https://schema.org vocabulary**"""

# # - para tautologia = vocabulario
# / - para datos

SCHEMA = Namespace("https://schema.org/")

g.add((ns.JaneSmithers, SCHEMA.email, Literal("jane.smithers@example.com")))  # Dirección de correo electrónico
g.add((ns.JaneSmithers, SCHEMA.name, Literal("Jane Smithers")))        # Nombre completo
g.add((ns.JaneSmithers, SCHEMA.givenName, Literal("Jane")))            # Nombre de pila
g.add((ns.JaneSmithers, SCHEMA.familyName, Literal("Smithers")))       # Apellido
for s,p,o in g.triples((ns.JaneSmithers, None, None)):
  print(s, p, o)

"""**TASK 6.5: Add UPM as the university where John Smith works. Use the "https://example.org/ namespace**"""

EXAMPLE = Namespace("https://example.org/")
vcard=Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
# EXAMPLE = Namespace("https://example.org#")
g.add((EXAMPLE.UPM, RDF.type, ns.University))           # sumeto = UPM + predicado = type + objeto = University
g.add((EXAMPLE.UPM, vcard.FN, Literal("Universidad Politecnica de Madrid")))    # sumeto = EXAMPLE.UPM + predicado = ns.FN + objeto = Universidad Politecnica de Madrid
g.add((ns.JohnSmith, ns.worksAt, EXAMPLE.UPM))  # sumeto = ns.JohnSmith+ predicado = EXAMPLE.whereworks + objeto = EXAMPLE.UPM

for s, p, o in g.triples((ns.JohnSmith, ns.works, None)):
    print(s, p, o)

from rdflib.plugins.sparql import prepareQuery


NS = Namespace("http://somewhere#")


q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject ns:worksAt example:UPM.
  }
  ''',
  initNs = { "ns": NS , "example":EXAMPLE}
)


for r in g.query(q1):
  print(r.Subject)

"""**Task 6.6: Add that Jown knows Jane using the FOAF vocabulary. Make sure the relationship exists.**"""

from rdflib.namespace import FOAF

g.add((ns.JohnSmith, FOAF.knows, ns.JaneSmith))

for s, p, o, in g.triples((None, FOAF.knows, None)):
  print (s,p,o)