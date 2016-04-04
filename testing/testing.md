class: center, middle

#Testing in Python

---

#Overview

* Motiviation for testing

--

* Testing functions 

--

* Testing classes

--

* Continuous Integration with Travis CI (lab section)

---

#Motivation

* You manually test your programs during and after you write them, why not make the process automatic?

--

* Testing can help find errors, and reducing errors should be an important 

--

* [A recent paper](http://f1000research.com/articles/3-303/v2) suggested that many scientific papers have errors in them due to software bugs

--

* Testing is included in the paper [Best practices for Scientific Computing](http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745).

--

* According to Mick Watson not testing your code is one of the [Five habits of bad bioinformaticians](http://www.opiniomics.org/the-five-habits-of-bad-bioinformaticians/)

--

* Testing also is an important part of refactoring. You probably will refactor as you test. 

--

* You will also be able to change your code in the future and be able to tell if you broke the functionality.

---

# A functional example

* For the first part of the the lecture we will be creating tests for a function that calculates GC content of a sequence

--

* In a file called `gc_calc.py` add the following code 

```Python
def gc(sequence):
    gc_count = 0
    for nuc in sequence:
        if nuc == 'G':
            gc_count += 1
        if nuc == 'C':
            gc_count += 1

    return (float(gc_count) / len(sequence))
```

--

```python
>>> from gc_calc import gc
>>> gc1('ACGT')
0.5
```

---

# Your first test

* Python comes with a built in testing library called unittest, which we'll be using today

--

* In a file called `test_gc.py` add the follwing code

```Python
import unittest

class GcTests(unittest.TestCase):
	def test_the_simplest(self):
		pass

if __name__ == '__main__':
	unittest.main()
```

--

* All unittest functions need to start with `test`  

--

* You can run the tests by using the command line `python test_gc.py`  

--

* You should see output like this:  
`.`  
`----------------------------------------------------------------------`  
`Ran 1 test in 0.000s`  
`OK`  

---

# Checking the function

* Before we can test the function we created we need to import it

--

* Add `from gc_calc import gc` to your imports

--

* The first thing we'll do is create a simple example to make sure our function works the way we think it will 

--

* Replace the old function with
```Python
def test_gc(self):
		self.assertEqual(gc('ACTG'), 0.5)
```

--

* Rerun the test using `python test_gc.py`. Make sure the test passes

---

# Adding more tests

* We added a very simple test, lets add a longer one

--

* Underneath your first function add
```Python
def test_long(self):
		self.assertAlmostEqual(gc('ACTGCAGATCTGAAATTCAGTAAGGG'), 0.4230769)```

--

* Testing is also about finding out what happens when inputs aren't what are expected, and we can add tests for that too

--

* We'll add a test that checks the functionality when no input is given

--

```Python
def test_empty(self):
	self.assertRaises(TypeError, gc, )
```

--

* Rerun your tests, and make sure they pass

---

#Asserts

* Most tests in unittest use asserts to asses the tests. 

--

* We've seen `assertEqual`, `assertAlmostTrue`, and `assertRaises`. 

--

* There are also `assertTrue`, `assertFalse`, `assertIsNone`, `assertIsNotEqual`, `assertIn`, `assertIsInstance`, `assertGreater`, `assertRegex`, `assertListEqual` and many more.

---

# Thinking about the intended function

* Now that we have working tests lets think about what we really want our function to do

--

* What would happen if our sequence was lowercase? Or if our sequence was mixed case?

--

```Python
>>> gc('actg')
0.0
>>> gc('aCTg')
0.25
```

--

* What would happen if we gave an empty string as the sequence?

--

```Python
>>> gc('')
Traceback (most recent call last):
		  File "<stdin>", line 1, in <module>
		    File "complement.py", line 10, in gc1
		      return (float(gc_count) / len(sequence))
		  ZeroDivisionError: float division by zero
```

---

# Thinking about the intended function (cont.)

* What would happen if our input string isn't a nucleotide string?

--

```Python
>>> gc('This is just a random sentance, but we still get a GC content back.')
0.029850746268656716
```

---
# Refactoring

* These are the things that you should be thinking about when programming, but you can also think about them during testing

--

* Lets refactor our GC function to take into account these different types of input

--

My version is below:
```Python
def gc3(sequence):
    gc_count = 0
    valid_nucleotides = ['A','C','T','U','G','N']
    for nuc in sequence:
        nuc = nuc.upper()
        if nuc not in valid_nucleotides:
            raise Exception(nuc + ' is not a valid nucleotide.')
        if nuc == 'G':
            gc_count += 1
        if nuc == 'C':
            gc_count += 1

    if len(sequence)==0:
        return 0 
    return (float(gc_count) / len(sequence))
```

---

# Testing the refactored function

* Now we can add tests for our refactored function

--

```Python
def test_lowercase(self):
	self.assertEqual(gc3('AcTg'), 0.5)
```

--

```Python
def test_random(self):
	self.assertRaises(Exception, gc3, 'This is just a random sentance, but we still get a gc content back.')
```

--

```Python
def test_empty_string(self):
	self.assertEqual(gc3(''), 0)
```

--

* Add these tests and rerun `test_gc.py`. Make sure that the test pass.

---

# Testing Classes

* Functions aren't the only things that you can test. You can (and should) also test the classes that you write

--

* We'll use the VcfHeader class we previously wrote as an example.

--

* If you don't have a copy of VcfHeader, open a text file called `vcffile.py` and paste the code from below into the file.

--

```Python
class VcfHeader(object):
    def __init__(self, vcf_header):
        self.header = vcf_header.replace('#','')
        self.fields = str(self.header).split()[:9]
        self.samples = str(self.header).split()[9:]

    def __str__(self):
        return('fields: ' + ' '.join(self.fields) + '\nsamples: ' + ' '.join(self.samples))

    __repr__ = __str__
```

---

# Testing VcfHeader

* What should we test in `VcfHeader`?

--

* We probably should test the data that is generated by the `__init__` method, and the `__str__` method

--

```Python
import unittest
from vcffile import *

class VcfTest(unittest.TestCase):
    def test_header(self):
        vh = VcfHeader('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
        self.assertEqual(vh.header, 'CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
    def test_fields(self):
        vh = VcfHeader('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
        self.assertEqual(vh.fields, ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'])
    def test_samples(self):
        vh = VcfHeader('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
        self.assertEqual(vh.samples, ['HG00096', 'HG00097', 'HG00099', 'HG00100', 'HG00101', 'HG00102', 'HG00103', 'HG00105', 'HG00106', 'HG00107'])
	def test_str(self):
        vh = VcfHeader('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG
00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
        expected = 'fields: CHROM POS ID REF ALT QUAL FILTER INFO FORMAT\nsamples: HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107'
        self.assertEqual(str(vh), expected)

if __name__ == '__main__':
    unittest.main()
```

---

# Testing VcfHeader (cont.)

* Save the tests in a file called `test_vcffile.py` and run them using `python test_vcffile.py`

--

* Make sure your tests pass

---

# Unintended changes

* Well written tests allow you catch any changes that break your functionality

--

* Let's make a breaking change to the VcfHeader class. Change the `self.fields` line to be `self.fields = str(self.header).split()[:8]`

--

* Save your changes and rerun the tests

---
```shell
F..F  
======================================================================
FAIL: test_fields (__main__.VcfTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_vcffile.py", line 10, in test_fields
    self.assertEqual(vh.fields, ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'])
AssertionError: Lists differ: ['CHROM', 'POS', 'ID', 'REF', ... != ['CHROM', 'POS', 'ID', 'REF', ...

Second list contains 1 additional elements.
First extra element 8:
FORMAT
 

- ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
+ ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']  
?                                                              ++++++++++  

  
======================================================================
FAIL: test_str (__main__.VcfTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_vcffile.py", line 17, in test_str
    self.assertEqual(str(vh), expected)

AssertionError: 'fields: CHROM POS ID REF ALT QUAL FILTER INFO\nsamples: HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107' != 'fields: CHROM POS ID REF ALT QUAL FILTER INFO FORMAT\nsamples: HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107'
  
----------------------------------------------------------------------
Ran 4 tests in 0.001s
 
FAILED (failures=2)
``` 
---

# Conclusions

* Writing tests require an initial upfront effort, but may have benefits down the road

--

* In my experience writing tests make you think about the code you've written, and can lead to improvements in the readability and functionality of the code

--

* This afternoon in lab section we will continue the theme of testing and explore continuous integration with Travis CI
