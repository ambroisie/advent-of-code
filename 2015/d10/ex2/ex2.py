#!/usr/bin/env python

import collections
import enum
import sys


# https://en.wikipedia.org/wiki/Look-and-say_sequence#Cosmological_decay
class Atom(enum.StrEnum):
    H = "22"
    He = "13112221133211322112211213322112"
    Li = "312211322212221121123222112"
    Be = "111312211312113221133211322112211213322112"
    B = "1321132122211322212221121123222112"
    C = "3113112211322112211213322112"
    N = "111312212221121123222112"
    O = "132112211213322112"
    F = "31121123222112"
    Ne = "111213322112"
    Na = "123222112"
    Mg = "3113322112"
    Al = "1113222112"
    Si = "1322112"
    P = "311311222112"
    S = "1113122112"
    Cl = "132112"
    Ar = "3112"
    K = "1112"
    Ca = "12"
    Sc = "3113112221133112"
    Ti = "11131221131112"
    V = "13211312"
    Cr = "31132"
    Mn = "111311222112"
    Fe = "13122112"
    Co = "32112"
    Ni = "11133112"
    Cu = "131112"
    Zn = "312"
    Ga = "13221133122211332"
    Ge = "31131122211311122113222"
    As = "11131221131211322113322112"
    Se = "13211321222113222112"
    Br = "3113112211322112"
    Kr = "11131221222112"
    Rb = "1321122112"
    Sr = "3112112"
    Y = "1112133"
    Zr = "12322211331222113112211"
    Nb = "1113122113322113111221131221"
    Mo = "13211322211312113211"
    Tc = "311322113212221"
    Ru = "132211331222113112211"
    Rh = "311311222113111221131221"
    Pd = "111312211312113211"
    Ag = "132113212221"
    Cd = "3113112211"
    In = "11131221"
    Sn = "13211"
    Sb = "3112221"
    Te = "1322113312211"
    I = "311311222113111221"
    Xe = "11131221131211"
    Cs = "13211321"
    Ba = "311311"
    La = "11131"
    Ce = "1321133112"
    Pr = "31131112"
    Nd = "111312"
    Pm = "132"
    Sm = "311332"
    Eu = "1113222"
    Gd = "13221133112"
    Tb = "3113112221131112"
    Dy = "111312211312"
    Ho = "1321132"
    Er = "311311222"
    Tm = "11131221133112"
    Yb = "1321131112"
    Lu = "311312"
    Hf = "11132"
    Ta = "13112221133211322112211213322113"
    W = "312211322212221121123222113"
    Re = "111312211312113221133211322112211213322113"
    Os = "1321132122211322212221121123222113"
    Ir = "3113112211322112211213322113"
    Pt = "111312212221121123222113"
    Au = "132112211213322113"
    Hg = "31121123222113"
    Tl = "111213322113"
    Pb = "123222113"
    Bi = "3113322113"
    Po = "1113222113"
    At = "1322113"
    Rn = "311311222113"
    Fr = "1113122113"
    Ra = "132113"
    Ac = "3113"
    Th = "1113"
    Pa = "13"
    U = "3"

    def decay(self) -> list["Atom"]:
        match self:
            case Atom.H:
                return [Atom.H]
            case Atom.He:
                return [Atom.Hf, Atom.Pa, Atom.H, Atom.Ca, Atom.Li]
            case Atom.Li:
                return [Atom.He]
            case Atom.Be:
                return [Atom.Ge, Atom.Ca, Atom.Li]
            case Atom.B:
                return [Atom.Be]
            case Atom.C:
                return [Atom.B]
            case Atom.N:
                return [Atom.C]
            case Atom.O:
                return [Atom.N]
            case Atom.F:
                return [Atom.O]
            case Atom.Ne:
                return [Atom.F]
            case Atom.Na:
                return [Atom.Ne]
            case Atom.Mg:
                return [Atom.Pm, Atom.Na]
            case Atom.Al:
                return [Atom.Mg]
            case Atom.Si:
                return [Atom.Al]
            case Atom.P:
                return [Atom.Ho, Atom.Si]
            case Atom.S:
                return [Atom.P]
            case Atom.Cl:
                return [Atom.S]
            case Atom.Ar:
                return [Atom.Cl]
            case Atom.K:
                return [Atom.Ar]
            case Atom.Ca:
                return [Atom.K]
            case Atom.Sc:
                return [Atom.Ho, Atom.Pa, Atom.H, Atom.Ca, Atom.Co]
            case Atom.Ti:
                return [Atom.Sc]
            case Atom.V:
                return [Atom.Ti]
            case Atom.Cr:
                return [Atom.V]
            case Atom.Mn:
                return [Atom.Cr, Atom.Si]
            case Atom.Fe:
                return [Atom.Mn]
            case Atom.Co:
                return [Atom.Fe]
            case Atom.Ni:
                return [Atom.Zn, Atom.Co]
            case Atom.Cu:
                return [Atom.Ni]
            case Atom.Zn:
                return [Atom.Cu]
            case Atom.Ga:
                return [Atom.Eu, Atom.Ca, Atom.Ac, Atom.H, Atom.Ca, Atom.Zn]
            case Atom.Ge:
                return [Atom.Ho, Atom.Ga]
            case Atom.As:
                return [Atom.Ge, Atom.Na]
            case Atom.Se:
                return [Atom.As]
            case Atom.Br:
                return [Atom.Se]
            case Atom.Kr:
                return [Atom.Br]
            case Atom.Rb:
                return [Atom.Kr]
            case Atom.Sr:
                return [Atom.Rb]
            case Atom.Y:
                return [Atom.Sr, Atom.U]
            case Atom.Zr:
                return [Atom.Y, Atom.H, Atom.Ca, Atom.Tc]
            case Atom.Nb:
                return [Atom.Er, Atom.Zr]
            case Atom.Mo:
                return [Atom.Nb]
            case Atom.Tc:
                return [Atom.Mo]
            case Atom.Ru:
                return [Atom.Eu, Atom.Ca, Atom.Tc]
            case Atom.Rh:
                return [Atom.Ho, Atom.Ru]
            case Atom.Pd:
                return [Atom.Rh]
            case Atom.Ag:
                return [Atom.Pd]
            case Atom.Cd:
                return [Atom.Ag]
            case Atom.In:
                return [Atom.Cd]
            case Atom.Sn:
                return [Atom.In]
            case Atom.Sb:
                return [Atom.Pm, Atom.Sn]
            case Atom.Te:
                return [Atom.Eu, Atom.Ca, Atom.Sb]
            case Atom.I:
                return [Atom.Ho, Atom.Te]
            case Atom.Xe:
                return [Atom.I]
            case Atom.Cs:
                return [Atom.Xe]
            case Atom.Ba:
                return [Atom.Cs]
            case Atom.La:
                return [Atom.Ba]
            case Atom.Ce:
                return [Atom.La, Atom.H, Atom.Ca, Atom.Co]
            case Atom.Pr:
                return [Atom.Ce]
            case Atom.Nd:
                return [Atom.Pr]
            case Atom.Pm:
                return [Atom.Nd]
            case Atom.Sm:
                return [Atom.Pm, Atom.Ca, Atom.Zn]
            case Atom.Eu:
                return [Atom.Sm]
            case Atom.Gd:
                return [Atom.Eu, Atom.Ca, Atom.Co]
            case Atom.Tb:
                return [Atom.Ho, Atom.Gd]
            case Atom.Dy:
                return [Atom.Tb]
            case Atom.Ho:
                return [Atom.Dy]
            case Atom.Er:
                return [Atom.Ho, Atom.Pm]
            case Atom.Tm:
                return [Atom.Er, Atom.Ca, Atom.Co]
            case Atom.Yb:
                return [Atom.Tm]
            case Atom.Lu:
                return [Atom.Yb]
            case Atom.Hf:
                return [Atom.Lu]
            case Atom.Ta:
                return [Atom.Hf, Atom.Pa, Atom.H, Atom.Ca, Atom.W]
            case Atom.W:
                return [Atom.Ta]
            case Atom.Re:
                return [Atom.Ge, Atom.Ca, Atom.W]
            case Atom.Os:
                return [Atom.Re]
            case Atom.Ir:
                return [Atom.Os]
            case Atom.Pt:
                return [Atom.Ir]
            case Atom.Au:
                return [Atom.Pt]
            case Atom.Hg:
                return [Atom.Au]
            case Atom.Tl:
                return [Atom.Hg]
            case Atom.Pb:
                return [Atom.Tl]
            case Atom.Bi:
                return [Atom.Pm, Atom.Pb]
            case Atom.Po:
                return [Atom.Bi]
            case Atom.At:
                return [Atom.Po]
            case Atom.Rn:
                return [Atom.Ho, Atom.At]
            case Atom.Fr:
                return [Atom.Rn]
            case Atom.Ra:
                return [Atom.Fr]
            case Atom.Ac:
                return [Atom.Ra]
            case Atom.Th:
                return [Atom.Ac]
            case Atom.Pa:
                return [Atom.Th]
            case Atom.U:
                return [Atom.Pa]


def solve(input: str) -> int:
    def look_and_say(atoms: dict[Atom, int]) -> dict[Atom, int]:
        res: collections.Counter[Atom] = collections.Counter()
        for atom, count in atoms.items():
            for split in atom.decay():
                res[split] += count
        return res

    # Happens to work, I assume for all inputs
    atoms = {Atom(input.strip()): 1}
    for _ in range(50):
        atoms = look_and_say(atoms)
    return sum(len(atom) * count for atom, count in atoms.items())


def main() -> None:
    input = sys.stdin.read()
    print(solve(input))


if __name__ == "__main__":
    main()
