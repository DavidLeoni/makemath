
from makemath import Var, Expr, check_type, check_eq, provable, wff, wffv
    
# DAVID: don't know if it make any sense do 'declare' in Python ...
"""
$( Declare the constant symbols we will use $)
    $c 0 + = -> ( ) term wff |- $.
"""
class term (Expr):
    def __init__(self):
        pass
    



    
# DAVID: don't know if it make any sense do 'declare' in Python ...
""" $( Declare the metavariables we will use $)
    $v t r s P Q $.
"""

#*****   $( Specify properties of the metavariables $)   *****


class termv (Var, term):
    pass

# tt $f term t $.

def tt():
    return termv('t')

# tr $f term r $.

def tr():
    return termv('r')

# ts $f term s $.

def ts():
    return termv('s')

# DAV this is pure convenience for global environment
t = tt()
r = tr()
s = ts()

# wp $f wff P $.
def wp():
    return wffv('P')
# wq $f wff Q $.
def wq():
    return wffv('Q')


# DAV this is pure convenience for global environment
P = wp()
Q = wq()
    
#*****   $( Define "term" and "wff" $)  *****

def tze():
    """ tze $a term 0 $. """
    return termv('0')
    
class tpl(term):
    """ tpl $a term ( t + r ) $. """
    def __init__(self,t,r):
        check_type(t, term)
        check_type(r, term)
        self.t = t
        self.r = r

    def __repr__(self):
        return self._repr2(t,r)
        
    def op(self):
        return '+'
    
    def __str__(self):
        return self._str2i(self.t,self.r)
        
class weq(wff):
    """ weq $a wff t = r $. """
    def __init__(self,t,r):
        check_type(t, term)
        check_type(r, term)
        self.t = t
        self.r = r

    def __repr__(self):
        return self._repr2(self.t, self.r)
        
    def op(self):
        return '='
    
    def __str__(self):
        return self._str2i(self.t, self.r)
    
class wim(wff):
    """ wim $a wff ( P -> Q ) $. """
    def __init__(self,P,Q):
        check_type(P, wff)
        check_type(Q, wff)
        self.P = P
        self.Q = Q
        
    def __repr__(self):
        return self._repr2(self.P, self.Q)
        
    def op(self):
        return '->'
    
    def __str__(self):
        return self._str2i(self.P,self.Q)
    
# ******   $( State the axioms $)


def a1(t,r,s):
    """ a1 $a |- ( t = r -> ( t = s -> r = s ) ) $. """
    check_type(t, term)
    check_type(r, term)
    check_type(s, term)
    return provable(wim(weq(t, r), wim(weq(t, s), weq(r, s) )))


def a2(t):
    """ a2 $a |- ( t + 0 ) = t $. """
    check_type(t, term)    
    return provable(weq(tpl(t, tze()), t))

def mp(min,maj):
    """
    $( Define the modus ponens inference rule $)
        ${
           min $e |- P $.
           maj $e |- ( P -> Q ) $.
           mp  $a |- Q $.
        $}
    """    
    check_type(min, provable)
    check_type(maj, provable)
    check_type(maj.wff, wim)
    check_eq('P1', 'P2', min.wff, maj.wff.P)
        
    return provable(maj.wff.Q)
