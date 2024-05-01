import pandas as pd

df = pd.read_csv(snakemake.input[0], index_col="PassengerId")

df.to_csv(snakemake.output[0])
