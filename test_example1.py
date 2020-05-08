from makemath import Var, Expr, check_type, check_eq, provable, wff, wffv
from example1 import t,r,s,P,Q,tze,tpl,a1,a2,weq,wim, mp

def test_example1():
    assert t == t
    assert t != r
    assert tze() == tze()
    assert tze() != t
    assert tpl(t,t) == tpl(t,t)
    assert tpl(t,t) != tpl(t,r)
    assert weq(t,r) == weq(t,r)
    assert weq(t,r) != weq(t,s)
    assert wim(P,Q) == wim(P,Q)
    assert wim(P,P) != wim(P,Q)
    assert mp(provable(P),provable(wim(P,Q))) == provable(Q)
    try:
        mp(P,wim(Q,Q))
    except ValueError:
        pass

def test_theorem():

    actual = mp(a2(t), 
                mp(a2(t), 
                a1( tpl(t, tze()), t, t)) )

    expected = provable(weq(t,t))

    assert actual == expected