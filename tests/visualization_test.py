from Visualization import Visualization
import pandas as pd

df  = pd.read_csv("../sim.csv")
visualizer = Visualization(df)
visualizer.create_price_plot("mean")
visualizer.create_price_plot("median")
visualizer.create_price_plot("min")
visualizer.create_price_plot("max")
visualizer.create_price_plot("kaka")