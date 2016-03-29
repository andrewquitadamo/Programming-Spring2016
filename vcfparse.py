class VcfHeader(object):
	def __init__(self, vcf_header):
		self.header = vcf_header.replace('#','')
		self.fields = str(self.header).split()[:9]
		self.samples = str(self.header).split()[9:]

	def __str__(self):
		return('fields: ' + ' '.join(self.fields) + '\nsamples: ' + ' '.join(self.samples))

	__repr__ = __str__


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

    def get_qual(self):
        return(str(self.data).split()[5])
    
    def get_filt(self):
        return(str(self.data).split()[6])
    
    def get_format(self):
        return(str(self.data).split()[8])
