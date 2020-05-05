# Utility stuff

import common
from common import *

# DAV Jupyter is driving me insane, method _repr_pretty_ is *not* inheritable !!  https://stackoverflow.com/a/41454816
# so putting this in expr is *not* enough !!
# def _repr_pretty_(self, p, cycle):
#       p.text(str(self) if not cycle else '...')
REPR_AS_STR = False


def check_type(x, c):
    if not isinstance(x, c):
        raise ValueError('%s is not instance of %s' % (x,c.__name__))

def check_eq(nx,ny,x,y):
    if not x == y:
        raise ValueError('%s should be equal to %s!\n%s: %s\n%s: %s' % (nx,ny,nx,x,ny,y))
        
def check_empty_str(name):
    if not type(name) == str:
        raise TypeError('Wrong type for %s' % name)
    if len(name) == 0:
        raise ValueError('String is empty: %s' & name)

def check_blank(name):
    if not type(name) == str:
        raise TypeError('Wrong type for %s' % name)
    if len(name.strip()) == 0:
        raise ValueError('String is blank: -->%s<--' & name)

class expr:
    def __eq__(self, other):
        return self.__class__ == other.__class__ and vars(self) == vars(other)
    
    def __hash__(self):
        return hash(tuple(vars(self).items())) # dirty, hope this doesn't mess up things ..

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)

    def __str__(self):
        return "%s()" % (self.__class__.__name__)
    
    def _repr1(self, x):
        if REPR_AS_STR:
            return str(x)
        else:
            return "%s(%r)" % (self.__class__.__name__, x)
    
    def _repr2(self,x,y):
        if REPR_AS_STR:
            return str(self)
        else:
            return "%s(%r, %r)" % (self.__class__.__name__,x,y)    
        
    def op(self):
        """ A string representation of the operator (as ASCII)
        """
        return self.__class__.__name__
    
    def op_unicode(self):
        """ A unicode representation of the operator
        """        
        return self.op()
    
    def _str1(self, x):
        return "%s %s" % (self.op(), x)
    
    def _str2(self, x, y):
        return "%s %s %s" % (self.op(), x, y)
    
    def _str2i(self, x, y):
        return "%s %s %s" % (x, self.op(), y)
    
#syntax:
# label $f typecode variable $.
# 2. No two $f statements may contain the same variable
#The second property tells us there must be only one type specified for a variable.
#   cit.: Chapter 4.2.7 Frames Matemath book

class Var (expr):
    
    def __init__(self, name):
        check_blank(name)
        self.name = name

    def __repr__(self):
        return self._repr1(self.name)
    
    def __str__(self):
        return self.name            


def get_vars(ex):
    check_type(ex, expr)
    ret = set()
    stack = [ex]
    visited = set()
    while len(stack) > 0:
        el = stack.pop()
        if hasattr(el, '__dict__'):  # checking isinstance(5, object) would return True ...
            visited.add(id(el))
            
            if isinstance(el, Var):
                ret.add(el)
            else:
                for attr in vars(el):
                    val = getattr(el, attr)
                    if id(val) in visited:
                        warn("Found circular reference!")
                    else:
                        stack.append(val)
    return ret
    
def is_contained(x, ex):
    check_type(x, Var)
    check_type(ex, expr)
    stack = [ex]
    # to prevent circular references. There should never be, but just in case ..
    visited = set()
    while len(stack) > 0:
        el = stack.pop()
        if hasattr(el, '__dict__'):  # checking isinstance(5, object) would return True ...
            visited.add(id(el))

            if isinstance(el, Var):
                if x.name == el.name:
                    return True
            else:
                for attr in vars(el):
                    val = getattr(el, attr)
                    if id(val) in visited:
                        warn("Found circular reference!")
                    else:
                        stack.append(val)
    return False


def shared_vars(ex1, ex2):
    check_type(ex1, expr)
    check_type(ex2, expr)
    return get_vars(ex1).intersection(get_vars(ex2))
    
def are_disjoint(ex1, ex2):
    return len(shared_vars(ex1, ex2)) == 0



#*****   $( Specify properties of the metavariables $)   *****
#syntax: The letters f stands for “floating” (roughly meaning used only if relevant) 
#label $f typecode variable $.

class setvar (Var):
    """ setvar : Individual set variable type 
                 (read: “the following is an individual set variable”). 
        Note that this is not the type of an arbitrary set expression,
        instead, it is used to ensure that there is only a single symbol
        used after quantifiers like for-all (∀) and there-exists (∃)
        $c setvar $. $( Individual variable type (read:  "the following is an individual (set) variable" $)

    """
    pass

# vx $f setvar x $.

def vx():
    return setvar('x')

# vy $f setvar y $.

def vy():
    return setvar('y')

# DAV this is pure convenience for global environment
x = vx()
y = vy()

class wff (expr):
    def __init__(self):
        pass

class provable (expr):
    """ read: “the following symbol sequence is provable” or “a proof exists for”.
        In Metamath *by convention* provable expressions are prefixed by a turnstile
    """
    def __init__(self,wff):
        self.wff = wff
        
    def __repr__(self):
        return self._repr1(self.wff)
    
    def op(self):
        return '|-'
    
    def op_unicode(self):
        return('⊢')
        
    def __str__(self):
        return self._str1(self.wff)


class wffv (Var, wff):
    pass

# wph $f wff ph $.
def wph():
    return wffv('ph')
# wps $f wff ps $.
def wps():
    return wffv('ps')
# wch $f wff ch $.
def wch():
    return wffv('ch')
# wth $f wff th $.
def wth():
    return wffv('th')

# DAV this is pure convenience for global environment
ph = wph()
ps = wch()
th = wth()


"""
Disjoint variables
$d x y $. means “assume x and y are distinct variables.”
$d x ph $. means “assume x does not occur in ϕ.”
$d ph ps $. means “assume ϕ and ψ have no variables
in common.”
"""


class forall (wff):
    """ 
    ${
        $v x $.
        $( Let ` x ` be an individual variable (temporary declaration). $)
        vx.wal $f setvar x $.
        $( Extend wff definition to include the universal quantifier ('for all').
        ` A. x ph ` is read " ` ph ` (phi) is true for all ` x ` ."  Typically,
        in its final application ` ph ` would be replaced with a wff containing
        a (free) occurrence of the variable ` x ` , for example ` x = y ` .  In
        a universe with a finite number of objects, "for all" is equivalent to a
        big conjunction (AND) with one wff for each possible case of ` x ` .
        When the universe is infinite (as with set theory), such a
        propositional-calculus equivalent is not possible because an infinitely
        long formula has no meaning, but conceptually the idea is the same. $)
        wal $a wff A. x ph $.
    $}
   """ 
    def __init__(self,x,ph):
        check_type(x, setvar)
        check_type(ph, wff)
        self.x = x
        self.ph = ph

    def __repr__(self):
        return self._repr2(self.x, self.ph)
    
    def op(self):
        """ $( Declare new symbols needed for predicate calculus. $)
            $c A. $. $( "inverted A" universal quantifier (read:  "for all") $)
        """
        return 'A.'
    
    def op_unicode(self):
        return '∀'
    
    def __str__(self):
        return self._str2(self.x, self.ph)
    

class exists (wff):
    """  """
    def __init__(self,x,ph):
        check_type(x, setvar)
        check_type(ph, wff)
        self.x = x
        self.ph = ph

    def __repr__(self):
        return self._repr2(self.x, self.ph)

    def op(self):
        return 'E.'
    
    def op_unicode(self):
        return '∃'
        
    def __str__(self):
        return self._str2(self.x, self.ph)    

