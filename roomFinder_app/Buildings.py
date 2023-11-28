import pandas as pd


def buildings():
    df = pd.read_csv("class_res.csv")

    df['Building'] = df['Building'].replace({'Engr': 'Engineering'}, regex=True)
    df['Building'] = df['Building'].str.replace('Bldg', '', regex=False)
    df['Building'] = df['Building'].str.replace(' Room', '', regex=False)
    df['Building'] = df['Building'].str.replace('The ', '', regex=False)
    df['Building'] = df['Building'].str.replace(' Rm', '', regex=False)
    df['Building'] = df['Building'].str.replace('  ', ' ', regex=True)
    df.loc[df['Building'].str.contains('Chemistry', case=False), 'Building'] = 'Chemistry'
    df.loc[df['Building'].str.contains('Darden', case=False), 'Building'] = 'Darden'
    df['Building'] = df['Building'].str.replace(r' (B|G)$', '', regex=True)
    df['Room'] = df['Room'].apply(lambda x: f"{x:03d}")
    df = df[~df['Building'].str.contains('CT', case=False)]
    df = df[~df['Building'].str.contains('UVA', case=False)]
    df["Building"] = df["Building"].str.strip()

    df.to_csv("class_res.csv")


buildings()
