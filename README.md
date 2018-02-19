# Overshoot plot

A utility written in Python that plots overshoot data from stellar convective regions.

## Setup

This code requires Python 3.6. Check the you have it installed by typing `python3 -V` or `python 3.6`.
If you don't have Python or have earlier version, please install Python3.6 before proceeding.

Make sure you have `pip3` installed.

On Ubuntu you may need to install tkinker for python 3.6 (not needed on MacOS):
```
sudo apt-get install python3.6-tk
```

Once this is done, setup the following libraries:

```
pip3 install matplotlib
```


## Usage

Clone the repository into a local folder:

```
git clone https://github.com/evgenyneu/OvershootPlot.git
cd OvershootPlot
```

## Plot evolution

Plot parameters that are changing with time:

```
python3 plot_evolution.py
```

To see the options, run:

```
python3 plot_evolution.py -h
```

### Examples of evolution plots

Show the extent of inward overshoot in meters from the intershell convective region #1.

```shell
python3 plot_evolution.py -x=model -y=overshoot_dr_m -t shell -z=1 -d=in
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/overshoot_extent_meter_shell_inwards.png' width='500' alt='Inward overshoot extent meters interhsell convective region #1'>



Show both the inner edge of intershell convective zone and the overshoot for zone 1, measured in mass/MSun.

```
python3 plot_evolution.py -x=model -y=convection_m_msun -y=overshoot_m_msun -t shell -z=1 -d=in
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/inner_overshoot_and_envelope_mass_sun.png' width='500' alt='Overshoot and convective region edge'>

### Evolution plot app

The model plots can be veiwed in an app:

```
python3 gui_evolution.py
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/gui_evolution_plot_2.png' width='800' alt='Overshoot evolution plot GUI'>


## Plot single model

Plot parameters for a single model 150, at one instance of time. The first model is plotted if the model option `-m` is not supplied:

```
python3 plot_model.py -m=170
```

To see the options, run:

```
python3 plot_model.py -h
```

### Examples of single model plots

See how density changes near the overshoot region marked with red lines:

```
python3 plot_model.py -y=rho -m=200
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/overshoot_plot_mode_density_200_3.png' width='500' alt='Overshoot model density'>



Show the change in the oxygen abundance:

```
python3 plot_model.py -x=m_msun -y=abund_o_16 -m=200
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/overshoot_mode_oxygen_200_3.png' width='500' alt='Overshoot model oxygen abundance'>

### Model plot app

The model plots can be veiwed in an app:

```
python3 gui_model.py
```

<img src='https://github.com/evgenyneu/OvershootPlot/raw/master/images/gui_model_plot_3.png' width='800' alt='Overshoot model plot GUI'>