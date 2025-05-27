from os import popen

int_short = popen('squeue -p int_short --noheader | wc -l').read().strip()
amd_short = popen('squeue -p amd_short --noheader | wc -l').read().strip()
int_medium = popen('squeue -p int_medium --noheader | wc -l').read().strip()
amd_medium = popen('squeue -p amd_medium --noheader | wc -l').read().strip()
int_large = popen('squeue -p int_large --noheader | wc -l').read().strip()
amd_large = popen('squeue -p amd_large --noheader | wc -l').read().strip()
gpu_int_k40 = popen('squeue -p gpu_int_k40 --noheader | wc -l').read().strip()
gpu_a100_192 = popen('squeue -p gpu_a100_192 --noheader | wc -l').read().strip()
gpu_a100_64 = popen('squeue -p gpu_a100_64 --noheader | wc -l').read().strip()

title_table = 'Número de jobs na fila:'
print("\n+------+--------+--------+--------+------------------------------+")
print(f"| {title_table.center(66 - 4)} |")
print("+------+--------+--------+--------+------------------------------+")
print("| Node | SHORT  | MEDIUM | LARGE  | GPU                          |")
print("+------+--------+--------+--------+------------------------------+")
gpu_int = f"INT_K40: {gpu_int_k40}"
print(f"| INT  | {str(int_short).ljust(6)} | {str(int_medium).ljust(6)} | {str(int_large).ljust(6)} | {gpu_int.ljust(28)} |")
gpu_amd = f"A100_192: {gpu_a100_192}, A100_64: {gpu_a100_64}"
print(f"| AMD  | {str(amd_short).ljust(6)} | {str(amd_medium).ljust(6)} | {str(amd_large).ljust(6)} | {gpu_amd.ljust(28)} |")
print("+------+--------+--------+--------+------------------------------+")
