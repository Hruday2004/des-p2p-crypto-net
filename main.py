from simulator import Simulator

if __name__=="__main__":

    #TODO make provision for command line parsing 

    num_nodes = 10
    slowfrac = 0.3
    lowCPUfrac = 0.3
    txnDelay_meantime = 0.03

    max_sim_time = 50


    sim = Simulator(num_nodes,slowfrac,lowCPUfrac,txnDelay_meantime, max_sim_time)

    sim.run()

