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
    name = Column(String(50))


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

    # Location
    assert item.__parent__ == container
    assert item.__name__ == '1'  # URL friendly

    # Iteration
    items = list(container)
    assert items == [content]

    # Add another item
    content2 = SomeClass(name='another test')
    container.add(content2)
    session.commit()

    # Slices
    items = list(container.slice(0, 1))
    assert len(items) == 1
    assert items[0] == content

    items = list(container.slice(0, 2))
    assert len(items) == 2
    assert items == [content, content2]

    # Deletion
    container.delete(content)
    assert len(container) == 1

    container.delete(content2)
    assert len(container) == 0
