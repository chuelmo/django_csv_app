import csv
import os
from .models import SizeCategory, Size

TOTAL_FIELDS = 24
TITLE_FIRST_FIELD = 'NOMBRE DE MARCA'
OK = 'OK'
# Categories
ALL_CATEGORIES = []
SIZES = {}

def loadSizesAndCategories():
    categorias = SizeCategory.objects.all()
    for c in categorias:
        ALL_CATEGORIES.append(c.description)
        sizes = SizeCategory.objects.get(id=c.id).size_set.all()
        sizesList = []
        for s in sizes:
            sizesList.append(s.name)
        SIZES[c.description] = sizesList

def getSizesFromCategory(category):
    return SIZES.get(category.upper()) #lista de sizes

def areFieldsOk(line, line_number, brand, offer):
    isOk = True
    error_message = 'linea: ' + str(line_number) + ' ERROR: '
    if line[2] == '': # 'Codigo de Color'
        error_message += 'falta Codigo de Color, '
        isOk = False
    if line[3] == '': # 'Nombre'
        error_message += 'falta Nombre, '
        isOk = False
    if line[4] == '': # 'Descripcion de Color'
        error_message += 'falta Descripcion de Color, '
        isOk = False
    if line[6].upper() not in ALL_CATEGORIES: # 'Size Category'
        error_message += 'Size Category no existe'
        isOk = False
    if line[14] == '': # 'Estilo'
        error_message += 'falta Estilo, '
        isOk = False
    if line_number > 2:
        if line[0] != brand:
            error_message += 'La marca no coincide con la primer fila, '
            isOk = False
        if line[1] != offer:
            error_message += 'La oferta no coincide con la primer fila'
            isOk = False
    if isOk:
        return OK
    return error_message

def writeLineWithSize(csv_writer, line):
    curva = line[7]
    size = line[5]
    category = line[6]
    isNeedToAddSize = curva == '' and size == '' and category.upper() in ALL_CATEGORIES
    if isNeedToAddSize:
        sizeList = getSizesFromCategory(category)
        for sizeName in sizeList:
            line[5] = sizeName
            csv_writer.writerow(line)
    else:
        csv_writer.writerow(line)


def procesarCSV(fileName):
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    def is_binary_string(bytes): return bool(bytes.translate(None, textchars))
    if is_binary_string(open(fileName, 'rb').read(1024)):
        return ['ERROR: El archivo no es del tipo esperado']
    with open(fileName, 'r') as fileToClean:
        readerObj = list(csv.reader(fileToClean))
    newName = fileName + "_CLEAN.csv"
    errors = []
    if len(readerObj) < 2:
        return ['ERROR: El archivo no tiene líneas para procesar']
    loadSizesAndCategories()
    with open(newName, 'w') as fileToWrite:
        csv_writer = csv.writer(fileToWrite, delimiter=',')
        line_number = 1
        brand_name = ''
        offer_name = ''
        for line in readerObj:
            if line_number == 1:
                if len(line) != 24 and line[0] != TITLE_FIRST_FIELD:
                    return ['ERROR: El formato del archivo no es el esperado']
                msg_error = OK
            elif line_number == 2:
                brand_name = line[0] # 'Nombre de Marca'
                offer_name = line[1] # 'Oferta'
                msg_error = areFieldsOk(line, line_number, brand_name, offer_name)
            else:
                msg_error = areFieldsOk(line, line_number, brand_name, offer_name)
            if msg_error == OK:
                writeLineWithSize(csv_writer, line)
            else:
                line.insert(0, msg_error)
                errors.append(line)
            line_number += 1
    os.remove(fileName)
    os.rename(newName, fileName)
    errors.insert(0,'OK')
    return errors
                
