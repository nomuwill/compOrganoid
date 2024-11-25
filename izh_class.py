'''
Noah Williams
11/9/2024

Simulation for the Izhikevich Neuron Model

    The Izhikevich model is a simple spiking neuron model that builds on the 
        dynamics of the simplistic leaky integrate-and-fire model, adding 
        complexity of the Hodgkin-Huxley model with minimal computational 
        cost.

        The model is described by the following system:

            v' = 0.04*v^2 + 5*v + 140 - u + I
            u' = a*(b*v - u)
            if v >= 30 then {v = c; u = u + d}

            where: 
                a, b, c, d = dimensionless constants

                    Regular Spiking (RS) Excitatory Neuron:
                        a = 0.02, b = 0.2, c = -65, d = 8
    
                    
                v = membrane potential
                u = membrane recovery (Na and K, neg feedback to v)
                a = time scale of the recovery variable u (small = slow recovery)
                b = sensitivity of the recovery variable u to v
                        Larger values increase sensitivity and lead to more 
                        spiking behavior. b<a(b>a) is saddle-node
                c = after spike reset value of v
                        caused by fast K+ channels
                d = after spike reset value of u
                        caused by slow Na+ & K+ channels
                I = input current

        The constants for the model differential equation v' are experimentally
            determined by fitting the model to the desired neuron behavior. In 
            the original paper (from which the equations are taken), the model 
            was fit to experimental data from Regular Spiking of a rat cortical 
            neuron.


    References:
    https://www.izhikevich.org/publications/spikes.pdf
'''


class IzhikevichNeuron:

    def __init__(self, thr):
        self.a = 0.02    # Time constant for u (recovery variable)
        self.b = 0.2    # Sensitivity of recovery variable to voltage
        self.c = -65    # Reset value for voltage when a spike occurs
        self.d = 8    # Reset value for recovery variable when a spike occurs
        self.thr = thr  # Spike threshold

        # Initial conditions
        self.v = -65   # Initial voltage (in mV)
        self.u = 0     # Initial recovery variable

        # Misc
        self.dt = .01    # Time step (ms) 

    def step(self, current):
        v_prime = (0.04 * self.v**2) + (5 * self.v) + 140 - self.u + current
        u_prime = self.a * (self.b * self.v - self.u)
        v_next = self.v + v_prime * self.dt
        u_next = self.u + u_prime * self.dt

        spike = 0
        if self.v >= self.thr:  
            self.v = self.c 
            self.u = self.u + self.d 
            spike = 1
        else:
            self.v = v_next
            self.u = u_next
        
        return spike
    

### WIP ###

class TTIzhikevichNeuron:

    '''

    Used to test HDL model of Izhikevich Neuron Model 
    
    Model includes fixed point representation of parameters, '
        and scaling to match the HDL TinyTapeout implementation. 

    Parameters:
        a, b, c, d, thr: 16bit
        
    '''

    def __init__(self, a, b, c, d, thr, 
                 initial_voltage=-65, 
                 initial_recovery=0,
                 dt=.01):

        self.a = a    # Time constant for u (recovery variable)
        self.b = b    # Sensitivity of recovery variable to voltage
        self.c = c    # Reset value for voltage when a spike occurs
        self.d = d    # Reset value for recovery variable when a spike occurs
        self.thr = thr  # Spike threshold

        # Initial conditions
        self.v = initial_voltage   # Initial voltage (in mV)
        self.u = initial_recovery     # Initial recovery variable

        # Misc
        self.dt = dt    # Time step (ms) 

    def step(self, current):

        # Convert current to 8 bit bin
        current = bin(current)[2:]

        v = '00000000' + current

        v_prime = (0.04 * self.v**2) + (5 * self.v) + 140 - self.u + current
        u_prime = self.a * (self.b * self.v - self.u)
        v_next = self.v + v_prime * self.dt
        u_next = self.u + u_prime * self.dt

        spike = 0
        if self.v >= self.thr:  
            self.v = self.c 
            self.u = self.u + self.d 
            spike = 1
        else:
            self.v = v_next
            self.u = u_next
        
        return spike