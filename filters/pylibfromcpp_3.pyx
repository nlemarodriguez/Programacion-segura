cimport filter3

cpdef filter_image(fileName):
    print(fileName)
    filter3.filter(fileName.encode('utf-8'))
    return 0
