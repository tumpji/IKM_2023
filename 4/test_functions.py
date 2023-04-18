# Create Search Spaces by Difficulty
import functools
import numpy as np
import matplotlib.pyplot as plt

def repair_range(xrange, yrange, minimum=(0,0)):
    #np.random.seed(random_state)
    #minimum = np.random.rand(1, D) * np.array(maxshift)
    #D, random_state=42, maxshift=(0.1,0.1) normrange_x, normrange_y = 
    
    minx, miny = minimum
    minx = (minx - xrange[0])/(xrange[1] - xrange[0])
    miny = (miny - yrange[0])/(yrange[1] - yrange[0])
    minimum = (minx, miny)
    
    def decorator(f): 
        @functools.wraps(f)
        def wrapper(x,y):
            x = x*(xrange[1] - xrange[0]) + xrange[0]
            y = y*(yrange[1] - yrange[0]) + yrange[0]
            return f(x, y)
        
        wrapper.minimum = minimum
        return wrapper
    
    return decorator

def optuna_wrapper(f):
    @functools.wraps(f)
    def wrapper(trial):
        x = trial.suggest_float("x", 0, 1)
        y = trial.suggest_float("y", 0, 1)
        return f(x, y)
    wrapper.minimum = f.minimum
    wrapper.f = f
    return wrapper
        
    
    
@repair_range(xrange=(-1,1), yrange=(-1,1), minimum=(0.123,-0.456))
def f1(x, y):
    ''' sphere function '''
    return np.square(x-0.123) + np.square(y+0.456)

@repair_range(xrange=(-15,-5), yrange=(-3,3), minimum=(-10,1))
def f2(x, y):
    ''' Bukin function N.6 '''
    return np.sqrt(np.abs(y - 0.01*np.square(x))) + 0.01*np.abs(x+10)
    
@repair_range(xrange=(-4.5,4.5), yrange=(-4.5,4.5), minimum=(3,0.5))
def f3(x, y):
    '''Beale function'''
    return np.log( (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 \
           + (2.635 - x + x*y**3)**2 +0.00001)

@repair_range(xrange=(-512,512), yrange=(-512,512), minimum=(512,404.2319))
def f4(x, y):
    ''' Rastrigin function '''
    return -(y + 47) * np.sin(np.sqrt(np.abs(x/2 + y + 47))) - x*np.sin(np.sqrt(np.abs(x - y -47)))
    
    
functions = [f1, f2, f3, f4]
functions_optuna = list(map(optuna_wrapper, functions))



def show_functions():
    fig, axs = plt.subplots(2,2)

    RESOLUTION = 200

    def draw(ax, f):
        ylin = np.linspace(0, 1, RESOLUTION)
        xlin = np.linspace(0, 1, RESOLUTION)
        xmesh, ymesh = np.meshgrid(xlin, ylin)
        y = f(xmesh.reshape(-1,1), ymesh.reshape(-1,1))
        ax.pcolormesh( xlin, ylin, y.reshape(RESOLUTION, RESOLUTION))
        ax.plot(*f.minimum, '+', color='red', markersize=20)

    draw(axs[0,0], f1)
    draw(axs[0,1], f2)
    draw(axs[1,0], f3)
    draw(axs[1,1], f4)