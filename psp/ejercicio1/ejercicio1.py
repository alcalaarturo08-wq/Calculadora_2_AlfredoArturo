class CalculadoraSum(object):
    def __init__(self, x,y,n):
        self.x = x
        self.y = y
        self.n=n
    def calsum(self):
        self.sumx=0
        self.sumy=0
        self.sumxy=0
        self.sumx2=0
        self.sumy2=0
        for i in range(self.n):
            self.sumx+=self.x[i]
            self.sumy+=self.y[i]
            self.sumxy+=(self.x[i]*self.y[i])
            self.sumx2+=(self.x[i]**2)
            self.sumy2+=(self.y[i]**2)
    def prom(self):
        self.xavg=self.sumx/self.n
        self.yavg=self.sumy/self.n
    def calbeta(self):
        numerador=self.sumxy-(self.n*self.xavg*self.yavg)
        denominador=self.sumx2-(self.n*self.xavg**2)
        
        self.b1=numerador/denominador
        
        self.b0=self.yavg-(self.b1*self.xavg)
    def calcula(self):
        self.calsum()
        self.prom()
        self.calbeta()  
        return self.b0, self.b1
