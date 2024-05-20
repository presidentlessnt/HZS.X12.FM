#! /usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# La data tiene 5 columnas: item, tiempo, aceleración "x", aceleracion "y" y aceleracion "z"
AA=np.loadtxt('T57a.txt')	# Data telar 57

# Nota: este código debe estar en la misma carpeta del archivo de datos .txt
# Funcion para procesar data y generar gráficas
def cplot(M,i,j,axs=None,**plt_kwargs):
    n=len(M)			# Obtiene cantidad de datos del ensayo
    M[:,1]*=0.005		# Convierte de 1/200 milisegundos a segundos
    B=np.fft.fft(M[:,4],n)	# función FFT en columna aceleracion "z" -> genera matriz de numeros complejos
    PSD=B*np.conj(B)/n		# Amplitud: multiplica complejo por su conjugado A·A* sobre cantidad de muestras 
    freq=(1/(0.005*n))*np.arange(n)		# Frecuencia
    L=np.arange(1,np.floor(n/2),dtype='int') 	# Genera lista de números desde 1 hasta mitad cantidad de muestras (entero) 
    mx=PSD.argmax()		# Frecuencia de pico de vibración en todo el rango
    nx=PSD[:5000].argmax()	# Frecuencia de pico de vibración en menor a 50 hz
    fig,ax=plt.subplots(2,1)		# inicio de generación de gráficas
    fig.suptitle('Frecuencia Telar') 	# título de gráfico
    ax[0].plot(M[:,1],M[:,4],lw=.5,label='z')
    ax[1].plot(freq[L],PSD[L],lw=.5)
    ax[0].set_xlabel('t $[s]$')
    ax[0].set_ylabel('Aceleración eje Z $[m/s^2]$')
    ax[1].set_xlabel('Frecuencia $[hz]$')
    ax[1].set_ylabel('Amplitud')
    ax[1].vlines(freq[nx],0,PSD[nx],lw=3,color='red',label='$\omega_1$=%1.2f$\,$hz'%freq[nx])
    ax[1].legend()
    return ax

# Llama a la función generadora de gráficas
cplot(AA,1,1)

plt.show()