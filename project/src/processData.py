import pandas as pd

# 3000 user_id
# 3000 news_id

class ArticlesSelectionDataframe:
    
    def __init__(self):
        self.ds = pd.read_csv("resources/news_clicks_dataset.csv", sep=",", header=0)
        self.userDataframe = self.getUserDataframe()
        self.newsDataframe = self.getNewsDataframe()
        self.allDataframe = pd.concat([self.userDataframe, self.newsDataframe], axis=1)
        self.clicks = self.ds['click']

    def getUserDataframe(self):

        # Process age
        ageLabels=['child', 'young_adult', 'adult', 'senior']
        ageBins = [0, 18, 30, 60, float('inf')]
        self.ds['age_group'] = pd.cut(self.ds['age'], bins=ageBins, labels=ageLabels)
        df_age = pd.get_dummies(self.ds['age_group'], prefix='age', dtype=int)

        # Process gender
        df_gender = pd.get_dummies(self.ds['gender'], dtype=int)

        # Process location - since there are too many location (243), we'll try not
        # to use it for now
        # df_location = pd.get_dummies['location']

        # Process device
        df_device = pd.get_dummies(self.ds['device'], dtype=int)

        return pd.concat([df_age, df_gender, df_device], axis=1)

    def getNewsDataframe(self):
        # Process category
        #df_category = pd.get_dummies(ds['category'], prefix='cat')
        
        # Process subcategory
        df_subcategory = pd.get_dummies(self.ds['subcategory'], prefix='subcat', dtype=int)
        
        # Process title or abstract
        # Not easy to parametize title and abstract. We'd need to get some time 
        # of indicator from it in order to check if any of this can define if the 
        # user clicks or not. Let only trust on subcategory to check if there is
        # relationship.
        #
        # Also, something that might be interesting to see is if there are any
        # relationship between what is written and/or how it`s written and the
        # click of users.
        
        # process publish_time
        # Probably, the public time will be used as a sorting key, in order
        # to simulate it
        return pd.concat([df_subcategory], axis=1)
