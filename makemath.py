# Utility stuff

import common
from common import *
import string

# DAV Jupyter is driving me insane, method _repr_pretty_ is *not* inheritable !!  https://stackoverflow.com/a/41454816
# so putting this in expr is *not* enough !!
# def _repr_pretty_(self, p, cycle):
#       p.text(str(self) if not cycle else '...')
REPR_AS_STR = False

MAKE_PREFIX = 'MAKE'
MAKE_DOT = 'DOT'
MAKE_HYPHEN = '_'
MAKE_DOUBLE_HYPHEN = '_2_'
MAKE_UNDERSCORE = '__'


def label_mm_to_python(mm_label):
    """ From Metamath book:
    > Label tokens are used to identify Metamath statements for later reference.
    > Label tokens may contain only letters, digits, and the three characters period,
    > hyphen, and underscore:
    > . - _

    mm_label: any legal Metamath string is accepted 
              EXCEPT strings containing '-_' or '_-' 
    """            
    if len(mm_label) == 0:
        raise ValueError("Found empty Metamath label")
    if '-_' in mm_label:
        raise ValueError("Unhandled case -_ in Metamath label=%s"% mm_label)
    if '_-' in mm_label:
        raise ValueError("Unhandled case _- in Metamath label=%s"% mm_label)

    ret = []
    if mm_label[0].isdigit():
        ret.extend(list(MAKE_PREFIX))
    i = 0
    while i < len(mm_label):
        c = mm_label[i]
        if c == '.':
            ret.extend(list(MAKE_DOT))            
        elif mm_label[i:].startswith('--'):
            ret.extend(list(MAKE_DOUBLE_HYPHEN))
            i += 1
        elif c == '-':
            ret.extend(list(MAKE_HYPHEN))            
        elif c == '_':          
            ret.extend(list(MAKE_UNDERSCORE))            
        else:
            if not(c in string.digits or c in string.ascii_letters):
                raise ValueError('Found illegal character %s in Metamath label %s', (c, mm_label))
            ret.append(c)
            
        i += 1
    return ''.join(ret)

def label_python_to_mm(python_label):
    """ From Metamath book:
    > Label tokens are used to identify Metamath statements for later reference.
    > Label tokens may contain only letters, digits, and the three characters period,
    > hyphen, and underscore:
    > . - _
    """    
    if len(python_label) == 0:
        raise ValueError("Found empty Python label")
    ret = []
    i = 0
    if python_label.startswith(MAKE_PREFIX):
        i += len(MAKE_PREFIX)
    while i < len(python_label):
        if python_label[i:].startswith(MAKE_DOT):
            ret.append('.')
            i += len(MAKE_DOT)            
        elif python_label[i:].startswith(MAKE_UNDERSCORE):
            ret.append('_')
            i += len(MAKE_UNDERSCORE)
        elif python_label[i:].startswith(MAKE_DOUBLE_HYPHEN):
            ret.append('--')
            i += len(MAKE_DOUBLE_HYPHEN)
        elif python_label[i:].startswith(MAKE_HYPHEN):
            ret.append('-')
            i += len(MAKE_HYPHEN)
        else:
            ret.append(python_label[i])
            i += 1
    return ''.join(ret)


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

class Expr:
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

class Var (Expr):
    
    def __init__(self, name):
        check_blank(name)
        self.name = name

    def __repr__(self):
        return self._repr1(self.name)
    
    def __str__(self):
        return self.name            


def get_vars(ex):
    check_type(ex, Expr)
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
    check_type(ex, Expr)
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
    check_type(ex1, Expr)
    check_type(ex2, Expr)
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

class wff (Expr):
    def __init__(self):
        pass

class provable (Expr):
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

