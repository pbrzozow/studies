import numpy as np
def print_and_clear_arr(arr):
    print(arr)
    arr=np.zeros((3,3))
    

arr=np.zeros((3,3))
# a
arr[2:,:]=1

print_and_clear_arr(arr)
# b
arr[1:,1:2]=1
print_and_clear_arr(arr)
# c
arr[1:,:]=1
print_and_clear_arr(arr)
# d
arr[0:1,:]=1
arr[:,1:2]=0
arr[2:,:]=0
print_and_clear_arr(arr)
# e
arr[:,:]=1
arr[0:1,:]=0
arr[:,0:1]=0
print_and_clear_arr(arr)
