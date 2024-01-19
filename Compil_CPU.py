import re
import random

#Opérations réalisées par l'UAL
operationsUAL = ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'SL', 'SR', 'MUL']
operationsMEM = ['STR', 'LD']
operationsCTRL = ['JMP', 'JEQU', 'JNEQ', 'JSUP','JINF', 'JEIN','CALL','RET']

labels = {'F' : '0101010101010101'}

def bin_to_hexa(binaire):
    try:
        # Convertir la chaîne binaire en entier
        entier = int(binaire, 2)
        
        # Convertir l'entier en hexadécimal
        hexadecimal = hex(entier).upper()

        return hexadecimal
    except ValueError:
        return "Format binaire invalide"

def traduire_instruction(instruction):
    # Définir l'expression régulière pour extraire les composants
    regex = re.compile(r'([A-Z]+)\s+([A-Z0-9]+)\s*(?:\s*([A-Z0-9]+))?\s*(?:\s*([A-Z0-9]+))?\s*(?:\s*(\d+))?')
    match = regex.match(instruction)

    if match:
        operation = match.group(1)
        reg_destination = match.group(2)
        reg_source1 = match.group(3)
        reg_source2_or_const = match.group(4)
        
        def is_constante(reg):
            if reg is None:
                return '0'
            if reg[0] == 'R':
                return '0'
            else:
                return '1'

        def get_reg_address(reg):
            if reg[0] == 'R':
                return format(int(reg[1:]), '03b')
            if reg in labels:
                return labels[reg]
            else:
                return ''
            
        def get_constante(const):
            if const[0] == 'R':
                return '0000000000000'
            else:
                return format(int(const), '016b')
        
        def get_jmp_address(const):
            if const[0] == 'R':
                return ''
            else:
                return format(int(const), '016b')
            
        if operation in operationsUAL:
            binaire = '0000'+get_constante(reg_source2_or_const) if reg_source2_or_const is not None else '0000000000000000'#Constante sur 16 bits
            binaire += '0' if not is_constante(reg_source2_or_const) else ''
            binaire += get_reg_address(reg_source2_or_const) if reg_source2_or_const else '' #Adresse source2
            binaire += get_reg_address(reg_source1) if reg_source1 else '000' #Adresse source 1
            binaire += get_reg_address(reg_destination) #Adrrese de destination
            binaire += is_constante(reg_source2_or_const)  #Op immédiate
            binaire += format(operationsUAL.index(operation), '03b') #Opérations
            binaire += '00'  # Instruction UAL par défaut
        
        elif operation in operationsMEM:
            binaire = '0000000'+get_constante(reg_source1) if reg_source1 is not None else '0000000000000000'#Constante sur 16 bits
            binaire += get_reg_address(reg_source1) if reg_source1 else '' #Adresse source 1
            binaire += get_reg_address(reg_destination) #Adresse de destination
            binaire += is_constante(reg_source1)  #Op immédiate
            binaire += (format(operationsMEM.index(operation), '03b'))[::-1] #Opérations
            binaire += '01'  # Instruction MEM par défaut
        
        elif operation in operationsCTRL:
            binaire = ('0000'+get_jmp_address(reg_source2_or_const) if reg_source2_or_const is not None else '') or ('0000000000'+get_jmp_address(reg_destination) if reg_destination is not None else '') #Constante sur 16 bits
            binaire += get_reg_address(reg_source2_or_const) if reg_source2_or_const else '' #Adresse source 2
            binaire += get_reg_address(reg_source1) if reg_source1 else '' #Adresse source 1
            binaire += get_reg_address(reg_destination) if reg_destination else '' #Adrrese de destination
            binaire += '0'  #Op immédiate
            binaire += format(operationsCTRL.index(operation), '03b') #Opérations
            binaire += '11'  # Instruction CTRL par défaut

        return binaire
    else:
        return "Format d'instruction invalide"

operation_aleatoire = random.choice(operationsMEM)

instructions = """
XOR R0 R0 R0
ADD R1 R0 2
ADD R2 R0 4
CALL 10
ADD R6 R0 1
MUL R3 R1 R2
RET 4
ADD R5 R0 1
"""
instructions = """
XOR R7 R7 R7
ADD R7 R7 16
LD R4 R7
"""

instructions = """
XOR R0 R0 R0
ADD R1 R0 2
ADD R2 R0 4
CALL 10
ADD R6 R0 1
MUL R3 R1 R2
RET 4
ADD R5 R0 1
"""

#factorielle ??
instructions = """
XOR R0 R0 R0
ADD R1 R0 1
ADD R2 R0 1
ADD R4 R0 2
MUL R2 R2 R1
ADD R1 R1 1
JINF R1 R4 4
"""
instructions_list = instructions.strip().split('\n')

for instruction in instructions_list:
    resultat = traduire_instruction(instruction)
    #print(len(resultat))
    #print(f"Instruction binaire traduite ({instruction}): {resultat}")
    resultatBin = resultat
    resultat = bin_to_hexa(resultat)
    print(f"Instruction Hexa traduite ({instruction})({resultatBin}): {resultat}")