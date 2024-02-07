from simulator import Simulator

if __name__=="__main__":

    num_nodes = 15
    slowfrac = 0.2
    lowCPUfrac = 0.2
    txnDelay_meantime = 30

    max_sim_time = 10000000


    sim = Simulator(num_nodes,slowfrac,lowCPUfrac,txnDelay_meantime, max_sim_time)

    sim.run()

