from back_up.Visualization import Visualization
import pandas as pd

df  = pd.read_csv("../sim.csv")
visualizer = Visualization(df)
visualizer.create_price_over_all_products_plot("mean")
visualizer.create_price_over_all_products_plot("median")
visualizer.create_price_over_all_products_plot("min")
visualizer.create_price_over_all_products_plot("max")

try:
    visualizer.create_price_over_all_products_plot("kaka")
except ValueError as e:
    print(str(e))


visualizer.create_price_per_product_plot("mean")
visualizer.create_price_per_product_plot("max")
visualizer.create_price_per_product_plot("min")
visualizer.create_price_per_product_plot("median")
