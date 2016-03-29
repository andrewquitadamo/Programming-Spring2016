class: center, middle

#Object Oriented Bioinformatics

---

#OO Based VCF Parser

* In this lecture we will walk through an example VCF parser

--

* We will use an object oriented programming style to solve our problem
---

#VCF files

* VCF stands for Variant Call Format, and is used to store genotypic information 

--

* The current VCF specification is [4.2](http://samtools.github.io/hts-specs/VCFv4.2.pdf), although the VCF file we're using today is based on [4.1](http://samtools.github.io/hts-specs/VCFv4.1.pdf)

--

* A VCF file can have metadata lines that start with "##", a header line that starts with "#" and then genotype records.
```Shell
##fileformat=VCFv4.1
##FILTER=<ID=PASS,Description="All filters passed">
##fileDate=20150218
...
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	HG00096	HG00097	HG00099	HG00100	HG00101	HG00102	HG00103	HG00105	HG00106	HG00107
1	10177	rs367896724	A	AC	100	PASS	AC=2130;AF=0.425319;AN=5008;NS=2504;DP=103152;EAS_AF=0.3363;AMR_AF=0.3602;AFR_AF=0.4909;EUR_AF=0.4056;SAS_AF=0.4949;AA=|||unknown(NO_COVERAGE);VT=INDEL	GT	1|0	0|1	0|1	1|0	0|0	1|0	1|0	1|0	1|0	0|0
```
--

* We are going to use a modified VCF file for todays lecture, which can be downloaded from the [Programming-Spring2016 GitHub repo](https://raw.githubusercontent.com/andrewquitadamo/Programming-Spring2016/master/example.vcf)

---

#VCF file fields

* A VCF file has multiple fields that contain potentially useful information

--

* The CHROM field contains the chromosome that the variant is found on

--

* The POS field contains the position (1-based)

--

* The ID field contains the id

--

* REF contains the reference sequence

--

* ALT contains the alternative sequence

--

* QUAL contains a phred based quality score

--

* FILTER indicates whether the variant has passed all filter checks

--

* INFO field (next slide)

--

* The FORMAT field indicates how the genotypes are reported 
---

# VCF file fields (cont.)

* The INFO field contains additional information, and is composed of semi-colon separated subfields

--

* For variants that are multiallelic some of these subfields are comma separated lists

--

* AC - Allele counts for the alternative allele(s)

--

* AF - Allele frequency for the alternative allele(s)

--

* AN - Total number of alleles

--

* NS - Number of samples

--

* DP - Total depth reads

--

* AA - Ancestral allele

--

* VT - Variant type, eg. SNP, INDEL

--

* There are other possible subfields in INFO which include SB (strand bias), SOMATIC and others

---

# The Plan

* We'll create an object oriented style representation of a VCF file by using classes. 

--

* The end result will be a VcfFile class, which will have subclasses for VcfHeader and VcfRecord

--

* We'll start by creating a class for the header

---

#VcfHeader

* Open up a text file called `vcfparse.py` and add a class called `VcfHeader`.

--

* There are a few things that this class should do.  
1) It should store the complete header in a `header` variable, but it should not include the '#'.  
2) It should store the first eight fields in a `fields` variable.  
3) It should store the sample IDs in a `samples` variable.

--

* Create an `__init__` method that takes two arguments (self and the header line)

--

* In the `__init__` method create a variable called `header` that stores the header without the `#`  
(Hint: use .replace())

--

Currently my code looks like:  
```Python
class VcfHeader(object):
	def __init__(self, vcf_header):
		self.header = vcf_header.replace('#','')
```

---

#VcfHeader -- fields

* Next we'll add some code to store the first eight fields

--

* Create a variable called `fields` that only contains the `CHROM POS ID REF ALT QUAL FILTER INFO FORMAT` portion of the header.  

--

* The `fields` variable should be a list.

--

My version looks like this:
```Python
class VcfHeader(object):
	def __init__(self, vcf_header):
		self.header = vcf_header.replace('#','')
		self.fields = str(self.header).split()[:9]
```

---

# VcfHeader -- samples

* Next let's add some code to store the sample IDs

--

* Create a variable called `samples`, which will store all of the sample IDs. 

--

My version looks like this:
```Python
class VcfHeader(object):
	def __init__(self, vcf_header):
		self.header = vcf_header.replace('#','')
		self.fields = str(self.header).split()[:9]
		self.samples = str(self.header).split()[9:]
```

---

# Testing VcfHeader

* Now that we have a version of VcfHeader let's make sure it works like we want

--

* Open up a Python shell (type `python` into the command line)

--

* You can import your class by typing `from vcfparse import VcfHeader`

--

* Next we'll create a new instance called `test_header`  

--

* To create the new instance use  
```Python 
test_header = VcfHeader('#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT HG00096 HG00097 HG00099 HG00100 HG00101 HG00102 HG00103 HG00105 HG00106 HG00107')
```

--

* See if `test_header` has a `.samples` attribute, a `.fields` attribute and a `.header` attribute

---

# VcfHeader \_\_str\_\_ method

* We need to add a way to convert the VcfHeader to a string so we can print it out

--

* Add a `__str__` method to print out the `fields` and the `samples` variable

--

My `VcfHeader` class now looks like:
```Python
class VcfHeader(object):
	def __init__(self, vcf_header):
		self.header = vcf_header.replace('#','')
		self.fields = str(self.header).split()[:9]
		self.samples = str(self.header).split()[9:]

	def __str__(self):
		return('fields: ' + ' '.join(self.fields) + '\nsamples: ' + ' '.join(self.samples))
```

---

# VcfHeader \_\_repr\_\_ method

* We can add a `__repr__` method so our `VcfHeader` class has a nice representation when printed out

--

* We can simply set `__repr__ = __str__`

--

My final `VcfHeader` class looks like:
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

#VcfRecord Class

* Now we'll create a class to represent a VCF record

--

* In the same text file create a new class called `VcfRecord`

--

* Just like VcfHeader create an `__init__` method that takes two arguments (self and the VCF line)

--

* Add a variable called `data` which will store the complete VCF record

--

My `VcfRecord` class currently looks like this:
```Python
class VcfRecord(object):
	def __init__(self, vcf_line):
		self.data = vcf_line
```

---

# VcfRecord chr variable

* Next we'll create some methods to deal with the informational fields

--

* Create a method called `get_chr` that takes only self as an argument

--

* `get_chr` should simply return the chromosome by splitting the `data` variable

--

My method looks like:
```Python
def get_chr(self):
	return(str(self.data).split()[0])
```
	
---

#VcfRecord chr variable (cont.)

* In the `__init__` method add a line to get the results from `get_chr` and store it in a variable called `chr`

--

My `VcfRecord` class now looks like:
```Python
class VcfRecord(object):
	def __init__(self, vcf_line):
		self.data = vcf_line
		self.chr = self.get_chr()

    def get_chr(self):
		return(str(self.data).split()[0])
```

---

#Other VcfRecord variables

* Now we'll create methods to get and store `pos`, `id`, `ref`, `alt`, `qual`, `filt`, and `formt` variables

--

* This should look very similar to the `get_chr` method, and the line in the `__init__` method to create the `chr` variable

---

# Other VcfRecord variables

My class now looks like:
```Python
class VcfRecord(object):
    def __init__(self, vcf_line):
        self.data = vcf_line
        self.chr = self.get_chr()
        self.pos = self.get_pos()
        self.id = self.get_id()
        self.ref = self.get_ref()
        self.alt = self.get_alt()
        self.qual = self.get_qual()
        self.filt = self.get_filt()
        self.formt = self.get_format()
        
    def get_chr(self):
        return(str(self.data).split()[0])
    
    def get_pos(self):
        return(str(self.data).split()[1])
    
    def get_id(self):
        return(str(self.data).split()[2])
    
    def get_ref(self):
        return(str(self.data).split()[3])
    
    def get_alt(self):
        return(str(self.data).split()[4])
```

---

```Python
    def get_qual(self):
        return(str(self.data).split()[5])
    
    def get_filt(self):
        return(str(self.data).split()[6])
    
    def get_format(self):
        return(str(self.data).split()[8])
```

---

# genotype variable

* We need to add a variable to hold the genotypes of the VCF record

--

* Add a method called `get_genotypes` that returns the list of genotypes

--

* Add a line in the `__init__` method to store the genotypes in the `genotypes` variable

--

My additional code looks like:
```Python
class VcfRecord(object):
	def __init__(self, vcf_line):
		...
		self.genotypes = self.get_genotypes()

	...

	def get_genotypes(self):
		return(self.data.split()[9:])
```

---

# VcfInfo class

* We will create a new class called `VcfInfo` to store all the data from the INFO field

--

* Add a `VcfInfo` class to your `vcfparse.py`

--

* Create an `__init__` method that takes two arguments, self and an info line

--

* To add the data from INFO to the info class we'll use a loop.  
The code to add the data from the AC portion is below  
```Python
for inf in info_line.split(';'):
	if inf.startswith('AC'):
		self.AC = inf.split('=')[-1].split(',')
```

--

* Add more if statements to add the data from `AF`, `AN`, `NS`, `DP` and `VT`

---

#VcfInfo \_\_str\_\_

* Next we'll add code to create a string from the `VcfInfo` class

--

The code I wrote for the `__str__` method is below
```Python
return('AC=' + ','.join(self.AC) + ' AF=' + ','.join(self.AF) + ' AN=' + ','.join(self.AN)
	   + ' NS=' + ','.join(self.NS) + ' DP=' + ','.join(self.DP) + ' VT=' + str(self.VT))
```

--

* We'll also add a `__repr__` method, just like for `VcfHeader`

---

# Completed VcfInfo

```Python
class VCF_info(object):
    def __init__(self, info_line):
        self.info_line = info_line
        for inf in info_line.split(';'):
            if inf.startswith('AC'):
                self.AC = inf.split('=')[-1].split(',')
            if inf.startswith('AF'):
                self.AF = inf.split('=')[-1].split(',')
            if inf.startswith('AN'):
                self.AN = inf.split('=')[-1].split(',')
            if inf.startswith('NS'):
                self.NS = inf.split('=')[-1].split(',')
            if inf.startswith('DP'):
                self.DP = inf.split('=')[-1].split(',')
            if inf.startswith('VT'):
                self.VT = inf.split('=')[-1]
                
    def __str__(self):
        return('AC=' + ','.join(self.AC) + ' AF=' + ','.join(self.AF) + ' AN=' + ','.join(self.AN)
               + ' NS=' + ','.join(self.NS) + ' DP=' + ','.join(self.DP) + ' VT=' + str(self.VT))
        
    __repr__ = __str__
```

---

# VcfRecord info variable

* Now we need to add code to use the `VcfInfo` class in `VcfRecord`

--

* Create a method to create a new instance of `VcfInfo` using the INFO field of a VCF record

--

* Add a line in the `__init__` method to store the `info` variable

--

My code is below:
```Python
class VcfRecord(object):
	def __init__(self, vcf_line):
		...
		self.info = self.get_info()

	...

	def get_info(self):
		info = VCF_info(str(self.data).split()[7])
		return(info)
```

---

# VcfFile class

* Now that we have working `VcfHeader` and `VcfRecord` classes let's create a `VcfFile` class to tie it all together

--

* Add a class called `VcfFile` to your Python code

--

* Create an `__init__` method that takes two arguments, self and a filename

--

* Create a method called `load_vcf` which just takes self as an argument, and returns a VcfHeader instance, and an array of VcfRecord instances.

---
# VcfFile class (cont.)

My code is below
```Python
class VcfFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.vh, self.vrs = self.load_vcf()

    def load_vcf(self):
        vrs = []
        with open(self.filename, 'r') as fh:
            for line in fh:
                if line.startswith('#'):
                    vh = VcfHeader(line)
                else:
                    vrs.append(VcfRecord(line))
            return(vh, vrs)
```

---

# Testing VcfFile

* Open a new Python interactive shell

--

* Import the `VcfFile` class

--

* Create a new instance of `VcfFile` using `example.vcf`

--

```Python
vcf = VcfFile('example.vcf')
```

--

* We can print out all of the record
```Python
for record in vcf.vrs:
		print record
```

--

* We can filter based on certain information
```Python
for record in vcf.vrs:
		if record.info.VT == 'INDEL':
			print record
```

---

# More things to do

* We probably should add `__str__` and `__repr__` methods for `VcfFile`

--

* What would happen if we had a really large VCF file? Maybe we should update our class so it doesn't read in all the information at once

--

* We could add methods to filter the data on VT, quality, position or other criteria

--

* We could add better multiallelic handling

--

* We could add handling for other INFO subfields

--

* [PyVCF](https://github.com/jamescasbon/PyVCF) is an object oriented based VCF parser written in Python. It is much more sofisticated than what we've created. You can check out the source code if you are interested.
