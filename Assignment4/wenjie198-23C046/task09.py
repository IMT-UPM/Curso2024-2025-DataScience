# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yHAfA-b0CHhAcKpJRayCtYAI8FYrJrnR

**Task 09: Data linking**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials/"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

from rdflib.plugins.sparql import prepareQuery
from rdflib import RDF, RDFS

q1 = prepareQuery("""
  SELECT ?individuo
  WHERE {
    ?clase rdf:type rdfs:Class .
    ?individuo rdf:type ?clase
  }
""",
                  initNs={"rdf":RDF, "rdfs":RDFS})


print("Individuos de g1:")
for r in g1.query(q1):
  print(r)

print("\nIndividuos de g2:")
for r in g2.query(q1):
  print(r)

datat = Namespace("http://data.three.org/#")
dataf = Namespace("http://data.four.org/#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
owl = Namespace("http://www.w3.org/2002/07/owl#")

g3.namespace_manager.bind("datat", datat)
g3.namespace_manager.bind("dataf", dataf)
g3.namespace_manager.bind("vcard", vcard)
g3.namespace_manager.bind("owl", owl)

for s1, p, apodo1 in g1.triples((None, vcard.Given, None)):
  family1 = g1.value(s1, vcard.FN)
  for s2, p, apodo2 in g2.triples((None, vcard.Given, None)):
    if apodo1 == apodo2:
      family2 = g2.value(s2, vcard.FN)
      if family1 == family2:
        g3.add((s1, owl.sameAs, s2))

print(g3.serialize(format = "ttl"))