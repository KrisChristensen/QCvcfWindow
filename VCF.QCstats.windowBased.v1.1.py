##########################################################
### Import Necessary Modules

import argparse                        #provides options at the command line
import sys                             #take command line arguments and uses it in the script
import gzip                            #allows gzipped files to be read
import re                              #allows regular expressions to be used

##########################################################
### Command-line Arguments

parser = argparse.ArgumentParser(description="A script to identify some statistics about the vcf file in windows")
parser.add_argument("-vcf", help = "A vcf file", default=sys.stdin, required=True)
parser.add_argument("-win", help = "The window size, default = 10000, smallest value=2", default=10000)
args = parser.parse_args()

#########################################################

class OpenFile():
    def __init__ (self, f, typ, fnum):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r')
        if typ == "vcf":
            if int(fnum) == 1:
                sys.stderr.write("\n\tOpened vcf file: {}\n\n".format(f))
            OpenVCF(self.filename,fnum)

class OpenVCF():
    def __init__ (self, f, fnum):
        self.open_vcf = f
        self.previousWindow = "NA"
        self.previousChrom = "NA"
        self.nucleotideCount = 0
        self.qualityScore = "NA"
        print ("{}\t{}\t{}\t{}".format("Scaffold", "Window", "NucleotideCount", "AverageQuality"))
        for line in self.open_vcf:
            try:
                line = line.decode('utf-8')
            except:
                pass        
            line = line.rstrip('\n')   
            if not re.search("^#", line):  
                self.chrom, self.pos, self.id, self.ref, self.alt, self.qual, self.filter, self.info, self.format = line.split("\t")[0:9]
                self.currentWindow = (int(int(self.pos)/int(args.win)) + 1) * int(args.win)
                if (self.previousChrom != "NA" and self.chrom != self.previousChrom) or (self.previousChrom != "NA" and int(self.previousWindow) != int(self.currentWindow)):
                    sys.stderr.write("\t\tWorking on {} window {}\n".format(self.previousChrom, self.previousWindow))
                    print("{}\t{}\t{}\t{}".format(self.previousChrom, self.previousWindow, self.nucleotideCount, float(self.qualityScore)/int(self.nucleotideCount)))
                    self.nucleotideCount = 0
                    self.qualityScore = "NA"
                self.previousWindow = self.currentWindow
                self.previousChrom = self.chrom
                self.nucleotideCount += 1
                if self.qualityScore == "NA":
                    self.qualityScore = float(self.qual)
                else:
                    self.qualityScore += float(self.qual)
        sys.stderr.write("\t\tWorking on {} window {}\n".format(self.previousChrom, self.previousWindow))        
        print("{}\t{}\t{}\t{}".format(self.previousChrom, self.previousWindow, self.nucleotideCount, float(self.qualityScore)/int(self.nucleotideCount)))
        self.open_vcf.close()                          


if __name__ == '__main__':
    open_vcf = OpenFile(args.vcf, "vcf", 1)
