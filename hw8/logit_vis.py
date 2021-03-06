import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

def genData(N=200, p=10):
  x = np.zeros((N, p))
  x[:,0] = 1
  x[:,1:] = np.random.randn(N, p-1)
  b = [-1, 1]*int(p/2)
  z = x.dot(b)
  sigmoid = 1/(1+np.exp(-z))
  threshold = np.random.rand(200)
  y = [int(sgm>thr) for thr, sgm in zip(threshold, sigmoid)]
  y = np.array(y)
  return x, y

class LogisticReg:
  def __init__(self, tol=5e-6, step=0.05, max_iter=1e4, is_plot=True):
    self.parameters = {'tol': tol, 'step':step, 'max_iter':max_iter}
    self.is_plot = is_plot
    self.plot = {'grad':[], 'loss':[], 'index':[]}

  def predict(self):
    z = self.x.dot(self.b)
    y_hat = 1/(1+np.exp(z))
    return y_hat

  def getGrad(self):
    y_hat = self.predict()
    grad = self.x.T.dot(y_hat-self.y)
    return grad

  def getLoss(self):
    y_hat = self.predict()
    loss = log_loss(self.y, y_hat)
    return loss

  def getPlot(self):
    return self.plot

  def fit(self, x, y):
    self.x = x
    self.y = y
    self.b = np.random.rand(x.shape[1])*2 - 1 

    n_iter = 0
    loss = 1 + self.parameters['tol']
    while ((n_iter<self.parameters['max_iter']) | (loss<self.parameters['tol'])):
      loss = self.getLoss()
      grad = self.getGrad()
      self.b += self.parameters['step']*grad
      n_iter+=1
      if(self.is_plot):
        self.plot['loss'].append(loss)
        self.plot['grad'].append(np.linalg.norm(grad))
        self.plot['index'].append(n_iter)

def main():
  x_train, y_train = genData()
  
  # from sklearn
  reg = LogisticRegression(max_iter=1e4)
  reg.fit(x_train, y_train)
  z = x_train.dot(reg.coef_.T)
  y_hat = 1/(1+np.exp(-z))
  loss = log_loss(y_train, y_hat)

  # my implementation
  reg_mine = LogisticReg(step=1e-4)
  reg_mine.fit(x_train, y_train)

  # plot
  plot = reg_mine.getPlot()
  plot['loss'] = [ls-loss for ls in plot['loss']]
  plt.figure(figsize = (15,5))
  plt.subplot(1,2,1)
  plt.yscale('log')
  plt.plot(plot['index'], plot['grad'])
  plt.xlabel('Iteration')
  plt.ylabel('gradient norm (log)')
  plt.subplot(1,2,2)
  plt.plot(plot['index'], plot['loss'])
  plt.xlabel('Iteration')
  plt.ylabel('l(B^r) - l(B^*)')
  plt.show()

if __name__ == '__main__':
  main()
