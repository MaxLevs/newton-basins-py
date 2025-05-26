import numpy as np
import pandas as pd
from pandas._typing import Axes

class PandasHelper:
    @staticmethod
    def append_to_dataframe(data_frame: pd.DataFrame, array: np.ndarray, columns: Axes) -> pd.DataFrame:
        data_frame[columns] = pd.DataFrame(array, columns=columns)
        return data_frame
