import streamlit as st
import numpy        as np
import random
import math
import json
import test_functions


st.set_page_config(
     page_title='HVDC MAIN',
     layout="wide",
     initial_sidebar_state="expanded",
)


##########################
# Main body of cheat sheet
##########################
#def cs_body():

st.title('⚡ Optimal design verification device for HVDC main setpoint calculation made by Kepco')
st.subheader('Frame the problem')


# Read JSON
with open('test_functions.json') as f:
    data = json.load(f)

test_functions_list = []
for key, value in data.items():
    
    test_functions_list.append(key)

func_pointer_dict = {
  'Firing_Angle': test_functions.firing_function,
  'Extinction_Angle': test_functions.extinction_function,
  'Main_Transfomer_Voltage': test_functions.main_transfomer_voltage_function,  
  'Reactive_Power': test_functions.reactive_Power_function,  
  'Untitled': test_functions.untitled_function,  
}

# Problem Statement and Parameters
#function_input = st.selectbox('Choose test function', sorted(test_functions_list))
#print(function_input)
# Latex Equation
st.markdown('The test function is a minimization problem and it is given by:')


# # Optimal values and its arguments
# st.markdown('The optimal value is: ' + str(data[function_input][0]['optimal']))

# # Retrieve optimization type
# optimization_type_input = data[function_input][0]['optimization_type']

# # Max number of variables
# if data[function_input][0]['max_variables'] > 3:
#     max_var = 3
# else:
#     max_var = 2

# n_variables = st.slider('Set number of variables/dimensions', 1, data[function_input][0]['max_variables'], max_var)

# if n_variables <= 3:
#     st.markdown("The optimal value is given by the following arguments: " + str([data[function_input][0]['arguments']] * n_variables))
# else:
#     st.markdown("The optimal value is given by the following arguments: [" + str(data[function_input][0]['arguments']) + ", ... , " + str(data[function_input][0]['arguments'])+"]")

# # Interval size
# interval = st.slider(
#     'Choose the bounded constraints of the interval',
#     data[function_input][0]['interval_min'],
#     data[function_input][0]['interval_max'],
#     (data[function_input][0]['interval_min'], data[function_input][0]['interval_max']))

st.markdown('Now that problem is set, please reach out to the sidebar to choose and tune your advanced arithmetic.')


# 왼쪽 사이드바 알고리즘 시작(Algorithm)
algorithm = st.sidebar.selectbox(
     '🛠️ Choose the Design algorithm you want to play with',
     ['선택하세요','주회로 정수', '절연협조'])
if algorithm == '주회로 정수':
    #test_functions.ackley_function(data)
    # selection_pointer_dict = {
    #     'Roulette': selection_methods.roulette_selection_method,
    #     'Log Roulette': selection_methods.log_roulette_selection_method,
    #     'Tournament': selection_methods.tournament_selection_method,
    # }

    # crossover_pointer_dict = {
    #     'Single Point': crossover_methods.single_point_crossover_method,
    # }

    # mutation_pointer_dict = {
    #     'Single Point A': mutation_methods.single_point_a_mutation_method,
    #     'Single Point B': mutation_methods.single_point_b_mutation_method,
    # }

    # elitism_pointer_dict = {
    #     'Elitism': elitism_methods.elitism,
    # }
    #function_input = st.selectbox('Choose test function', sorted(test_functions_list))
    selection_method_input = st.sidebar.selectbox('🔍 Detail Selection Method', sorted(test_functions_list))
    # selection_method_input = selection_pointer_dict[selection_method_input]
    global df_value
    if selection_method_input == 'Firing_Angle':
        df_value = test_functions.firing_function(data,selection_method_input)
    if selection_method_input == 'Extinction_Angle':
        df_value = test_functions.extinction_function(data,selection_method_input)
    if selection_method_input == 'Main_Transfomer_Voltage':
        df_value = test_functions.main_transfomer_voltage_function(data,selection_method_input)
    if selection_method_input == 'Reactive_Power':
        df_value = test_functions.reactive_Power_function(data,selection_method_input)

    st.dataframe(df_value) 

if st.sidebar.button('Run'):

    st.subheader('Optimization Results')

#     if algorithm == 'Genetic Algorithm':
#        optimization_result, arguments_result = genetic_algorithm.genetic_algorithm(interval, n_variables, bits_number, n_individuals, n_max_gen, selection_method_input, crossover_method_input, crossover_probability_input, mutation_method_input, mutation_probability_input, elitism_method_input, elitism_probability_input, func_pointer_dict[function_input], optimization_type_input, seed)

#     elif algorithm == 'Particle Swarm':
#        optimization_result, arguments_result = particle_swarm.pso(interval, n_variables, n_individuals, n_max_gen, func_pointer_dict[function_input], optimization_type_input, w_min_input, w_max_input, c1, c2, particle_swarm.clipper, seed)

    st.markdown('The expected value was '  '.')
    st.markdown('The arguments which brought this result are '  '.')
    st.markdown('The expected arguments were ' '.')

    st.warning(
        "⚠️ *Note:* Your input data will be deduplicated"
        " on the selected column to reduce computation requirements."
        " You will need to re-join the results on your offense text column."
    )
st.info("""
            Feel free to reach out if you want to learn more about hvdc algorithms, colaborate with the project or hire me for any Data Science, Machine Learning and Optimization demand you might have.
            Developed by: [Kepco Yi](https://) | Source: [GitHub](https://github.com/)
        """)

