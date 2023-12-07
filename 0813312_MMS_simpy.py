import random
import simpy



# Source to generate job arrivals
def source(env, number, inter_arrival_time, processing_time, processor):
    
    for i in range(number):
        c = processing(env, 'Customer%02d' % i, processor, processing_time)
        env.process(c)              # Job arrival event: Generating a new job 
        duration = random.expovariate(1.0 / inter_arrival_time)
        yield env.timeout(duration) # Waiting for generating the next job 
        

# Processor or resource to process job request

### counter is variable for counting how much zeros there are in waiting time
### max_wait is the longest waiting time
### max_endwait is the end waiting time of max_wait
counter = 0
max_wait = 0
max_endwait = 0
def processing(env, name, processor, processing_time):
    
 ### these three variables have to be global to be printed at last   
    global counter
    global max_wait
    global max_endwait
    
    
    arrive = env.now
    with processor.request() as req: 
        yield req                     # Waiting for processing 
        wait = env.now - arrive     
        global TTL_WAIT
        TTL_WAIT = TTL_WAIT + wait
        duration = random.expovariate(1.0 / processing_time)   
        yield env.timeout(duration)   # Processing 
        
### if waiting time equals to 0, add 1 to counter
        if wait==0:
            counter = counter +1
            
### max_wait is zero at first
### if waiting time is larger than old max_wait
### save new waiting time to max_wait
        if wait > max_wait:
            max_wait = wait
### end waiting time = arrival time + waiting time
### so calculate the max end waiting time 
            max_endwait = env.now
            
        
 ### print arrival/waiting/end waiting time for each job        
        print('arrival time = %7.4f' % arrive)     
        print('waiting time = %7.4f' % wait)
        print('end waiting = %7.4f' % (env.now))  
        
        
   
        
# Simulation parameters
RANDOM_SEED = 132342
NUM_CUSTOMERS = 1000        # The number of jobs
NUM_PROCESSORS = 1
INTER_ARRIVAL_TIME = 10.0   
PROCESSING_TIME= 8.0
TTL_WAIT = 0

# Start simulation
print('\nM/M/%1.0f Model:' % NUM_PROCESSORS)
print('   inter_arrival time = %7.4f' % INTER_ARRIVAL_TIME)
print('   processing_time=%7.4f' % PROCESSING_TIME)

random.seed(RANDOM_SEED)
env = simpy.Environment()
processor = simpy.Resource(env, capacity=NUM_PROCESSORS)
env.process(source(env, NUM_CUSTOMERS, INTER_ARRIVAL_TIME, PROCESSING_TIME, processor))
env.run(until=1000)
print('####################################')
print(' Average waiting time: %7.4f' % (TTL_WAIT/NUM_CUSTOMERS))

##Print end waiting time/ waiting time
print('total wait = %7.4f' % TTL_WAIT)
print('####################################')
###print the results
print('Number of zero wait = %7.4f' % counter)
print('max wait = %7.4f' % max_wait)
print('max end wait = %7.4f' % max_endwait)




