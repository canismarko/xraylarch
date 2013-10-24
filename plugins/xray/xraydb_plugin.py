import sys
from math import pi
import larch
from larch import Group
from larch.larchlib import use_plugin_path

use_plugin_path('xray')

from physical_constants import R_ELECTRON_CM, AVOGADRO, PLANCK_HC
from chemparser import chemparse
from xraydb import xrayDB

MODNAME = '_xray'


def get_xraydb(_larch):
    symname = '%s._xraydb' % MODNAME
    if _larch.symtable.has_symbol(symname):
        return _larch.symtable.get_symbol(symname)
    xraydb = xrayDB()
    _larch.symtable.set_symbol(symname, xraydb)
    return xraydb

def f0(ion, q, _larch=None):
    """returns elastic x-ray scattering factor, f0(q), for an ion.

    based on calculation from
       D. Waasmaier and A. Kirfel, Acta Cryst. A51 p416 (1995)
    and tables from International Tables for Crystallography, Vol. C.

    arguments
    ---------
    ion:  atomic number, atomic symbol or ionic symbol
           (case insensitive) of scatterer

    q:    single q value, list, tuple, or numpy array of q value
              q = sin(theta) / lambda
          theta = incident angle, lambda = x-ray wavelength
    Z values from 1 to 98 (and symbols 'H' to 'Cf') are supported.
    The list of ionic symbols can be read with the function .f0_ions()
    """
    if _larch is None:  return
    xdb = get_xraydb(_larch)
    return xdb.f0(ion, q)

def f0_ions(element=None, _larch=None):
    """return list of ion names supported in the f0() calculation from
    Waasmaier and Kirfel.

    arguments
    ---------
    element:  atomic number, atomic symbol or ionic symbol
              (case insensitive) of scatterer

    if element is None, all 211 ions are returned.  If element is
    not None, the ions for that element (atomic symbol) are returned
    """
    if _larch is None:  return
    xdb = get_xraydb(_larch)
    return xdb.f0_ions(element=element)

def chantler_energies(element, emin=0, emax=1.e9, _larch=None):
    """ return array of energies (in eV) at which data is
    tabulated in the Chantler tables for a particular element.

    arguments
    ---------
    element:  atomic number, atomic symbol for element

    emin:  lower bound of energies in eV returned (default=0)
    emax:  upper bound of energies in eV returned (default=1.e9)
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.chantler_energies(element, emin=emin, emax=emax)

def chantler_data(element, energy, column, _larch=None, **kws):
    """returns data from Chantler tables.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    column:   one of 'f1', 'f2', 'mu_photo', 'mu_incoh', 'mu_total'
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb._getChantler(element, energy, column=column, **kws)

def f1_chantler(element, energy, _larch=None, **kws):
    """returns real part of anomalous x-ray scattering factor for
    a selected element and input energy (or array of energies) in eV.
    Data is from the Chantler tables.

    Values returned are in units of electrons

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb._getChantler(element, energy, column='f1', **kws)

def f2_chantler(element, energy, _larch=None):
    """returns imaginary part of anomalous x-ray scattering factor for
    a selected element and input energy (or array of energies) in eV.
    Data is from the Chantler tables.

    Values returned are in units of electrons.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb._getChantler(element, energy, column='f2')

def mu_chantler(element, energy, incoh=False, photo=False, _larch=None):
    """returns x-ray mass attenuation coefficient, mu/rho, for a
    selected element and input energy (or array of energies) in eV.
    Data is from the Chantler tables.

    Values returned are in units of cm^2/gr.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    photo=True: flag to return only the photo-electric contribution
    incoh=True: flag to return only the incoherent contribution

    The default is to return total attenuation coefficient.
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    col = 'mu_total'
    if photo: col = 'mu_photo'
    if incoh: col = 'mu_incoh'
    return xdb._getChantler(element, energy, column=col)

def mu_elam(element, energy, _larch=None):
    """returns x-ray mass attenuation coefficient, mu/rho, for a
    selected element and input energy (or array of energies) in eV.
    Data is from the Elam tables.

    Values returned are in units of cm^2/gr.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.mu_elam(element, energy)

def coherent_cross_section_elam(element, energy, _larch=None):
    """returns coherent scattering cross section
    selected element and input energy (or array of energies) in eV.
    Data is from the Elam tables.

    Values returned are in units of cm^2/gr.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.coherent_cross_section_elam(element, energy)

def incoherent_cross_section_elam(element, energy, _larch=None):
    """returns incoherent scattering cross section
    selected element and input energy (or array of energies) in eV.
    Data is from the Elam tables.

    Values returned are in units of cm^2/gr.

    arguments
    ---------
    element:  atomic number, atomic symbol for element
    energy:   energy or array of energies in eV
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.incoherent_cross_section_elam(element, energy)

def atomic_number(element, _larch=None):
    "return z for element name"
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return int(xdb._getElementData(element).atomic_number)

def atomic_symbol(z, _larch=None):
    "return element symbol from z"
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb._getElementData(z).element

def atomic_mass(element, _larch=None):
    "return molar mass (amu) from element symbol or atomic number"
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    if isinstance(element, int):
        element = atomic_symbol(element, _larch=_larch)
    return xdb._getElementData(element).molar_mass

def atomic_density(element, _larch=None):
    "return density (gr/cm^3) from element symbol or atomic number"
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    if isinstance(element, int):
        element = atomic_symbol(element, _larch=_larch)
    return xdb._getElementData(element).density

def xray_edges(element, _larch=None):
    """returns dictionary of all x-ray absorption edge energies
    (in eV), fluorescence yield, and jump ratio for an element.

    the returned dictionary has keys of edge (iupac symol),
    each with value containing a tuple of (energy,
    fluorescence_yield, edge_jump)

    Data from Elam, Ravel, and Sieber
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.xray_edges(element)

def xray_edge(element, edge, _larch=None):
    """returns edge energy (in eV), fluorescence yield, and
    jump ratio for an element and edge.

    Data from Elam, Ravel, and Sieber
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.xray_edge(element, edge)

def xray_lines(element, initial_level=None, excitation_energy=None,
               _larch=None):
    """returns dictionary of x-ray emission lines of an element, with
    key = siegbahn symbol (Ka1, Lb1, etc)  and
    value = (energy (in eV), intensity, initial_level, final_level)

    arguments
    ---------
    element:           atomic number, atomic symbol for element
    initial_level:     limit output to an initial level(s) -- a string or list of strings
    excitation_energy: limit output to those excited by given energy (in eV)

    Note that excitation energy will overwrite initial_level, as it means
       'all intial levels with below this energy/

    Data from Elam, Ravel, and Sieber.
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.xray_lines(element, initial_level=initial_level,
                          excitation_energy=excitation_energy)

def xray_line(element, line='Ka1', _larch=None):
    """returns data for an  x-ray emission lines of an element, given
    the siegbahn notation for the like (Ka1, Lb1, etc).  Returns:
         energy (in eV), intensity, initial_level, final_level

    arguments
    ---------
    element:   atomic number, atomic symbol for element
    line:      siegbahn notation for emission line

    Data from Elam, Ravel, and Sieber.
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    lines = xdb.xray_lines(element)
    return lines.get(line.title(), None)



def fluo_yield(symbol, edge, emission, energy,
               energy_margin=-150, _larch=None):
    """Given
         atomic_symbol, edge, emission family, and incident energy,

    where 'emission' is the family of emission lines ('Ka', 'Kb', 'Lb', etc)
    returns

    fluorescence_yield, weighted-average fluorescence energy, net_probability

    fyield = 0  if energy < edge_energy + energy_margin (default=-150)

    > fluo_yield('Fe', 'K', 'Ka', 8000)
    0.350985, 6400.752419799043, 0.874576096

    > fluo_yield('Fe', 'K', 'Ka', 6800)
    0.0, 6400.752419799043, 0.874576096

    > fluo_yield('Ag', 'L3', 'La', 6000)
    0.052, 2982.129655446868, 0.861899000000000

    compare to xray_lines() which gives the full set of emission lines
    ('Ka1', 'Kb3', etc) and probabilities for each of these.

    Adapted for Larch from code by Yong Choi
    """
    e0, fyield, jump = xray_edge(symbol, edge, _larch=_larch)
    trans  = xray_lines(symbol, initial_level=edge, _larch=_larch)

    lines = []
    net_ener, net_prob = 0., 0.
    for name, vals in trans.items():
        en, prob = vals[0], vals[1]
        if name.startswith(emission):
            lines.append([name, en, prob])

    for name, en, prob in lines:
        if name.startswith(emission):
            net_ener += en*prob
            net_prob += prob
    if net_prob <= 0:
        net_prob = 1
    net_ener = net_ener / net_prob
    if energy < e0 + energy_margin:
        fyield = 0
    return fyield, net_ener, net_prob

def CK_probability(element, initial, final, total=True, _larch=None):
    """return transition probability for an element, initial, and final levels.

    arguments
    ---------
    element:     atomic number, atomic symbol for element
    initial:     initial level ('K', 'L1', ...)
    final:       final level ('L1', 'L2', ...)
    total:       whether to include transitions via possible intermediate
                 levels (default = True)

    Data from Elam, Ravel, and Sieber.
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.CK_probability(element, initial, final, total=total)

def core_width(element=None, edge=None, _larch=None):
    """returns core hole width for an element and edge

    arguments
    ---------
    if element is None, values are returned for all elements
    if edge is None, values are return for all edges


    Data from Keski-Rahkonen and Krause
    """
    if _larch is None:
        return
    xdb = get_xraydb(_larch)
    return xdb.corehole_width(element=element, edge=edge)


###

class Scatterer:
    """Scattering Element

    lamb=PLANCK_HC /(eV0/1000.)*1e-11    # in cm, 1e-8cm = 1 Angstrom
    Xsection=2* R_ELECTRON_CM *lamb*f2/BARN    # in Barns/atom
    """
    def __init__(self, symbol, energy=10000, _larch=None):
        # atomic symbol and incident x-ray energy (eV)
        self.symbol = symbol
        self.number = atomic_number(symbol, _larch=_larch)
        self.mass   = atomic_mass(symbol, _larch=_larch)
        self.f1     = chantler_data(symbol, energy, 'f1', _larch=_larch)
        self.f1     = self.f1 + self.number
        self.f2     = chantler_data(symbol, energy, 'f2', _larch=_larch)
        self.mu_photo = chantler_data(symbol, energy, 'mu_photo', _larch=_larch)
        self.mu_total = chantler_data(symbol, energy, 'mu_total', _larch=_larch)

def xray_delta_beta(material, density, energy, photo_only=False, _larch=None):
    """
    return anomalous components of the index of refraction for a material,
    using the tabulated scattering components from Chantler.

    arguments:
    ----------
       material:   chemical formula  ('Fe2O3', 'CaMg(CO3)2', 'La1.9Sr0.1CuO4')
       density:    material density in g/cm^3
       energy:     x-ray energy in eV
       photo_only: boolean for returning photo cross-section component only
                   if False (default), the total cross-section is returned
    returns:
    ---------
      (delta, beta, atlen)

    where
      delta :  real part of index of refraction
      beta  :  imag part of index of refraction
      atlen :  attenuation length in cm

    These are the anomalous scattering components of the index of refraction:

    n = 1 - delta - i*beta = 1 - lambda**2 * r0/(2*pi) Sum_j (n_j * fj)

    Adapted for Larch from code by Yong Choi
    """
    lamb_cm = 1.e-8 * PLANCK_HC / energy # lambda in cm
    elements = []
    for symbol, number in chemparse(material).items():
        elements.append((number, Scatterer(symbol, energy, _larch=_larch)))

    total_mass, delta, beta_photo, beta_total = 0, 0, 0, 0
    for (number, scat) in elements:
        weight      = density*number*AVOGADRO
        delta      += weight * scat.f1
        beta_photo += weight * scat.f2
        beta_total += weight * scat.f2*(scat.mu_total/scat.mu_photo)
        total_mass += number * scat.mass

    scale = lamb_cm * lamb_cm * R_ELECTRON_CM / (2*pi * total_mass)
    delta = delta * scale
    beta  = beta_total * scale
    if photo_only:
        beta  = beta_photo * scale
    return delta, beta, lamb_cm/(4*pi*beta)

def initializeLarchPlugin(_larch=None):
    """initialize xraydb"""
    if _larch is not None:
        xdb = get_xraydb(_larch)

def registerLarchPlugin():
    return (MODNAME, {'f0': f0, 'f0_ions': f0_ions,
                      'chantler_energies': chantler_energies,
                      'chantler_data': chantler_data,
                      'f1_chantler': f1_chantler,
                      'f2_chantler': f2_chantler,
                      'mu_chantler': mu_chantler,
                      'mu_elam': mu_elam,
                      'coherent_xsec': coherent_cross_section_elam,
                      'incoherent_xsec': incoherent_cross_section_elam,
                      'atomic_number': atomic_number,
                      'atomic_symbol': atomic_symbol,
                      'atomic_mass':   atomic_mass,
                      'atomic_density': atomic_density,
                      'xray_edges': xray_edges,
                      'xray_edge': xray_edge,
                      'xray_lines': xray_lines,
                      'xray_line': xray_line,
                      'fluo_yield': fluo_yield,
                      'core_width':  core_width,
                      'ck_probability': CK_probability,
                      'xray_delta_beta': xray_delta_beta,
                      })


