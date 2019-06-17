cimport filters_mono

cpdef filter_image(fileName):
    print(fileName)
    filters_mono.filter(fileName.encode('utf-8'))
    return 0
