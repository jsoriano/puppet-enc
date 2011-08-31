from sqlalchemy import Integer, ForeignKey, String, Column, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, object_session

#from sqlalchemy import create_engine
#engine = create_engine('sqlite:///:memory:', echo=True)
#from sqlalchemy.orm import sessionmaker
#session = sessionmaker(engine)()

Base = declarative_base()

host_groups = Table('host_group', Base.metadata,
    Column('host_id', Integer, ForeignKey('host.id'), primary_key=True, nullable=False),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True, nullable=False),
)

group_classes = Table('group_class', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True, nullable=False),
    Column('class_id', Integer, ForeignKey('class.id'), primary_key=True, nullable=False),
)

class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    groups = relation('Group', secondary=host_groups)

    def _get_classes(self):
        classes = []
        for group in self.groups:
            classes += group.classes
        return classes
    classes = property(_get_classes)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    classes = relation('Class', secondary=group_classes)

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
