# -*- coding: utf-8 -*-

import crom
import dolmen.message

from crom import testing
from cromlech.browser import setSession
from dolmen.message import IMessageReceiver, IMessageSource
from dolmen.message import components, utils, BASE_MESSAGE_TYPE


SESSION = {}


def setup_module(module):
    """ grok the publish module
    """
    testing.setup()
    setSession(SESSION)
    crom.configure(dolmen.message)


def teardown_module(module):
    """ undo groking
    """
    setSession()
    testing.teardown()


def test_registered_source_receiver():
    source = IMessageSource.component()
    assert source.__class__ == components.SessionSource

    source.send(u'Message that is a test.')
    assert 'dolmen.message.session' in SESSION
    assert len(source) == 1

    assert ([(msg.message, msg.type) for msg in source] ==
            [(u'Message that is a test.', u'message')])

    # iterating did not pop anything
    assert len(source) == 1

    # a receiver can be fetched through adapation of the source.
    receiver = IMessageReceiver(source)
    assert receiver.__class__ == components.MessageReceiver

    # Receiving will delete by default.
    messages = list(receiver.receive())
    assert len(messages) == 1
    assert len(source) == 0
    assert messages[0].type == BASE_MESSAGE_TYPE


def test_send_receive():
    utils.send('Something')

    messages = utils.receive('nothing')
    assert messages == None

    messages = list(utils.receive())
    assert len(messages) == 1
    assert messages[0].type == BASE_MESSAGE_TYPE


def test_send_receive_type():
    result = utils.send('Something', type='error')
    assert result == True

    messages = list(utils.receive(type='nothing'))
    assert len(messages) == 0

    messages = list(utils.receive())
    assert len(messages) == 0

    messages = list(utils.receive(type='error'))
    assert len(messages) == 1


def test_send_receive_failing_name():
    messages = utils.receive(name='unexisting')
    assert messages == None

    result = utils.send('Some message', name='unexisting')
    assert result == False


def test_send_receive_some():
    """verify we get all message if there are some"""
    utils.send('Tomorrow, and tomorrow, and tomorrow,')
    utils.send('Creeps in this petty pace from day to day,')
    utils.send('To the last syllable of recorded time;')
    utils.send('And all our yesterdays have lighted fools')
    utils.send('The way to dusty death. Out, out, brief candle!')

    messages = list(utils.receive())
    assert len(messages) == 5
