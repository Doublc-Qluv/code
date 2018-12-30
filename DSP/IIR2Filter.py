import numpy as np
import scipy.signal as signal


class IIR2Filter:
    def __init__(self,_order,_cutoff,*args,**kwargs):
        
        '''
            Constructor to calculate the coefficients of the filter and set up various arrays/variables
            to be used in the filter
            
            Takes in:
                _order = the order of the filter to by created
                _cutoff = the cutoff frequency(s) of the filter normalised to sample rate
            
            Optional:
                filter_type = defines if the filter is lowpass/bandpass/highpass/bandstop
                analogue_filter = defines the type of analogue filter to be replicated
                cheby_ripple = defines the acceptable ripple in a chebyshev filter in dB
                direct_form = defines if a direct form 1 or 2 filter is to be used
                fixed_point = defines if a direct form 1 filter should be fixed point
            
        '''
        
        #Check the optional arguments
        filter_type = kwargs.get('filter_type', 'low')
        analogue_filter = kwargs.get('analogue_filter', 'butter')
        cheby_ripple = kwargs.get('cheby_ripple',5)
        self.direct_form = kwargs.get('direct_form',2)
        self.fixed_point = kwargs.get('fixed_point',False)
        
        #change the cutoffs to be normalised to Nyquist rather than sample rate
        _cutoff = 2* _cutoff
           
        #select which type of analogue filter to replicate
        #output = 'sos' to give second order sections coefficients
        if analogue_filter == 'bessel':
            
            self.sos = signal.bessel(_order,_cutoff,btype=filter_type,analog=False,output='sos')
            
        elif analogue_filter == 'butter':
            
            self.sos = signal.butter(_order,_cutoff,btype=filter_type,analog=False,output='sos')
            
        elif analogue_filter == 'cheby1':
            
            self.sos = signal.cheby1(_order,cheby_ripple,_cutoff,btype=filter_type,analog=False,output='sos')
            
        elif analogue_filter == 'cheby2':
            
            self.sos = signal.cheby2(_order,cheby_ripple,_cutoff,btype=filter_type,analog=False,output='sos')
        
        
        #convert the coefficients to scaled integers if fixed point requested
        #only available for Direct Form 1
        self.fixed_scaling = 30
        if self.fixed_point==True and self.direct_form==1:
            self.sos=self.sos * (2**self.fixed_scaling)
            self.sos=self.sos.astype(int)
        
             
        #define the number of second order sections required to implement that order of filter
        shape = np.shape(self.sos)
        self.sections=shape[0]


        #set up arrays to store the x and y values for each second order section for direct form 1
        self.x=np.zeros([(self.sections),3])
        self.y=np.zeros([(self.sections),3])
        
        #set up delays for direct form 2
        self.delay=np.zeros([self.sections,2])


    def filter(self,v):
        
        '''
             Implements the IIR filtering operation element by element. Does so for
             the correct number of second order sections as defined in the constructor.
             
             
            Takes in:
                v = input data value to the filter
                
            Returns:
                result = output value from the filter
             
        '''
    
        if self.direct_form == 1:
            
            #create second order chain
            for i in range(self.sections):
            
                #load input to each IIR section
                self.x[i,0]=v
            
                buff=np.zeros(5)
                #implements the multiplications by the coefficients and stores in buffer
                buff[0]=self.sos[i,0]*self.x[i,0]
                buff[1]=self.sos[i,1]*self.x[i,1]
                buff[2]=self.sos[i,2]*self.x[i,2]
                buff[3]=-self.sos[i,4]*self.y[i,1]
                buff[4]=-self.sos[i,5]*self.y[i,2]
            
                #sums the buffers
                self.y[i,0]= np.sum(buff)
            
            
                if self.fixed_point == True:
                    
                    self.y[i,0] = int(self.y[i,0]/(2**self.fixed_scaling))
                    
            
                #shifts arrays by one for next loop
                self.x[i,2]=self.x[i,1]
                self.x[i,1]=self.x[i,0]
                self.y[i,2]=self.y[i,1]
                self.y[i,1]=self.y[i,0]
            
                #output from filter set
                v = self.y[i,0]
                
            
                 
            
        elif self.direct_form == 2:
            
            #create second order chain
            for i in range(self.sections):
                
                #implements the multiplications by the coefficients and stores in buffer
                input_acc = v - (self.delay[i,0] * self.sos[i,4]) - (self.delay[i,1] * self.sos[i,5])
                output_acc = (input_acc * self.sos[i,0]) + (self.delay[i,0] * self.sos[i,1]) + (self.delay[i,1] * self.sos[i,2])
            
                   
                #shifts arrays by one for next loop
                self.delay[i,1]=self.delay[i,0]
                self.delay[i,0]=input_acc

                #output from filter set
                v = output_acc                

        #return filter output     
        result = v
        return result