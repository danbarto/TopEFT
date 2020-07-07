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
