import math
import warnings
from typing import Dict, Any, Optional, Union

# --- Constantes ---
# Constantes centralizadas para facilitar a manutenção, imitando a estrutura do código R.
# NOTA: Alguns desses valores são padrão, enquanto outros são derivados de aproximações
#       comuns encontradas na literatura de fórmulas de LIO.

CONSTANTS = {
    "biometry": {
        "corneal_index": 1.3375,
        "aqueous_index": 1.336,
    },
    "iol": {
        # Conversão SRK/T de constante A para ACD
        "a_to_acd_a0": -68.747,
        "a_to_acd_a1": 0.62467,
        # Aproximação padrão de Holladay para Fator do Cirurgião (S) a partir da constante A
        "a_to_s_a0": -64.60,
        "a_to_s_a1": 0.5663,
        # Aproximação de Holladay para Fator do Cirurgião (S) a partir de pACD
        "pacd_to_s_a0": 0.0,
        "pacd_to_s_a1": 1.0,
    }
}


class IOLFormulas:
    """
    Uma coleção de fórmulas de cálculo de potência de Lentes Intraoculares (LIO)
    traduzidas de R para Python, seguindo princípios de código limpo.

    Os métodos são organizados por geração e tipo (teórico, empírico, híbrido).
    Cada cálculo de potência que depende de uma Posição Efetiva da Lente (ELP) tem
    um método _elp correspondente.
    """

    def _return_result(self, result: float, params: Dict[str, Any]) -> Dict[str, Any]:
        """Formata a saída para incluir o resultado e os parâmetros de entrada."""
        return {"result": result, "parameters": params}

    # ==========================================================================
    # ## Fórmulas de Primeira Geração
    # ==========================================================================

    def colenbrander_power(
        self, axial_length: float, keratometry: float, elp: float
    ) -> Dict[str, Any]:
        """
        Calcula a potência da LIO usando a fórmula teórica de Colenbrander.

        Args:
            axial_length (float): Comprimento axial do olho em mm (L).
            keratometry (float): Potência média da córnea em dioptrias (K).
            elp (float): Posição Efetiva da Lente em mm.

        Returns:
            Dict[str, Any]: Um dicionário contendo a potência da LIO calculada e os parâmetros de entrada.
        """
        params = {"axial_length": axial_length, "keratometry": keratometry, "elp": elp}
        if keratometry == 0 or (axial_length - elp - 0.05) == 0 or (1336 / keratometry - elp - 0.05) == 0:
            return self._return_result(math.nan, params)
        
        power = (1336 / (axial_length - elp - 0.05)) - \
                (1336 / (1336 / keratometry - elp - 0.05))
        return self._return_result(power, params)

    def srk_power(
        self,
        axial_length: float,
        keratometry: float,
        a_constant: Optional[float] = None,
        elp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Calcula a potência da LIO usando a fórmula de regressão empírica SRK.

        Args:
            axial_length (float): Comprimento axial do olho em mm (L).
            keratometry (float): Potência média da córnea em dioptrias (K).
            a_constant (Optional[float]): A constante A da LIO.
            elp (Optional[float]): Posição Efetiva da Lente em mm. Usado para aproximar a constante A se não for fornecida.

        Returns:
            Dict[str, Any]: Um dicionário contendo a potência da LIO calculada e os parâmetros de entrada.
        """
        params = {"axial_length": axial_length, "keratometry": keratometry}
        if a_constant is None:
            if elp is None:
                raise ValueError("Either 'a_constant' or 'elp' must be provided for SRK.")
            # Aproximação de Holladay para A a partir de ELP
            a_constant = (elp + 63.896) / 0.58357
            warnings.warn(f"Using Holladay approximation for SRK A-constant from ELP: {a_constant:.2f}")
            params["elp"] = elp
        
        params["a_constant"] = a_constant
        power = a_constant - (2.5 * axial_length) - (0.9 * keratometry)
        return self._return_result(power, params)

    # ==========================================================================
    # ## Fórmulas de Segunda Geração
    # ==========================================================================

    def _hoffer_elp(
        self,
        axial_length: float,
        pacd: Optional[float] = None,
        a_constant: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Auxiliar para calcular o ELP de Hoffer."""
        params = {"axial_length": axial_length}
        if pacd is None:
            if a_constant is None:
                raise ValueError("Either 'pacd' or 'a_constant' must be provided for Hoffer ELP.")
            # Usando a aproximação de Holladay para pACD a partir da constante A
            # pACD = 0.58357 * A - 63.896 (rearranjado da aproximação SRK)
            pacd = (0.58357 * a_constant) - 63.896
            warnings.warn(f"Using Holladay approximation for Hoffer's pACD from A-constant: {pacd:.4f} mm")
            params["a_constant"] = a_constant
        
        params["pacd"] = pacd
        elp = 0.292 * axial_length - 2.93 + (pacd - 3.94)
        return self._return_result(elp, params)
    
    def hoffer_power(
        self, axial_length: float, keratometry: float, elp: float
    ) -> Dict[str, Any]:
        """
        Calcula a potência da LIO usando a fórmula teórica de Hoffer.
        Nota: A fórmula de potência em si é idêntica à de Colenbrander.
        A diferença está em como o ELP é determinado.
        """
        return self.colenbrander_power(axial_length, keratometry, elp)

    def srk_2_power(
        self,
        axial_length: float,
        keratometry: float,
        a_constant: Optional[float] = None,
        elp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Calcula a potência da LIO usando a fórmula SRK II, que ajusta a constante A
        com base no comprimento axial.
        """
        params = {"axial_length": axial_length, "keratometry": keratometry}
        if a_constant is None:
            if elp is None:
                raise ValueError("Either 'a_constant' or 'elp' must be provided for SRK II.")
            a_constant = (elp + 63.896) / 0.58357
            warnings.warn(f"Using Holladay approximation for SRK II A-constant from ELP: {a_constant:.2f}")
            params["elp"] = elp
        
        params["a_constant"] = a_constant
        
        # Ajusta a constante A com base no comprimento axial
        adj_a = a_constant
        if axial_length < 20.0:
            adj_a = a_constant + 3.0
        elif 20.0 <= axial_length < 21.0:
            adj_a = a_constant + 2.0
        elif 21.0 <= axial_length < 22.0:
            adj_a = a_constant + 1.0
        elif axial_length >= 24.5:
            adj_a = a_constant - 0.5
            
        power = adj_a - (2.5 * axial_length) - (0.9 * keratometry)
        return self._return_result(power, params)
        
    # ==========================================================================
    # ## Fórmulas de Terceira Geração
    # ==========================================================================

    def _holladay_1_elp(
        self,
        axial_length: float,
        keratometry: Optional[float] = None,
        radius_of_curvature: Optional[float] = None,
        surgeon_factor: Optional[float] = None,
        a_constant: Optional[float] = None,
        pacd: Optional[float] = None,
        corneal_index: float = CONSTANTS["biometry"]["corneal_index"],
    ) -> Dict[str, Any]:
        """
        Auxiliar para calcular o ELP de Holladay 1.
        A lógica foi mantida, mas a legibilidade foi melhorada.
        """
        params = {"axial_length": axial_length}
        
        if radius_of_curvature is None:
            if keratometry is None:
                raise ValueError("Either 'keratometry' or 'radius_of_curvature' is required.")
            radius_of_curvature = 1000 * (corneal_index - 1) / keratometry
            warnings.warn(f"Converted K ({keratometry} D) to R ({radius_of_curvature:.4f} mm) for Holladay 1.")
            params.update({"keratometry": keratometry, "corneal_index": corneal_index})

        params["radius_of_curvature"] = radius_of_curvature

        if surgeon_factor is None:
            if a_constant is not None:
                surgeon_factor = CONSTANTS["iol"]["a_to_s_a0"] + CONSTANTS["iol"]["a_to_s_a1"] * a_constant
                params["a_constant"] = a_constant
                warnings.warn(f"Used Holladay approximation for S from A-constant: {surgeon_factor:.4f} mm")
            elif pacd is not None:
                surgeon_factor = CONSTANTS["iol"]["pacd_to_s_a0"] + CONSTANTS["iol"]["pacd_to_s_a1"] * pacd
                params["pacd"] = pacd
                warnings.warn(f"Used Holladay approximation for S from pACD: {surgeon_factor:.4f} mm")
            else:
                raise ValueError("One of 'surgeon_factor', 'a_constant', or 'pacd' must be provided.")
        
        params["surgeon_factor"] = surgeon_factor
        
        # Estima a largura da cúpula da córnea com base no comprimento axial (L).
        # AG <- L * 12.5 * 1 / 23.45
        corneal_dome_width_ag = axial_length * 12.5 / 23.45
        
        # Calcula um termo temporário para a altura sagital.
        # temp <- R * R - AG * AG / 4
        temp_calc = radius_of_curvature**2 - (corneal_dome_width_ag**2 / 4)
        
        if temp_calc < 0:
            warnings.warn("Calculation of aACD is poorly defined for this K/AL combination in Holladay 1.")
            return self._return_result(math.nan, params)
            
        # Calcula a profundidade da câmara anterior anatômica (aACD).
        # aACD <- 0.56 + R - sqrt(temp)
        aacd = 0.56 + radius_of_curvature - math.sqrt(temp_calc)
        
        # O ELP é a aACD mais o fator do cirurgião.
        # ELP <- aACD + S
        elp = aacd + surgeon_factor
        return self._return_result(elp, params)

    def holladay_1_power(
        self,
        axial_length: float,
        elp: float,
        keratometry: Optional[float] = None,
        radius_of_curvature: Optional[float] = None,
        corneal_index: float = CONSTANTS["biometry"]["corneal_index"],
        aqueous_index: float = CONSTANTS["biometry"]["aqueous_index"],
        retinal_thickness: float = 0.2,
        refractive_target: float = 0.0,
        vertex_distance: float = 13.0,
    ) -> Dict[str, Any]:
        """
        Calcula a potência da LIO usando a fórmula teórica de Holladay 1.
        Esta versão foi reescrita para espelhar diretamente a estrutura da fórmula em R,
        melhorando a clareza e garantindo uma tradução precisa.
        """
        params = {
            "axial_length": axial_length,
            "elp": elp,
            "aqueous_index": aqueous_index,
            "retinal_thickness": retinal_thickness,
            "refractive_target": refractive_target,
            "vertex_distance": vertex_distance,
        }

        if radius_of_curvature is None:
            if keratometry is None:
                raise ValueError("Either 'keratometry' or 'radius_of_curvature' is required.")
            radius_of_curvature = 1000 * (corneal_index - 1) / keratometry
            warnings.warn(f"Converted K ({keratometry} D) to R ({radius_of_curvature:.4f} mm) for Holladay 1.")
            params.update({"keratometry": keratometry, "corneal_index": corneal_index})
        
        params["radius_of_curvature"] = radius_of_curvature
        
        # Comprimento axial modificado (Alm)
        alm = axial_length + retinal_thickness
        # Índice de refração do vítreo (nc)
        nc = 4 / 3
        
        # Termos intermediários da fórmula, como no código R
        # naRnc1Alm <- aqueous_n * R - (nc - 1) * Alm
        term_alm = aqueous_index * radius_of_curvature - (nc - 1) * alm
        # naRnc1ELP <- aqueous_n * R - (nc - 1) * ELP
        term_elp = aqueous_index * radius_of_curvature - (nc - 1) * elp
        
        # Numerador da fórmula de Holladay 1
        numerator = 1000 * aqueous_index * (term_alm - 0.001 * refractive_target * (vertex_distance * term_alm + alm * radius_of_curvature))
        
        # Denominador da fórmula de Holladay 1
        denominator = (alm - elp) * (term_elp - 0.001 * refractive_target * (vertex_distance * term_elp + elp * radius_of_curvature))

        if denominator == 0:
            return self._return_result(math.nan, params)

        power = numerator / denominator
        
        return self._return_result(power, params)

    def _hoffer_q_elp(
        self,
        axial_length: float,
        keratometry: float,
        pacd: Optional[float] = None,
        a_constant: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Auxiliar para calcular o ELP de Hoffer Q."""
        params = {"axial_length": axial_length, "keratometry": keratometry}
        if pacd is None:
            if a_constant is None:
                raise ValueError("Either 'pacd' or 'a_constant' must be provided for Hoffer Q ELP.")
            pacd = (0.58357 * a_constant) - 63.896 # Aproximação Holladay/SRK
            warnings.warn(f"Using Holladay approximation for Hoffer Q's pACD from A-constant: {pacd:.4f} mm")
            params["a_constant"] = a_constant

        params["pacd"] = pacd
        
        m, g = (-1, 23.5) if axial_length > 23.0 else (1, 28.0)
        
        # Limita o comprimento axial ao intervalo efetivo da fórmula
        l_clamped = max(18.5, min(axial_length, 31.0))
        
        elp = (pacd + 
               0.3 * (l_clamped - 23.5) +
               math.tan(math.radians(keratometry))**2 +
               (0.1 * m * (23.5 - l_clamped)**2 * math.tan(math.radians(0.1 * (g - l_clamped)**2))) -
               0.99166)
        
        return self._return_result(elp, params)

    def hoffer_q_power(
        self,
        axial_length: float,
        keratometry: float,
        elp: float,
        refractive_target: float = 0.0,
        vertex_distance: float = 13.0,
    ) -> Dict[str, Any]:
        """Calcula a potência da LIO usando a fórmula teórica de Hoffer Q."""
        params = {
            "axial_length": axial_length,
            "keratometry": keratometry,
            "elp": elp,
            "refractive_target": refractive_target,
            "vertex_distance": vertex_distance
        }

        # Alvo refrativo ajustado para a distância do vértice
        r = refractive_target / (1 - (0.001 * vertex_distance * refractive_target))

        denom = (1.336 / (keratometry + r)) - ((elp + 0.05) / 1000)
        if (axial_length - elp - 0.05) == 0 or denom == 0:
            return self._return_result(math.nan, params)

        power = 1336 / (axial_length - elp - 0.05) - (1.336 / denom)
        return self._return_result(power, params)
        
    def _srk_t_elp(
        self,
        axial_length: float,
        keratometry: float,
        acd_const: Optional[float] = None,
        a_constant: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Auxiliar para calcular o ELP de SRK/T."""
        params = {"axial_length": axial_length, "keratometry": keratometry}
        
        if acd_const is None:
            if a_constant is None:
                raise ValueError("Either 'acd_const' or 'a_constant' must be provided for SRK/T.")
            acd_const = 0.62467 * a_constant - 68.747
            warnings.warn(f"Using SRK/T conversion from A-constant to ACD: {acd_const:.4f} mm")
            params["a_constant"] = a_constant
        
        params["acd_const"] = acd_const
        
        radius_of_curvature = 337.5 / keratometry
        
        # Comprimento axial corrigido
        l_corr = axial_length
        if axial_length > 24.2:
            l_corr = -3.446 + (1.715 * axial_length) - (0.0237 * axial_length**2)
            
        # Largura e altura da córnea computadas
        cw = -5.41 + (0.58412 * l_corr) + (0.098 * keratometry)
        temp = radius_of_curvature**2 - cw**2 / 4
        
        if temp < 0:
            warnings.warn("Calculation of SRK/T corneal height is poorly defined for this K/AL combination.")
            return self._return_result(math.nan, params)
            
        h = radius_of_curvature - math.sqrt(temp)
        
        # Deslocamento específico da LIO e ELP estimado
        offset = acd_const - 3.336
        elp = h + offset
        
        return self._return_result(elp, params)

    def srk_t_power(
        self, axial_length: float, keratometry: float, elp: float
    ) -> Dict[str, Any]:
        """Calcula a potência da LIO usando a fórmula teórica de SRK/T."""
        params = {"axial_length": axial_length, "keratometry": keratometry, "elp": elp}
        
        na = 1.336 # Índice do aquoso
        ncm1 = 1.333 - 1.0 # Aproximação do índice da córnea menos o índice do ar
        
        radius_of_curvature = 337.5 / keratometry
        retinal_thickness = 0.65696 - (0.02029 * axial_length)
        l_opt = axial_length + retinal_thickness
        
        # Verificação do denominador
        denom_part1 = l_opt - elp
        denom_part2 = na * radius_of_curvature - ncm1 * elp
        if denom_part1 == 0 or denom_part2 == 0:
            return self._return_result(math.nan, params)

        num = 1000 * na * (na * radius_of_curvature - ncm1 * l_opt)
        den = denom_part1 * denom_part2
        
        power = num / den
        return self._return_result(power, params)

    # ==========================================================================
    # ## Fórmulas de Quarta Geração
    # ==========================================================================
    
    # As fórmulas de Olsen e Holladay 2 não são fornecidas no código-fonte.
    # Elas requerem mais parâmetros e cálculos proprietários complexos.
    
    def _haigis_elp(
        self,
        axial_length: float,
        acd: float = 3.37,
        a0: Optional[float] = None,
        a1: float = 0.4,
        a2: float = 0.1,
        pacd: Optional[float] = None,
        a_constant: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Auxiliar para calcular o ELP de Haigis. Usa uma hierarquia de constantes:
        a0 -> pACD -> constante A.
        """
        params = {"axial_length": axial_length, "acd": acd, "a1": a1, "a2": a2}
        
        if a0 is None:
            if pacd is None:
                if a_constant is None:
                    raise ValueError("One of 'a0', 'pacd', or 'a_constant' must be provided for Haigis.")
                # Aproxima pACD a partir da constante A
                pacd = CONSTANTS["iol"]["a_to_acd_a0"] + a_constant * CONSTANTS["iol"]["a_to_acd_a1"]
                warnings.warn(f"Using Haigis approximation for pACD from A-constant: {pacd:.4f} mm")
                params["a_constant"] = a_constant
            
            # Aproxima a0 a partir de pACD
            a0 = pacd - (a1 * 3.37) - (a2 * 23.39)
            warnings.warn(f"Using Haigis approximation for a0 from pACD: {a0:.4f}")
            params["pacd"] = pacd
        
        params["a0"] = a0
        
        elp = a0 + (a1 * acd) + (a2 * axial_length)
        return self._return_result(elp, params)
    
    def haigis_power(
        self,
        axial_length: float,
        radius_of_curvature: float,
        elp: float,
        refractive_target: float = 0.0,
        vertex_distance: float = 12.0,
    ) -> Dict[str, Any]:
        """Calcula a potência da LIO usando a fórmula teórica de Haigis."""
        params = {
            "axial_length": axial_length,
            "radius_of_curvature": radius_of_curvature,
            "elp": elp,
            "refractive_target": refractive_target,
            "vertex_distance": vertex_distance
        }
        
        nc = 1.3315 # Índice da córnea de Haigis
        n = 1.336  # Índice do aquoso
        
        dc = (nc - 1.0) / (radius_of_curvature / 1000)
        
        # Verificação do denominador
        if (1.0 - refractive_target * (vertex_distance / 1000)) == 0:
             return self._return_result(math.nan, params)
        z = dc + refractive_target / (1.0 - refractive_target * (vertex_distance / 1000))

        if (axial_length / 1000 - elp / 1000) == 0 or (n / z - elp / 1000) == 0:
            return self._return_result(math.nan, params)

        power = n / (axial_length / 1000 - elp / 1000) - n / (n / z - elp / 1000)
        return self._return_result(power, params)


# ==============================================================================
## Exemplo de Uso
# ==============================================================================
if __name__ == "__main__":
    # --- Dados do Paciente ---
    # Valores típicos para um olho médio
    patient_axial_length = 23.5  # em mm
    patient_keratometry = 44.0  # em Dioptrias
    patient_a_constant = 118.9 # para um modelo de LIO específico
    patient_acd = 3.5           # profundidade da câmara anterior pré-operatória em mm

    # Converte Ceratometria (K) para Raio de Curvatura (R) para fórmulas que precisam dele
    # R = (n-1)*1000 / K, usando o índice da córnea padrão n=1.3375
    patient_radius_of_curvature = (1.3375 - 1) * 1000 / patient_keratometry

    print("=" * 60)
    print("Exemplo de Cálculo de Potência de LIO para Todas as Fórmulas")
    print("-" * 60)
    print(f"Dados do Paciente:")
    print(f"  Comprimento Axial (AL): {patient_axial_length} mm")
    print(f"  Ceratometria (K): {patient_keratometry} D")
    print(f"  Constante A: {patient_a_constant}")
    print(f"  ACD pré-op: {patient_acd} mm")
    print(f"  Raio de Curvatura (R): {patient_radius_of_curvature:.2f} mm")
    print("=" * 60, "\n")

    # Inicializa a calculadora
    calculator = IOLFormulas()

    # Vamos calcular um ELP moderno (de SRK/T) para usar como proxy para
    # as fórmulas de primeira geração que requerem um ELP fixo.
    srk_t_elp_for_proxy = calculator._srk_t_elp(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )['result']

    # ==========================================================================
    # ## Fórmulas de Primeira Geração
    # ==========================================================================

    print("--- Calculando com Colenbrander (1ª Geração) ---")
    # NOTA: Colenbrander requer um ELP fixo. Usamos o ELP de SRK/T como exemplo.
    colenbrander_result = calculator.colenbrander_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        elp=srk_t_elp_for_proxy
    )
    print(f"  (Usando ELP proxy: {srk_t_elp_for_proxy:.4f} mm)")
    print(f"Potência Calculada: {colenbrander_result['result']:.2f} D\n")

    print("--- Calculando com SRK (1ª Geração) ---")
    srk_result = calculator.srk_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )
    print(f"Potência Calculada: {srk_result['result']:.2f} D\n")

    # ==========================================================================
    # ## Fórmulas de Segunda Geração
    # ==========================================================================

    print("--- Calculando com Hoffer (2ª Geração) ---")
    hoffer_elp_result = calculator._hoffer_elp(
        axial_length=patient_axial_length,
        a_constant=patient_a_constant
    )
    hoffer_elp = hoffer_elp_result['result']
    print(f"  ELP Intermediário: {hoffer_elp:.4f} mm")
    hoffer_power_result = calculator.hoffer_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        elp=hoffer_elp
    )
    print(f"Potência Calculada: {hoffer_power_result['result']:.2f} D\n")

    print("--- Calculando com SRK II (2ª Geração) ---")
    srk2_result = calculator.srk_2_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )
    print(f"Potência Calculada: {srk2_result['result']:.2f} D\n")

    # ==========================================================================
    # ## Fórmulas de Terceira Geração
    # ==========================================================================

    print("--- Calculando com Holladay 1 (3ª Geração) ---")
    holladay1_elp_result = calculator._holladay_1_elp(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )
    holladay1_elp = holladay1_elp_result['result']
    print(f"  ELP Intermediário: {holladay1_elp:.4f} mm")
    holladay1_power_result = calculator.holladay_1_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        elp=holladay1_elp
    )
    print(f"Potência Calculada: {holladay1_power_result['result']:.2f} D\n")

    print("--- Calculando com Hoffer Q (3ª Geração) ---")
    hoffer_q_elp_result = calculator._hoffer_q_elp(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )
    hoffer_q_elp = hoffer_q_elp_result['result']
    print(f"  ELP Intermediário: {hoffer_q_elp:.4f} mm")
    hoffer_q_power_result = calculator.hoffer_q_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        elp=hoffer_q_elp
    )
    print(f"Potência Calculada: {hoffer_q_power_result['result']:.2f} D\n")

    print("--- Calculando com SRK/T (3ª Geração) ---")
    srk_t_elp_result = calculator._srk_t_elp(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        a_constant=patient_a_constant
    )
    srk_t_elp = srk_t_elp_result['result']
    print(f"  ELP Intermediário: {srk_t_elp:.4f} mm")
    srk_t_power_result = calculator.srk_t_power(
        axial_length=patient_axial_length,
        keratometry=patient_keratometry,
        elp=srk_t_elp
    )
    print(f"Potência Calculada: {srk_t_power_result['result']:.2f} D\n")

    # ==========================================================================
    # ## Fórmulas de Quarta Geração
    # ==========================================================================

    # Nota: Olsen e Holladay 2 não estão incluídas, conforme o código-fonte.

    print("--- Calculando com Haigis (4ª Geração) ---")
    haigis_elp_result = calculator._haigis_elp(
        axial_length=patient_axial_length,
        acd=patient_acd,
        a_constant=patient_a_constant
    )
    haigis_elp = haigis_elp_result['result']
    print(f"  ELP Intermediário: {haigis_elp:.4f} mm")
    haigis_power_result = calculator.haigis_power(
        axial_length=patient_axial_length,
        radius_of_curvature=patient_radius_of_curvature,
        elp=haigis_elp
    )
    print(f"Potência Calculada: {haigis_power_result['result']:.2f} D\n")
