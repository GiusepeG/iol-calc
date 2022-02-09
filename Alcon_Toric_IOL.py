# -*- coding: utf-8 -*-

import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select



# https://www.myalcon-toriccalc.com/
# did it resolve to 
https://www.myalcon-toriccalc.com/#/calculator
or 
https://www.myalcon-toriccalc.com/#/countryLanguage

<select name="countrydropDown" id="countrydropDown" class="form-control ng-pristine ng-valid ng-touched" 
ng-model="selectedCountry" ng-change="countryChanged(selectedCountry)" ng-options="country as country.name for country in countries">
<option value="" disabled="" selected="" data-i18n="CountryDefault" class="">Select A Country</option>
<option value="0" label="United States">United States</option>
<option value="1" label="European Union + EFTA">European Union + EFTA</option>
<option value="2" label="Asia">Asia</option>
<option value="3" label="Australia">Australia</option>
<option value="4" label="Canada">Canada</option>
<option value="5" label="Japan">Japan</option>
<option value="6" label="Latin America">Latin America</option>
<option value="7" label="Other">Other</option></select>
"United States"


language_select_elem = Select(chromedriver.find_element(By.ID, 'languagedropDown'))  # By.Name w/ same arg would also work.
language_select_elem.select_by_value("English")
time.sleep(1)
# ToC
time.sleep(1)


<button type="button" id="countryLanguageContinue" class="btn pull-right"
 ng-disabled="(selectedCountry.id == undefined) || (selectedLanguage.id == undefined)" 
 ng-click="countryLanguageContinueClick(selectedCountry, selectedLanguage)" 
 data-i18n="ContinueButtonLabel">Continue</button>

https://www.myalcon-toriccalc.com/#/termsConditions
<input type="checkbox" id="termsConditionsIAgree" ng-model="accepted" class="ng-pristine ng-untouched ng-valid">
<button type="button" id="termsConditionsContinue" class="btn pull-right" ng-disabled="!accepted" ng-click="termsConditionsContinueClick(accepted)" data-i18n="ContinueButtonLabel">Continue</button>


def input_dummy_names():
	surgeon_name_elem = chromedriver.find_element(By.Name, 'surgeonNameTextbox')
	patient_name_elem = chromedriver.find_element(By.Name, 'patientFirstNametextBox')
	surgeon_name_elem.send_keys("Demo Surgeon")
	patient_name_elem.send_keys("Demo Patient")




<select name="productdropdown" class="col-input select form-control ng-pristine 
ng-valid ng-valid-required ng-touched" style="border-radius:10px;" 
ng-model="selectedProduct" ng-options="product.productName group by product.grouping for product in products" 
ng-change="productChange()" tabindex="3" 
ng-disabled="(calculatorForm.patientFirstNametextBox.$invalid || calculatorForm.surgeonNameTextbox.$invalid)" 
ng-required="true" required="required">
<option value="" disabled="" selected="" data-i18n="ProductDefault" class="">Select Alcon Toric product</option>
<optgroup label="AcrySof®">
<option value="0" label="IQ Toric SN6ATx">IQ Toric SN6ATx</option>
<option value="1" label="UV Only Toric SA6ATx">UV Only Toric SA6ATx</option>
<option value="2" label="ReSTOR® Toric +3.0 SND1Tx">ReSTOR® Toric +3.0 SND1Tx</option>
<option value="3" label="ReSTOR® Toric +2.5 SV25Tx">ReSTOR® Toric +2.5 SV25Tx</option>
<option value="4" label="UV Only ReSTOR® Toric +2.5 SA25Tx">UV Only ReSTOR® Toric +2.5 SA25Tx</option>
<option value="5" label="IQ PanOptix® Toric TFNTx0">IQ PanOptix® Toric TFNTx0</option>
<option value="6" label="UV Only PanOptix® Toric TFATx0">UV Only PanOptix® Toric TFATx0</option>
<option value="7" label="IQ Vivity™ Toric DFTx15">IQ Vivity™ Toric DFTx15</option>
<option value="8" label="UV Only Vivity™ Toric DATx15">UV Only Vivity™ Toric DATx15</option></optgroup></select>

# these are in order they appear in the dropdown, could be referenced using list index and value parameter (int) in option tag.
models = ["IQ Toric SN6ATx", "UV Only Toric SA6ATx", "ReSTOR® Toric +3.0 SND1Tx",
		  "ReSTOR® Toric +2.5 SV25Tx", "UV Only ReSTOR® Toric +2.5 SA25Tx", "IQ PanOptix® Toric TFNTx0",
		  "UV Only PanOptix® Toric TFATx0", "IQ Vivity™ Toric DFTx15", "UV Only Vivity™ Toric DATx15"]

# YOU HAVE TO RE-SELECT PRODUCT IF YOU SELECT an eye and then select another eye; the form remembers your selections.
# no eye is default selected.
# may have to click the label, I think the element may occlude the actual radio button.
<label for="eyeSelectRightEye" data-i18n="EyeSelectRightEyeLabel" tabindex="4" ng-keypress="selectEyeKey($event, 'Right')">Right Eye</label>
<input type="radio" class="radio-custom radio-big right ng-untouched ng-valid ng-pristine" id="eyeSelectRightEye" name="formEye" value="Right" ng-model="preopData.eyeType" ng-click="eyeChanged(preopData)" ng-disabled="(preopData.eyeType === 'Right' || calculatorForm.patientFirstNametextBox.$invalid || calculatorForm.surgeonNameTextbox.$invalid)">

<label for="eyeSelectLeftEye" data-i18n="EyeSelectLeftEyeLabel" tabindex="5" ng-keypress="selectEyeKey($event, 'Left')">Left Eye</label>
<input type="radio" class="radio-custom radio-big left ng-untouched ng-valid ng-valid-parse ng-pristine" id="eyeSelectLeftEye" name="formEye" value="Left" ng-model="preopData.eyeType" ng-click="eyeChanged(preopData)" ng-disabled="(preopData.eyeType === 'Left' || calculatorForm.patientFirstNametextBox.$invalid || calculatorForm.surgeonNameTextbox.$invalid)" disabled="disabled">



# have to pick one of these radio buttons; again, 
# may have to click the label, I think the element may occlude the actual radio button.
<input type="radio" name="formulaRadio" id="formulaBarrett" class="radio-custom radio-grey radio-big ng-untouched ng-valid ng-valid-required ng-pristine" ng-value="formulas[0]" ng-model="preopData.formula" ng-click="formulaChanged(preopData)" required="" ng-hide="!selectedCountry.barrettEnabled" ng-disabled="(noEyeSelected) || selectedProduct.productId == null" value="[object Object]">
<label tabindex="6" data-i18n="BarrettLabel" for="formulaBarrett" ng-keypress="selectFormulaKey($event, 'Barrett')">Barrett</label>

<input type="radio" name="formulaRadio" id="formulaHolladayI" class="radio-custom radio-grey radio-big ng-untouched ng-valid ng-valid-required ng-pristine" ng-value="formulas[1]" ng-model="preopData.formula" ng-click="formulaChanged(preopData)" required="" ng-disabled="(noEyeSelected) || selectedProduct.productId == null" value="[object Object]">
<label tabindex="7" data-i18n="HolladayILabel" for="formulaHolladayI" ng-keypress="selectFormulaKey($event, 'HolladayI')">Holladay</label>



# if Holladay is picked, only Axial length (mm) is an input option; 
# checkbox is default-checked (Total Sia for a small 2.5mm temporal corneal incision) and 
# the following fields in the bottom-most box are grayed out: total SIA, flattening meridian, both empty,
# and incision location is fixed at 180 degrees, and K index is set to 1.3375 (what barrett and Hoffer are default set to)
# IF YOU UNCHECK IT: bottom fields shift to : surgically induced astigmatiasm (SIA),
#  incision location (default 180 degrees) becomes settable, and K index is set to 1.3375 .

# if Barrett is picked:
# axial length is an option:
<input name="axialLengthTextbox" type="text" class="form-control form-input-ctrl ng-pristine ng-invalid ng-invalid-required ng-invalid-digit-restriction ng-touched" ng-model="preopData.eyeData.axialLength" ng-model-options="{ allowInvalid: true }" ng-change="hideResults()" digit-restriction="" restrict-max="38" restrict-min="14" restrict-precision="2" restrict-len="5" required="" tabindex="8" ng-disabled="(noEyeSelected) || selectedProduct.productId == null">
# anterior chamber depth is an option:
<input name="anteriorChamberDepthTextbox" type="text" class="form-control form-input-ctrl ng-pristine ng-untouched ng-invalid ng-invalid-required ng-invalid-restrict-min ng-invalid-digit-restriction" ng-model="preopData.eyeData.anteriorChamberDepth" ng-model-options="{ allowInvalid: true }" ng-change="hideResults()" digit-restriction="" restrict-max="6" restrict-min="1" restrict-precision="2" restrict-len="5" required="" tabindex="9" ng-disabled="(noEyeSelected) || selectedProduct.productId == null">



calculate_button_elem    = chromedriver.find_element(By.Name, 'buttonCalculate')  # <button type="submit">
clear_fields_button_elem = chromedriver.find_element(By.Name, 'buttonReset')      # <button type="button">
