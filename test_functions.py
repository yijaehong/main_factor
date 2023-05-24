import numpy as np
import random
import math
import streamlit as st
import pandas as pd
#from matplotlib.backends.backend_agg import RendererAgg


df=pd.DataFrame(index=['main_character']) 
"""
최소점호운전각 : min_fire_oper_angle
최대점호운전각 : max_fire_oper_angle
△Qrr         : qrr_value
△T(us)       : t_us_value
△T(º)        : t_angle_value
최소절대소호각 : min_extinction_angle
소호운전각     : extinction_oper_angle
"""

#_lock = RendererAgg.lock


def firing_function(data,function_input):
    st.latex(data[function_input][0]['latex'])
    """점호각 선정 Function"""

    dataset_container = st.expander("🛠️ 최소 운전 점호각(Firing Angle) 선정 입력값?", True)
    with dataset_container:  
        # 역상분
        n_angle_variables = st.slider('Set number of variables/역상분(a) 입력', data[function_input][0]['min_variables'],
            data[function_input][0]['max_variables'], data[function_input][0]['origin_value'],
            data[function_input][0]['interval'])

        # 전압변동율
        n_voltage_variables = st.slider(
            'Set number of variables/전압변동율 여유(b)', data[function_input][0]['min_variables'],
            data[function_input][0]['max_variables'], 1.5,
            data[function_input][0]['interval'])

    n_firing_angle_variables=math.acos((100-n_angle_variables-n_voltage_variables)/100) #임시 계산 변수
    min_fire_oper_angle_origin = n_firing_angle_variables*180/3.14
    min_fire_oper_angle = math.ceil(min_fire_oper_angle_origin)  #반올림
    st.write('최소 운전 점호각(Firing Angle) : ',min_fire_oper_angle)
    


    st.latex(data[function_input][0]['latex2'])
    dataset_container2 = st.expander("최대 운전 점호각(Firing Angle) 선정 입력값?", True)
    with dataset_container2:  
        # deadband여유
        n_dead_variables = st.slider('Set number of variables/DeadBand 여유(a) 입력', data[function_input][0]['min_variables2'],
            data[function_input][0]['max_variables2'], data[function_input][0]['origin_value2'],data[function_input][0]['interval2'])

        # 측정설비 오차
        n_measure_variables = st.slider(
            'Set number of variables/측정설비 오차(b)', data[function_input][0]['min_variables3'],
            data[function_input][0]['max_variables3'],  data[function_input][0]['origin_value3'],
            data[function_input][0]['interval3'])

    n_firing_angle_variables_oper=math.acos(math.cos(min_fire_oper_angle*3.14/180)/(1+n_dead_variables/100)) #임시 계산 변수
    max_fire_oper_angle_origin = n_firing_angle_variables_oper*180/3.14
    max_fire_oper_angle = math.ceil(max_fire_oper_angle_origin) #반올림
    st.write('최대 운전 점호각(Firing Angle) : ',max_fire_oper_angle)

    seperation_line()
    #if st.button('Add'):
    if (min_fire_oper_angle):
        df=dataframe_create('Mix Operation Firing Angle',min_fire_oper_angle)    
    if (max_fire_oper_angle):
        df=dataframe_create('Max Operation Firing Angle',max_fire_oper_angle)
    #st.dataframe(df.style.highlight_max(axis=1))
    return df


def extinction_function(data,function_input):
    qrr_col, delta_v_col = st.columns(2)
    with qrr_col:    
        st.latex(data[function_input][0]['latex'])
        st.latex(data[function_input][0]['latex2'])
        st.latex(data[function_input][0]['terms'])        
        """소호각 선정 Function"""
        e_qrr_container = st.expander("△Qrr(Reverse recovery charge) 선정 입력값?", expanded=True)
        with e_qrr_container:  
            # 델타 Qrr
            e_dtdi = st.number_input('Set number of (dt/di)', 10, 500, 300,10)
            e_prv = st.number_input('Set number of (PRV)', 1.0, 20.0, 8.3,0.1)
            e_nt = st.number_input('Set number of (nT)', 1, 100,69,1)
            e_tj = st.number_input('Set number of (Tj)', 10, 100, 90,1)
        x1=(e_dtdi*0.025)**0.53
        y1=(e_prv/(e_nt*3.5))**0.154
        z1=math.exp(0.01*(e_tj-90))
        qrr_value=round(750*x1*y1*z1,3) #Qrr 값
        st.write('△Qrr  : ', qrr_value)

    with delta_v_col: 
        st.latex(data[function_input][0]['latex3'])
        e_t_container = st.expander("△T(Forward current decrease rate) 선정 입력값?", True)
        
        with e_t_container:        
            # 델타 T
            e_dvdt = st.number_input('Set number of (dv/dt)', 100, 10000, 7000,100)
            e_cd = st.number_input('Set number of (Cd)', 0.0, 2.0, 1.0,0.1)

        t_us_value=qrr_value/(e_cd*e_dvdt)
        t_angle_value=round((t_us_value/(7.3/337.6)),1)

        #turn off 타임관련 데어터셋을 만들어서 비교할것
        if t_angle_value:
            df=dataframe_open()
            st.dataframe(data=df)        
            zz=float(df.loc[df['temperature'] == e_tj,'angle'])
            
        st.write('[ Turn off time 선정 ]',zz)
        st.write('[ △T(º) ]', t_angle_value)
        min_extinction_angle= t_angle_value + zz
        st.write('최소 절대 소호각',float(min_extinction_angle))

        extinction_oper_angle=round(oper_extinction_function(min_extinction_angle),1) #운전 소호각 선정
        st.write('운전 소호각', extinction_oper_angle)
    
    if (min_extinction_angle):
        df=dataframe_create('Min Extinction Angle',min_extinction_angle)
    if (extinction_oper_angle):
        df=dataframe_create('Operation Extinction Angle',extinction_oper_angle)        
    #st.dataframe(df.style.highlight_max(axis=1))
    return df

def oper_extinction_function(min_extinction_angle):
    """운전 소호각 선정 Function"""   
    n_min_extinction_angle=math.ceil(min_extinction_angle) * 3.14 / 180
    n_oper_extinction_angle= math.acos(math.cos(n_min_extinction_angle)/(1+(3/100))) #임시 계산 변수
    n_extinction_oper_angle = n_oper_extinction_angle*180/3.14
    return n_extinction_oper_angle

def dataframe_open(): 
    file_path = './timeoff_data.csv'
    df1 = pd.read_csv(file_path)
        #이하 문자은 함수를 만들어 입력해 볼것 
    return df1
def dataframe_create(column_name,column_value):   
    global df
    if column_name:
        df[column_name]=column_value
    return df
def seperation_line():      
    st.markdown("---")

def main_transfomer_voltage_function(data,function_input):
    with st.container():    
        voltage_col, power_impedance_col = st.columns(2)
        with voltage_col:
            st.subheader('🎛️ Converter transformer Winding Rating Voltage(kV)')            
            st.latex(data[function_input][0]['latex'])
            st.latex(data[function_input][0]['terms'])
            tr_voltage_container = st.expander("main transformer voltage ?", True)       
            with tr_voltage_container:  
        # 권선 정격 전압
                mtr_valve_v = st.number_input('Set number of 공칭 DC전압(Vdn) ', 10, 1000, 500,10)
                mtr_valve_i = st.number_input('Set number of 공칭 DC전류(Idn)', 100, 10000,4000,5)
                fire_angle = st.number_input('Set number of 점호각(알파)', 1.0, 50.0,15.5,0.5)
                mtr_impedance = st.number_input('Set number of 변압기 임피던스(Xc)', 1.0, 50.0, 6.74,1.0)
            temp_a=3.14/(3*math.sqrt(2))
            temp_b=((mtr_valve_v/2)+((3/3.14)*mtr_impedance*(mtr_valve_i/1000)))   
            mtr_winding_2ndv= round(temp_a*(temp_b/math.cos(math.pi * (fire_angle / 180))),2)
            st.write('변환용 변압기 밸브측 정격 전압',mtr_winding_2ndv)

        with power_impedance_col:
            st.subheader('🏷️Converter transformer Rating Power & impedance(Ω)')   
            st.latex(data[function_input][0]['latex3'])
            st.latex(data[function_input][0]['terms3'])
            tr_power_container = st.expander("main transformer Rating Power ?", True)       
            with tr_power_container:  
        # 변압기 정격용량, mtr_winding_2ndv 값의 유무비교문 넣을것
                mtr_valve_p_v = st.number_input('Set number of 밸브 측 권선의 정격 전압(VLN) ', 10.0, 1000.0, mtr_winding_2ndv,10.0)
                mtr_valve_p_i = st.number_input('Set number of 공칭 DC전류(Idn)_2', 100, 10000,4000,5)
            mtr_winding_rating_power=round(math.sqrt(2) * mtr_valve_p_v * (mtr_valve_p_i /1000),2)
            st.write('변환용 변압기 정격 용량',mtr_winding_rating_power)


            st.latex(data[function_input][0]['latex2'])
            st.latex(data[function_input][0]['terms2'])      
            tr_impedance_container = st.expander("main transformer 임피던스 ?", True)       
            with tr_impedance_container:  
                # 임피던스
                mtr_winding_v = st.number_input('Set number of 권선 공칭전압(Uvnom) ', 10, 500, 212,1)
                mtr_power = st.number_input('Set number of 3상 용량(MVA)', 500, 2500, 1200,10)
                mtr_p_impedance = st.number_input('Set number of %임피던스(Zxmer)', 0.0, 1.0, 0.18 ,0.01)
            mtr_impedance= (mtr_p_impedance*math.pow(mtr_winding_v, 2))/mtr_power
            st.write('main transformer 임피던스 Xc',float(mtr_impedance))  

    seperation_line()

    row3_space1, pretap_value_col, row3_space2, tap_col, row3_space4 = st.columns((.1, 1, .1, 1, .1))

    with pretap_value_col: 
        st.subheader("🔃 transformer tap variable(Uvw min, max) ")        
        tr_tap_value_container1 = st.expander("Uvm min값 ?", True)       
        with tr_tap_value_container1:  
            # Uvm min
            mtr_tap_v1 = st.number_input('Set number of 최소부하 권선 공칭전압(Vd)', 10, 800, 450,5)
            mtr_tap_alpha1 = st.number_input('Set number of 최소부하 점호/소호각(α, γ)', 1.0, 50.0, 18.0,0.5)
            mtr_tap_i1 = st.number_input('Set number of 최소부하 공칭 DC전류(Id)', 100, 10000,200,5)
            
        mtr_tap_uvm_min=round((mtr_tap_v1/2 + mtr_tap_i1*mtr_impedance/1000)/math.cos((math.pi * ( mtr_tap_alpha1/ 180)))*3.14/3,2)
        st.write('Uvm min값',float(mtr_tap_uvm_min))  

        tr_impedance_container2 = st.expander("Uvm max값 ?", True)       
        with tr_impedance_container2:  
            # Uvm max
            mtr_tap_v2 = st.number_input('Set number of 권선 최대부하 공칭전압(Vd)', 10, 800, 505,5)
            mtr_tap_alpha2 = st.number_input('Set number of 최대부하 점호/소호각(α, γ)', 1.0, 50.0, 18.0,0.5)
            mtr_tap_i2 = st.number_input('Set number of 최대부하 공칭 DC전류(Id)', 100, 10000,4000,5)
        mtr_tap_uvm_max=round((mtr_tap_v2/2 + mtr_tap_i2*mtr_impedance/1000)/math.cos((math.pi * ( mtr_tap_alpha2/ 180)))*3.14/3,2)
        st.write('Uvm max값',float(mtr_tap_uvm_max))   

    with tap_col:
        st.subheader('📉 Converter transformer Tap')
        st.latex(data[function_input][0]['latex4'])
        st.latex(data[function_input][0]['latex5']) 
        st.markdown("<p>1. 주요 변수<br>  UAC_nom : Nominal AC Voltate [kV]<br>  UAC_max/min : 계통 최대/최소 AC Voltate [kV]<br>  UVW_nom : V/V에 걸리는 Nominal Voltate [kV]<br>  UVW_max/min : V/V에 걸리는 최대/최소 Voltate [kV] *<br>"
            "2. calculate UVW_max/min <br>"
            "3. calculate min/max tap range! :sparkles:</p>", unsafe_allow_html=True)


        tr_tap_container = st.expander("main transformer Tap Negative ?", True)       
        with tr_tap_container:  
        # 임피던스
            mtr_v_U2nom=math.ceil(mtr_winding_2ndv* math.sqrt(2))
            mtr_v_U1min = st.number_input('Set number of U1min ', 10, 500, 328,1)
            mtr_v_U1max = st.number_input('Set number of U1max', 10, 500, 362,1)
            mtr_v_U1nom = st.number_input('Set number of U1nom ',  10, 500, 345,1)
            mtr_v_U2nom = st.number_input('Set number of U2nom',  10, 500,mtr_v_U2nom ,1)
        mtr_tap_uvm_max=round((mtr_v_U1min/mtr_v_U1nom)*(mtr_v_U2nom/mtr_tap_uvm_max)-1,3)
        mtr_tap_uvm_min=round((mtr_v_U1max/mtr_v_U1nom)*(mtr_v_U2nom/mtr_tap_uvm_min)-1,3)
        st.write('Max Tap Range:',float(mtr_tap_uvm_max))   
        st.write('Min Tap Range:',float(mtr_tap_uvm_min))  

    seperation_line()
    if (mtr_winding_2ndv):
        df=dataframe_create('Mtr Winding Voltage',mtr_winding_2ndv)        
    if (mtr_winding_rating_power):
        df=dataframe_create('Mtr Rating Power',mtr_winding_rating_power)
    if (mtr_impedance):
        df=dataframe_create('Mtr Impedance',mtr_impedance)        
    #st.dataframe(df.style.highlight_max(axis=1))
    return df

def reactive_Power_function(data,function_input):
    st.markdown("---")
    Q_col, Per_Q_col = st.columns(2)
    with Q_col:
        st.subheader('🎛️ reactive power absorption of the converter at DC current[p.u]')            
        st.latex(data[function_input][0]['latex'])
        st.latex(data[function_input][0]['terms'])        
        reactive_container = st.expander("Reactive power ?", True)       
        with reactive_container:  
    # 권선 정격 전압,  기본입력값으로 불러올것
            reactive_total_p = st.slider('Set number of 무효전력 계산_P total(MVA) ', 10, 5000, 4000,10)
            reactive_rpc_q = st.slider('Set number of 무효전력 계산_최소 Q(Reactive Power) RPC하단값 ? ', 100, 1000,800,5)
            reactive_fire_angle = st.slider('Set number of 무효전력 계산_ 점호각(알파)', 1.0, 50.0,15.5,0.5)
            reactive_impedance = st.slider('Set number of 무효전력 계산_ 변압기  % 임피던스(%z)', 1.0, 50.0, 18.0,1.0)
        Q_pu_value=round(math.tan(math.acos(math.cos(3.14*(reactive_fire_angle/180))-((reactive_impedance/100)/2))),3)
        #Q_pu_value=math.tan(math.acos(math.cos(math.pi*(reactive_fire_angle/180))-(reactive_impedance/2)))
        Q_total_value=round(reactive_total_p*Q_pu_value-reactive_rpc_q,2)
        st.write('전체 무효전력 (Q_total)',Q_total_value)          
        st.write('무효전력 소비량(Q_dc)',Q_pu_value)

    with Per_Q_col:
        st.subheader('🎛️ Converter transformer Winding Rating Voltage(kV)')   
        st.latex(data[function_input][0]['latex1'])
        st.latex(data[function_input][0]['terms1']) 
        reactive_container = st.expander("Reactive power ?", True)       
        with reactive_container:  
    # 권선 정격 전압,  기본입력값으로 불러올것
            reactive_scl_min = st.slider('Set number of 최소 단락용량(SCLmin)', 10000, 30000, 20400,10)
            reactive_delta_voltage = st.slider('Set number of 전압 변동율(ΔV, 기술규격서 참고) ? ', 0.0, 20.0,1.5,0.1)
            reactive_control_margin = st.radio("제어전략 선택",('Angle_CEA', 'Tap_Control'))
        Q_switch=round(reactive_scl_min*reactive_delta_voltage/100,2)
        if reactive_control_margin == 'Angle_CEA' : Q_switch_apply=Q_switch*1
        elif reactive_control_margin == 'Tap_Control' : Q_switch_apply=Q_switch*2
        #Q_pu_value=math.tan(math.acos(math.cos(math.pi*(reactive_fire_angle/180))-(reactive_impedance/2)))
        Q_total_value=round(reactive_total_p*Q_pu_value-reactive_rpc_q,2)
        st.write('단일 무효전력량',Q_switch)          
        st.write('단일 무효전력량(제어전략 적용)',Q_switch_apply)
    st.markdown("---")

    Q_Total, Filter_col = st.columns(2)
    with Q_Total:
        st.subheader('Total reactive power of the converter and Filter calculation')            

    # 권선 정격 전압,  기본입력값으로 불러올것
        filter_count=math.ceil(Q_total_value/Q_switch)  
        filter_unit_capacity=Q_total_value/filter_count     
        st.metric(label="Total reactive power", value=Q_total_value)
        st.metric(label="Filter count", value=filter_count)  
        st.metric(label="Filter unit capacity", value=filter_unit_capacity) 
    
    with Filter_col:
        st.subheader('If the C value per standard filter is exceeded, the number of filters is adjusted') 

        Single_C_Max_Q_Supply=filter_unit_capacity*math.pow(1.05,2)*60.2/60*1.02
        if filter_unit_capacity < Single_C_Max_Q_Supply:
            ad_filter_count=filter_count+1  
            ad_filter_unit_capacity=Q_total_value/ad_filter_count     
            st.metric(label="Total reactive power", value=Q_total_value)
            st.metric(label="Filter count", value=ad_filter_count,delta=ad_filter_count-filter_count)  
            st.metric(label="Filter unit capacity", value=ad_filter_unit_capacity, delta=round(ad_filter_unit_capacity-filter_unit_capacity,1)) 

    seperation_line()
    if (ad_filter_count):
        df=dataframe_create('filter Count',ad_filter_count)        
    if (ad_filter_unit_capacity):
        df=dataframe_create('filter unit Capacity',ad_filter_unit_capacity)

    return df


def untitled_function(transposed_decimal_pop_input):
    """Untitled Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        untitled = 0
        parentheses = 0
        term_1 = 0
        term_2 = 1

        for xi in individual:
            parentheses = parentheses + xi**2
            term_2 = term_2*(math.cos(20*math.pi*xi))
        term_1 = parentheses/2
        untitled = term_1 - term_2 + 2
        y.append(untitled)
    return y