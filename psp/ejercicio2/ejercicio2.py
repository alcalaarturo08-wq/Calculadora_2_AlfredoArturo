import math
class Sumasim:
    def __init__(self,a,b,n,dof):
        self.a=a
        self.b=b
        self.n=n
        self.dof=dof
        self.fx=0
        self.resultado=0
        
        if self.n % 2!=0:
            raise ValueError("n debe ser un numero par animal")
        
    def F(self,x):
        num=math.gamma((self.dof+1)/2)
        den=math.sqrt(self.dof*math.pi)*math.gamma(self.dof/2)
        self.fx=(num/den)*(1+(x**2)/self.dof)**(-(self.dof+1)/2)
    def integrar(self):
        w=(self.b-self.a)/self.n
        suma_i=0
        suma_p=0
        self.F(self.a)
        fa=self.fx
        
        self.F(self.b)
        fb=self.fx
        for i in range (1,self.n,2):
            self.F(self.a+i*w)
            suma_i+=4*self.fx
            
        for i in range(2, self.n, 2):
            self.F(self.a + i * w)
            suma_p += 2 * self.fx
        self.resultado=(w/3)*(fa+suma_i+suma_p+fb)
