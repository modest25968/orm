import os.path
from model import BaseModel
from field import BaseField


def isFilesExist(filenames):
    for filename in filenames:
        if not os.path.isfile(filename+'.py'):
            print("file '"+filename+"' not exist")
            return False
    return True


def findModelsAndFieldsInFiles(filenames):
    if not isFilesExist(filenames):
        return

    for filename in filenames:
        #импортирование файла для поиска моделей с полями
        exec("import " + filename + " as m")
        dm = eval("m.__dict__")
        for className, classType in dm.items():
            if isinstance(classType, type) and classType.__base__ == BaseModel:
                print(className)

                variables = classType.__dict__
                fields = []

                for nameVar, typeVar in variables.items():
                    if isinstance(typeVar, BaseField) and \
                            (typeVar.__class__.__base__ == BaseField):
                        fields.append((nameVar, type(typeVar)))
                        print("  find field name='"+nameVar+"'", type(typeVar))
