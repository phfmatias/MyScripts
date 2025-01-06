from os import popen

x = popen("squeue -p int_short --noheader | wc -l").read()
print("INT_SHORT -> {}".format(x), end='')

x = popen("squeue -p amd_short --noheader | wc -l").read()
print("AMD_SHORT -> {}".format(x), end='')

print('\n')

x = popen("squeue -p int_medium --noheader | wc -l").read()
print("INT_MEDIUM -> {}".format(x), end='')

x = popen("squeue -p amd_medium --noheader | wc -l").read()
print("AMD_MEDIUM -> {}".format(x), end='')

print('\n')

x = popen("squeue -p int_large --noheader | wc -l").read()
print("INT_LARGE -> {}".format(x), end='')

x = popen("squeue -p amd_large --noheader | wc -l").read()
print("AMD_LARGE -> {}".format(x), end='')

print('\n')

x = popen("squeue -p gpu_int_k40 --noheader | wc -l").read()
print("GPU_INTEL -> {}".format(x), end='')

x = popen("squeue -p gpu_amd_v100 --noheader | wc -l").read()
print("GPU_AMD -> {}".format(x), end='')