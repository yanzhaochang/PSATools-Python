# Global data
# Store all the simulation imported data
import pandas as pd


Base = {}  # System base data

YMatrix = {'basic': pd.DataFrame(columns=('row', 'column', 'real', 'imag')), 
    'B1': pd.DataFrame(columns=('row', 'column', 'real', 'imag')),
    'B2': pd.DataFrame(columns=('row', 'column', 'real', 'imag')),
    'dynamic': pd.DataFrame(columns=('row', 'column', 'real', 'imag')),
    'positive': pd.DataFrame(columns=('row', 'column', 'real', 'imag')),
    'negative': pd.DataFrame(columns=('row', 'column', 'real', 'imag')),
    'zero': pd.DataFrame(columns=('row', 'column', 'real', 'imag'))}  # Network matrix

PowFlowPar = {'k_max': 20, 'max_err': 0.00001, 'process': False}  # Power flow solution parameter

DynSimPar = {'current_time': 0.000, 'time_step': 0.001, 'output_file': '', 'meter': []}

  
# The following storage power flow model data
BusData = pd.DataFrame(columns=('BASKV', 'IDE', 'VM', 'VA')) 

LoadData = pd.DataFrame(columns=('PL', 'QL'))

ShuntData = pd.DataFrame(columns=('BL', ))

GenData = pd.DataFrame(columns=('PG', 'QG', 'QT' ,'QB' ,'VS', 'MBASE', 'ZR', 'ZX', 'PT', 'PB'))
 
LineData = pd.DataFrame(columns=('R', 'X', 'B', 'BI', 'BJ'))
 
TransData = pd.DataFrame(columns=('MAG1', 'MAG2', 'R1_2', 'X1_2', 'SBASE1_2','R2_3',
    'X2_3', 'SBASE2_3', 'R3_1', 'X3_1', 'SBASE3_1', 'WINDV1', 'NOMV1', 'WINDV2', 'NOMV2', 'WINDV3', 'NOMV3'))
 
HvdcData = pd.DataFrame(columns=('RDC', 'SETVL', 'VSCHD', 
    'NBR', 'ANMXR', 'ANMNR', 'RCR', 'XCR', 'EBASR', 'TRR', 'TAPR', 'TMXR', 'TMNR', 'STPR', 'XCAPR',
    'NBI', 'ANMXI', 'ANMNI', 'RCI', 'XCI', 'EBASI', 'TRI', 'TAPI', 'TMXI', 'TMNI', 'STPI', 'XCAPI',))

WtGenData = pd.DataFrame(columns=('PG', 'QG', 'QT' ,'QB' ,'VS', 'MBASE', 'ZR', 'ZX', 'PT', 'PB'))

PvUnitData = pd.DataFrame(columns=('PG', 'QG', 'QT' ,'QB' ,'VS', 'MBASE', 'ZR', 'ZX', 'PT', 'PB'))


# The following storage sequence network model data
BusSqData = pd.DataFrame(columns=('VP', 'VN', 'VZ'))  # Store node sequence voltage 

GenSqData = pd.DataFrame(columns=('ZRPOS', 'ZXPPDV', 'ZXPDV', 'ZXSDV', 'ZRNEG', 'ZXNEGDV', 'ZR0', 'ZX0DV', 'ZRG', 'ZXG'))

WtGenSqData = pd.DataFrame(columns=('ZRPOS', 'ZXPPDV', 'ZXPDV', 'ZXSDV', 'ZRNEG', 'ZXNEGDV', 'ZR0', 'ZX0DV', 'ZRG', 'ZXG'))

PvUnitSqData = pd.DataFrame(columns=('ZRPOS', 'ZXPPDV', 'ZXPDV', 'ZXSDV', 'ZRNEG', 'ZXNEGDV', 'ZR0', 'ZX0DV', 'ZRG', 'ZXG'))

LoadSqData = pd.DataFrame(columns=('PNEG', 'QNEG', 'PZERO', 'QZERO'))

LineSqData = pd.DataFrame(columns=('RLINZ', 'XLINZ', 'BCHZ', 'BI0', 'BJ0'))

ShuntSqData = pd.DataFrame(columns=('BSZERO', ))

TransSqData = pd.DataFrame(columns=('CC', 'RG1', 'XG1', 'R01', 'X01', 'RG2', 'XG2', 'R02', 'X02', 'RG3', 'XG3', 'R03', 'X03'))


# The following is used for dynamic simulation
SyncGenMd = {}  # Storage generator model data

ExciterMd = {}  # Storage excitation model data

TurGovMd = {}  # Storage turbine governor model data


# The following list variables are used to store the model state variables during dynamic simulation
# The state variable of each model consists of actual value and estimated value, and the end of estimated value contains '0'
GenStateVar = {}  # Generator state variables 

BusStateVar = {} # Bus state variables, bus voltage

ExcStateVar = {}  # State variables of excitation system

TurStateVar = {}  # State variable of speed control system


