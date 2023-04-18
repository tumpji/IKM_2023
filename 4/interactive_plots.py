import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
from matplotlib import animation

import optuna.visualization

from test_functions import *
import GPEI_sampler

from ipywidgets import *
import numpy as np
import matplotlib.pyplot as plt


import optuna
optuna.logging.disable_default_handler()
RESOLUTION = 100


class InteractivePlot:
    RESOLUTION = 200
    
    def __init__(self, path):
        self.fid = -1
        self.process_data(path)

        self.ylin = self.xlin = np.linspace(0, 1, self.RESOLUTION)
        self.xmesh, self.ymesh = np.meshgrid(self.xlin, self.ylin)
        self.xmesh = self.xmesh.reshape(-1, 1)
        self.ymesh = self.ymesh.reshape(-1, 1)
        
        # generates plot placeholders ...
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        
        self.ax_background = self.ax.pcolormesh(self.xlin, self.ylin, 
                np.zeros((self.RESOLUTION, self.RESOLUTION)), vmin=0., vmax=1.) 
        
        self.ax_test_points, = self.ax.plot([], [], '+', color='white', markersize=20)
        self.ax_found, = self.ax.plot(0.5,0.5, 'x', color='yellow', markersize=100)
        self.ax_optimum, = self.ax.plot(0.5,0.5, '+', color='red', markersize=20)
        
       
        # generate widget
        self.ax_complexity_slider = IntSlider(value=self.points[0], max=100, min=1,
                                              description='number of test points')
        self.ax_function_slider = IntSlider(value=0, max=3, min=0,
                                              description='function id')
        
        self.widget = interact(self.update, 
                               function_id = (0,3,1), 
                complexity_selector=self.ax_complexity_slider
                              );
        self.update()
        
    def process_data(self, path):
        full_data = np.load(path, allow_pickle=True)
        if path.endswith('.npz'):
            full_data = full_data['data']
        
        self.points, values = zip(*full_data)
        values = list(zip(*values))
        
        self.test_points = [[
                (np.array([v.params['x'] for v in t.trials]), np.array([v.params['y'] for v in t.trials])) 
                for t in fid ] for fid in values
        ]
        
        self.best_points = [
            [(t.best_params['x'], t.best_params['y']) for t in fid]
            for fid in values ]
        
    def update_background(self):
        # compute
        f = functions[self.fid]
        y = f(self.xmesh, self.ymesh).reshape(self.RESOLUTION, self.RESOLUTION)
        y -= np.min(y)
        y /= np.max(y)
        # update plot
        self.ax_background.set_array(y)
        # update optimum
        self.ax_optimum.set_data(*f.minimum)
        
    def update_testpoints(self, value):
        # fid ...
        index = np.searchsorted(self.points, value)
        
        if value != self.points[index]:
            self.ax_complexity_slider.value = self.points[index]
            
        # get test points
        test_points = self.test_points[self.fid][index]
        self.ax_test_points.set_data(*test_points)
        
        # set best points
        best_point = self.best_points[self.fid][index]
        self.ax_found.set_data(*best_point)

    def get_test_points(self):
        pass
        
        
    def update(self, function_id=0, complexity_selector=1):
        if function_id != self.fid:
            self.fid = function_id
            self.update_background()
            
        self.update_testpoints(complexity_selector)
        self.fig.canvas.draw_idle()


class RandomPlot:
    RESOLUTION = 200
    
    def __init__(self, path):
        self.fid = -1
        self.process_data(path)

        self.ylin = self.xlin = np.linspace(0, 1, self.RESOLUTION)
        self.xmesh, self.ymesh = np.meshgrid(self.xlin, self.ylin)
        self.xmesh = self.xmesh.reshape(-1, 1)
        self.ymesh = self.ymesh.reshape(-1, 1)
        
        # generates plot placeholders ...
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        
        self.ax_background = self.ax.pcolormesh(self.xlin, self.ylin, 
                np.zeros((self.RESOLUTION, self.RESOLUTION)), vmin=0., vmax=1.) 
        
        self.ax_test_points, = self.ax.plot([], [], '+', color='white', markersize=20)
        self.ax_found, = self.ax.plot(0.5,0.5, 'x', color='yellow', markersize=100)
        self.ax_optimum, = self.ax.plot(0.5,0.5, '+', color='red', markersize=20)
        
       
        # generate widget
        self.ax_complexity_slider = IntSlider(value=self.points[0], max=100, min=1,
                                              description='number of test points')
        self.ax_function_slider = IntSlider(value=0, max=3, min=0,
                                              description='function id')
        
        self.widget = interact(self.update, 
                               function_id = (0,3,1), 
                i=self.ax_complexity_slider
                              );
        self.update()
        
    def process_data(self, path):
        full_data = np.load(path, allow_pickle=True)
        if path.endswith('.npz'):
            full_data = full_data['data']
        
        self.points, values = zip(*full_data)
        values = list(zip(*values))
        
        self.test_points = [[
                (np.array([v.params['x'] for v in t.trials]), np.array([v.params['y'] for v in t.trials])) 
                for t in fid ] for fid in values
        ]
        
        self.best_points = [
            [(t.best_params['x'], t.best_params['y']) for t in fid]
            for fid in values ]
        
    def update_background(self):
        # compute
        f = functions[self.fid]
        y = f(self.xmesh, self.ymesh).reshape(self.RESOLUTION, self.RESOLUTION)
        y -= np.min(y)
        y /= np.max(y)
        # update plot
        self.ax_background.set_array(y)
        # update optimum
        self.ax_optimum.set_data(*f.minimum)
        
    def update_testpoints(self, value):
        # fid ...
        index = np.searchsorted(self.points, value)
        
        if value != self.points[index]:
            self.ax_complexity_slider.value = self.points[index]
            
        # get test points
        test_points = self.test_points[self.fid][index]
        self.ax_test_points.set_data(*test_points)
        
        # set best points
        best_point = self.best_points[self.fid][index]
        self.ax_found.set_data(*best_point)

    def get_test_points(self):
        pass
        
        
    def update(self, function_id=0, i=1):
        if function_id != self.fid:
            self.fid = function_id
            self.update_background()
            
        self.update_testpoints(i)
        self.fig.canvas.draw_idle()
