# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spinn_front_end_common.utilities.connections import LiveEventConnection
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities.constants import NOTIFY_PORT


class SpynnakerPoissonControlConnection(LiveEventConnection):
    __slots__ = [
        "__control_label_extension"]

    def __init__(
            self, poisson_labels=None, local_host=None, local_port=NOTIFY_PORT,
            control_label_extension="_control"):
        """

        :param poisson_labels: Labels of Poisson populations to be controlled
        :type poisson_labels: iterable of str
        :param local_host: Optional specification of the local hostname or\
            IP address of the interface to listen on
        :type local_host: str
        :param local_port: Optional specification of the local port to listen\
            on.  Must match the port that the toolchain will send the\
            notification on (19999 by default)
        :type local_port: int
        :param control_label_extension:\
            The extra name added to the label of each Poisson source
        :type control_label_extension: str

        """
        control_labels = None
        if poisson_labels is not None:
            control_labels = [
                "{}{}".format(label, control_label_extension)
                for label in poisson_labels
            ]

        super(SpynnakerPoissonControlConnection, self).__init__(
            live_packet_gather_label=None, send_labels=control_labels,
            local_host=local_host, local_port=local_port)

        self.__control_label_extension = control_label_extension

    def add_poisson_label(self, label):
        self.add_send_label(self._control_label(label))

    def _control_label(self, label):
        return "{}{}".format(label, self.__control_label_extension)

    @overrides(LiveEventConnection.add_start_callback)
    def add_start_callback(self, label, start_callback):
        super(SpynnakerPoissonControlConnection, self).add_start_callback(
            self._control_label(label), start_callback)

    @overrides(LiveEventConnection.add_start_resume_callback)
    def add_start_resume_callback(self, label, start_resume_callback):
        super(SpynnakerPoissonControlConnection, self)\
            .add_start_resume_callback(
            self._control_label(label), start_resume_callback)

    @overrides(LiveEventConnection.add_init_callback)
    def add_init_callback(self, label, init_callback):
        super(SpynnakerPoissonControlConnection, self).add_init_callback(
            self._control_label(label), init_callback)

    @overrides(LiveEventConnection.add_receive_callback)
    def add_receive_callback(self, label, live_event_callback,
                             translate_key=False):
        raise ConfigurationException(
            "SpynnakerPoissonControlPopulation can't receive data")

    @overrides(LiveEventConnection.add_pause_stop_callback)
    def add_pause_stop_callback(self, label, pause_stop_callback):
        super(SpynnakerPoissonControlConnection, self).add_pause_stop_callback(
            self._control_label(label), pause_stop_callback)

    def set_rate(self, label, neuron_id, rate):
        """ Set the rate of a Poisson neuron within a Poisson source

        :param label: The label of the Population to set the rates of
        :param neuron_id: The neuron ID to set the rate of
        :param rate: The rate to set in Hz
        """
        self.set_rates(label, [(neuron_id, rate)])

    def set_rates(self, label, neuron_id_rates):
        """ Set the rates of multiple Poisson neurons within a Poisson source

        :param label: The label of the Population to set the rates of
        :param neuron_id_rates: A list of tuples of (neuron ID, rate) to be set
        """
        control_label = label
        if not control_label.endswith(self.__control_label_extension):
            control_label = self._control_label(label)
        datatype = DataType.S1615
        atom_ids_and_payloads = [(nid, datatype.encode_as_int(rate))
                                 for nid, rate in neuron_id_rates]
        self.send_events_with_payloads(label, atom_ids_and_payloads)
