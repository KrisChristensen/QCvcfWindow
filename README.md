# QCvcfWindow
A script to count nucleotide variants from a VCF file in non-overlapping windows and also output the average quality score for the window.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

The script requires a VCF file (can be compressed).

<!-- usage -->
## Usage

Find the variant count and output the average variant quality score for windows that have variants:
python VCF.QCstats.windowBased.v1.1.py -vcf file.vcf -win 10000 > SNPCountAndQuality.10K.win.txt

To see the usage and get futher information: python VCF.QCstats.windowBased.v1.1.py -h

<!-- license -->
## License 

Distributed under the MIT License.
