import os.path
from model import BaseModel
from field import BaseField


def isFilesExist(filenames):
    for filename in filenames:
        if not os.path.isfile(filename):
            return False
    return True


def findModelsAndFieldsInFiles(filenames):
    if not isFilesExist(filenames):
        return

    for filename in filenames:
        #импортирование файла для поиска моделей с полями
        filename = 'testt/modelfortest.py'
        newfilename = filename.replace("/", ".")
        newfilename = newfilename.replace(".py", "")
        exec("import " + newfilename + " as m")
        dm = eval("m.__dict__")
        classes = {}
        for className, classType in dm.items():
            if isinstance(classType, type) and classType.__base__ == BaseModel:
                #print(className)

                variables = classType.__dict__
                fields = []

                for nameVar, typeVar in variables.items():
                    if isinstance(typeVar, BaseField) and \
                            (typeVar.__class__.__base__ == BaseField):
                        fields.append((nameVar, type(typeVar)))
                        # print("  find field name='"+nameVar+"'", type(typeVar))
                classes[className] = fields

        return classes
