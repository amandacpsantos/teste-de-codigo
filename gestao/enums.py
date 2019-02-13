from enum import Enum


class Escolaridade(Enum):
    EF = 'Ensino Fundamental'
    EM = 'Ensino Médio'
    TG = 'Tecnólogo'
    ES = 'Ensino Superior'
    PS = 'Pós / MBA / Mestrado'
    DR = 'Doutorado'


class FaixaSalarial(Enum):
    A1 = 'Até 1.000'
    D1A2 = 'De 1.000 a 2.000'
    D2A3 = 'De 2.000 a 3.000'
    AC3 = 'Acima de 3.000'
