#ifndef _ADDITIONAL_INPUT_POTASSIUM_
#define _ADDITIONAL_INPUT_POTASSIUM_

#include "additional_input.h"

//----------------------------------------------------------------------------
//----------------------------------------------------------------------------

typedef struct additional_input_t {

    // Potassium Current
    accum    I_DK;
    accum    m;         // not used here
    accum    m_inf;
    accum    D;         // instead of h
    accum    NaInflux;  // instead of h_inf
    accum    e_to_t_on_tau;
    accum    e_to_t_on_tau_h;  // not used here
    accum    g_DK;      // max potassium conductance
    accum    E_DK;      // potassium reversal potential
    accum    dt;

} additional_input_t;

static input_t additional_input_get_input_value_as_current(
        additional_input_pointer_t additional_input,
        state_t membrane_voltage) {

    profiler_write_entry_disable_irq_fiq(
        PROFILER_ENTER | PROFILER_INTRINSIC_CURRENT);

    additional_input->g_DK = 1.25k;

	additional_input->e_to_t_on_tau = 1.00008k;  // exp(0.1/1250)

    additional_input->NaInflux = 0.025k
        / (1k + expk(-(membrane_voltage- -10k) * 0.2k)); //1/5 = 0.2

    accum D_infinity = 1250k * additional_input->NaInflux + 0.001k;

	// Update D (Same form as LIF dV/dt solution)
	additional_input->D = D_infinity +
        (additional_input->D - D_infinity) * additional_input->e_to_t_on_tau;

	additional_input->m_inf = 1k / (1k + (0.0078125k /                          // 0.25^3.5 = 0.0078125
                                          (additional_input->D
                                           * additional_input->D
                                           * additional_input->D)));            // TODO: Actual exponent is D^3.5.

	additional_input->I_DK = -
	    additional_input->g_DK *
		additional_input->m_inf *
		(membrane_voltage - -90k); //additional_input->E_H);

/*
	log_info("mem_V: %k, D: %k, m_inf: %k, NaInflux: %k, I_DK = %k",
			membrane_voltage,
			additional_input->D,
			additional_input->m_inf,
			additional_input->NaInflux,
			additional_input->I_DK);
*/
    profiler_write_entry_disable_irq_fiq(
        PROFILER_EXIT | PROFILER_INTRINSIC_CURRENT);

    return additional_input->I_DK;
}

static void additional_input_has_spiked(
        additional_input_pointer_t additional_input) {
	// no action to be taken on spiking
}

#endif // _ADDITIONAL_INPUT_PACEMAKER_H_