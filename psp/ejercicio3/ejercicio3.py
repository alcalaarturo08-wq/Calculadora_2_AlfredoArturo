import math
import sys
import os
try:
    from psp.ejercicio2.ejercicio2 import Sumasim
except ModuleNotFoundError:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parent = os.path.abspath(os.path.join(root, '..'))
    if parent not in sys.path:
        sys.path.insert(0, parent)
    try:
        from psp.ejercicio2.ejercicio2 import Sumasim
    except Exception:
        mod_path = os.path.join(root, 'ejercicio2', 'ejercicio2.py')
        spec = None
        if os.path.exists(mod_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location('ejercicio2.ejercicio2', mod_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            Sumasim = getattr(module, 'Sumasim')
        else:
            raise


import math
import sys
import os
try:
    from psp.ejercicio2.ejercicio2 import Sumasim
except ModuleNotFoundError:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parent = os.path.abspath(os.path.join(root, '..'))
    if parent not in sys.path:
        sys.path.insert(0, parent)
    try:
        from psp.ejercicio2.ejercicio2 import Sumasim
    except Exception:
        mod_path = os.path.join(root, 'ejercicio2', 'ejercicio2.py')
        spec = None
        if os.path.exists(mod_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location('ejercicio2.ejercicio2', mod_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            Sumasim = getattr(module, 'Sumasim')
        else:
            raise


class Findx:

    def __init__(self, dof: float):
        self.dof = float(dof)

    def find_x(self, p_target: float, x0: float, d0: float, tol: float = 1e-6, n: int = 100, max_iter: int = 1000):

        p = float(p_target)
        if not (0.0 < p < 1.0):
            raise ValueError('p_target debe estar entre 0 y 1 (excluidos)')
        x = float(x0)
        d = abs(float(d0))
        tol = float(tol)
        n = int(n)
        if n % 2 != 0:
            n += 1

        two_sided = False
        if p > 0.5:
            area_target = p - 0.5
            two_sided = True
        else:
            area_target = p

        if x < 0:
            x = abs(x)

        s = Sumasim(0.0, x, n, self.dof)
        s.integrar()
        p_calc = getattr(s, 'resultado', 0.0)

        if p_calc < area_target:
            x = x + d
        else:
            x = max(0.0, x - d)

        errorSignoAnterior = area_target - p_calc
        iters = 0

        while iters < max_iter:
            iters += 1
            s = Sumasim(0.0, x, n, self.dof)
            s.integrar()
            p_calc = getattr(s, 'resultado', 0.0)
            errorSigno = area_target - p_calc
            errorSinSigno = abs(errorSigno)

            if errorSinSigno <= tol:
                break

            if errorSigno * errorSignoAnterior < 0:
                d = d / 2.0

            errorSignoAnterior = errorSigno

            if p_calc < area_target:
                x = x + d
            else:
                x = max(0.0, x - d)

            if x > 1e6:
                raise RuntimeError('x creció demasiado; posible no convergencia')

        final_p = (0.5 + p_calc) if two_sided else p_calc
        return x, final_p, iters


