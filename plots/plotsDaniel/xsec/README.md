# Plots

### Example

E.g. calculate the xsecs for the following Wilson coefficients
```
run.py --model SMEFTatNLO --process ttZ --couplings cpt -25.0 -22.5 -20.0 -17.5 -15.0 -12.5 -10.0 -7.5 -5.0 -2.5 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 --calcXSec
```

Then the respective plot can be create with the following command.
```
python plot_SMEFT.py --coupling cpt --points 20 --xmin -25.0
```
Right now, only the ttZ process is ploted. Add whatever processes you're interested in.

Your plots will show up in http://uaf-10.t2.ucsd.edu/~YOURUSER/TopEFT/SMEFTatNLO/

In order to make the plots readable from the web, run the following commands in `/home/users/$USER/public_html/`:
```
setfacl -R -m default:other:r-x .
setfacl -R -m default:mask:r-x .

find . -type d -exec chmod a+rx {} \;
find . -type f -exec chmod a+r {} \;
```
