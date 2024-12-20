# -*- coding: utf-8 -*-
"""Task09.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-G1OK8l78g03RSoMJ5iHD6K80yHQH7va

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
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
vcard=Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
d3=Namespace("http://data.three.org#")

q1 = prepareQuery('''
  SELECT ?Subject ?Family ?Given WHERE {
    ?Subject vcard:Given ?Given.
    ?Subject vcard:Family ?Family
  }
  ''',
  initNs = {"d3": d3 , "rdf": RDF , "vcard": vcard}
)


for r3 in g1.query(q1):
  print(r3.Subject, ' ', r3.Family , ' ', r3.Given)

result_3 = g1.query(q1)
for r3 in result_3:
  print(r3.Subject, ' ', r3.Family , ' ', r3.Given)

result_4 = g2.query(q1)
for r4 in result_4:
  print(r4.Subject, ' ', r4.Family , ' ', r4.Given)

owl = Namespace("http://www.w3.org/2002/07/owl#")
# OWL:sameAs

for t4 in result_4:
  for t3 in result_3:
    if t4[1] == t3[1] and t4[2] == t3[2]:
      g3.add((t4[0], owl.sameAs, t3[0]))

# Sacamos el resultado
for t in g3:
  print(t)