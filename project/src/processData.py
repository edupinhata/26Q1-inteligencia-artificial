import pandas as pd

ds = pd.read_csv("resources/news_clicks_dataset.csv", sep=",", header=0)


def age_group(age):
    if age < 18:
        return "child"
    elif age < 30:
        return "young adult"
    elif age < 60:
        return "adult"
    else:
        return "senior"

#ages = sorted(ds["age"].unique())
#print(list(map(lambda age: age_group(age), ages)))

ds['age_group'] = pd.cut(ds['age'], bins=[0, 18, 30, 60, float('inf')], labels=['child', 'young adult', 'adult', 'senior'])
df_encoded = pd.get_dummies(ds, columns=['age_group'])
#print (df_encoded.columns)
print(df_encoded['age_group_child', 'age_group_young adult', 'age_group_adult', 'age_group_senior'].head())

