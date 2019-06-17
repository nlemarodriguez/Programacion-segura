cimport filters

cpdef filter_image(fileName):
    print(fileName)
    filters.filter(fileName.encode('utf-8'))
    return 0
