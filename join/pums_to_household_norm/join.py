__author__ = 'SEOKHO'

import pandas as pd
import numpy as np
from collections import Counter

pums = pd.read_csv("join_features.csv")
del pums[pums.columns.values[0]]

household = pd.read_csv("../../data/household_electricity_usage/recs2009_public.csv")
variables = pd.read_csv("variables.tsv", delimiter = '\t')

household_variables = variables['household']
#reduction of household to the features we need
for column in list(household.columns):
    if column not in household_variables.values:
        del household[column]

def household_DIVISION(input):
    if input == 8 or input == 9:
        return 8
    if input == 10:
        return 9
    return input

def pums_ST(input):
    mapping = {1: 18,
     2: 27,
     4: 24,
     5: 20,
     6: 26,
     8: 22,
     9: 1,
     10: 14,
     11: 14,
     12: 17,
     13: 15,
     15: 27,
     16: 23,
     17: 6,
     18: 7,
     19: 10,
     20: 11,
     21: 18,
     22: 20,
     23: 1,
     24: 14,
     25: 2,
     26: 8,
     27: 10,
     28: 18,
     29: 12,
     30: 23,
     31: 11,
     32: 25,
     33: 1,
     34: 4,
     35: 25,
     36: 3,
     37: 16,
     38: 10,
     39: 7,
     40: 20,
     41: 27,
     42: 5,
     44: 1,
     45: 16,
     46: 10,
     47: 19,
     48: 21,
     49: 23,
     50: 1,
     51: 13,
     53: 27,
     54: 14,
     55: 9,
     56: 23,
     72 : 1}
    return mapping[input]

def pums_YBL(input):
    if input == 1:
        return 1939
    if input == 2:
        return 1945
    if input == 3:
        return 1955
    if input == 4:
        return 1965
    if input == 5:
        return 1975
    if input == 6:
        return 1985
    if input == 7:
        return 1995
    if input == 8:
        return 2002
    return 1996 + input

def pums_MV(input):
    if input == 1:
        return 1
    if input == 2:
        return 2
    if input == 3:
        return 3
    if input == 4:
        return 7
    if input == 5:
        return 15
    if input == 6:
        return 25
    if input == 7:
        return 30

def household_OCCUPYRANGE(input):
    if input == 8:
        return 2
    if input == 7:
        return 7
    if input == 6:
        return 14
    if input == 5:
        return 24
    if input == 4:
        return 34
    if input == 3:
        return 44
    if input == 2:
        return 54
    if input == 1:
        return 64

def household_MONEYPY(input):
    if input == 1:
        return 2500
    if input == 2:
        return 3750
    if input == 3:
        return 6250
    if input == 4:
        return 8750
    if input == 5:
        return 12500
    if input == 6:
        return 17500
    if input == 7:
        return 22500
    if input == 8:
        return 27500
    if input == 9:
        return 32500
    if input == 10:
        return 37500
    if input == 11:
        return 42500
    if input == 12:
        return 47500
    if input == 13:
        return 52500
    if input == 14:
        return 57500
    if input == 15:
        return 62500
    if input == 16:
        return 67500
    if input == 17:
        return 72500
    if input == 18:
        return 77500
    if input == 19:
        return 82500
    if input == 20:
        return 87500
    if input == 21:
        return 92500
    if input == 22:
        return 97500
    if input == 23:
        return 110000
    if input == 24:
        return 120000

def pums_TEN(input):
    if input == 1 or input == 2:
        return 1
    return input - 1

def household_NUMAPTS_TYPEHUQ(input):
    numapts, typehuq = input
    output = None
    if typehuq >= 1 and typehuq <= 4:
        output = typehuq
    if numapts >= 5 and numapts <= 9:
        output = 6
    if numapts >= 10 and numapts <= 19:
        output = 7
    if numapts >= 20 and numapts <= 49:
        output = 8
    if numapts >= 50:
        output = 9
    return (0, output)

def pums_BLD(input):
    if input == 5:
        return 4
    return input

def pums_FS(input):
    if input == 2:
        return 0
    return input

def pums_ACCESS(input):
    if input == 2:
        return 1
    if input == 3:
        return 0
    return input

def pums_flag(input):
    if input == 2:
        return 0
    return 1

def pums_DSL_FIBEROP(input):
    dsl, fiberop = input
    if dsl == 1 or fiberop == 1:
        return (1, 0)
    return (2, 0)

def household_FUELHEAT(input):
    if input == 1 or input == 2:
        return input
    if input == 5:
        return 3
    if input == 3:
        return 4
    if input == 4:
        return 4
    if input == 7:
        return 6
    if input == 8:
        return 7
    if input == 9 or input == 21:
        return 8
    return -2

def household_NUMPC(input):
    if input == 0:
        return 2
    return 1

def household_NUMFRIG(input):
    if input == 0:
        return 2
    return 1

def pums_FES(input):
    if input >= 1 and input <= 3:
        return 1
    if input == 5 or input == 7:
        return 2
    return 0

def household_EMPLOYHH_SPOUSE(input):
    employhh, spouse = input
    if (employhh == 1 or employhh == 2) and spouse == 0:
        return (0, 1)
    if (employhh == 1 or employhh == 2) and spouse == 1:
        return (0, 2)
    return (0, 0)

def pums_HISP(input):
    if input == 1:
        return 0
    return 1

def pums_RAC1P(input):
    if input == 4:
        return 3
    if input == 5:
        return 3
    if input == 6:
        return 4
    if input == 7:
        return 5
    if input == 8:
        return 6
    if input == 9:
        return 7
    return input

def pums_SCHL(input):
    if input == 1:
        return 0
    if input >= 2 and input <= 15:
        return 1
    if input == 16:
        return 2
    if input == 17:
        return 2
    if input == 18 or input == 19:
        return 3
    return input + 16

def pums_INTP(input):
    if input > 0:
        return 1
    return 0

def pums_FULP(input):
    return input * 12

def household_POVERTY(input):
    poverty100, poverty150 = input
    if poverty100 == 1:
        return (100, 0)
    if poverty150 == 1:
        return (150, 0)
    return (501, 0)

def household_FULP(input):
    dollarker, dollarel, dollarp = input
    return (0, 0, dollarker + dollarel + dollarp)

def pums_ELEP(input):
    if input < 3:
        return input
    return input * 12

#No changes to DIVISON
#No changes to ST
pums['ST'] = pums['ST'].apply(pums_ST)
household['DIVISION'] = household['DIVISION'].apply(household_DIVISION)

#Not changing ELEP/DOLLAREL - the codes will have very little overlap since who pays $1-2? They should retain their significance and mostly pass unharmed
#pums differing dollar metric might be problematic however, but I don't have ADJHSG values

#same for GASP
#FULP~=DOLLARLP
pums['FULP'] = pums['FULP'].apply(pums_FULP)
pums['ELEP'] = pums['ELEP'].apply(pums_ELEP)
household[['DOLLARKER', 'DOLLARFO', 'DOLLARLP']] = household[['DOLLARKER', 'DOLLARFO', 'DOLLARLP']].apply(household_FULP, axis = 1, broadcast = True)
del household['DOLLARKER']
del household['DOLLARFO']

pums['YBL'] = pums['YBL'].apply(pums_YBL)
pums['MV'] = pums['MV'].apply(pums_MV)
household['OCCUPYYRANGE'] = household['OCCUPYYRANGE'].apply(household_OCCUPYRANGE)
household['MONEYPY'] = household['MONEYPY'].apply(household_MONEYPY)
pums['TEN'] = pums['TEN'].apply(pums_TEN)

#not modifying NP/NHSLDMEM

#condominium fields are next to useless I feel
del pums['CONP']
del household['CONDCOOP']

pums['BLD'] = pums['BLD'].apply(pums_BLD)
#merge away NUMAPTS so BLD ~= NUMAPTS
household[['NUMAPTS', 'TYPEHUQ']] = household[['NUMAPTS', 'TYPEHUQ']].apply(household_NUMAPTS_TYPEHUQ, axis = 1, broadcast = True)
del household['NUMAPTS']

#not changing bdsp, RMSP

pums['FS'] = pums['FS'].apply(pums_FS)
pums['ACCESS'] = pums['ACCESS'].apply(pums_ACCESS)
pums['MODEM'] = pums['MODEM'].apply(pums_flag)
pums['SATELLITE'] = pums['SATELLITE'].apply(pums_flag)
pums['DIALUP'] = pums['DIALUP'].apply(pums_flag)

#merge fiberop into dsl, dsl~= INDSL
pums[['DSL', 'FIBEROP']] = pums[['DSL', 'FIBEROP']].apply(pums_DSL_FIBEROP, axis = 1, broadcast = True)
del pums['FIBEROP']

household['FUELHEAT'] = household['FUELHEAT'].apply(household_FUELHEAT)
household['NUMPC'] = household['NUMPC'].apply(household_NUMPC)
household['STOVEN'] = household['STOVEN'].apply(household_NUMPC) #applies here too

household[['EMPLOYHH', 'SPOUSE']] = household[['EMPLOYHH', 'SPOUSE']].apply(household_EMPLOYHH_SPOUSE, axis = 1, broadcast = True)
del household['SPOUSE']
pums['FES'] = pums['FES'].apply(pums_FES)

pums['HISP'] = pums['HISP'].apply(pums_HISP)

pums['RAC1P'] = pums['RAC1P'].apply(pums_RAC1P)

#AGEP left alone
pums['SCHL'] = pums['SCHL'].apply(pums_SCHL)

pums['INTP'] = pums['INTP'].apply(pums_INTP)
pums['WAGP'] = pums['WAGP'].apply(pums_INTP)
pums['RETP'] = pums['RETP'].apply(pums_INTP)
pums['SSIP'] = pums['SSIP'].apply(pums_INTP)

#might be better to combine the other way...
#dropping POVERTY150, so POVPIP~=POVERTY100
household[['POVERTY100', 'POVERTY150']] = household[['POVERTY100', 'POVERTY150']].apply(household_POVERTY, axis = 1, broadcast = True)
del household['POVERTY150']

pums.to_csv("join_features_normalized.csv", index = False)
household.to_csv("household_normalized.csv", index = False)
