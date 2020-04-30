from config import *
from utils import *
import Simulation
import Contract




def main():
    products_list = generate_data_products(NUMBER_OF_PRODUCTS, MINIMAL_NUMBER_OF_EXAMPLES,
                                           MAXIMAL_NUMBER_OF_EXAMPLES, MINIMAL_NUMBER_OF_FEATURES,
                                           MAXIMAL_NUMBER_OF_FEATURES)

    players = {"buyers":{},"sellers":{}}
    types_of_buyers = [LinearRegressionCostStrategty(), AggregatedHistoryCostStrategy("mean"),
                       AggregatedHistoryCostStrategy("median"), AggregatedHistoryCostStrategy("max"),
                       AggregatedHistoryCostStrategy("min"),
                       AggregatedHistoryCostStrategy("last")]

    generate_buyers(BUDGET,products_list,TIME_HORIZON,players,types_of_buyers)
    generate_sellers(products_list,NUMBER_OF_PRODUCTS_PER_SELLER,TIME_HORIZON,players)
    valuations_list = generate_valuations(len(players["buyers"]),products_list,MINIMAL_VALUATION_VALUE,MAXIMAL_VALUATION_VALUE)
    contract = Contract.SimpleSellingContract()
    for offset in range(len(valuations_list)):
        assign_valuations_to_buyers(players["buyers"],valuations_list,offset)
        my_sim = Simulation.DataMarketSimulation(TIME_HORIZON, products_list, players, contract)
        my_sim.run_simulation(offset)
        generate_buyers(BUDGET, products_list, TIME_HORIZON, players, types_of_buyers)


if __name__ == '__main__':
    main()
