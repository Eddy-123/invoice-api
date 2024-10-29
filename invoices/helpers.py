from io import BytesIO
import pandas as pd


def generate_excel_file(data):
    output = BytesIO()
    df = pd.DataFrame(data)
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output
