from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard
from spynnaker.pyNN.models.defaults import default_initial_values
from spynnaker.pyNN.models.neuron.synapse_types import ExpIzhikevichNeuromodulated
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic
from spynnaker.pyNN.models.neuron.neuron_models import NeuronModelIzh



_IZK_THRESHOLD = 30.0

class IZKCurrExpIzhikevichNeuromodulation(AbstractPyNNNeuronModelStandard):
    """ Izhikevich neuron with an exponentially decaying \
        current input
    """

    @default_initial_values({"v", "u", "isyn_exc", "isyn_inh"})
    def __init__(
            self, a=0.02, b=0.2, c=-65.0, d=2.0, i_offset=0.0, u=-14.0,
            v=-70.0, tau_syn_E=5.0, tau_syn_I=5.0, isyn_exc=0.0, isyn_inh=0.0):
            
        # pylint: disable=too-many-arguments, too-many-locals
        neuron_model = NeuronModelIzh(
            a, b, c, d, v, u, i_offset)
        synapse_type = ExpIzhikevichNeuromodulated(
            tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)
        input_type = InputTypeCurrent()
        threshold_type = ThresholdTypeStatic(_IZK_THRESHOLD)
        
      
       
        super(IZKCurrExpIzhikevichNeuromodulation, self).__init__(
            model_name="IZK_curr_exp_stdp_izhikevich_neuromodulation",
            binary="IZK_curr_exp_stdp_izhikevich_neuromodulation.aplx",
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
            
          
