import math

import scipy.stats as stats
import numpy as np


def chi_cuadrado_test(datos, bins, alpha, distribucion, params):
    global chi2_calculado
    observados, bordes = np.histogram(datos, bins=bins)
    esperados = []

    for i in range(len(bordes) - 1):
        #limite inferior y superior
        a, b = bordes[i], bordes[i + 1]

        #probabilidad del intervalo entre el limite inferior y superior segun la distribucion
        if distribucion == "Normal":
            mu, sigma = params
            prob = stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma)
        elif distribucion == "Uniforme":
            a_, b_ = params
            prob = stats.uniform.cdf(b, a_, b_ - a_) - stats.uniform.cdf(a, a_, b_ - a_)
        elif distribucion == "Poisson":
            lambda_ = params[0]
            # Para Poisson, convertir los bordes a enteros y sumar probabilidades
            prob = stats.poisson.cdf(b, lambda_) - stats.poisson.cdf(a, lambda_)
        elif distribucion == "Exponencial":
            lambda_ = params[0]
            prob = stats.expon.cdf(b, scale=1/lambda_) - stats.expon.cdf(a, scale=1/lambda_)
        else:
            prob = 0

        #se agrega la frecuencia a una lista de los valores esperados
        esperados.append(prob * len(datos))

    # Agrupar esperados menores a 5
    obs_agrupados = []
    exp_agrupados = []
    temp_obs = 0
    temp_exp = 0

    #si en el intervalo tiene una frecuencia menor a 5 se combinan intervalos para poder hacer chi2
    for o, e in zip(observados, esperados):
        temp_obs += o
        temp_exp += e
        if temp_exp >= 5:

            obs_agrupados.append(temp_obs)
            exp_agrupados.append(temp_exp)
            temp_obs = 0
            temp_exp = 0

    # Si quedan residuos al final los agrega al ultimo intervalo combinado y si no hay intervalos devuelve none
    if temp_exp > 0:
        if exp_agrupados:
            obs_agrupados[-1] += temp_obs
            exp_agrupados[-1] += temp_exp
        else:
            return None, None, None

    chi2_calculado = 0
    #calcula chi2 segun los valores observados y esperados agrupados
    for i in range(len(obs_agrupados)):
        chi2_calculado += (obs_agrupados[i] - exp_agrupados[i]) ** 2 / exp_agrupados[i]

    #intervalos - 1 ya que no se calcula ningun dato empirico
    grados_libertad = len(obs_agrupados) - 1
    if not grados_libertad > 0:
        return None, None, None
    chi2_tabla = stats.chi2.ppf(1 - alpha, df=grados_libertad)



    return chi2_calculado, chi2_tabla, grados_libertad