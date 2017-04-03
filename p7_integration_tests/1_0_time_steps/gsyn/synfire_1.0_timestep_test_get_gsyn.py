"""
Synfirechain-like example
"""

import unittest

import p7_integration_tests.scripts.synfire_run as synfire_run
import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker
import spynnaker.gsyn_tools as gsyn_tools

n_neurons = 10  # number of neurons in each population
max_delay = 14.4
timestep = 1
neurons_per_core = n_neurons/2
delay = 1.7
runtime = 50


class TestGetGsyn(unittest.TestCase):
    """
    tests the printing of get gsyn given a simulation
    """
    def test_get_gsyn(self):
        results = synfire_run.do_run(n_neurons, max_delay=max_delay,
                                     timestep=timestep,
                                     neurons_per_core=neurons_per_core,
                                     delay=delay,
                                     runtimes=[runtime])
        (v, gsyn, spikes) = results
        self.assertEquals(12, len(spikes))
        spike_checker.synfire_spike_checker(spikes, n_neurons)
        gsyn_tools.check_sister_gysn(__file__, n_neurons, runtime, gsyn)


if __name__ == '__main__':
    results = synfire_run.do_run(n_neurons, max_delay=max_delay,
                                 timestep=timestep,
                                 neurons_per_core=neurons_per_core,
                                 delay=delay,
                                 runtimes=[runtime])
    (v, gsyn, spikes) = results
    print len(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v)
    plot_utils.heat_plot(gsyn)
    gsyn_tools.check_sister_gysn(__file__, n_neurons, runtime, gsyn)
