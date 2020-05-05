from makemath import *

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
