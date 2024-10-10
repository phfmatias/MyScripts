file = open('PT2X.gjf')
template = file.read()


def generate_iop(value):
    #if value do not have 3 digits, add 0 in the right
    if len(value) < 3:
        value = value + '0'*(3-len(value))

    name = int(value)
    value = value+'0000000'

    return name, value

for i in range(1, 101):
    value = str(i/100).replace('.','')
    name, omega = generate_iop(value)

    x = str(float(name/100)).replace('.','')

    if len(x) == 2:
        x += '0'

    arq = open('PT2X'+'_w0'+x+'.gjf', 'w')
    arq.write(template.replace('#p HF/STO-3G ','#p lc-blyp/def2svp polar NoSymm density=current IOP(3/107={0}) IOP(3/108={0})'.format(omega)))
    arq.close()


    
