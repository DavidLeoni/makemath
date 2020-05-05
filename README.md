
# MakeMath

A Python representation of [MetaMath](http://us.metamath.org) theorems and proofs

**DISCLAIMER: I'm no logician, just a programmer trying to figure out things. What follows may well be quite wrong.**

The idea is to build proofs like you compose Python objects, and test/debug them like regular programs

**Status: proof of concept (incomplete)**

**Expected benefits:**

- syntax familiar to developers with no formal training of  Python popular programming language
- you can debug proofs like they were code in regular IDEs
- if used in Jupyter, you should be able to interactively display proofs exploiting the many Python visualization libraries

**Cons:**

- we bring in all Python baggage, which could cause confusion
- if users' Python proofs are not checked carefully, they could write code which cannot be translated back to MetaMath

**Current limitions (MANY):**

- does not parse .mm databases
- proofs code is manually written, and only supports `t=t` first example from the book
- Metamath classes are not supported
- there is no way to go from Python proofs to Metamath ones
- does not exploit any Python feature which could help simplifying syntax (sets, comprehensions, functions, typing with mypy, ...)


## Example

As found in [test_example1.py](test_example1.py):

```python
from makemath import Var, expr, check_type, check_eq, provable, wff, wffv
from example1 import t,r,s,P,Q,tze,tpl,a1,a2,weq,wim, mp

# if test passes, you proved it !

def test_theorem():
    assert mp(a2(t), mp(a2(t), a1(tpl(t,tze()),t,t))) == provable(weq(t,t))
```

## Testing:

Install dependencies:

```
python3 -m pip install --user requirements.txt 
```

Execute tests:

```bash
pytest 
```

