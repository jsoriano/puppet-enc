# Copyright (c) 2011 Tuenti Technologies
# See LICENSE for details

from sqlalchemy import Integer, ForeignKey, String, Column, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, object_session

Base = declarative_base()

node_groups = Table('node_group', Base.metadata,
    Column('node_id', Integer, ForeignKey('node.id'), primary_key=True, nullable=False),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True, nullable=False),
)

group_modules = Table('group_module', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True, nullable=False),
    Column('module_id', Integer, ForeignKey('module.id'), primary_key=True, nullable=False),
)

class Node(Base):
    __tablename__ = 'node'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    groups = relation('Group', secondary=node_groups)

    def _get_modules(self):
        # TODO: Very optimizable
        modules = []
        for group in self.groups:
            modules += group.modules
        return sorted(set(modules))
    modules = property(_get_modules)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    modules = relation('Module', secondary=group_modules)

class Module(Base):
    __tablename__ = 'module'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
