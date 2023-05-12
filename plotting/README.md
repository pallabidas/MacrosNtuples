# MacrosNtuples/plotting

This folder contains several scripts to draw plots generated using the tools in `MacrosNtuples/l1macros`.
You can draw plots individually by calling `drawplots.py`, use one of the `make_"OBJ"_plots.sh` 
to draw a bunch of plots for a given type of object (Muon, EGamma, Jets or MET) at once,
or use the `draw_all.sh` to make all plots for all 4 object types.

You can find plots generated with these tools for all of 2022 here: https://test-l1studies-plots.web.cern.ch/L1studies/

## Drawing plots individually

This is done using the `drawplots.py` program. If saved, the plots will be stored in a directory called `plotL1Run3`.
You need to create this directory yourself beforehand.

### Types of plots
The `drawplots.py` can make different types of plots, specified with the `--type` command line argument.

These types are:
   - `--type efficiency` computes and draws one/several efficiencies given numerator(s) and denominator(s).
   - `--type resolvsx` compute the response and resolution of a 2D histogram along its x axis. Makes two separate plots.
   - `--type distribution` draws the distribution from a 1D histogram.
   - `--type profilex_fromh2` draws the profile of a 2D histogram along its x axis.

### Command line arguments
The different type need different command line arguments. These are:
   - Common, required arguments:
      - `--type` The type of plot (see above)
      - `--input` The input file to read the histograms from

   - Required for `efficiency`:
      - `--den` Name of the denominator histogram(s). If only one, the same is used for every numerator(s). 
      If several, pairs each denominator with one numerator, the numbers need to be the same.
      - `--num` Name of the numerator histogram(s).

   - Optionnal for `efficiency`:
      - `--addnumtoden` Add numerator histogram to denominator

   - Required for `resolvsx` and `profilex_fromh2`:
      - `--h2d` The 2D histogram to use.

   - Required for `distribution`:
      - `--h1d` The 1D histogram to use.

   - Commun, optionnal arguments: 
      - `--xtitle`, `--ytitle`, `--ztitle` The X/Y/Z axis title
      - `--extralabel` A label to put in the top left corner of the plot.
      - `--toplabel` A label to put above the plot (for sqrt(s) and lumi values)
      - `--setlogx` Whether to set the x axis to log scale or not. 
      - `--axisranges` Axis ranges `[xmin, xmax, ymin, ymax, zmin, zmax]`
      - `--legend` Legend labels. For `efficiency`, one per numerator.
      - `--legendpos` Position of the legend. (Either `top` or `bottom`, default is `bottom`)
      - `--saveplot` Whether to save the plot(s) or not.
      - `--plotname` Name of the plot to save. Saves both a `.png` and a `.pdf`
      - `--interactive` Run in interactive mode.
      - `--suffix_files` Input files suffix.
      - `--nvtx_suffix` Suffix to append to dirname and histogram names, to make plots in bins of nvtx.

### Example usage 
To draw the effiency, given a file `input.root` with two histograms `numerator` and `denominator`:
```
python3 drawplots.py --type efficiency --input input.root --num numerator --den denominator --saveplot True --plotname myplot
```
This will save to files, `myplot.png` and `myplot.pdf`.

## Drawing all the plots for one kind of object

### 2022 setup

This is done using one of the for script, `make_mu_plots.sh`, `make_eg_plots.sh`, `make_jets_plots.sh` or `make_etsum_plots.sh`.
These are for Muons, EGamma, Jets and MET respectively.

Every script is called the same way:
```
./make_"OBJ"_script dirname lumi_value nvtx_suffix
```

The `dirname` argument is required. The script will search for input files and store plots inside `dirname`.
Depending of the type of object, you will require an input files named 
`dirname/all_zmumu.root`, `dirname/all_zee.root`, `dirname/all_mujet.root` and/or `dirname/all_photonjet.root`.
You will also need to create a `dirname/plotL1Run3` directory to save the plots.

The `lumi_value` is the value of the integrated luminosity to be added in the label above the plot. 

The `nvtx_suffix` can be passed if you want to make the plots for a certain bin of nvtx.
It is of the form `_nvtxXXtoYY` where `XX` and `YY` are the minimum and maximum nvtx values respectively. 
Make sure the correponding histograms exist in your input file.
To generate histograms in bins of nvtx, see `--plot_nvtx` and `--nvtx_bins` arguments in `MacrosNtuples/l1macros/performances.py` or `MacrosNtuples/l1macros/performances_nano.py`.
If `nvtx_suffix` is passed, then the corresponding directory to save the plots should be `dirname/plotL1Run3_nvtxXXtoYY`
(where `_nvtxXXtoYY` is the argument that was passed).

#### Example usage
To draw all plots for muons, for a directory `MyData` containing the input file `MyData/all_zmumu.root` 
and directory `MyData/plotsL1Run3` to store the plot, corresponding to `X` inverse femtobarns of inverse luminosity, run:
```
./make_mu_plots.sh MyData X
```

If you now want to make the same plots, with nvtx between 30 and 40, you will need the directory `MyData/plotsL1Run3_nvtx30to40`,
and run:
```
./make_mu_plots.sh MyData X _nvtx30to40
```

### 2023 setup

The bash script from 2022 should be somewhat compatible with histograms generated from NANOAOD 
using `performances_nano.py`, but some figures might be broken.

The recommanded scripts for the 2023 setup are the `make_ZToMuMu_plots.py` `make_ZToEE_plots.py` `make_MuonJet_plots.py` `make_PhotonJet_plots.py` python scripts. 

Each script draws all the plots for the corresponding channel.
All the scripts  take the same following inputs:

   - `--dir` The directory to read the inputs files from and draw the plots to.
   - `--config` The YAML configuration file to read from. The default ones are the templates `../config_cards/full_<Channel>.yaml`
   - `--lumi` The integrated luminosity to display in the top right corner of the plot.

`make_<Channel>_plots.py` will look in the input directory for an input file called `all_<Channel>.root`,
and will try to save the plots in a subdirectory called `plotsL1Run3` inside the input directory.
You need to create this subdirectory before running the scripts.

Furthermore, the scripts will only draw a plot if the field for the corresponding
kind is set in the configuration file. For instance, by setting `TurnOns: false`
in the configuration file, the script will not produce any of the turn on plots.
The scripts also rely on the values of the different fields in the configuration files
to look for histograms in the input file.

**You should make sure the configuration file used for producing the plots
is compatible with the one given to `perfomances_nano.py` to fill the histograms**

Otherwise, the script might look for histogram names that are not present
in the input file.
The default cards contain comments on how to use them.

#### Example usage

To draw all plots for muons, for a directory `MyData` containing the input file `MyData/all_ZToMuMu.root`,
produced with the configuration card `my_ZToMuMu_config.yaml`,
and a directory `MyData/plotsL1Run3` to store the plot, corresponding to `X` inverse femtobarns of inverse luminosity, run:
```
python3 make_ZToMuMu_plots.py --dir MyData --config my_ZToMuMu_config.yaml --lumi "X fb^{-1}"
```
Making plots in bins of nvtx is not supported yet.

## Drawing all the plots for all objects

### 2022 setup

The script `draw_all.sh` loops on a (hard-coded) list of directories and calls the for `make_"OBJ"_plots.sh` scripts 
on each of them, with all possible `nvtx_suffix`. It takes no arguments, and can be run by simply calling `./draw_all.sh`
(provided that all needed directories and input files exist).

### 2022 setup

The script `draw_nano.sh` works in a similar way to `draw_all.sh`. 
It internaly calls the `make_<Channel>_plots.py` script, and runs on a (hard-coded) loop.
You can run it by simply calling `./draw_nano.sh`.
