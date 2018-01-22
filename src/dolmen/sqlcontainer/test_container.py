# -*- coding: utf-8 -*-

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from dolmen.sqlcontainer import SQLContainer

Base = declarative_base()

configs = {
    'drivername': 'sqlite',
    'username': '',
    'password': '',
    'host': '',
    'port': 0,
    'database': ':memory:',
    'query': '',
}


class SomeClass(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50))


@pytest.fixture
def session_factory():
    engine = create_engine(URL(**configs))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield lambda: session
    Base.metadata.drop_all(bind=engine)


def test_container(session_factory):
    
    # We create the container
    container = SQLContainer(session_factory)
    container.model = SomeClass
    
    # We can now add content
    content = SomeClass(name='test')
    container.add(content)

    # We commit
    session = session_factory()
    session.commit()

    # The container should have some stuff for us now
    assert len(container) == 1

    # Get the key for URL building
    assert container.key_reverse(content) == '1'

    # Resolve the key from URL
    assert container.key_converter('1') == 1
    
    # getter
    item = container['1']  # using the id from an URL
    assert item == content

    item = container[1]  # using the id directly
    assert item == content
    
    # Iteration
    items = list(container)
    assert items == [content]

    # Deletion
    container.delete(content)
    assert len(container) == 0
