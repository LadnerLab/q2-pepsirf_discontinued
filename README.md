# q2-pepsirf: A QIIME 2 plugin for the [pep_sirf](https://github.com/LadnerLab/PepSIRF) software package

### Install 
The [pep_sirf](https://github.com/LadnerLab/PepSIRF) package must first be installed and built, 
and the executable must be accessible by calling 'pep_sirf' from your command-line environment.
The best way to do this would be to put the [pep_sirf](https://github.com/LadnerLab/PepSIRF) executable
somewhere located in your $PATH.

Clone this repo and enter the ```q2-pepsirf``` directory.
Then, activate your qiime2 conda environment and run 
```
python setup.py install
qiime dev refresh-cache
```
The plugin should now be available from qiime.
