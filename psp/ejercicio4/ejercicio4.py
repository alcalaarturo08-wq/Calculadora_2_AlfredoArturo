import math
from typing import List, Tuple


def fx(x: float, dof: float) -> float:
    """Densidad t-student en x para grados de libertad dof."""
    num = math.gamma((dof + 1) / 2)
    den = math.sqrt(dof * math.pi) * math.gamma(dof / 2)
    return (num / den) * (1 + (x ** 2) / dof) ** (-(dof + 1) / 2)


def calcularsimson(xcalculada: float, dof: float, tol: float = 1e-5) -> float:
    """Calcula la integral de 0 a xcalculada de la densidad t usando regla de Simpson adaptativa."""
    n = 10
    pPrev = 0.0
    while True:
        w = (xcalculada) / n
        s = fx(0.0, dof)
        for i in range(1, n):
            xi = i * w
            val = fx(xi, dof)
            s += (4 if i % 2 == 1 else 2) * val
        s += fx(xcalculada, dof)
        p = (w / 3.0) * s
        if abs(p - pPrev) < tol:
            return p
        pPrev = p
        n *= 2


def calcular_sigma(n: int, yi: List[float], b0: float, b1: float, xi: List[float]) -> Tuple[float, float, float]:
    """Calcula sigma, suma de (xi-xavg)^2 y xavg. Retorna (sigma, sumax, xavg)."""
    n = int(n)
    if n <= 2:
        raise ValueError('n debe ser mayor que 2')
    if len(yi) != len(xi) or len(yi) != n:
        raise ValueError('Longitudes de yi y xi deben ser iguales a n')
    s = 0.0
    for i in range(n):
        resid = yi[i] - (b0 + b1 * xi[i])
        s += resid * resid
    sigma = math.sqrt(s / (n - 2))
    xavg = sum(xi) / n
    sumax = sum((x - xavg) ** 2 for x in xi)
    return sigma, sumax, xavg


def calcular_rango(tval: float, sigma: float, n: int, xk: float, xavg: float, sumax: float) -> float:
    """Calcula el rango usado en UPI/LPI: tval * sigma * sqrt(1 + 1/n + (xk-xavg)^2 / sumax)"""
    n = int(n)
    if sumax == 0:
        raise ValueError('sumax (variación de xi) es 0')
    factor = math.sqrt(1.0 + 1.0 / n + ((xk - xavg) ** 2) / sumax)
    return tval * sigma * factor


def calcular_upi_lpi(yk: float, rango: float) -> Tuple[float, float]:
    return yk + rango, yk - rango


if __name__ == '__main__':
    print('módulo ejercicio4 cargado')
