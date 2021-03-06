#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from functools import partial

import pyapprox as pya
from pyapprox.benchmarks.sensitivity_benchmarks import *
from pyapprox.benchmarks.surrogate_benchmarks import *
from pyapprox.models.genz import GenzFunction

from scipy.optimize import OptimizeResult
class Benchmark(OptimizeResult):
    """
    Contains functions and results needed to implement known
    benchmarks.

    The quantities

    Attributes
    ----------
    fun : callable
        The function being analyzed

    variable : pya.variable
        Class containing information about each of the nvars inputs to fun

    jac : callable
        The jacobian of fun. (optional)

    hess : callable
        The Hessian of fun. (optional)

    hessp : callable
        Function implementing the hessian of fun multiplied by a vector. 
        (optional)

    mean: np.ndarray (nvars)
        The mean of the function with respect to the PDF of var

    variance: np.ndarray (nvars)
        The variance of the function with respect to the PDF of var

    main_effects : np.ndarray (nvars)
        The variance based main effect sensitivity indices

    total_effects : np.ndarray (nvars)
        The variance based total effect sensitivity indices

    sobol_indices : np.ndarray
        The variance based Sobol sensitivity indices

    Notes
    -----
    Use the `keys()` method to see a list of the available 
    attributes for a specific benchmark
    """
    pass

def setup_sobol_g_function(nvars):
    r"""
    Setup the Sobol-G function benchmark 

    .. math:: f(z) = \prod_{i=1}^d\frac{\lvert 4z_i-2\rvert+a_i}{1+a_i}, \quad a_i=\frac{i-2}{2}

    using 

    >>> from pyapprox.benchmarks.benchmarks import setup_benchmark
    >>> benchmark=setup_benchmark('sobol_g',nvars=2)
    >>> print(benchmark.keys())
    dict_keys(['fun', 'mean', 'variance', 'main_effects', 'total_effects', 'variable'])

    Parameters
    ----------
    nvars : integer
        The number of variables of the Sobol-G function

    Returns
    -------
    benchmark : pya.Benchmark
       Object containing the benchmark attributes

    References
    ----------
    .. [Saltelli1995] `Saltelli, A., & Sobol, I. M. About the use of rank transformation in sensitivity analysis of model output. Reliability Engineering & System Safety, 50(3), 225-239, 1995. <https://doi.org/10.1016/0951-8320(95)00099-2>`_
    """
    
    univariate_variables = [stats.uniform(0,1)]*nvars
    variable=pya.IndependentMultivariateRandomVariable(univariate_variables)
    a = (np.arange(1,nvars+1)-2)/2
    mean, variance, main_effects, total_effects = \
        get_sobol_g_function_statistics(a)
    return Benchmark({'fun':partial(sobol_g_function,a),
            'mean':mean,'variance':variance,'main_effects':main_effects,
            'total_effects':total_effects,'variable':variable})

def setup_ishigami_function(a,b):
    r"""
    Setup the Ishigami function benchmark 

    .. math:: f(z) = \sin(z_1)+a\sin^2(z_2) + bz_3^4\sin(z_0)

    using 

    >>> from pyapprox.benchmarks.benchmarks import setup_benchmark
    >>> benchmark=setup_benchmark('ishigami',a=7,b=0.1)
    >>> print(benchmark.keys())
    dict_keys(['fun', 'jac', 'hess', 'variable', 'mean', 'variance', 'main_effects', 'total_effects', 'sobol_indices'])

    Parameters
    ----------
    a : float
        The hyper-parameter a

    b : float
        The hyper-parameter b

    Returns
    -------
    benchmark : pya.Benchmark
       Object containing the benchmark attributes

    References
    ----------
    .. [Ishigami1990] `T. Ishigami and T. Homma, "An importance quantification technique in uncertainty analysis for computer models," [1990] Proceedings. First International Symposium on Uncertainty Modeling and Analysis, College Park, MD, USA, 1990, pp. 398-403 <https://doi.org/10.1109/ISUMA.1990.151285>`_
    """
    univariate_variables = [stats.uniform(-np.pi,2*np.pi)]*3
    variable=pya.IndependentMultivariateRandomVariable(univariate_variables)
    mean, variance, main_effects, total_effects, sobol_indices = \
        get_ishigami_funciton_statistics()
    return Benchmark(
        {'fun':partial(ishigami_function,a=a,b=b),
         'jac':partial(ishigami_function_jacobian,a=a,b=b),
         'hess':partial(ishigami_function_hessian,a=a,b=b),
         'variable':variable,'mean':mean,'variance':variance,
         'main_effects':main_effects,'total_effects':total_effects,
         'sobol_indices':sobol_indices})

def setup_oakley_function():
    r"""
    Setup the Oakely function benchmark 

    .. math:: f(z) = a_1^Tz + a_2^T\sin(z) + a_3^T\cos(z) + z^TMz

    where :math:`z` consists of 15 I.I.D. standard Normal variables and the data :math:`a_1,a_2,a_3` and :math:`M` are defined in the function :func:`pyapprox.benchmarks.sensitivity_benchmarks.get_oakley_function_data`.

    >>> from pyapprox.benchmarks.benchmarks import setup_benchmark
    >>> benchmark=setup_benchmark('oakley')
    >>> print(benchmark.keys())
    dict_keys(['fun', 'variable', 'mean', 'variance', 'main_effects'])

    Returns
    -------
    benchmark : pya.Benchmark
       Object containing the benchmark attributes

    References
    ----------
    .. [OakelyOJRSB2004] `Oakley, J.E. and O'Hagan, A. (2004), Probabilistic sensitivity analysis of complex models: a Bayesian approach. Journal of the Royal Statistical Society: Series B (Statistical Methodology), 66: 751-769. <https://doi.org/10.1111/j.1467-9868.2004.05304.x>`_
    """
    univariate_variables = [stats.norm()]*15
    variable=pya.IndependentMultivariateRandomVariable(univariate_variables)
    mean, variance, main_effects = oakley_function_statistics()
    return Benchmark(
        {'fun':oakley_function,
         'variable':variable,'mean':mean,'variance':variance,
         'main_effects':main_effects})

def setup_rosenbrock_function(nvars):
    r"""
    Setup the Rosenbrock function benchmark 

    .. math:: f(z) = \sum_{i=1}^{d/2}\left[100(z_{2i-1}^{2}-z_{2i})^{2}+(z_{2i-1}-1)^{2}\right]

    using 

    >>> from pyapprox.benchmarks.benchmarks import setup_benchmark
    >>> benchmark=setup_benchmark('rosenbrock',nvars=2)
    >>> print(benchmark.keys())
    dict_keys(['fun', 'jac', 'hessp', 'variable'])

    Parameters
    ----------
    nvars : integer
        The number of variables of the Rosenbrock function

    Returns
    -------
    benchmark : pya.Benchmark
       Object containing the benchmark attributes

    References
    ----------
    .. [DixonSzego1990] `Dixon, L. C. W.; Mills, D. J. "Effect of Rounding Errors on the Variable Metric Method". Journal of Optimization Theory and Applications. 80: 175–179. 1994 <https://doi.org/10.1007%2FBF02196600>`_
    """
    univariate_variables = [stats.uniform(-2,4)]*nvars
    variable=pya.IndependentMultivariateRandomVariable(univariate_variables)
    
    return Benchmark(
        {'fun':rosenbrock_function,'jac':rosenbrock_function_jacobian,
         'hessp':rosenbrock_function_hessian_prod,'variable':variable})

def setup_genz_function(nvars,test_name,coefficients=None):
    r"""
    Setup the Genz Benchmarks.
    
    For example, the two-dimensional oscillatory Genz problem can be defined 
    using
    
    >>> from pyapprox.benchmarks.benchmarks import setup_benchmark
    >>> benchmark=setup_benchmark('genz',nvars=2,test_name='oscillatory')
    >>> print(benchmark.keys())
    dict_keys(['fun', 'mean', 'variable'])

    Parameters
    ----------
    nvars : integer
        The number of variables of the Genz function
    
    test_name : string
        The test_name of the specific Genz function. See notes
        for options the string needed is given in brackets
        e.g. ('oscillatory')

    coefficients : tuple (ndarray (nvars), ndarray (nvars))
        The coefficients :math:`c_i` and :math:`w_i`
        If None (default) then 
        :math:`c_j = \hat{c}_j\left(\sum_{i=1}^d \hat{c}_i\right)^{-1}` where 
        :math:`\hat{c}_i=(10^{-15\left(\frac{i}{d}\right)^2)})`

    Returns
    -------
    benchmark : pya.Benchmark
       Object containing the benchmark attributes

    References
    ----------
    .. [Genz1984] `Genz, A. Testing multidimensional integration routines. In Proc. of international conference on Tools, methods and languages for scientific and engineering computation (pp. 81-94), 1984 <https://dl.acm.org/doi/10.5555/2837.2842>`_

    Notes
    -----

    Corner Peak ('corner-peak')

    .. math:: f(z)=\left( 1+\sum_{i=1}^d c_iz_i\right)^{-(d+1)}

    Oscillatory ('oscillatory')

    .. math:: f(z) = \cos\left(2\pi w_1 + \sum_{i=1}^d c_iz_i\right) 

    Gaussian Peak ('gaussian-peak')

    .. math:: f(z) = \exp\left( -\sum_{i=1}^d c_i^2(z_i-w_i)^2\right)

    Continuous ('continuous')

    .. math:: f(z) = \exp\left( -\sum_{i=1}^d c_i\lvert z_i-w_i\rvert\right)
    
    Product Peak ('product-peak')

    .. math:: f(z) = \prod_{i=1}^d \left(c_i^{-2}+(z_i-w_i)^2\right)^{-1}

    Discontinuous ('discontinuous')

    .. math:: f(z) = \begin{cases}0 & x_1>u_1 \;\mathrm{or}\; x_2>u_2\\\exp\left(\sum_{i=1}^d c_iz_i\right) & \mathrm{otherwise}\end{cases}
    
    """
    genz = GenzFunction(test_name,nvars)
    univariate_variables = [stats.uniform(0,1)]*nvars
    variable=pya.IndependentMultivariateRandomVariable(univariate_variables)
    if coefficients is None:
        genz.set_coefficients(1,'squared-exponential-decay',0)
    else:
        genz.c,genz.w = coefficients
    attributes = {'fun':genz,'mean':genz.integrate(),'variable':variable}
    if test_name=='corner-peak':
        attributes['variance']=genz.variance()
        from scipy.optimize import OptimizeResult
    return Benchmark(attributes)

try:
    from pyapprox.fenics_models.advection_diffusion_wrappers import \
        setup_advection_diffusion_benchmark as setup_advection_diffusion
except:
    pass

def setup_benchmark(name,**kwargs):
    benchmarks = {'sobol_g':setup_sobol_g_function,
                  'ishigami':setup_ishigami_function,
                  'oakley':setup_oakley_function,
                  'rosenbrock':setup_rosenbrock_function,
                  'genz':setup_genz_function}

    try:
        # will fail if fenics is not installed and the import of the fenics
        # benchmarks fail
        fenics_benchmarks={
            'advection-diffusion':setup_advection_diffusion}
        benchmarks.update(fenics_benchmarks)
    except:
        pass


    if name not in benchmarks:
        msg = f'Benchmark "{name}" not found.\n Avaiable benchmarks are:\n'
        for key in benchmarks.keys():
            msg += f"\t{key}\n"
        raise Exception(msg)

    return benchmarks[name](**kwargs)
