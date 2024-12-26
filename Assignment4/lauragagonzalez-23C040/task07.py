# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/FacultadInformatica-LinkedData/Curso2024-2025-DataScience/blob/master/Assignment4/course_materials/notebooks/Task07.ipynb

**Task 07: Querying RDF(s)**
"""

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2024-2025/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO

ns = Namespace("http://somewhere#")
living_thing = ns.LivingThing
query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?subclass
WHERE {
  ?subclass rdfs:subClassOf <http://somewhere#LivingThing> .
}
"""
#for r in g.query(q1):
#  print(r)
for row in g.query(query):
    print(row.subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
person_class = ns.Person
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?individual
WHERE {
  {
    ?individual rdf:type <http://somewhere#Person> .
  } UNION {
    ?individual rdf:type ?subclass .
    ?subclass rdfs:subClassOf <http://somewhere#Person> .
  }
}
"""
# Visualize the results
for row in g.query(query):
    print(row.individual)

"""**TASK 7.3: List all individuals of just "Person" or "Animal". You do not need to list the individuals of the subclasses of person (in SPARQL only)**

"""

# TO DO
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?individual
WHERE {
  {
    ?individual rdf:type <http://somewhere#Person> .
  } UNION {
    ?individual rdf:type <http://somewhere#Animal> .
  }
}
"""
# Visualize the results
for row in g.query(query):
    print(row.individual)

"""**TASK 7.4:  List the name of the persons who know Rocky (in SPARQL only)**"""

# TO DO
from rdflib.namespace import RDF, RDFS, FOAF
g.namespace_manager.bind('foaf', FOAF)
query = """
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://somewhere#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person  ?name
WHERE {
  ?person rdf:type  ?type .
  ?type rdfs:subClassOf*  ns:Person .
  ?person foaf:knows ns:RockySmith .
  ?person vcard:FN ?name .
}
"""
# Visualize the results
for r in g.query(query):
    print(r.name)

"""**Task 7.5: List the name of those animals who know at least another animal in the graph (in SPARQL only)**"""

# TO DO
query = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
PREFIX ns: <http://somewhere#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?animalName
WHERE {
  ?animal rdf:type ?type.
  ?animal foaf:knows ?otherAnimal .
  ?otherAnimal rdf:type ?type .
  ?animal vcard:Given ?animalName .
}
"""

# Visualize the results
for row in g.query(query):
    print(row.animalName)

"""**Task 7.6: List the age of all living things in descending order (in SPARQL only)**"""

# TO DO
query = """
SELECT ?livingThing ?age
WHERE {
    ?livingThing rdf:type ?type .
    ?livingThing foaf:age ?age .
}
ORDER BY DESC(?age)
"""

for row in g.query(query):
    print(f"Living Thing: {row.livingThing}, Age: {row.age}")