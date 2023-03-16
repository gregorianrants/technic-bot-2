class PIController:
    def __init__(self, proportional_constant=0, integral_constant=0,derivative_constant=0):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant
        self.derivative_constant = derivative_constant
        # Running sums
        self.integral_sum = 0
        self.previous = 0
    def handle_proportional(self,error):
      return self.proportional_constant * error
    def handle_integral(self,error):
      self.integral_sum += error
      return self.integral_constant * error
    def handle_derivative(self,error):
       derivative = self.derivative_constant*(error - self.previous)
       self.previous = error
       return derivative

     
    def get_value(self,error):
      p=self.handle_proportional(error)
      i=self.handle_integral(error)
      d= self.handle_derivative(error)
      return p+i+d

class PI_PVD_Controller:
    def __init__(self, proportional_constant=0, integral_constant=0,derivative_constant=0):
        self.proportional_constant = proportional_constant
        self.integral_constant = integral_constant
        self.derivative_constant = derivative_constant
        # Running sums
        self.integral_sum = 0
        self.previous_proccess_variable = 0
    def handle_proportional(self,error):
      return self.proportional_constant * error
    def handle_integral(self,error):
      self.integral_sum += error
      return self.integral_constant * error
    def handle_derivative(self,process_variable):
       derivative = self.derivative_constant*(process_variable - self.previous_proccess_variable)
       self.previous_proccess_variable = process_variable
       return derivative

     
    def get_value(self,error,process_variable):
      p=self.handle_proportional(error)
      i=self.handle_integral(error)
      d= self.handle_derivative(process_variable)
      return p+i-d


    


