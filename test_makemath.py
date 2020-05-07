from makemath import *
import string
from hypothesis import given, reject
from hypothesis.strategies import integers, text


@given(text(min_size=1, alphabet=string.ascii_letters + string.digits + '-' + '.' + '_'))
def test_label_mm_to_python(x):    
    if '-_' not in x and '_-' not in x:
        assert label_python_to_mm(label_mm_to_python(x)) == x

def test_label_mm_to_python_cornercases():
    try:
        label_mm_to_python('')
    except ValueError:
        pass
    try:
        label_mm_to_python('-_')
    except ValueError:
        pass
    try:
        label_mm_to_python('_-')
    except ValueError:
        pass
    try:
        label_mm_to_python('è')
    except ValueError:
        pass
    label_python_to_mm(label_mm_to_python('.')) == '.'
    label_python_to_mm(label_mm_to_python('-')) == '-'
    label_python_to_mm(label_mm_to_python('--')) == '--'
    label_python_to_mm(label_mm_to_python('__')) == '__'
    label_python_to_mm(label_mm_to_python('_')) == '_'

@given(text(min_size=1,max_size=1, alphabet=string.ascii_letters + '_'), text(min_size=1, alphabet=string.ascii_letters + string.digits + '_'))
def test_label_python_to_mm(x,y):
    assert label_mm_to_python(label_python_to_mm(x+y)) == x+y

def test_label_python_to_mm_cornercases():
    try:
        label_python_to_mm('')
    except ValueError:
        pass
    

def test_is_contained():
    v1 = Var('v1')
    v2 = Var('v2')
    
    class C (expr):
        def __init__(self,p1,p2=None):
            self.p1=p1
            self.p2=p2
    assert is_contained(v1, C(v1))
    assert not is_contained(v2, C(v1))
    assert is_contained(v1, C(C(v1)))
    assert not is_contained(v2, C(C(v1)))
    # circular
    c = C(None)
    c.p1 = c
    c.p2 = v1
    assert is_contained(v1, c)
    assert not is_contained(v2, c)
    
def test_get_vars():
    v1 = Var('v1')
    v2 = Var('v2')
    
    class C (expr):
        def __init__(self,p1,p2=None):
            self.p1=p1
            self.p2=p2
            
    assert get_vars(C(None)) == set()
    assert get_vars(C(v1)) == set([v1])
    assert get_vars(C(v1, p2=v2)) == set([v1, v2])
    assert get_vars(C(C(v1))) == set([v1])
    assert get_vars(C(C(v1), p2=C(v1))) == set([v1])
    assert get_vars(C(C(v1), p2=C(v2))) == set([v1,v2])
       
    c = C(None)
    c.p1 = c
    c.p2 = v1
    assert get_vars(C(c)) == set([v1])

def test_shared_vars():
    v1 = Var('v1')
    v2 = Var('v2')
    
    class C (expr):
        def __init__(self,p1=None,p2=None):
            self.p1=p1
            self.p2=p2

    assert shared_vars(C(), C()) == set()
    assert shared_vars(C(v1), C()) == set()
    assert shared_vars(C(), C(v1)) == set()
    assert shared_vars(C(v1), C(v1)) == set([v1])
    assert shared_vars(C(v1, C(v2)), C(v1)) == set([v1])
    assert shared_vars(C(v1, C(v2)), C(v2)) == set([v2])
    assert shared_vars(C(v1, C(v2)), C(v2, C(C(v1)))) == set([v1,v2])

def test_are_disjoint():
    v1 = Var('v1')
    v2 = Var('v2')
    
    class C (expr):
        def __init__(self,p1=None,p2=None):
            self.p1=p1
            self.p2=p2

    assert are_disjoint(C(), C())
    assert are_disjoint(C(v1), C())
    assert are_disjoint(C(), C(v1))
    assert are_disjoint(C(), C(C(v1)))
    assert not are_disjoint(C(v1), C(v1))
    assert not are_disjoint(C(v1, C(v2)), C(v1))
    assert not are_disjoint(C(v1, C(v2)), C(v2))
    assert not are_disjoint(C(v1, C(v2)), C(v2, C(C(v1))))

def test_forall():
    # TODO
    print(forall(x,ph))

def test_exist():    
    # TODO
    print(exists(x,ph))
