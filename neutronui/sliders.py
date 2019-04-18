''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve sliders.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/sliders

in your browser.

'''
import numpy as np
import neutronpy as npy

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, gridplot
from bokeh.models import ColumnDataSource, Range1d, Label
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, show

# Set up plot
plot1 = figure(plot_height=300, plot_width=300, title="", tools="")
plot2 = figure(plot_height=300, plot_width=300, title="", tools="")
plot3 = figure(plot_height=300, plot_width=300, title="", tools="")

PLOTS = (plot1, plot2, plot3)
QSLICES = ['QxQy', 'QxW', 'QyW']

def generate_data(projections, num=0):
    fill_data = dict()
    line_data = dict()
    limits = dict()
    dQ = dict()

    for qslice in QSLICES:
        dQ1, dQ2 = [], []

        fill_data[qslice + '_x'] = projections[qslice][0, :][:, num]
        fill_data[qslice + '_y'] = projections[qslice][1, :][:, num]

        line_data[qslice + '_x'] = projections[qslice + 'Slice'][0, :][:, num]
        line_data[qslice + '_y'] = projections[qslice + 'Slice'][1, :][:, num]

        dQ1.append(np.max(projections[qslice][0, :][:, num]) - np.min(projections[qslice][0, :][:, num]))
        dQ2.append(np.max(projections[qslice][1, :][:, num]) - np.min(projections[qslice][1, :][:, num]))

        limits[qslice + '_x'] = [np.min(projections[qslice][0, :][:, num]), np.max(projections[qslice][0, :][:, num])]
        limits[qslice + '_y'] = [np.min(projections[qslice][1, :][:, num]), np.max(projections[qslice][1, :][:, num])]

        dQ[qslice + '_dQ1'], dQ[qslice + '_dQ2'] = [np.max(item) for item in [dQ1, dQ2]]

    return fill_data, line_data, limits, dQ


def plot_init(fill_source, line_source, limits, dQ, instrument):
    for plot, qslice in zip(PLOTS, QSLICES):
        plot.patch(qslice + '_x', qslice + '_y', source=fill_source, fill_alpha=0.6)
        plot.line(qslice + '_x', qslice + '_y', source=line_source, line_width=3, color='red')

    render_labels(dQ)
    # set_limits(limits)


def render_labels(dQ):
    for plot, qslice in zip(PLOTS, QSLICES):
        xlabel = 'Q1 (along ' + '{1}) (r.l.u.), dQ1={0:.3f}'.format(dQ[qslice + '_dQ1'], instrument.sample.u)
        if 'W' in qslice:
            ylabel = 'hw (meV), dhw={0:.3f}'.format(dQ[qslice + '_dQ2'])
        else:
            ylabel = 'Q2 (along ' + '{1}) (r.l.u.)' + ', dQ2={0:.3f}'.format(dQ[qslice + '_dQ2'], instrument.sample.v)

        plot.xaxis.axis_label = xlabel
        plot.yaxis.axis_label = ylabel


def set_limits(limits):
    for plot, qslice in zip(PLOTS, QSLICES):
        plot.set(x_range=Range1d(limits[qslice + '_x'][0], limits[qslice + '_x'][1]),
                 y_range=Range1d(limits[qslice + '_y'][0], limits[qslice + '_y'][1]))


instrument = npy.Instrument()
instrument.calc_projections([1, 1, 0, 0])
projections = instrument.projections

fill_data, line_data, limits, dQ = generate_data(instrument.projections)
fill_source = ColumnDataSource(fill_data)
line_source = ColumnDataSource(line_data)

plot_init(fill_source, line_source, limits, dQ, instrument)

# Set up widgets
hkle = TextInput(title="hkle", value='1, 1, 0, 0')
amplitude = Slider(title="k", value=1.0, start=-5.0, end=5.0)
phase = Slider(title="l", value=0.0, start=0.0, end=2 * np.pi)
freq = Slider(title="e", value=1.0, start=0.1, end=5.1)


def update_data(attrname, old, new):
    # Get the current slider values
    hkle_new = [float(item) for item in hkle.value.split(',')]

    instrument.calc_projections(hkle_new)

    fill_data, line_data, limits, dQ = generate_data(instrument.projections)
    fill_source.data, line_source.data = fill_data, line_data

    render_labels(dQ)
    # set_limits(limits)


for w in [hkle, amplitude, phase, freq]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(hkle, amplitude, phase, freq)

curdoc().add_root(row(inputs, gridplot([[plot1, plot2], [None, plot3]])))
curdoc().title = "NeutronPy TAS Resolution"
