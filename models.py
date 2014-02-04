from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo
from uuid import uuid4

# class Scenario(StructuredNode):
#    uid = StringProperty(unique_index=True, default=uuid4)
#    measure = RelationshipTo('Measure', 'MEASURED_BY')

class Intent(StructuredNode):
    uid = StringProperty(unique_index=True, default=uuid4)
    title = StringProperty(required=True)
    description = StringProperty()

    measure = RelationshipTo('Measure', 'MEASURED_BY')

class Measure(StructuredNode):
    uid = StringProperty(unique_index=True, default=uuid4)
    title = StringProperty(required=True)
    description = StringProperty()

    # @property
    # def id(self):
    #   return self.__node__._id

# from py2neo import neo4j, ogm

# class Intent(object):

#     def __init__(self, title=None, description=None):
#         self.title = title
#         self.description = description

#     def __str__(self):
#         return self.title

# class Measure(Node):

#     element_type = "measure"

#     name = String(nullable=False)

# class MeasuredBy(Relationship):

#     label = "measured by"

#     created = DateTime(default=current_datetime, nullable=False)