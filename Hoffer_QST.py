# -*- coding: utf-8 -*-

import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

opts = Options()  # options for chromedriver
opts.add_argument("--window-size=1000,1000")  # specifies window width,height
opts.add_argument("headless")  # runs without the browser visible
exe_path = chromedriver_binary.chromedriver_filename
chromedriver = None # initialize chromedriver global variable.

# TODO: fix warning
# https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
def start_chromedriver():
	global chromedriver  # use the global chromedriver variable.
	chromedriver = webdriver.Chrome(executable_path=exe_path, options=opts)
	chromedriver.get('https://hofferqst.com/')

def quit_chromedriver():
	global chromedriver  # use the global chromedriver variable.
	chromedriver.quit()

def close_disclaimer_modal():
	global chromedriver
	model_button_elem = chromedriver.find_element(By.XPATH, "//*[contains(text(), 'Agree')]")
	if model_button_elem is not None:
		model_button_elem.click()

def reset_form():
	global chromedriver  # use the global chromedriver variable.
	reset_button_elem = chromedriver.find_element(By.XPATH, "//*[contains(text(), 'Reset')]")
	reset_button_elem.click()	

def calculate_values():
	global chromedriver  # use the global chromedriver variable.
	calculate_button_elem = chromedriver.find_element(By.XPATH, "//*[contains(text(), 'Calculate')]")
	calculate_button_elem.click()

def select_gender(patient_data: dict):
	if patient_data['gender'] == 'M':
		male_button_elem   = chromedriver.find_element(By.ID, 'input-Gender_BV_option_0')
		parent_elem = male_button_elem.find_element(By.XPATH, '..')  # to avoid ElementClickInterceptedException
		parent_elem.click()
	if patient_data['gender'] == 'F':
		female_button_elem = chromedriver.find_element(By.ID, 'input-Gender_BV_option_1')
		parent_elem = female_button_elem.find_element(By.XPATH, '..')  # to avoid ElementClickInterceptedException
		parent_elem.click()

# Alcon, Bausch & Lomb, and Zeiss are the only 3 manufacturers with constants in both calculators.
# HOWEVER, I did NOT check to see if the actual types overlap in both tools.
# TODO: pull the IOL model names for the empty manufacturers in this dictionary:
# manufacturers = {
# 	'Alcon': ["Alcon - SN60WF/SA60WF", "Alcon - SN60AT/SA60AT", "Alcon - SN6ATx (2-9)",
# 			  "Alcon - CLAREON CNA0T0", "Alcon - MA60AC", "Alcon - MA60MA",
# 			  "Alcon - VIVITY DFTx15 (2-5)", "Alcon - PANOPTIX TFNT00", 
# 			  "Alcon - PANOPTIX TFNTx (30-60)"],
# 	'B+L':   ["B+L - EnVista MX60", "B+L - EyeCEE One", "B+L - Akreos MICS MI60", 
# 			  "B+L - Akreos Adapt AO", "B+L - LuxSmart", "B+L - LuxGood"],
# 	'J&amp;J': [],	
# 	'Rayner': [],
# 	'SIFI': [],
# 	'Soleko': [],
# 	'Zeiss': ["Zeiss - CT SPHERIS 209 M", "Zeiss - CT LUCIA 211P/PY", "Zeiss - CT LUCIA 221P", 
# 			  "Zeiss - CT LUCIA 611P/PY", "Zeiss - CT LUCIA 621P/PY", "Zeiss - CT ASPHINA 409M/MP", 
# 			  "Zeiss - CT ASPHINA 509M/MP", "Zeiss - AT LARA 829MP", "Zeiss - AT LISA TRI 839MP"]
# }
def select_IOL_model(patient_data: dict):
	if patient_data['eye_side'] == 'R':
		iol_mfr_elem = Select(chromedriver.find_element(By.ID, 'input-right-IOLModel'))
		iol_mfr_elem.select_by_value(patient_data['mfr'])
		iol_model_elem = Select(chromedriver.find_element(By.ID, 'input-right-IOLType'))
		iol_model_elem.select_by_value(patient_data['model'])
	if patient_data['eye_side'] == 'L':
		iol_mfr_elem = Select(chromedriver.find_element(By.ID, 'input-left-IOLModel'))
		iol_mfr_elem.select_by_value(patient_data['mfr'])
		iol_model_elem = Select(chromedriver.find_element(By.ID, 'input-left-IOLType'))
		iol_model_elem.select_by_value(patient_data['model'])

def get_IOL_model_value(patient_data: dict) -> str:
	if patient_data['eye_side'] == 'R':
		R_hoffer_pACD_elem = chromedriver.find_element(By.ID, 'input-right-pACD')
		return str(R_hoffer_pACD_elem.get_attribute('value'))
	if patient_data['eye_side'] == 'L':
		L_hoffer_pACD_elem = chromedriver.find_element(By.ID, 'input-left-pACD')
		return str(L_hoffer_pACD_elem.get_attribute('value'))

def input_OD(patient_data: dict):
	R_axial_length_elem = chromedriver.find_element(By.ID, 'input-right-AL')
	R_K1_elem           = chromedriver.find_element(By.ID, 'input-right-K1')
	R_K2_elem           = chromedriver.find_element(By.ID, 'input-right-K2')
	R_ACD_elem          = chromedriver.find_element(By.ID, 'input-right-ACD')

	R_axial_length_elem.send_keys(str(patient_data['axial_length']))
	R_K1_elem.send_keys(str(patient_data['meas_K1']))
	R_K2_elem.send_keys(str(patient_data['meas_K2']))
	R_ACD_elem.send_keys(str(patient_data['optical_ACD']))

	## optional: ##
	# R_target_PO_rx_elem = chromedriver.find_element(By.ID, 'input-right-TargetRx')  # defaults to zero
	# R_ACD_elem.send_keys(str(patient_data['target_PO_rx']))

def input_OS(patient_data: dict):
	L_axial_length_elem = chromedriver.find_element(By.ID, 'input-left-AL')
	L_K1_elem           = chromedriver.find_element(By.ID, 'input-left-K1')
	L_K2_elem           = chromedriver.find_element(By.ID, 'input-left-K2')
	L_ACD_elem          = chromedriver.find_element(By.ID, 'input-left-ACD')

	L_axial_length_elem.send_keys(str(patient_data['axial_length']))
	L_K1_elem.send_keys(str(patient_data['meas_K1']))
	L_K2_elem.send_keys(str(patient_data['meas_K2']))
	L_ACD_elem.send_keys(str(patient_data['optical_ACD']))

	## optional: ##
	# L_target_PO_rx_elem = chromedriver.find_element(By.ID, 'input-left-TargetRx')  # defaults to zero
	# L_ACD_elem.send_keys(str(patient_data['target_PO_rx']))

# This will return a list of lists, each list representing one row of the table.
# The two headers for the table are IOL power (D), Predicted Rx
# Example: [[12.0, 1.22], [12.5, 0.93], [13.0, 0.64]]
def get_results(patient_data: dict) -> list:
	eye_side = patient_data['eye_side']
	if eye_side == 'R':
		eye_table_elem = chromedriver.find_element(By.ID, 'right-se-table')  # left-hand column, for right eye.
	if eye_side == 'L':
		eye_table_elem = chromedriver.find_element(By.ID, 'left-se-table')  # right-hand column, for left eye.

	result_group  = []  # empty list
	## two values: IOL power (D), Predicted Rx (in that order) ##
	rows = eye_table_elem.find_elements(By.TAG_NAME, 'tr')
	for row in rows:
		result_row = []  # empty list
		cells = row.find_elements(By.TAG_NAME, 'td')
		for cell in cells:
			result_row.append(cell.text)
		result_group.append(result_row)
	result_group.pop(0)  # there's an empty list b/c of the table header, this cleans it out of the results.
	return result_group

def run_form(patient_data):
	start_chromedriver()
	close_disclaimer_modal()
	time.sleep(1)  # needed to make sure modal isn't obscuring form elements
	reset_form()  # preemptively clear form, just in case

	## surgeon name not required: ##
	# surgeon_name_elem = chromedriver.find_element(By.ID, 'input-Surgeon')
	# surgeon_name_elem.send_keys("Brian Eyeballman")

	## patient name required: ##
	patient_name_elem = chromedriver.find_element(By.ID, 'input-PatientName')
	patient_name_elem.send_keys("Demo Patient")

	select_gender(patient_data)  # form will not run if one is not selected
	select_IOL_model(patient_data)

	if patient_data['eye_side'] == 'R':
		input_OD(patient_data)
	if patient_data['eye_side'] == 'L':
		input_OS(patient_data)

	calculate_values()
	time.sleep(1)  # needed to give results table a chance to show up in DOM
	result_group = get_results(patient_data)
	IOL_model_value = get_IOL_model_value(patient_data)

	reset_form()
	## you can alternatively just quit the chromedriver after each "run": ##
	quit_chromedriver()

	## proof it works; you can return these however you like. ##
	print(IOL_model_value)
	print(result_group)


## SAMPLE VALUES FOR DEMONSTRATION
patient_data = { 'IOL_model':    'Alcon SN60WF', 
				 'mfr':          'Alcon',
				 'model':        'Alcon - SN60WF/SA60WF',
				 'eye_side':     'R',
				 'axial_length':  25,
				 'meas_K1':       45, 
				 'meas_K2':       46, 
				 'optical_ACD':   3.56,
				 'gender':        'M',
				 'target_PO_rx':  0  # default value
				}  # DEBUG samples

# process main method call
if __name__ == '__main__':
	run_form(patient_data)


# TODO: set index?
# index is default set to 1.3375; I believe this is the default setting in the Barrett calc.

# there's a "post myopic LASIK/PRK" button option; it adds a whole extra block of optional inputs
# above the normal block of inputs...
# there is also a "SE / Toric" option that defaults to SE; I believe we want SE.