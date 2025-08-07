# SNFit
Supernova Lightcurve Fitting: Takes a supernova light curve and fits a polynomial of up to 20th degree.

The input file should be in CSV format with the following columns:
- `time / Phase`: Time in days or phase of the supernova (days since explosion).
- `magnitude / Luminosity / Bolometric Luminosity`: Magnitude/Luminosity/Bolometric luminosity of the supernova.

| Time / Phase | Magnitude / Luminosity / Bolometric Luminosity / Flux |
|--------------|-------------------------------------------------------|
| 0            | 15.0                                                  |
| 1            | 14.8                                                  |
| 2            | 14.5                                                  |
| ...          | ...                                                   |

# Test
There are other files in the repository inside the test folder which the user can use to test how the visualization and fitting works.
The test files are located in the `SNFit/SNFit/test/` directory. For example the type II Supernovae [SN 2017eaw](https://www.wis-tns.org/search?name=sn2017eaw&include_frb=1)

s