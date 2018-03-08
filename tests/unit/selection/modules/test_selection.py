# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.selection.modules import All, Any, Not
from alphatwirl.selection.modules import AllwCount, AnywCount, NotwCount

##__________________________________________________________________||
all_classes = [All, AllwCount]
all_classe_ids = [c.__name__ for c in all_classes]

any_classes = [Any, AnywCount]
any_classe_ids = [c.__name__ for c in any_classes]

not_classes = [Not, NotwCount]
not_classe_ids = [c.__name__ for c in not_classes]

##__________________________________________________________________||
allany_classes = all_classes + any_classes
allany_classe_ids = all_classe_ids + any_classe_ids

##__________________________________________________________________||
@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_init(Class):
    obj = Class()
    obj = Class(name='name_of_object')

@pytest.mark.parametrize('Class', allany_classes, ids=allany_classe_ids)
def test_allany_repr(Class):
    obj = Class()
    repr(obj)
    obj = Class(name='name_of_object')
    repr(obj)

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_init(Class):
    sel1 = mock.Mock()
    obj = Class(sel1)
    obj = Class(sel1, name='name_of_object')

@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not_repr(Class):
    sel1 = mock.Mock()
    obj = Class(sel1)
    repr(obj)
    obj = Class(sel1, name='name_of_object')
    repr(obj)

@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all(Class):
    sel1 = mock.Mock()
    sel2 = mock.Mock()
    sel1.side_effect = [True, True, False, False]
    sel2.side_effect = [True, False, True, False]

    obj = Class()
    obj.add(sel1)
    obj.add(sel2)

    event = mock.Mock()

    obj.begin(event)

    assert obj(event)
    assert not obj(event)
    assert not obj(event)
    assert not obj(event)

    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any(Class):
    sel1 = mock.Mock()
    sel2 = mock.Mock()
    sel1.side_effect = [True, True, False, False]
    sel2.side_effect = [True, False, True, False]

    obj = Class()
    obj.add(sel1)
    obj.add(sel2)

    event = mock.Mock()

    obj.begin(event)

    assert obj(event)
    assert obj(event)
    assert obj(event)
    assert not obj(event)

    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', all_classes, ids=all_classe_ids)
def test_all_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert obj(event)
    obj.end()

@pytest.mark.parametrize('Class', any_classes, ids=any_classe_ids)
def test_any_empty(Class):
    obj = Class()
    event = mock.Mock()
    obj.begin(event)
    assert not obj(event)
    obj.end()

##__________________________________________________________________||
@pytest.mark.parametrize('Class', not_classes, ids=not_classe_ids)
def test_not(Class):
    sel1 = mock.Mock()
    sel1.side_effect = [True, False]

    obj = Class(sel1)

    event = mock.Mock()

    obj.begin(event)

    assert not obj(event)
    assert obj(event)

    obj.end()

##__________________________________________________________________||