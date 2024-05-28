#! /usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import warnings
warnings.filterwarnings("ignore")

# La data tiene 5 columnas: item, tiempo, aceleración "x", aceleracion "y" y aceleracion "z"
AA=np.loadtxt('T57a.txt')	# Data telar 57
AA[:,1]*=0.001

# Nota: este código debe estar en la misma carpeta del archivo de datos .txt
# Funcion para procesar data y generar gráficas
def cplot(M,i,axs=None,**plt_kwargs):
    n=len(M)			# Obtiene cantidad de datos del ensayo
#    M[:,1]*=0.001		# Convierte de 1/200 milisegundos a segundos
    if i==0:
        MM=M[:,2]
    elif i==1:
        MM=M[:,3]
    elif i==2:
        MM=M[:,4]
    MM=np.convolve(MM,np.ones(3)/3,mode='same')
    B=np.fft.fft(MM,n)	# función FFT en columna aceleracion "i" -> genera matriz de numeros complejos
    PSD=B*np.conj(B)/n		# Amplitud: multiplica complejo por su conjugado A·A* sobre cantidad de muestras 
    freq=(1/(0.005*n))*np.arange(n)		# Frecuencia
    L=np.arange(1,np.floor(n/2),dtype='int') 	# Genera lista de números desde 1 hasta mitad cantidad de muestras (entero) 
#    mx=PSD.argmax()		# Frecuencia de pico de vibración en todo el rango
    mx=np.argsort(PSD[:5000])[-1]	# Frecuencia de pico de vibración en todo el rango
    nx=PSD[:1000].argmax()	# Frecuencia de pico de vibración menor a 10 Hz
    print(PSD[nx])
    C=['green','blue','red']
    fig,ax=plt.subplots(2,1)		# inicio de generación de gráficas
    fig.suptitle('Frecuencia Telar') 	# título de gráfico
    ax[0].plot(M[:,1],MM[:],lw=.5,color=C[i])
    ax[1].plot(freq[L],PSD[L],lw=.5,color=C[i])
    ax[0].set_xlabel('t $[s]$')
    ax[0].set_ylabel('Aceleración $[m/s^2]$')
    ax[1].set_xlabel('Frecuencia $[Hz]$')
    ax[1].set_ylabel('Amplitud')
    ax[1].vlines(freq[nx],0,PSD[nx],lw=3,color='black',label='$\omega_1$=%1.2f$\,$Hz'%freq[nx])
    ax[1].vlines(freq[mx],0,PSD[mx],lw=3,color='black',label='$\omega_{max}$=%1.2f$\,$Hz'%freq[mx])
    ax[1].legend()
    formatter = FormatStrFormatter('%.1f')
    ax[0].yaxis.set_major_formatter(formatter)
    ax[1].yaxis.set_major_formatter(formatter)
    ax[0].grid(True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax[1].grid(True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax[0].set_xlim(left=0)
    ax[1].set_xlim(left=0)
    ax[0].set_xlim(right=60)
    ax[1].set_xlim(right=100)
    return ax

# Llama a la función generadora de gráficas
cplot(AA,0)
cplot(AA,1)
cplot(AA,2)

plt.show()