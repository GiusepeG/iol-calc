# -*- coding: utf-8 -*-

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

opts = Options()  # options for chromedriver
opts.add_argument("--window-size=1000,800")  # specifies window width,height
opts.add_argument("headless")  # runs without the browser visible
exe_path = chromedriver_binary.chromedriver_filename
chromedriver = None # initialize chromedriver global variable.

# TODO: fix warning
# https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
def start_chromedriver():
	global chromedriver  # use the global chromedriver variable.
	chromedriver = webdriver.Chrome(executable_path=exe_path, options=opts)
	chromedriver.get('https://calc.apacrs.org/barrett_universal2105/')

	## preemptively clear form, just in case: ##
	reset_form_button = chromedriver.find_element(By.ID, 'MainContent_btnReset')
	reset_form_button.click()

def quit_chromedriver():
	global chromedriver  # use the global chromedriver variable.
	chromedriver.quit()

def reset_form():
	global chromedriver  # use the global chromedriver variable.
	reset_form_button = chromedriver.find_element(By.ID, 'MainContent_btnReset')
	reset_form_button.click()	

def calculate_values():
	global chromedriver  # use the global chromedriver variable.
	calculate_button = chromedriver.find_element(By.ID, 'MainContent_Button1')
	calculate_button.click()

# models = ['Alcon SN60WF', 'Alcon SN6AD', 'Alcon SN6ATx', 'Alcon SND1Tx', 'Alcon SV25Tx', 
# 			'Alcon SA60AT', 'Alcon MN60MA', 'AMO ZCB00', 'AMO ZCT', 'AMO AR40e', 'AMO AR40M', 
# 			'Zeiss 409M', 'Zeiss 709M', 'Hoya iSert 251', 'Hoya iSert 351', 
# 			'Bausch &amp; Lomb MX60', 'Bausch &amp; Lomb BL1UT', 'Bausch &amp; Lomb LI60AO']
def select_IOL_model(patient_data: dict):
	model_val = patient_data['IOL_model']
	iol_model_elem = Select(chromedriver.find_element(By.ID, 'MainContent_IOLModel'))
	iol_model_elem.select_by_value(model_val)

def get_IOL_model_values() -> tuple:
	lens_factor_elem = chromedriver.find_element(By.ID, 'MainContent_LensFactor')  # (-2.0 ~ 5.0)
	a_constant_elem  = chromedriver.find_element(By.ID, 'MainContent_Aconstant')   # (112 ~ 125)
	lens_factor_val  = lens_factor_elem.get_attribute('value')
	a_constant_val   = a_constant_elem.get_attribute('value')
	return lens_factor_val, a_constant_val

def input_OD(patient_data: dict):
	R_axial_length_elem = chromedriver.find_element(By.ID, 'MainContent_Axlength')    # 12~38 mm
	R_meas_K1_elem      = chromedriver.find_element(By.ID, 'MainContent_MeasuredK1')  # 30~60 D
	R_meas_K2_elem      = chromedriver.find_element(By.ID, 'MainContent_MeasuredK2')  # 30~60 D 
	R_optical_ACD_elem  = chromedriver.find_element(By.ID, 'MainContent_OpticalACD')  # 0~6 mm
	# R_refraction_elem = chromedriver.find_element(By.ID, 'MainContent_Refraction')  # -10~10 D

	R_axial_length_elem.send_keys(str(patient_data['axial_length']))
	R_meas_K1_elem.send_keys(str(patient_data['meas_K1']))
	R_meas_K2_elem.send_keys(str(patient_data['meas_K2']))
	R_optical_ACD_elem.send_keys(str(patient_data['optical_ACD']))
	# R_refraction_elem.send_keys(str(patient_data['']))

	# optional # 
	R_lens_thickness_elem = chromedriver.find_element(By.ID, 'MainContent_LensThickness')  # 2~8 mm
	R_wtw_elem            = chromedriver.find_element(By.ID, 'MainContent_WTW')            # 8~14 mm

	if 'lens_thickness' in patient_data:
		R_lens_thickness_elem.send_keys(str(patient_data['lens_thickness']))
	if 'wtw' in patient_data:
		R_wtw_elem.send_keys(str(patient_data['wtw']))

def input_OS(patient_data: dict):
	L_axial_length_elem = chromedriver.find_element(By.ID, 'MainContent_Axlength0')    # 12~38 mm
	L_meas_K1_elem      = chromedriver.find_element(By.ID, 'MainContent_MeasuredK10')  # 30~60 D
	L_meas_K2_elem      = chromedriver.find_element(By.ID, 'MainContent_MeasuredK20')  # 30~60 D 
	L_optical_ACD_elem  = chromedriver.find_element(By.ID, 'MainContent_OpticalACD0')  # 0~6 mm 
	# L_refraction_elem = chromedriver.find_element(By.ID, 'MainContent_Refraction0')  # -10~10 D

	L_axial_length_elem.send_keys(str(L_axial_length))
	L_meas_K1_elem.send_keys(str(L_meas_K1))
	L_meas_K2_elem.send_keys(str(L_meas_K2))
	L_optical_ACD_elem.send_keys(str(L_optical_ACD))
	# L_refraction_elem.send_keys(str(L_refraction))

	# optional #
	L_lens_thickness_elem = chromedriver.find_element(By.ID, 'MainContent_LensThickness0')  # 2~8 mm
	L_wtw_elem            = chromedriver.find_element(By.ID, 'MainContent_WTW0')            # 8~14 mm

	if 'lens_thickness' in patient_data:
		L_lens_thickness_elem.send_keys(str(patient_data['lens_thickness']))
	if 'wtw' in patient_data:
		L_wtw_elem.send_keys(str(patient_data['wtw']))

def open_results_tab():
	univ_formula_tab_elem = chromedriver.find_element(By.XPATH, "//*[contains(text(), 'Universal Formula')]")
	univ_formula_tab_elem.click()

def open_data_tab():
	patient_data_tab_elem = chromedriver.find_element(By.XPATH, "//*[contains(text(), 'Patient Data')]")
	patient_data_tab_elem.click()

# This will return a list of lists, each list representing one row of the table.
# The three headers for the table are IOL Power, Optic, Refraction
# Example: [['15.5', 'Biconvex', '-1.09'], ['15', 'Biconvex', '-0.76'], ['14.5', 'Biconvex', '-0.42']]
def get_results(eye_side: str) -> list:

	if eye_side == 'R':
		eye_table_elem = chromedriver.find_element(By.ID, 'MainContent_GridView1')  # left-hand column, for right eye.
	if eye_side == 'L':
		eye_table_elem = chromedriver.find_element(By.ID, 'MainContent_GridView2')  # right-hand column, for left eye.
	
	result_group  = []  # empty list
	## three values: IOL Power, Optic, Refraction (in that order) ##
	rows = eye_table_elem.find_elements(By.TAG_NAME, 'tr')
	for row in rows:
		result_row = []  # empty list
		cells = row.find_elements(By.TAG_NAME, 'td')
		for cell in cells:
			result_row.append(cell.text)
		result_group.append(result_row)
	result_group.pop(0)  # there's an empty list b/c of the table header, this cleans it out of the results.

	return result_group

def run_form(patient_data: dict):  
	global chromedriver  # use the global chromedriver variable.
	start_chromedriver()  # resets form after loading.

	patient_name_elem = chromedriver.find_element(By.ID, 'MainContent_PatientName')
	patient_name_elem.send_keys("Demo Patient")
	# doctor_name_elem = chromedriver.find_element(By.ID, 'MainContent_DoctorName')
	# doctor_name_elem.send_keys("Brian Eyeballman")
	select_IOL_model(patient_data)

	if patient_data['eye_side'] == 'R':
		input_OD(patient_data)
	if patient_data['eye_side'] == 'L':
		input_OS(patient_data)

	calculate_values()  # must be on Patient Data tab!
	lens_factor_val, a_constant_val = get_IOL_model_values()  # fetch before switching tabs
	open_results_tab()
	result_group = get_results(patient_data['eye_side'])

	## get form back in a data-submission-ready state: ##
	open_data_tab()
	reset_form()  # must be on Patient Data tab!

	## you can alternatively just quit the chromedriver after each "run": ##
	quit_chromedriver()

	## proof it works; you can return these however you like. ##
	print(lens_factor_val)
	print(a_constant_val)
	print(result_group)

## SAMPLE VALUES FOR DEMONSTRATION
patient_data = { 'IOL_model':    'Alcon SN60WF', 
				 'eye_side':     'R',
				 'axial_length':  25,
				 'meas_K1':       45, 
				 'meas_K2':       46, 
				 'optical_ACD':   3.56
				}  # DEBUG samples

# process main method call
if __name__ == '__main__':
	run_form(patient_data)

# TODO: do we care about the two K-index radio buttons at the top??
# K Index 1.3375 
# K Index 1.332

# <span id="MainContent_RadioButtonList1">
# 		<label for="MainContent_RadioButtonList1_0"> K Index 1.3375</label>
# 		<input id="MainContent_RadioButtonList1_0" type="radio" name="ctl00$MainContent$RadioButtonList1" value="337.5" checked="checked">
# 		<label for="MainContent_RadioButtonList1_1"> K Index 1.332</label>
# 		<input id="MainContent_RadioButtonList1_1" type="radio" name="ctl00$MainContent$RadioButtonList1" value="332">
# </span>