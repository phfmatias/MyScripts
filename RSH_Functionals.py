from math import erf
from numpy import arange
import matplotlib.pyplot as plt


def short_range(w,r):
    return (1 - erf(w*r))/r 

def long_range(w,r):
    return erf(w*r)/r

def r12(sr,lr):
    return sr+lr

def couloumb_f(r):
    return 1/r


r = arange(0.1, 10, 0.01)

w1 = 0.01

sr_1 = [short_range(w1, i) for i in r]
lr_1 = [long_range(w1, i) for i in r]

# if len(sr_1) > len(lr_1):
#     sr_1 = sr_1[:len(lr_1)]

# if len(lr_1) > len(sr_1):
#     lr_1 = lr_1[:len(sr_1)]

w2 = 0.99

sr_2 = [short_range(w2, i) for i in r]
lr_2 = [long_range(w2, i) for i in r]

# if len(sr_2) > len(lr_2):
#     sr_2 = sr_2[:len(lr_2)]

# if len(lr_2) > len(sr_2):
#     lr_2 = lr_2[:len(sr_2)]

w1_switch = 1/(2*w1)
w2_switch = 1/(2*w2)


print('Switch when w = {}, will be near to r = {} bohr'.format(w1, w1_switch))
print('Switch when w = {}, will be near to r = {} bohr'.format(w2, w2_switch))

couloumb = [couloumb_f(i) for i in r]

#get the point where the absolute deviation of the SR_1 and LR_1 is minimum

min_deviation = 1000
for i in range(len(sr_1)):
    deviation = abs(sr_1[i] - lr_1[i])
    if deviation < min_deviation:
        min_deviation = deviation
        w1_switch = r[i]

min_deviation = 1000
for i in range(len(sr_2)):
    deviation = abs(sr_2[i] - lr_2[i])
    if deviation < min_deviation:
        min_deviation = deviation
        w2_switch = r[i]


import matplotlib.ticker as tck

figure = plt.figure()
ax = figure.add_subplot(111)
#ax.set_ylim(-0.05,0.55)
# ax.set_xlim(1, 11)

ax.plot(r, sr_1, '-', linewidth=7, color='#01701b', label=r'SR ($\omega$ = {}'.format(w1) + r' $a_{0}^{-1}$)', solid_capstyle='round')
ax.plot(r, lr_1, '-', linewidth=7, color='#02b42c', label=r'LR ($\omega$ = {}'.format(w1) + r' $a_{0}^{-1}$)', solid_capstyle='round')

ax.plot(r, sr_2, '-', linewidth=7, color='#0036ff', label=r'SR ($\omega$ = {}'.format(w2) + r' $a_{0}^{-1}$)', solid_capstyle='round')
ax.plot(r, lr_2, '-', linewidth=7, color='#009dff', label=r'LR ($\omega$ = {}'.format(w2) + r' $a_{0}^{-1}$)', solid_capstyle='round')

ax.plot(r, couloumb, '--', color='#000000', label=r'($1/r_{12}$)')

#! W1=0.1, W2=0.4

# ax.annotate('Inversão', xy=(w1_switch, short_range(w1, w1_switch)-.025), xytext=(w1_switch, short_range(w1, w1_switch)+0.3),
#                 arrowprops=dict(facecolor='black', shrink=0.1), ha='center', fontweight='bold')

# ax.annotate('', xy=(w2_switch-0.3, short_range(w2, w2_switch)), xytext=(w1_switch-0.7, short_range(w1, w1_switch)+0.31),
#                             arrowprops=dict(facecolor='black', shrink=0.1))


ax.set_xticks([i for i in range(0, 11) if i % 2 == 0])
ax.set_yticks([i for i in arange(0, 0.51, 0.1)])

ax.yaxis.set_minor_locator(tck.AutoMinorLocator(2))
ax.xaxis.set_minor_locator(tck.AutoMinorLocator(2))

ax.set_xlabel(r'$\mathbf{r_{12}}$ ($\mathbf{a_{0}}$)', fontsize=12, fontweight='bold')
ax.set_ylabel(r'Operador 1/$\mathbf{r_{12}}$', fontsize=12, fontweight='bold')

plt.legend(loc='best', frameon=False)
plt.show()
#plt.savefig('RSH_Operators.png', dpi=300)