# -*- coding: utf-8 -*-
# NOME DO ARQUIVO: barrett_scraper_lib.py

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from typing import List, Optional

# --- Classes de Dados (Data Classes) ---
@dataclass
class PatientData:
    """Representa os dados de entrada para um paciente."""
    iol_model: str
    eye_side: str
    axial_length: float
    meas_k1: float
    meas_k2: float
    optical_acd: float
    patient_name: str = "Demo Patient"
    lens_thickness: Optional[float] = None
    wtw: Optional[float] = None

@dataclass
class CalculationResult:
    """Representa uma única linha da tabela de resultados."""
    iol_power: float
    optic: str
    refraction: float

    def __str__(self):
        return f"Power: {self.iol_power}, Optic: {self.optic}, Refraction: {self.refraction}"

# --- Classe Principal de Automação ---
class BarrettCalculatorScraper:
    """
    Gerencia a automação do site da calculadora Barrett Universal II.
    Funciona como um gerenciador de contexto para garantir a limpeza dos recursos.
    """
    BASE_URL = 'https://calc.apacrs.org/barrett_universal2105/'

    def __init__(self, headless: bool = True):
        self._driver = None
        self._wait = None
        
        service = Service(executable_path=chromedriver_binary.chromedriver_filename)
        options = Options()

        # --- MODIFICAÇÕES ANTI-DETECÇÃO ---
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu") 

        self._service = service
        self._options = options

    def __enter__(self):
        self._driver = webdriver.Chrome(service=self._service, options=self._options)
        self._wait = WebDriverWait(self._driver, 20) 
        self._driver.get(self.BASE_URL)
        self._reset_form()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver:
            self._driver.quit()

    def _reset_form(self):
        try:
            reset_button = self._wait.until(EC.presence_of_element_located((By.ID, 'MainContent_btnReset')))
            self._driver.execute_script("arguments[0].click();", reset_button)
        except Exception as e:
            print(f"Erro ao tentar resetar o formulário: {e}")
            raise

    def _fill_form(self, patient: PatientData):
        self._driver.find_element(By.ID, 'MainContent_PatientName').send_keys(patient.patient_name)
        Select(self._driver.find_element(By.ID, 'MainContent_IOLModel')).select_by_value(patient.iol_model)
        
        if patient.eye_side == 'R':
            self._driver.find_element(By.ID, 'MainContent_Axlength').send_keys(str(patient.axial_length))
            self._driver.find_element(By.ID, 'MainContent_MeasuredK1').send_keys(str(patient.meas_k1))
            self._driver.find_element(By.ID, 'MainContent_MeasuredK2').send_keys(str(patient.meas_k2))
            self._driver.find_element(By.ID, 'MainContent_OpticalACD').send_keys(str(patient.optical_acd))
            if patient.lens_thickness:
                self._driver.find_element(By.ID, 'MainContent_LensThickness').send_keys(str(patient.lens_thickness))
            if patient.wtw:
                self._driver.find_element(By.ID, 'MainContent_WTW').send_keys(str(patient.wtw))

    def _calculate(self):
        self._driver.find_element(By.ID, 'MainContent_Button1').click()

    def _open_results_tab(self):
        results_tab = self._wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Universal Formula')]")))
        results_tab.click()

    def _scrape_results(self, eye_side: str) -> List[CalculationResult]:
        table_id = 'MainContent_GridView1' if eye_side == 'R' else 'MainContent_GridView2'
        try:
            table = self._wait.until(EC.presence_of_element_located((By.ID, table_id)))
            rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
            
            results = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) == 3:
                    result = CalculationResult(
                        iol_power=float(cells[0].text),
                        optic=cells[1].text,
                        refraction=float(cells[2].text)
                    )
                    results.append(result)
            return results
        except Exception as e:
            print(f"Não foi possível extrair os resultados da tabela com ID '{table_id}'. Erro: {e}")
            return []

    def run_calculation(self, patient: PatientData) -> List[CalculationResult]:
        """Executa o fluxo completo e retorna os resultados."""
        self._fill_form(patient)
        self._calculate()
        self._open_results_tab()
        return self._scrape_results(patient.eye_side)