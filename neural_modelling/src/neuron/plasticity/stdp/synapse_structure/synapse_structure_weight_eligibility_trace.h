#ifndef _SYNAPSE_STRUCUTRE_WEIGHT_ELIGIBILITY_TRACE_H_
#define _SYNAPSE_STRUCUTRE_WEIGHT_ELIGIBILITY_TRACE_H_

//---------------------------------------
// Structures
//---------------------------------------
// Plastic synapse types have weights and eligibility traces
typedef int32_t plastic_synapse_t;

// The update state is purely a weight state
typedef weight_state_t update_state_t;

// The final state is just a weight as this is
// Both the weight and the synaptic word
typedef weight_t final_state_t;

//---------------------------------------
// Synapse interface functions
//---------------------------------------
// Synapse parameter get and set helpers
static inline int32_t synapse_structure_get_weight(plastic_synapse_t state) {
    return (state >> 16);
}

static inline int32_t synapse_structure_get_eligibility_trace(plastic_synapse_t state) {
    return (state & 0xFFFF);
}

static inline int32_t synapse_structure_update_state(int32_t trace, int32_t weight) {
    return (plastic_synapse_t)(weight << 16 | trace);
}

#endif  // _SYNAPSE_STRUCUTRE_WEIGHT_ELIGIBILITY_TRACE_H_